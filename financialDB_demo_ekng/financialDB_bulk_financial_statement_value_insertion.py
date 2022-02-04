"""
Author: Edward KGN
Last Update: 04/02/2022

Bulk insertion using .xlsx documents whose details are given through 'financialDB_company_data_and_source.yaml'
dictionary.

Dependent on financialDB_operations
"""
from financialDB_operations import *
import pandas as pd
# import numpy as np


def bulk_financial_statement_values_insert():
    with open('financialDB_company_data_and_source.yaml', 'r') as g:
        company_info_dict = yaml.safe_load(g.read())

    logger.debug(f"Dictionary details >\nCompany Name: {company_info_dict['Company Name']}, "
                 f"Excel File Name: {company_info_dict['Excel Name']},"
                 f"Excel Sheet Name: {company_info_dict['Sheet Name']}")

    # Get Company Data and retrieve company_id for data
    filtered_company = get_company(company_info_dict['Company Name'])

    # Dictionary for Insertion Input -> to incl. Company Name, Excel Name, Sheet Name

    # Select Financial Years
    if filtered_company is None:
        logger.error(f"{filtered_company} is not found in the database.")
        return  # Terminate process here
    else:
        rows_financial_statement_value_old = session.query(func.count(FinancialStatementValue.id)).scalar()
        logger.debug(f"Number of rows of > financial_statement_value: {rows_financial_statement_value_old}")

        # Extract data from excel sheet
        xlsx_file_name = company_info_dict['Excel Name']
        sheet_name = company_info_dict['Sheet Name']
        index_column = None

        # Extract main data from bulk source, reading from subdirectory (source also have template)
        source_directory_name = "financial_statement_values_source"
        if os.path.isdir(source_directory_name):
            logger.debug(f"Get source directory: {os.path.join(source_directory_name, xlsx_file_name)}")

            # in_path = os.path.join(os.getcwd(), xlsx_filename)  # Current Directory
            in_path = os.path.join(source_directory_name, xlsx_file_name)  # Subdirectory
            df_financial_data = pd.read_excel(in_path, sheet_name=sheet_name, index_col=index_column)
            logger.debug(f"df_retrieved >\n{df_financial_data}")
        else:
            logger.debug(f"{source_directory_name} directory not found")
            return

        logger.debug(f'\n{df_financial_data}')

        # Get Financial Data Items
        ls_financial_statement_items = df_financial_data[df_financial_data.columns[0]].values
        logger.debug(f"Financial Data Items detected:\n{ls_financial_statement_items}\n")

        # Extract Financial Value Data
        # Require indexing by element (Item Name and Year). Not possible to insert row due to database requirements

        # Assuming Column 0, and 1 are Item name and Source Document respectively
        input_financial_value = df_financial_data[df_financial_data.columns[2:]]  # Get only values
        logger.debug(f"Dataframe of values:\n{input_financial_value}\n")

        # Get Financial Years
        ls_financial_years = input_financial_value.columns.values
        logger.debug(f"Year columns:\n{ls_financial_years}\n")

        # Loop Through Year
        for year_index, year in enumerate(ls_financial_years):
            logger.debug(f"Year_index: {year_index}, year: {year}")

            ls_financial_values = input_financial_value[input_financial_value.columns[year_index]]
            # Inner Loop Through Financial Statement Items
            for item_index, item in enumerate(ls_financial_statement_items):
                logger.debug(f"Item_index: {item_index}, item: {item}, value: {ls_financial_values[item_index]}")

                # Check if Financial Statement Items is already present. If not pass and send warning.
                filtered_financial_statement_item = session.query(FinancialStatementItem).filter(
                    FinancialStatementItem.item == item).first()

                if filtered_financial_statement_item is None:
                    logger.error(f"{item} is not found in database")
                    pass
                else:
                    # Check if Financial Statement Value is already present. If not proceed with insertion, else pass.
                    filtered_financial_statement_value = session.query(FinancialStatementValue).filter(
                        and_(FinancialStatementValue.company_id == filtered_company.id,
                             FinancialStatementValue.item_id == filtered_financial_statement_item.id,
                             FinancialStatementValue.financial_year == datetime.strftime(
                                 datetime(year, 12, 31), '%Y-%m-%d'))
                    ).first()

                    if filtered_financial_statement_value is None:
                        logger.info(
                            f"{item} data for {year} not found, inserting data as new entry")

                        session.add(FinancialStatementValue(company_id=filtered_company.id,
                                                            item_id=filtered_financial_statement_item.id,
                                                            financial_year=datetime(year, 12, 31),
                                                            value=ls_financial_values[item_index]))

                        session.commit()
                    else:
                        logger.info(f"{item} data for {year}  found, skipping")
                        pass

        rows_financial_statement_value_new = session.query(func.count(FinancialStatementValue.id)).scalar()
        logger.debug(f"Number of rows of > financial_statement_value: {rows_financial_statement_value_new}")
        logger.info(f"Rows inserted > companies: "
                    f"{rows_financial_statement_value_new - rows_financial_statement_value_old}")

        logger.info("~~~ End of financial statement insertion script ~~~")


if __name__ == "__main__":
    bulk_financial_statement_values_insert()
