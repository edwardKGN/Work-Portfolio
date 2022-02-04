"""
Author: Edward KGN
Last Update: 04/02/2022

Bulk insertion using specific template .xlsx documents as named below. Useful for initialization of database

Dependent on financialDB_operations
"""
from financialDB_operations import *
import pandas as pd
import os


def bulk_insertion_companies():
    rows_companies_old = session.query(func.count(Company.id)).scalar()
    logger.debug(f"Number of rows of > companies: {rows_companies_old}")

    # User Input / Setting
    xlsx_file_name = "CompaniesData.xlsx"
    sheet_name = "Sheet1"
    index_column = 0

    # Extract main data from bulk source, reading from subdirectory (source also have template)
    source_directory_name = "company_data_source"
    if os.path.isdir(source_directory_name):
        logger.debug(f"Get source directory: {os.path.join(source_directory_name, xlsx_file_name)}")

        # in_path = os.path.join(os.getcwd(), xlsx_filename)  # Current Directory
        in_path = os.path.join(source_directory_name, xlsx_file_name)  # Subdirectory
        df_company_data = pd.read_excel(in_path, sheet_name=sheet_name, index_col=index_column)
        logger.debug(f"df_retrieved >\n{df_company_data}")
    else:
        logger.debug(f"{source_directory_name} directory not found")
        return

    # Current Directory
    # df_company_data = pd.read_excel(xlsx_name, sheet_name=sheet_name, index_col=index_column)

    # Iterate through rows
    for index, row in df_company_data.iterrows():
        logger.debug(f"Index: '{index}', {type(index)}, Row >\n{row}\n{row['ticker']}, {type(row['ticker'])}, "
                     f"{row['exchange']}, {row['sector']}, {row['industry']}\n")

        if isinstance(index, str):
            index_cleaned = index.strip()
        else:
            index_cleaned = index

        # Check if data in rows are already present in database, pass, else proceed to insert
        filtered_company = session.query(Company).filter(
            Company.name == index_cleaned).first()  # Direct Search to streamline process
        logger.debug(f"Direct Search Result: {filtered_company}")

        # filtered_company = get_company(index_cleaned)  # Bug: Bypasses close matches

        if filtered_company is not None:
            logger.info(f"{index_cleaned} found in database, skipping")
            pass
        else:
            logger.info(f"{index_cleaned} not found in database, inserting")

            # Clean inputs before insertion via stripping
            if isinstance(str(row['ticker']), str):  # Kind of redundant, set as safety net in case conversion failed
                ticker_cleaned = str(row['ticker']).strip()
            else:
                ticker_cleaned = str(row['ticker'])

            if isinstance(row['exchange'], str):
                exchange_cleaned = row['exchange'].strip()
            else:
                exchange_cleaned = row['exchange']

            if isinstance(row['sector'], str):
                sector_cleaned = row['sector'].strip()
            else:
                sector_cleaned = row['sector']

            if isinstance(row['industry'], str):
                industry_cleaned = row['industry'].strip()
            else:
                industry_cleaned = row['industry']

            session.add(Company(name=index_cleaned,
                                ticker=ticker_cleaned,
                                exchange=exchange_cleaned,
                                sector=sector_cleaned,
                                industry=industry_cleaned))
            session.commit()

    rows_companies_new = session.query(func.count(Company.id)).scalar()
    logger.debug(f"New number of rows > companies: {rows_companies_new}")

    logger.info(f"Rows inserted > companies: {rows_companies_new - rows_companies_old}")

    logger.debug("~~~ End of bulk company insertion script ~~~")


def bulk_insertion_financial_statement_items():
    rows_financial_statement_item_old = session.query(func.count(FinancialStatementItem.id)).scalar()
    logger.debug(f"Number of rows of > rows_financial_statement_item_old: {rows_financial_statement_item_old}")

    # User Input / Setting
    xlsx_file_name = "unique_financial_statement_items.xlsx"
    sheet_name = "unique_financial_statement_item"
    index_column = 0

    # Extract main data from bulk source, reading from subdirectory (source also have template)
    source_directory_name = "financial_statement_items_source"
    if os.path.isdir(source_directory_name):
        logger.debug(f"Get source directory: {os.path.join(source_directory_name, xlsx_file_name)}")

        # in_path = os.path.join(os.getcwd(), xlsx_filename)  # Current Directory
        in_path = os.path.join(source_directory_name, xlsx_file_name)  # Subdirectory
        df_financial_statement_data = pd.read_excel(in_path, sheet_name=sheet_name, index_col=index_column)
        logger.debug(f"df_retrieved >\n{df_financial_statement_data}")
    else:
        logger.debug(f"{source_directory_name} directory not found")
        return

    # Iterate through rows
    for index, row in df_financial_statement_data.iterrows():
        logger.debug(f"Index: {index}, {type(index)}, Row >\n{row}\n{row['source_document']}, {row['unit']}\n")

        if isinstance(index, str):
            index_cleaned = index.strip()
        else:
            index_cleaned = index

        # print(f"'{index_cleaned}'")

        # Check if data in rows are already present in database, pass, else proceed to insert
        filtered_financial_statement_item = session.query(FinancialStatementItem).filter(
            FinancialStatementItem.item.like(index_cleaned)).first()  # Direct Search to streamline process
        logger.debug(f"Direct Search Result: {filtered_financial_statement_item}")

        # filtered_financial_statement_item = get_financial_statement_item(index_cleaned)  # Search error Detected

        if filtered_financial_statement_item is not None:
            logger.info(f"'{index_cleaned}' found in database, skipping")
            pass
        else:
            logger.info(f"'{index_cleaned}' not found in database, inserting")

            # Clean inputs before insertion via stripping
            if isinstance(row['source_document'], str):
                source_document_cleaned = row['source_document'].strip()
            else:
                source_document_cleaned = row['source_document']

            logger.debug(f"'{source_document_cleaned}'")

            if isinstance(row['unit'], str):
                unit_cleaned = row['unit'].strip()
            else:
                unit_cleaned = row['unit']

            logger.debug(f"'{unit_cleaned}'")

            session.add(FinancialStatementItem(item=index_cleaned,
                                               source_document=source_document_cleaned,
                                               units=unit_cleaned))
            session.commit()

    rows_financial_statement_item_new = session.query(func.count(FinancialStatementItem.id)).scalar()
    logger.debug(f"New number of rows > companies: {rows_financial_statement_item_new}")

    logger.info(f"Rows inserted > financial_statement_item: "
                f"{rows_financial_statement_item_new - rows_financial_statement_item_old}")

    logger.debug("~~~ End of bulk financial_statement_item insertion script ~~~")


if __name__ == "__main__":
    bulk_insertion_companies()
    bulk_insertion_financial_statement_items()
