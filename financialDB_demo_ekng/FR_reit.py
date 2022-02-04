"""
Author: Edward KGN
Last Update: 29/01/2022

Sub-subclass of FR_main, specialized for REIT industry

Confidence in this analysis is relatively weak due to missing information and inconsistency of reporting in each REIT

Dependent on FR_main
"""
from FR_main import *


class FR_reit(FR_valuation_general, FR_profitability_general, FR_efficiency_general, FR_liquidity_general,
              FR_solvency_general, FR_dividend_paying, FR_sales, FR_stock_inventory, FR_main):
    """
    List of Unique Financial Ratios
    # Derived
    - Funds from Operations
    - Adjusted from Operations
    # Valuation
    - Net Asset Value
    - Price to FFO
    - Price to AFFO
    # Profitability
    - AFFO Yield
    - Capitalization Rate
    # Efficiency
    - Management Expense to Profit Ratio
    """

    def analyze_reit(self):
        self.analyze_efficiency_gen()
        self.analyze_liquidity_gen()
        self.analyze_solvency_gen()

        self.analyze_dividend()

        self.analyze_sales()
        self.analyze_stock_inventory()

        self.set_financial_ratios("Funds from Operation", self.FFO())
        self.set_financial_ratios("Adjusted Funds from Operations", self.AFFO())

        self.set_financial_ratios("Net Asset Value", self.net_asset_value())
        self.set_financial_ratios("Price to FFO", self.price_to_ffo())
        self.set_financial_ratios("Price to AFFO", self.price_to_ffo())

        self.set_financial_ratios("AFFO Yield", self.affo_yield())
        self.set_financial_ratios("Capitalization Rate", self.capitalization_rate())

        self.set_financial_ratios("Management Expense to Profit Ratio", self.management_expense_to_profit_ratio())

    def FFO(self):
        net_income = self.get_financial_statement_values_row("Net Income")
        depreciation = self.get_financial_statement_values_row("Depreciation")
        amortization = self.get_financial_statement_values_row("Amortization")
        losses_on_property_sales = self.get_financial_statement_values_row("Losses on Property Sales")
        gains_on_property_sales = self.get_financial_statement_values_row("Gains on Property Sales")
        interest_income = self.get_financial_statement_values_row("Interest Income")
        other_income = self.get_financial_statement_values_row("Other Income")

        return net_income + depreciation + amortization + losses_on_property_sales - (gains_on_property_sales
                                                                                      + interest_income + other_income)

    def AFFO(self):
        ffo = self.FFO()
        capital_expenditure = self.get_financial_statement_values_row("Capital Expenditure")
        rent_increases = self.get_financial_statement_values_row("Rent Increases")
        property_operating_expenses = self.get_financial_statement_values_row("Property Operating Expenses")

        return ffo + rent_increases - capital_expenditure - property_operating_expenses

    def net_asset_value(self):
        total_assets = self.get_financial_statement_values_row("Total Assets")
        total_liabilities = self.get_financial_statement_values_row("Total Liabilities")
        outstanding_shares = self.get_financial_statement_values_row("Outstanding Shares")

        net_assets = (total_assets - total_liabilities) * 1000  # Convert to Currency

        return calculate_financial_ratio(net_assets, outstanding_shares)

    def price_to_ffo(self):
        share_unit_price = self.get_financial_statement_values_row("Share Unit Price")
        outstanding_shares = self.get_financial_statement_values_row("Outstanding Shares")

        market_capitalization = share_unit_price * outstanding_shares / 1000

        return calculate_financial_ratio(market_capitalization, self.FFO())

    def price_to_affo(self):
        share_unit_price = self.get_financial_statement_values_row("Share Unit Price")
        outstanding_shares = self.get_financial_statement_values_row("Outstanding Shares")

        market_capitalization = share_unit_price * outstanding_shares / 1000

        return calculate_financial_ratio(market_capitalization, self.AFFO())

    def affo_yield(self):
        share_unit_price = self.get_financial_statement_values_row("Share Unit Price")
        outstanding_shares = self.get_financial_statement_values_row("Outstanding Shares")

        market_capitalization = share_unit_price * outstanding_shares / 1000

        return calculate_financial_ratio(self.AFFO(), market_capitalization)

    def capitalization_rate(self):
        share_unit_price = self.get_financial_statement_values_row("Share Unit Price")
        outstanding_shares = self.get_financial_statement_values_row("Outstanding Shares")

        market_capitalization = share_unit_price * outstanding_shares / 1000

        net_operating_income = self.get_financial_statement_values_row("Net Operating Income")

        return calculate_financial_ratio(net_operating_income, market_capitalization)

    def management_expense_to_profit_ratio(self):
        net_income = self.get_financial_statement_values_row("Net Income")
        management_expense = self.get_financial_statement_values_row("Management Expense")

        return calculate_financial_ratio(management_expense, net_income)
