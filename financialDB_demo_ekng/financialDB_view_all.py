"""
Author: Edward KGN
Last Update: 29/01/2022

Simple view all system for tables with few entries expected such as companies and financial statement items.
Can be computationally-taxing if the database is large (many entries)

Dependent on financialDB_operations
"""
from financialDB_operations import *


def view_all_companies():
    returned_companies = session.query(Company).all()

    for company in returned_companies:
        print(company)


def view_all_financial_statement_items():
    returned_financial_statement_items = session.query(FinancialStatementItem).all()

    for item in returned_financial_statement_items:
        print(item)


if __name__ == "__main__":
    view_all_companies()
    view_all_financial_statement_items()
