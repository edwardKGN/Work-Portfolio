"""
Author: Edward KGN
Last Update: 04/02/2022

A Simple Command Line Interface to interact with underlying database.
These codes are the foundation for further advanced functions such as bulk insertions, viewers and analytics.
"""

# Other Modules
from sqlalchemy import create_engine, inspect, MetaData, Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import and_  # , or_
from datetime import datetime  # , time
from sqlalchemy import func

# Other Modules
import logging.config  # To return process logs
import yaml  # Need PyYAML module
import os

# Setup log directories
debug_directory_destination = "debug_log"
if os.path.isdir(debug_directory_destination):
    # print(f"Get destination directory: {os.path.join(destination_directory_name)}")
    print(f"{debug_directory_destination} directory found")
else:
    print(f"{debug_directory_destination} directory not found")
    os.makedirs(debug_directory_destination)

info_directory_destination = "info_log"
if os.path.isdir(info_directory_destination):
    print(f"{info_directory_destination} log destination found")
else:
    print(f"{info_directory_destination} destination not found")
    os.makedirs(info_directory_destination)

# Access logger config dictionary
with open('financialDB_operations_logging.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

# Create access to custom_logger
logger = logging.getLogger('financialDB_operations_logger')
logger.setLevel(logging.DEBUG)

# Create Engine/Connection to database
engine = create_engine('sqlite:///financialDB_demo.db')  # Using sqlite type with name 'financialDB.db'

base = declarative_base()

inspector = inspect(engine)  # Creates inspector object


# Declaring relationship map of tables
class Company(base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    ticker = Column(String(10))
    exchange = Column(String(10))
    sector = Column(String(50))
    industry = Column(String(50))

    financial_statement_values = relationship("FinancialStatementValue",
                                              back_populates="companies",
                                              cascade="all, delete, delete-orphan")

    # If parent is deleted, all child are deleted

    def __repr__(self):
        return "<Company(id='{0}', name='{1}', ticker='{2}', exchange='{3}', sector='{4}', industry='{5}'>".format(
            self.id, self.name, self.ticker, self.exchange, self.sector, self.industry)


class FinancialStatementItem(base):
    __tablename__ = "financial_statement_items"

    id = Column(Integer, primary_key=True)
    item = Column(String(100))
    source_document = Column(String(100))
    units = Column(String(20))

    financial_statement_values = relationship("FinancialStatementValue",
                                              back_populates="financial_statement_items",
                                              cascade="all, delete, delete-orphan")

    # If parent is deleted, all child are deleted

    def __repr__(self):
        return "<FinancialStatementItem(id='{0}', item='{1}', source_document='{2}', units='{3}'>".format(
            self.id, self.item, self.source_document, self.units)


class FinancialStatementValue(base):
    __tablename__ = "financial_statement_values"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    item_id = Column(Integer, ForeignKey('financial_statement_items.id'))
    financial_year = Column(Date)
    value = Column(Float)

    financial_statement_items = relationship("FinancialStatementItem", back_populates="financial_statement_values")
    companies = relationship("Company", back_populates="financial_statement_values")

    def __repr__(self):
        return "<FinancialStatementValue(id='{0}', company_id='{1}', item_id='{2}', " \
               "financial_year='{3}', value='{4}'>".format(self.id, self.company_id, self.item_id, self.financial_year,
                                                           self.value)


metadata = MetaData()  # Create empty metadata dictionary for key-pair = "dictionary name"-"table"
metadata.reflect(bind=engine)  # Get database's metadata

# Create table if not present (by default, checks if table is not created and creates them
base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def get_company(input_company_name):  # Relative Search
    company_search_query = "%" + input_company_name + "%"
    logger.debug(f"company_search_query: {company_search_query}")

    filtered_companies = session.query(Company).filter(
        Company.name.like(company_search_query)).all()

    logger.debug(f'Entry extracted: {filtered_companies}')

    print(f'Entry extracted: \n{filtered_companies}')

    returned_company = None  # Set initial value

    if filtered_companies is None or len(filtered_companies) == 0:
        print(f"{input_company_name} not found in database")
    else:
        print(f"Query match(es) found for {input_company_name} >")

        for filtered_company_index, filtered_company in enumerate(filtered_companies):
            print(f"{filtered_company_index} > {filtered_company.name}")

        print(f"If matches are false positive, press Q")

        while True:  # Get user Input
            selected_company_index = input("Desired company index > ").upper()

            if selected_company_index == "Q":
                print("False positive confirmed. Returning none")
                break
            elif len(selected_company_index) == 0:
                print("Invalid entry received")
                pass
            elif selected_company_index.isdigit():
                if (0 > int(selected_company_index)) or (int(selected_company_index) > len(filtered_companies) - 1):
                    print("Invalid index")
                    pass
                elif 0 <= int(selected_company_index) <= (len(filtered_companies) - 1):
                    print(f"Company data retrieved > {filtered_companies[int(selected_company_index)].name}")
                    returned_company = filtered_companies[int(selected_company_index)]
                    break
                else:
                    print("Invalid entry received")
                    pass
            else:
                print("Invalid entry received")
                pass

    return returned_company


def get_financial_statement_item(input_financial_statement_item):  # Relative Search
    financial_statement_item_search_query = "%" + input_financial_statement_item + "%"
    logger.debug(f"financial_statement_item_search_query: {financial_statement_item_search_query}")

    filtered_financial_statement_items = session.query(FinancialStatementItem).filter(
        FinancialStatementItem.item.like(financial_statement_item_search_query)).all()

    logger.debug(f"Entry extracted: \n{filtered_financial_statement_items}")

    returned_financial_statement_item = None

    if filtered_financial_statement_items is None or len(filtered_financial_statement_items) == 0:
        print(f"{input_financial_statement_item} not found in database")
    else:
        print(f"Query match(es) found for {input_financial_statement_item} >")

        for filtered_financial_statement_items_index, filtered_financial_statement_item \
                in enumerate(filtered_financial_statement_items):
            print(f"{filtered_financial_statement_items_index} > {filtered_financial_statement_item.item}")

        print(f"If false positive, press Q")

        while True:
            selected_financial_statement_item_index = input("Desired financial statement item index > ").upper()

            if selected_financial_statement_item_index == "Q":
                print("False positive confirmed. Returning none")
                break
            elif len(selected_financial_statement_item_index) == 0:
                print("Invalid entry received")
                pass
            elif selected_financial_statement_item_index.isdigit():
                if (0 > int(selected_financial_statement_item_index)) or \
                        (int(selected_financial_statement_item_index) > len(filtered_financial_statement_items) - 1):
                    print("Invalid index")
                    pass
                elif 0 <= int(selected_financial_statement_item_index) <= (len(filtered_financial_statement_items) - 1):
                    print(f"Retrieved financial statement item > "
                          f"{filtered_financial_statement_items[int(selected_financial_statement_item_index)].item}")
                    returned_financial_statement_item = \
                        filtered_financial_statement_items[int(selected_financial_statement_item_index)]
                    break
                else:
                    print("Invalid entry received")
            else:
                print("Invalid entry received")

    return returned_financial_statement_item


def get_financial_statement_value(input_company_name, input_financial_statement_item, input_financial_year):
    filtered_company = get_company(input_company_name)
    filtered_financial_statement_item = get_financial_statement_item(input_financial_statement_item)

    if filtered_company is None:
        logger.error(f"{input_company_name} is not found in the database")
        return None
    elif filtered_financial_statement_item is None:
        logger.error(f"{input_financial_statement_item} is not found in the database")
        return None
    else:
        filtered_financial_statement_value = session.query(FinancialStatementValue).filter(
            and_(FinancialStatementValue.company_id == filtered_company.id,
                 FinancialStatementValue.item_id == filtered_financial_statement_item.id,
                 FinancialStatementValue.financial_year == datetime.strftime(
                     datetime(int(input_financial_year), 12, 31), '%Y-%m-%d'))).first()

        logger.debug(f"Entry extracted: {filtered_financial_statement_value}")

        return filtered_financial_statement_value


def view_company():
    input_company_name = input("Enter company name > ")
    returned_company = get_company(input_company_name)

    if returned_company is None:
        logger.info(f"{input_company_name} is not found in database")
    else:
        logger.info(f"Returned company details > \n"
                    f"Name: {returned_company.name}\n"
                    f"Ticker: {returned_company.ticker}\n"
                    f"Exchange: {returned_company.exchange}\n"
                    f"Sector: {returned_company.sector}\n"
                    f"Industry: {returned_company.industry}")


def view_financial_statement_item():
    input_financial_statement_item = input("Enter financial statement item's name > ")
    returned_financial_statement_item = get_financial_statement_item(input_financial_statement_item)

    if returned_financial_statement_item is None:
        logger.info(f"{input_financial_statement_item} is not found in database")
    else:
        logger.info(f"Returned financial statement item >\n"
                    f"Item: {returned_financial_statement_item.item}\n"
                    f"Source document: {returned_financial_statement_item.source_document}\n"
                    f"Units: {returned_financial_statement_item.units}")


def view_financial_statement_value():
    input_company_name = input("Enter company name > ")
    input_financial_statement_item = input("Enter financial statement item's name > ")
    input_financial_year = input("Enter financial year > ")
    returned_financial_statement_value = get_financial_statement_value(input_company_name,
                                                                       input_financial_statement_item,
                                                                       input_financial_year)

    if returned_financial_statement_value is None:
        logger.info(f"Financial statement value is not found in database")
    else:
        logger.info(f"Returned financial statement value >\n"
                    f"Company ID: {returned_financial_statement_value.company_id}\n"
                    f"Item ID: {returned_financial_statement_value.item_id}\n"
                    f"Financial Year: {returned_financial_statement_value.financial_year}\n"
                    f"Value: {returned_financial_statement_value.value}")


def insert_company():
    # Initial Row prior to Insertion
    rows_companies_old = session.query(func.count(Company.id)).scalar()
    logger.debug(f"Number of rows of > companies: {rows_companies_old}")

    input_company_name = input("Enter company name > ")
    filtered_company = get_company(input_company_name)

    # Report if Company data is present and return the id for Foreign Key input in FinancialStatementValue table
    if filtered_company is not None:
        logger.info(f"{input_company_name} is already in companies database")
    else:
        # Insertion Script
        logger.info(f"{input_company_name} does not exist in database. Proceeding with insertion protocols.")

        # Get Full Company Name from user after checking if previous entry is not Full Name

        # Initialization for While loop
        input_company_ticker = None
        input_company_exchange = None
        input_company_sector = None
        input_company_industry = None

        while input_company_ticker is None:
            input_company_ticker = input("No ticker found, input company ticker > ")

        while input_company_exchange is None:
            input_company_exchange = input("No stock exchange found, input company's stock exchange > ")

        while input_company_sector is None:
            input_company_sector = input("No company sector found, input company's sector > ")

        while input_company_industry is None:
            input_company_industry = input("No company industry found, input company's industry > ")

        logger.info(f"Company details input are as follows > "
                    f"\nName: {input_company_name}"
                    f"\nTicker: {input_company_ticker}"
                    f"\nCompany's Exchange: {input_company_exchange}"
                    f"\nCompany's Sector: {input_company_sector}"
                    f"\nCompany's Industry: {input_company_industry}")

        # Get user's confirmation that information is valid
        # user_data_confirmation = False

        session.add(Company(name=input_company_name,
                            ticker=input_company_ticker,
                            exchange=input_company_exchange,
                            sector=input_company_sector,
                            industry=input_company_industry))
        session.commit()

    rows_companies_new = session.query(func.count(Company.id)).scalar()
    logger.debug(f"New number of rows > companies: {rows_companies_new}")

    logger.info(f"Rows inserted > companies: {rows_companies_new - rows_companies_old}")

    logger.debug("~~~ End of company insertion script ~~~")
    return


def insert_financial_statement_item():
    # Initial Row prior to Insertion
    rows_financial_statement_item_old = session.query(func.count(FinancialStatementItem.id)).scalar()
    logger.debug(f"Number of rows of > companies: {rows_financial_statement_item_old}")

    input_financial_statement_item = input("Enter financial statement item > ")
    filtered_financial_statement_item = get_financial_statement_item(input_financial_statement_item)

    if filtered_financial_statement_item is None:
        logger.info(f"{input_financial_statement_item} not found in database. Proceeding with insertion protocols.")

        input_source_document = None
        input_units = None

        while input_source_document is None:
            input_source_document = input("No source document found, enter source document > ")

        while input_units is None:
            input_units = input("No units found, enter units > ")

        session.add(FinancialStatementItem(item=input_financial_statement_item,
                                           source_document=input_source_document,
                                           units=input_units))
        session.commit()

    else:
        logger.info(f"{input_financial_statement_item} found in database. Terminating process")

    rows_financial_statement_item_new = session.query(func.count(FinancialStatementItem.id)).scalar()
    logger.debug(f"Number of rows of > financial_statement_items: {rows_financial_statement_item_new}")

    logger.info(f"Rows inserted > financial_statement_items: "
                f"{rows_financial_statement_item_new - rows_financial_statement_item_old}")

    logger.debug("~~~ End of financial_statement_items insertion script ~~~")
    return


# Slight inconsistency with insertion
def insert_financial_statement_value():
    # Initial Row prior to Insertion
    rows_financial_statement_value_old = session.query(func.count(FinancialStatementValue.id)).scalar()
    logger.debug(f"Number of rows of > financial_statement_value: {rows_financial_statement_value_old}")

    input_company_name = input("Enter company name > ")
    filtered_company = get_company(input_company_name)

    input_financial_statement_item = input("Enter financial statement unit > ")
    filtered_financial_statement_item = get_financial_statement_item(input_financial_statement_item)

    input_financial_year = input("Enter financial year > ")

    # Check if value already present
    filtered_financial_statement_value = get_financial_statement_value(input_company_name,
                                                                       input_financial_statement_item,
                                                                       input_financial_year)

    if filtered_financial_statement_value is None:
        input_value = input("Enter value > ")

        logger.info("Financial statement value does not exist in database. Inserting new entry")
        session.add(FinancialStatementValue(company_id=filtered_company.id,
                                            item_id=filtered_financial_statement_item.id,
                                            financial_year=datetime(int(input_financial_year), 12, 31),
                                            value=input_value))
        session.commit()

        logger.info(f"Inserted entry are > \n"
                    f"Company_id = {filtered_company.id}\n"
                    f"Item_id = {filtered_financial_statement_item.id}\n"
                    f"Financial Year = {datetime.strftime(datetime(int(input_financial_year), 12, 31), '%Y-%m-%d')}"
                    f"\n"  # As it appears in database.
                    f"Value = {input_value}")

    else:
        logger.info("Financial statement value already present in database. Terminating process")
        return

    rows_financial_statement_value_new = session.query(func.count(FinancialStatementValue.id)).scalar()
    logger.debug(f"Number of rows of > financial_statement_value: {rows_financial_statement_value_new}")
    logger.info(f"Rows inserted > companies: "
                f"{rows_financial_statement_value_new - rows_financial_statement_value_old}")

    logger.debug("~~~ End of financial_statement_value insertion script ~~~")

    return


def update_company():
    input_company_name = input("Enter company name > ")
    filtered_company = get_company(input_company_name)

    while True:
        logger.info(f"Which item do you want to update?\n"
                    f"A) Name: {filtered_company.name}\n"
                    f"B) Ticker: {filtered_company.ticker}\n"
                    f"C) Exchange: {filtered_company.exchange}\n"
                    f"D) Sector: {filtered_company.sector}\n"
                    f"E) Industry: {filtered_company.industry}\n"
                    f"Q) Quit")

        user_response = input(f"> ").upper()

        if len(user_response) > 1:
            logger.warning("User response exceeded length limit of 1")
            continue
        elif user_response in 'ABCDEQ':
            break  # Exit while loop when desired response is met
        else:
            logger.warning("Invalid response received")
            continue

    if user_response == "A":
        new_company_name = input("Enter new name > ")
        filtered_company.name = new_company_name
    elif user_response == "B":
        new_ticker = input("Enter new ticker > ")
        filtered_company.ticker = new_ticker
    elif user_response == "C":
        new_exchange = input("Enter new exchange > ")
        filtered_company.exchange = new_exchange
    elif user_response == "D":
        new_sector = input("Enter new sector > ")
        filtered_company.sector = new_sector
    elif user_response == "E":
        new_industry = input("Enter new industry > ")
        filtered_company.industry = new_industry
    elif user_response == "Q":
        logger.info("Exiting process")
        return
    else:
        logger.error("Invalid user response received, terminating process")
        return

    logger.info(f"New company details are as follows > \n"
                f"Name: {filtered_company.name}\n"
                f"Ticker: {filtered_company.ticker}\n"
                f"Exchange: {filtered_company.exchange}\n"
                f"Sector: {filtered_company.sector}\n"
                f"Industry: {filtered_company.industry}")

    session.commit()


def update_financial_statement_item():
    item_name = input("Enter financial statement item > ")
    filtered_financial_statement_item = get_financial_statement_item(item_name)

    if filtered_financial_statement_item is None:
        logger.error(f"{item_name} not found in database. Terminating process")
    else:
        while True:
            print(f"Which item do you wish to update?\n"
                  f"A) Item name: {filtered_financial_statement_item.item}\n"
                  f"B) Source document: {filtered_financial_statement_item.source_document}\n"
                  f"C) Units: {filtered_financial_statement_item.units}\n"
                  f"Q) Quit")

            user_response = input("> ")

            if len(user_response) > 1:
                logger.warning("User response exceeded length limit of 1.")
                continue
            elif user_response in "ABCQ":
                break
            else:
                logger.warning("Invalid user response received.")
                continue

        if user_response == "A":
            new_item_name = input("Enter new item name > ")
            filtered_financial_statement_item.item = new_item_name
        elif user_response == "B":
            new_source_document = input("Enter new source document > ")
            filtered_financial_statement_item.source_document = new_source_document
        elif user_response == "C":
            new_units = input("Enter new units > ")
            filtered_financial_statement_item.units = new_units
        elif user_response == "Q":
            logger.info("Exiting process")
            return
        else:
            logger.error("Invalid user response received. Terminating process")
            return

        logger.info(f"New financial statement item details are as follows >\n"
                    f"Item: {filtered_financial_statement_item.item}\n"
                    f"Source document: {filtered_financial_statement_item.source_document}\n"
                    f"Units: {filtered_financial_statement_item.units}")

        session.commit()


def update_financial_statement_value():
    input_company_name = input("Enter company name > ")
    filtered_company = get_company(input_company_name)

    input_financial_statement_item = input("Enter financial statement unit > ")
    filtered_financial_statement_item = get_financial_statement_item(input_financial_statement_item)

    input_financial_year = input("Enter financial year > ")

    # Check if value already present
    filtered_financial_statement_value = get_financial_statement_value(input_company_name,
                                                                       input_financial_statement_item,
                                                                       input_financial_year)

    if filtered_financial_statement_value is None:
        logger.info("Financial statement value does not exist in database. Terminating process")
        return
    else:
        logger.info("Financial statement value present in database")

        # Jump menu to select specific entry to update
        while True:
            print(f"Which item do you wish to update?\n"
                  f"A) Company name: {filtered_company.name}\n"  # Used company name for readability
                  f"B) Item: {filtered_financial_statement_item.item}\n"  # Used item name for readability
                  f"C) Financial Year: {filtered_financial_statement_value.financial_year}\n"
                  f"D) Value: {filtered_financial_statement_value.value}\n"
                  f"Q) Quit")

            user_response = input("> ").upper()

            if len(user_response) > 1:
                logger.warning("User response exceeded length limit of 1.")
                continue
            elif user_response in "ABCDQ":
                break
            else:
                logger.warning("Invalid user response received.")
                continue

        if user_response == "A":
            new_company_name = input("Enter new company's name > ")
            filtered_company = get_company(new_company_name)

            if filtered_company is None:
                logger.error(f"{new_company_name} does not exist in database. Terminating process")
            else:
                filtered_financial_statement_value.company_id = filtered_company.id
        elif user_response == "B":
            new_item_name = input("Enter new item's name > ")
            filtered_financial_statement_item = get_financial_statement_item(new_item_name)

            if filtered_financial_statement_item is None:
                logger.error(f"{new_item_name} does not exist in database. Terminating process")
            else:
                filtered_financial_statement_value.item_id = filtered_financial_statement_item.id
        elif user_response == "C":
            new_financial_year = input("Enter new financial year > ")
            filtered_financial_statement_value.financial_year = datetime(int(new_financial_year), 12, 31)
        elif user_response == "D":
            new_value = input("Enter new value > ")
            filtered_financial_statement_value.value = new_value
        else:
            logger.error("Invalid user response received")
            return

        logger.info(f"New financial statement value > \n"
                    f"Company ID: {filtered_financial_statement_value.company_id}\n"
                    f"Item ID: {filtered_financial_statement_value.item_id}\n"
                    f"Financial Year: {filtered_financial_statement_value.financial_year}\n"
                    f"Value: {filtered_financial_statement_value.value}")

        session.commit()


def remove_company():
    input_company_name = input("Enter company name > ")
    filtered_company = get_company(input_company_name)

    if filtered_company is None:
        logger.info(f"{input_company_name} does not exist in database")
        return
    else:
        logger.info(f"{input_company_name} found. Deleting")

        session.delete(filtered_company)
        session.commit()

        # Check if removal was successful
        filtered_company = get_company(input_company_name)

        if filtered_company is None:
            logger.info(f"{input_company_name} is removed from database")
        else:
            logger.warning(f"{input_company_name} is still present in database")

        return


def remove_financial_statement_item():
    item_name = input("Enter financial statement item > ")
    filtered_financial_statement_item = get_financial_statement_item(item_name)

    if filtered_financial_statement_item is None:
        logger.info(f"{item_name} not found in database")
        return
    else:
        logger.info(f"{item_name} found. Deleting")

        session.delete(filtered_financial_statement_item)
        session.commit()

        # Check if removal was successful
        filtered_financial_statement_item = get_financial_statement_item(item_name)

        if filtered_financial_statement_item is None:
            logger.info(f"{item_name} is removed from database")
        else:
            logger.info(f"{item_name} is still present in database")
        return


def remove_financial_statement_value():
    input_company_name = input("Enter company name > ")
    input_financial_statement_item = input("Enter financial statement unit > ")
    input_financial_year = input("Enter financial year > ")

    # Check if value already present
    filtered_financial_statement_value = get_financial_statement_value(input_company_name,
                                                                       input_financial_statement_item,
                                                                       input_financial_year)

    if filtered_financial_statement_value is None:
        logger.info("Financial statement value does not exist in database. Terminating process")
        return
    else:
        logger.info("Financial statement value exist in database. Deleting entry")

        session.delete(filtered_financial_statement_value)
        session.commit()

        # Check if removal was successful
        filtered_financial_statement_value = get_financial_statement_value(input_company_name,
                                                                           input_financial_statement_item,
                                                                           input_financial_year)

        if filtered_financial_statement_value is None:
            logger.info(f"Financial statement value is removed from database")
        else:
            logger.info(f"Financial statement value is still present in database")
        return


if __name__ == "__main__":
    # CLI Jump Menu for Users
    while True:
        logger.debug("~~~ New Process ~~~")

        print("What do you wish to do with the database?\n"
              "A) View an entry\n"
              "B) Insert a new entry\n"
              "C) Update an entry\n"
              "D) Delete an entry \n"
              "Q) Quit\n")
        user_action = input("> ").upper()

        if user_action == "Q":
            logger.info("Exiting program")
            break

        print("Which entry do you wish to interact with?\n"
              "A) Companies\n"
              "B) Financial Statement Items\n"
              "C) Financial Statement Values\n")
        entry_type = input("> ").upper()

        if user_action in "ABCD" and entry_type in "ABC":
            if user_action == "A":

                if entry_type == "A":
                    view_company()
                elif entry_type == "B":
                    view_financial_statement_item()
                elif entry_type == "C":
                    view_financial_statement_value()
                else:
                    logger.error("Invalid response received. Terminating process")
                    break

            elif user_action == "B":

                if entry_type == "A":
                    insert_company()
                elif entry_type == "B":
                    insert_financial_statement_item()
                elif entry_type == "C":
                    insert_financial_statement_value()
                else:
                    logger.error("Invalid entry type, terminating process")
                    break
            elif user_action == "C":

                if entry_type == "A":
                    update_company()
                elif entry_type == "B":
                    update_financial_statement_item()
                elif entry_type == "C":
                    update_financial_statement_value()
                else:
                    logger.error("Invalid entry type, terminating process")
                    break

            elif user_action == "D":

                if entry_type == "A":
                    remove_company()
                elif entry_type == "B":
                    remove_financial_statement_item()
                elif entry_type == "C":
                    remove_financial_statement_value()
                else:
                    logger.error("Invalid entry type, terminating process")
                    break

            else:
                logger.error("Invalid user response received")
                break

            logger.debug("~~~ End of Process ~~~")

            # A pause before continuing to next loop
            input("Press Enter to continue...\n")
            continue
        elif len(user_action) > 1 or len(entry_type) > 1:
            logger.error("User response exceed length limit of 1")
            continue
        else:
            logger.error("Invalid input detected")
            continue

    # insert_company()
    # update_company()
    # remove_company()

    # insert_financial_statement_item()
    # update_financial_statement_item()
    # remove_financial_statement_item()

    # insert_financial_statement_value()
    # update_financial_statement_value()
    # remove_financial_statement_value()
