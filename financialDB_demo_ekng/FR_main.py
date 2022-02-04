"""
Author: Edward KGN
Last Update: 29/01/2022

Object-Oriented Encapsulation of Financial Ratios extractor, calculator, and write-out.
Consists of a base class FR_main and a number of general sub-classes Valuation, Profitability etc and further
sub-sub-classes such as FR_default, FR_banking, FR_insurance and FR_reit.

The main class defines the methods to extract data from a dataframe, and write-out.
A separate function, calculate_financial_ratio, is used to calculate financial ratios.
The sub-sub-classes defines which financial ratios are called to be calculated.
"""

import itertools
import logging.config  # To return process logs
import pandas as pd
import numpy as np
import os
import yaml  # Need PyYAML module

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

with open('financialDB_analytics_logging.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

# Create access to custom_logger
logger = logging.getLogger('financialDB_analytics_logger')
logger.setLevel(logging.DEBUG)


# Overall Function
def calculate_financial_ratio(numerators, denominators):
    financial_ratio_row = []

    for index, numerator in enumerate(numerators):
        if denominators[index] == 0:
            financial_ratio_row.append(0)  # Avoid division by 0
        else:
            financial_ratio_row.append(numerator / denominators[index])

    return np.array(financial_ratio_row)  # Allow application of math operations


# Base Class
class FR_main:
    df_FR = None
    df_values = None
    ls_financial_years = []

    def __init__(self, df_values):
        self.df_values = df_values
        self.ls_financial_years = df_values.columns[1:]

        # print(self.ls_financial_years)

        ls_columns = list(itertools.chain(["Financial Ratios"], self.ls_financial_years))
        # Create dataframe to hold values
        self.df_FR = pd.DataFrame(columns=ls_columns)

    def get_FR(self):
        return self.df_FR

    def get_financial_years(self):
        return self.ls_financial_years

    def get_values(self):
        return self.df_values

    def get_financial_statement_values_row(self, financial_statement_item):
        # print(self.df_values.columns[0], self.df_values[self.df_values.columns[0]])

        # Code requires this to aggregate true-false values
        if (self.df_values[self.df_values.columns[0]] == financial_statement_item).any():
            # print((self.df_values.loc[
            # self.df_values[self.df_values.columns[0]] == financial_statement_item]).values[0][1:])
            return (self.df_values.loc[
                self.df_values[self.df_values.columns[0]] == financial_statement_item]).values[0][1:]
        else:
            logger.warning(f"{financial_statement_item} not found")
            return np.zeros(len(self.get_financial_years()))

    def set_financial_ratios(self, financial_ratio_name, financial_ratio_row):
        df_FR_dict = {"Financial Ratios": financial_ratio_name}
        self.df_FR = self.df_FR.append(df_FR_dict, ignore_index=True)  # Create new row with financial_ratio_name

        # print(f"Post-insertion > {self.df_FR}")

        for index, item in enumerate(financial_ratio_row):
            logger.debug(f"Year: {self.ls_financial_years[index]}, item: {item}")
            self.df_FR.loc[self.df_FR[self.df_FR.columns[0]] == financial_ratio_name,
                           self.ls_financial_years[index]] = item

    def write_out(self, company_name):
        # Check if subdirectory destination has been created. If not, create said subdirectory
        logger.info(f"Writing out to {company_name}_FR_output.xlsx")

        destination_directory_name = "FR_output"
        if not os.path.isdir(destination_directory_name):  # If not existent already
            os.makedirs(destination_directory_name)

        xlsx_filename = company_name + "_FR_output.xlsx"

        out_path = os.path.join(destination_directory_name, xlsx_filename)  # subdirectory

        writer = pd.ExcelWriter(out_path)

        self.df_FR.to_excel(writer, sheet_name='FR_sheet')
        writer.save()

        return


class FR_valuation_general(FR_main):
    """
    List of Financial Ratios
    # Valuation
    - Market Cap (as of 31/12 of Financial Year)
    - Price to Book
    - Price to Earnings
    - Composite PB and PB
    - Price to Net Working Capital (Prefer less than 1)
    - Price to 2/3 Value (Prefer less than 1)
    """

    def analyze_valuation_gen(self):
        # print(self.price_to_book())
        self.set_financial_ratios("Market Capitalization", self.market_cap())
        self.set_financial_ratios("Price to Book", self.price_to_book())
        self.set_financial_ratios("Price to Earnings", self.price_to_earnings())
        self.set_financial_ratios("Composite PB and PE", self.price_to_book() * self.price_to_earnings())
        self.set_financial_ratios("Price to Net Working Capital", self.price_to_net_working_capital())
        self.set_financial_ratios("Price to Two Thirds Value", self.price_to_two_third_value())

    def market_cap(self):
        # Large Capitalization if < $10 billion ~= MYR 40 billion
        market_cap = (self.get_financial_statement_values_row("Share Unit Price") *
                      self.get_financial_statement_values_row("Outstanding Shares")) / 1000

        return np.array(market_cap)

    def price_to_book(self):
        # Prefer < 1.5
        market_cap = self.market_cap()

        book_value = self.get_financial_statement_values_row("Total Assets") - (
                self.get_financial_statement_values_row("Total Liabilities") +
                self.get_financial_statement_values_row("Intangible Assets"))

        return calculate_financial_ratio(market_cap, book_value)

    def price_to_earnings(self):
        # Prefer < 15
        market_cap = self.market_cap()
        net_income = self.get_financial_statement_values_row("Net Income")

        return calculate_financial_ratio(market_cap, net_income)

    def price_to_net_working_capital(self):
        # Based on Benjamin Graham's Intelligent Investor, prefer between [0, 1]
        market_cap = self.market_cap()

        net_working_capital = (self.get_financial_statement_values_row("Current Assets")
                               - self.get_financial_statement_values_row("Total Liabilities"))

        return calculate_financial_ratio(market_cap, net_working_capital)

    def price_to_two_third_value(self):
        # Based on Benjamin Graham's Intelligent Investor, prefer between [0, 1]
        market_cap = self.market_cap()

        PE = self.price_to_earnings()

        # print(f"Internal PE > {PE}, {type(PE)}")

        # From Linear Regression of Table 11-4 of Intelligent Investor book
        expected_annual_growth_rate = 0.005*PE - 0.0425

        # ASSUMPTION: Equivalent to Current (Normal) Earnings
        net_income = self.get_financial_statement_values_row("Net Income")

        value = net_income * (8.5 + 2 * expected_annual_growth_rate)

        return calculate_financial_ratio(market_cap, ((2/3)*value))


class FR_profitability_general(FR_main):
    """
    List of Financial Ratios
    # Profitability
    - Return on Equity
    - Return on Capital Employed
    - Return on Assets

    Preferred value depends on industry average. Generally prefer higher and > 0
    """
    def analyze_profitability_gen(self):
        self.set_financial_ratios("Return on Equity", self.return_on_equity())
        self.set_financial_ratios("Return on Capital Employed", self.return_on_capital_employed())
        self.set_financial_ratios("Return on Assets", self.return_on_assets())

    def return_on_equity(self):
        net_income = self.get_financial_statement_values_row("Net Income")
        shareholders_equity = self.get_financial_statement_values_row("Shareholders Equity")

        return calculate_financial_ratio(net_income, shareholders_equity)

    def return_on_capital_employed(self):
        net_income = self.get_financial_statement_values_row("Net Income")
        total_assets = self.get_financial_statement_values_row("Total Assets")
        current_liabilities = self.get_financial_statement_values_row("Current Liabilities")

        capital_employed = total_assets - current_liabilities

        return calculate_financial_ratio(net_income, capital_employed)

    def return_on_assets(self):
        net_income = self.get_financial_statement_values_row("Net Income")
        total_assets = self.get_financial_statement_values_row("Total Assets")
        intangible_assets = self.get_financial_statement_values_row("Intangible Assets")

        total_tangible_assets = total_assets - intangible_assets

        return calculate_financial_ratio(net_income, total_tangible_assets)


class FR_efficiency_general(FR_main):
    """
    List of Financial Ratios
    # Efficiency
    - Revenue to Expense Ratio
    """
    def analyze_efficiency_gen(self):
        self.set_financial_ratios("Revenue to Expense", self.revenue_to_expense_ratio())

    def revenue_to_expense_ratio(self):
        revenue = self.get_financial_statement_values_row("Revenue")
        tot_expense = self.get_financial_statement_values_row("Total Expenses")

        return calculate_financial_ratio(revenue, tot_expense)


class FR_liquidity_general(FR_main):
    """
        List of Financial Ratios
        # Liquidity
        - Current Ratio
        - Cash Ratio
        - Operating Cashflow Ratio
        - Cash Conversion Ratio
        - Net Operating Cashflow to Net Financing Cashflow Ratio
        """
    def analyze_liquidity_gen(self):
        self.set_financial_ratios("Current Ratio", self.current_ratio())
        self.set_financial_ratios("Cash Ratio", self.cash_ratio())
        self.set_financial_ratios("Operating Cashflow Ratio", self.operating_cashflow_ratio())
        self.set_financial_ratios("Cash Conversion Ratio", self.cash_conversion_ratio())
        self.set_financial_ratios("Net Operating Cashflow to Net Financing Cashflow Ratio",
                                  self.net_operating_cashflow_to_net_financing_cashflow_ratio())

    def current_ratio(self):
        current_assets = self.get_financial_statement_values_row("Current Assets")
        current_liabilities = self.get_financial_statement_values_row("Current Liabilities")

        return calculate_financial_ratio(current_assets, current_liabilities)

    def cash_ratio(self):
        cash_and_cash_equivalent = self.get_financial_statement_values_row("Cash and Cash Equivalent")
        current_liabilities = self.get_financial_statement_values_row("Current Liabilities")

        return calculate_financial_ratio(cash_and_cash_equivalent, current_liabilities)

    def operating_cashflow_ratio(self):
        operating_cash_flow = self.get_financial_statement_values_row("Net Cash Flow from Operations")
        current_liabilities = self.get_financial_statement_values_row("Current Liabilities")

        return calculate_financial_ratio(operating_cash_flow, current_liabilities)

    def cash_conversion_ratio(self):
        operating_cash_flow = self.get_financial_statement_values_row("Net Cash Flow from Operations")
        net_income = self.get_financial_statement_values_row("Net Income")

        return calculate_financial_ratio(operating_cash_flow, net_income)

    def net_operating_cashflow_to_net_financing_cashflow_ratio(self):
        # From Benjamin Graham's Intelligent Investor, prefer > 1
        operating_cash_flow = self.get_financial_statement_values_row("Net Cash Flow from Operations")
        financing_cash_flow = self.get_financial_statement_values_row("Net Cash Flow from Financing")

        return calculate_financial_ratio(operating_cash_flow, financing_cash_flow)


class FR_solvency_general(FR_main):
    """
    List of Solvency Ratios
    # Solvency
    - Debt Ratio
    - Debt to Equity Ratio
    - Interest Coverage Ratio
    - Years to Repay Debt
    - Average Interest Rate
    """
    def analyze_solvency_gen(self):
        self.set_financial_ratios("Debt Ratio", self.debt_ratio())
        self.set_financial_ratios("Debt to Equity Ratio", self.debt_to_equity_ratio())
        self.set_financial_ratios("Interest Coverage Ratio", self.interest_coverage_ratio())
        self.set_financial_ratios("Years to Repay Debt", self.years_to_repay_debt())
        self.set_financial_ratios("Average Interest Rate", self.average_interest_rate())

    def debt_ratio(self):
        total_debt = self.get_financial_statement_values_row("Total Debt")
        total_assets = self.get_financial_statement_values_row("Total Assets")

        return calculate_financial_ratio(total_debt, total_assets)

    def debt_to_equity_ratio(self):
        total_debt = self.get_financial_statement_values_row("Total Debt")
        shareholders_equity = self.get_financial_statement_values_row("Shareholders Equity")

        return calculate_financial_ratio(total_debt, shareholders_equity)

    def years_to_repay_debt(self):
        total_debt = self.get_financial_statement_values_row("Total Debt")
        net_income = self.get_financial_statement_values_row("Net Income")

        return calculate_financial_ratio(total_debt, net_income)

    def interest_coverage_ratio(self):
        interest_expense = self.get_financial_statement_values_row("Interest Expense")
        net_income = self.get_financial_statement_values_row("Net Income")

        return calculate_financial_ratio(interest_expense, net_income)

    def average_interest_rate(self):
        interest_expense = self.get_financial_statement_values_row("Interest Expense")
        total_debt = self.get_financial_statement_values_row("Total Debt")

        return calculate_financial_ratio(interest_expense, total_debt)


class FR_dividend_paying(FR_main):
    """
    List of Dividend Paying Ratios
    # Profitability
    - Dividend Yield
    # Liquidity
    - Dividend Coverage Ratio
    - Dividend Payout Ratio
    """
    def analyze_dividend(self):
        if (self.get_financial_statement_values_row("Gross Dividend Payout per Share")).any():
            logger.info(f"Dividend data found. Proceeding with analysis")
            self.set_financial_ratios("Dividend Yield", self.dividend_yield())
            self.set_financial_ratios("Dividend Coverage Ratio", self.dividend_coverage_ratio())
            self.set_financial_ratios("Dividend Payout Ratio", self.dividend_payout_ratio())
        else:
            logger.warning(f"No dividend data found")

    def dividend_yield(self):
        gross_dividend_payout = self.get_financial_statement_values_row("Gross Dividend Payout per Share")
        share_unit_price = self.get_financial_statement_values_row("Share Unit Price")

        return calculate_financial_ratio(gross_dividend_payout, share_unit_price)

    def dividend_coverage_ratio(self):
        gross_dividend_payout = self.get_financial_statement_values_row("Gross Dividend Payout per Share")
        outstanding_shares = self.get_financial_statement_values_row("Outstanding Shares")

        total_gross_dividend_payout = gross_dividend_payout * outstanding_shares

        net_income = self.get_financial_statement_values_row("Net Income")

        return calculate_financial_ratio(net_income, total_gross_dividend_payout)

    def dividend_payout_ratio(self):
        gross_dividend_payout = self.get_financial_statement_values_row("Gross Dividend Payout per Share")
        outstanding_shares = self.get_financial_statement_values_row("Outstanding Shares")

        total_gross_dividend_payout = gross_dividend_payout * outstanding_shares

        net_income = self.get_financial_statement_values_row("Net Income")

        return calculate_financial_ratio(total_gross_dividend_payout, net_income)
    

class FR_sales(FR_main):
    """
        List of Dividend Paying Ratios
        # Profitability
        - Gross Margin
        - Capital Productivity
        - COGS per Sale
        # Efficiency
        - Working Capital Productivity
        - Fixed Assets Productivity
        # Liquidity
        - Trade Debtor Productivity
        - Trade Debtor Days
        - Trade Creditor Productivity
        - Trade Creditor Days
        """
    def analyze_sales(self):
        if (self.get_financial_statement_values_row("Sales")).any():
            logger.info(f"Sales data found")
            self.set_financial_ratios("Gross Margin", self.gross_margin())
            self.set_financial_ratios("Capital Productivity", self.capital_productivity())
            self.set_financial_ratios("COGS per Sale", self.cogs_per_sale())

            self.set_financial_ratios("Working Capital Productivity", self.working_capital_productivity())
            self.set_financial_ratios("Fixed Assets Productivity", self.fixed_assets_productivity())

            self.set_financial_ratios("Trade Debtors Productivity", self.trade_debtor_productivity())
            self.set_financial_ratios("Trade Debtors Days", self.trade_debtor_days())
            self.set_financial_ratios("Trade Creditors Productivity", self.trade_creditor_productivity())
            self.set_financial_ratios("Trade Creditors Days", self.trade_creditor_days())
        else:
            logger.warning(f"Sales data not found")

    def gross_margin(self):
        revenue = self.get_financial_statement_values_row("Revenue")
        cost_of_goods_sold = self.get_financial_statement_values_row("Cost of Goods Sold")
        sales = self.get_financial_statement_values_row("Sales")

        net_revenue = revenue - cost_of_goods_sold

        return calculate_financial_ratio(net_revenue, sales)

    def capital_productivity(self):
        operating_profit = self.get_financial_statement_values_row("Operating Profit")
        sales = self.get_financial_statement_values_row("Sales")

        return calculate_financial_ratio(operating_profit, sales)

    def cogs_per_sale(self):
        cost_of_goods_sold = self.get_financial_statement_values_row("Cost of Goods Sold")
        sales = self.get_financial_statement_values_row("Sales")

        return calculate_financial_ratio(cost_of_goods_sold, sales)

    def working_capital_productivity(self):
        sales = self.get_financial_statement_values_row("Sales")
        current_assets = self.get_financial_statement_values_row("Current Assets")
        current_liabilities = self.get_financial_statement_values_row("Current Liabilities")

        working_capital = current_assets - current_liabilities

        return calculate_financial_ratio(sales, working_capital)

    def fixed_assets_productivity(self):
        sales = self.get_financial_statement_values_row("Sales")
        fixed_assets = self.get_financial_statement_values_row("Fixed Assets")

        return calculate_financial_ratio(sales, fixed_assets)

    def trade_debtor_productivity(self):
        sales = self.get_financial_statement_values_row("Sales")
        trade_debtors = self.get_financial_statement_values_row("Trade Debtors")

        return calculate_financial_ratio(sales, trade_debtors)

    def trade_debtor_days(self):
        trade_debtors = self.get_financial_statement_values_row("Trade Debtors")
        sales = self.get_financial_statement_values_row("Sales")

        return calculate_financial_ratio(trade_debtors, sales) * 365
        # return np.multiply(calculate_financial_ratio(trade_debtors, sales), 365)

    def trade_creditor_productivity(self):
        sales = self.get_financial_statement_values_row("Sales")
        trade_creditors = self.get_financial_statement_values_row("Trade Creditors")

        return calculate_financial_ratio(sales, trade_creditors)

    def trade_creditor_days(self):
        trade_creditors = self.get_financial_statement_values_row("Trade Creditors")
        sales = self.get_financial_statement_values_row("Sales")

        return calculate_financial_ratio(trade_creditors, sales) * 365
        # return np.multiply(calculate_financial_ratio(trade_creditors, sales), 365)


class FR_stock_inventory(FR_main):
    """
    List of Financial Ratios
    # Efficiency
    - Stock Days
    - Stock Turnover
    # Liquidity
    - Quick Ratio
    """
    def analyze_stock_inventory(self):
        if self.get_financial_statement_values_row("Stock Inventory").any():
            logger.info("Stock Inventory data found")
            self.set_financial_ratios("Stock Days", self.stock_days())

            self.set_financial_ratios("Quick Ratio", self.quick_ratio())

            if self.get_financial_statement_values_row("Sales").any():
                logger.info("Sales data found")
                self.set_financial_ratios("Stock Turnover", self.stock_turnover())
            else:
                logger.warning("Sales data not found")
        else:
            logger.warning("Stock Inventory data not found")

    def stock_days(self):
        stock_inventory = self.get_financial_statement_values_row("Stock Inventory")
        cost_of_goods_sold = self.get_financial_statement_values_row("Cost of Goods Sold")

        return calculate_financial_ratio(stock_inventory, cost_of_goods_sold) * 365
        # return np.multiply(calculate_financial_ratio(stock_inventory, cost_of_goods_sold), 365)

    def stock_turnover(self):
        sales = self.get_financial_statement_values_row("Sales")
        stock_inventory = self.get_financial_statement_values_row("Stock Inventory")

        return calculate_financial_ratio(sales, stock_inventory)

    def quick_ratio(self):
        current_assets = self.get_financial_statement_values_row("Current Assets")
        stock_inventory = self.get_financial_statement_values_row("Stock Inventory")
        current_liabilities = self.get_financial_statement_values_row("Current Liabilities")

        quick_numerator = current_assets - stock_inventory

        return calculate_financial_ratio(quick_numerator, current_liabilities)


class FR_default(FR_valuation_general, FR_profitability_general, FR_efficiency_general, FR_liquidity_general,
                 FR_solvency_general, FR_dividend_paying, FR_sales, FR_stock_inventory, FR_main):

    def default_analysis(self):
        self.analyze_valuation_gen()
        self.analyze_profitability_gen()
        self.analyze_efficiency_gen()
        self.analyze_liquidity_gen()
        self.analyze_solvency_gen()

        self.analyze_dividend()
        self.analyze_sales()
        self.analyze_stock_inventory()
