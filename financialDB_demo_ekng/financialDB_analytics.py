"""
Author: Edward KGN
Last Update: 04/02/2022

Financial Ratios' calculator interface, utilizing Object-Oriented Program technique to encapsulate extraction,
calculation and write out operations

Dependent on financialDB_operations, FR_main, FR_banking, FR_insurance, FR_reit
"""

from financialDB_operations import *
from FR_main import *  # Second creation of logger over-written logger in operations
from FR_banking import *
from FR_insurance import *
from FR_reit import *

# Other Modules
import pandas as pd


def financial_ratio_calculator():
    # Get Company Name
    input_company_name = input("Enter company name > ")
    filtered_company = get_company(input_company_name)

    if filtered_company is None:
        logger.error(f"{input_company_name} does not exist in database")
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

        logger.debug(f"joined_results > \n{joined_results}")

        if joined_results is None or len(joined_results) == 0:
            logger.info(f"No data for {input_company_name} from {input_year_start} to {input_year_end} found"
                        f" in database.")
        else:
            logger.info(f"Data for {input_company_name} from {input_year_start} to {input_year_end} found"
                        f" in database.\n")

            # Generate Empty Dataframe Table with columns
            financial_years = []
            for financial_year in range(int(input_year_end), int(input_year_start) - 1, -1):  # In reverse order
                financial_years.append(str(financial_year))  # Convert from integer to string to standardize types
            logger.debug(f"Financial years extracted: {financial_years}")

            ls_columns = ["Financial Statement Item"] + financial_years
            logger.debug(f"Column list: {ls_columns}")

            df_values = pd.DataFrame(columns=ls_columns)

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

            # print(ls_dict_to_input)
            # print(ls_dict_to_input[0]["Financial Statement Item"])

            ls_unique_financial_statement_items = list(set(ls_financial_statement_items))  # De-duplication
            ls_unique_financial_statement_items.sort()

            for element in ls_unique_financial_statement_items:
                logger.debug(f"{element}, {type(element)}")

                financial_statement_item_row = {"Financial Statement Item": element}
                logger.debug(f"{financial_statement_item_row}")

                df_values = df_values.append(financial_statement_item_row, ignore_index=True)

            # print(df_values)

            # Element by Element insertion using dictionary
            # logger.debug(f"{df_values.loc[df_values[df_values.columns[0]] ==
            #                      ls_dict_to_input[0]["Financial Statement Item"],
            #                      ls_dict_to_input[0]["Financial Year"]]}")

            for dict_financial_statement_value in ls_dict_to_input:
                df_values.loc[df_values[df_values.columns[0]] ==
                              dict_financial_statement_value["Financial Statement Item"],
                              dict_financial_statement_value["Financial Year"]] = \
                    dict_financial_statement_value["Value"]

            logger.debug(df_values)

            # Detect and report then Drop NaN columns
            logger.debug(df_values.isnull().any())
            logger.debug(type(df_values.isnull().any()))
            logger.debug((df_values.isnull().any()).values)

            ser_nan_test = df_values.isnull().any()

            # Inform User of missing data for specific years
            for index, item in ser_nan_test.items():
                if item:
                    logger.info(f"There are no financial values for year {index}")

            # Drop non-existent values
            df_values.dropna(axis=1, inplace=True)

            # Encapsulate Group of Financial Ratios to Call in a Separate Module
            if filtered_company.industry == "Banking":
                logger.info("Company's industry is Banking, applying specific ratios for it")
                FR_object = FR_banking(df_values)
                FR_object.analyze_banking()
                logger.debug(f"\n{FR_object.get_FR()}")
            elif filtered_company.industry == "Insurance":
                logger.info("Company's industry is Insurance, applying specific ratios for it")
                FR_object = FR_insurance(df_values)
                FR_object.analyze_insurance()
                logger.debug(f"\n{FR_object.get_FR()}")
            elif filtered_company.industry == "Real Estate Investment Trust":
                logger.info("Company's industry is REIT, applying specific ratios for it")
                FR_object = FR_reit(df_values)
                FR_object.analyze_reit()
                logger.debug(f"\n{FR_object.get_FR()}")
            else:
                logger.info("Applying general financial ratio analysis")
                FR_object = FR_default(df_values)
                FR_object.default_analysis()
                logger.debug(f"\n{FR_object.get_FR()}")

            FR_object.write_out(filtered_company.name)

            logger.info("~~~ End of Analytics ~~~")


if __name__ == "__main__":
    financial_ratio_calculator()
