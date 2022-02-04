"""
Author: Edward KGN
Last Update: 30/01/2022

A conditional (by Company and Financial Year) viewer for financial statement values. Writes out .xlsx for financial
values found in database.

Dependent on financialDB_operations
"""

from financialDB_operations import *
import pandas as pd
import os
# import numpy as np


def viewer():
    # Get Company Data and retrieve company_id for data
    input_company_name = input("Enter company name > ")

    filtered_company = get_company(input_company_name)

    # Select Financial Years
    if filtered_company is None:
        logger.error(f"{filtered_company} is not found in the database.")
        return  # Terminate process here
    else:
        # Select from financial_statement_values table at specific number of years
        input_year_start = input("Enter starting financial year > ")
        # input_year_start = "2015"
        input_year_end = input("Enter ending financial year > ")
        # input_year_end = "2020"

        # Simple Join method, not using join()
        joined_results = session.query(FinancialStatementValue, FinancialStatementItem).filter(
            and_(FinancialStatementValue.item_id == FinancialStatementItem.id,
                 FinancialStatementValue.company_id == filtered_company.id,
                 FinancialStatementValue.financial_year >= datetime.strftime(
                     datetime(int(input_year_start), 1, 1), '%Y-%m-%d'),
                 FinancialStatementValue.financial_year <= datetime.strftime(
                     datetime(int(input_year_end), 12, 31), '%Y-%m-%d')
                 )
        ).all()

        logger.debug(f"joined_results \n{joined_results}")

        if joined_results is None or len(joined_results) == 0:
            logger.info(f"No data for {input_company_name} from {input_year_start} to {input_year_end} found"
                        f" in database.")
        else:
            logger.info(f"Data for {input_company_name} from {input_year_start} to {input_year_end} found"
                        f" in database.")

            # Generate Empty Dataframe Table with columns
            financial_years = []
            for financial_year in range(int(input_year_end), int(input_year_start)-1, -1):  # In reverse order
                financial_years.append(str(financial_year))  # Convert from integer to string to standardize types
            logger.debug(f"Financial years extracted: {financial_years}")

            ls_columns = ["Financial Statement Item"] + financial_years
            logger.debug(f"Column list: {ls_columns}")

            df_viewer = pd.DataFrame(columns=ls_columns)

            # Get financial statement items to insert into columns
            ls_financial_statement_items = []
            ls_dict_to_input = []

            # Extract key data from database
            for row in joined_results:
                # print(f"{row[0]}, {row[1]})
                # print(f"Financial Year > "
                #       f"{row[0].financial_year, type(row[0].financial_year), row[0].financial_year.strftime('%Y')}, "
                #       f"Value > {row[0].value} | "
                #       f"Item > {row[1].item}")

                # Extract a list of financial statement items for df_viewer
                ls_financial_statement_items.append(row[1].item)

                # Extract key value of interest
                ls_dict_to_input.append({"Financial Statement Item": row[1].item,
                                         "Financial Year": row[0].financial_year.strftime('%Y'),
                                         "Value": row[0].value})

            logger.debug(ls_dict_to_input)
            logger.debug(ls_dict_to_input[0]["Financial Statement Item"])

            ls_unique_financial_statement_items = list(set(ls_financial_statement_items))  # De-duplication
            ls_unique_financial_statement_items.sort()

            for element in ls_unique_financial_statement_items:
                logger.debug(f"{element}, {type(element)}")

                financial_statement_item_row = {"Financial Statement Item": element}
                logger.debug(f"{financial_statement_item_row}")

                df_viewer = df_viewer.append(financial_statement_item_row, ignore_index=True)

            logger.debug(df_viewer)

            # Element by Element insertion using dictionary
            # logger.debug(f"{df_viewer.loc[df_viewer[df_viewer.columns[0]] ==
            # ls_dict_to_input[0]['Financial Statement Item'], ls_dict_to_input[0]['Financial Year']]}")

            for dict_financial_statement_value in ls_dict_to_input:
                df_viewer.loc[df_viewer[df_viewer.columns[0]] ==
                              dict_financial_statement_value["Financial Statement Item"],
                              dict_financial_statement_value["Financial Year"]] = \
                    dict_financial_statement_value["Value"]

            ser_nan_test = df_viewer.isnull().any()

            # Inform User of missing data for specific years
            for index, item in ser_nan_test.items():
                if item:
                    logger.info(f"There are no financial values for year {index}")

            # Exclude missing values
            df_viewer.dropna(axis=1, inplace=True)

            # View in Console
            print(f"\n{df_viewer}")

            # Write Excel sheet to subdirectory
            logger.info(f"Writing out to {filtered_company.name}_viewer_output.xlsx")

            destination_directory_name = "viewer_output"
            if not os.path.isdir(destination_directory_name):  # If not existent already
                os.makedirs(destination_directory_name)

            xlsx_filename = filtered_company.name + "_viewer_output.xlsx"

            out_path = os.path.join(destination_directory_name, xlsx_filename)  # subdirectory

            writer = pd.ExcelWriter(out_path)

            df_viewer.to_excel(writer, sheet_name='viewer_sheet')
            writer.save()

            # Write to excel sheet for easier checking
            # xlsx_name = input_company_name + "_output.xlsx"
            # df_viewer.to_excel(xlsx_name, sheet_name="output")


if __name__ == "__main__":
    viewer()
