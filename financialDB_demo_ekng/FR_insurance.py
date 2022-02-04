"""
Author: Edward KGN
Last Update: 29/01/2022

Sub-subclass of FR_main, specialized for insurance industry

Dependent on FR_main
"""

from FR_main import *


class FR_insurance(FR_valuation_general, FR_profitability_general, FR_efficiency_general, FR_liquidity_general,
                   FR_solvency_general, FR_dividend_paying, FR_main):
    """
    List of Unique Financial Ratios
    # Profitability
    - Investment Return
    - Net Investment Income Ratio
    # Efficiency
    - Loss Ratio
    - Underwriting Expense Ratio
    """

    def analyze_insurance(self):
        self.analyze_valuation_gen()
        self.analyze_profitability_gen()
        self.analyze_efficiency_gen()
        self.analyze_liquidity_gen()
        self.analyze_solvency_gen()

        self.analyze_dividend()

        self.set_financial_ratios("Investment Return", self.investment_return())
        self.set_financial_ratios("Net Investment Income Ratio", self.net_investment_income_ratio())
        self.set_financial_ratios("Loss Ratio", self.loss_ratio())
        self.set_financial_ratios("Underwriting Expense Ratio", self.underwriting_expense_ratio())

    def investment_return(self):
        investment_income = self.get_financial_statement_values_row("Investment Income")
        investment_expense = self.get_financial_statement_values_row("Investment Expense")

        net_investment_income = investment_income - investment_expense

        gains_on_investment_assets = self.get_financial_statement_values_row("Gains on Investment Assets")
        losses_on_investment_assets = self.get_financial_statement_values_row("Losses on Investment Assets")

        net_investment_gains = gains_on_investment_assets - losses_on_investment_assets

        net_investment_profits = net_investment_income - net_investment_gains

        investment_assets = self.get_financial_statement_values_row("Investment Assets")

        return calculate_financial_ratio(net_investment_profits, investment_assets)

    def net_investment_income_ratio(self):
        investment_income = self.get_financial_statement_values_row("Investment Income")
        investment_expense = self.get_financial_statement_values_row("Investment Expense")

        net_investment_income = investment_income - investment_expense

        net_premiums_earned = self.get_financial_statement_values_row("Net Premiums Earned")

        return calculate_financial_ratio(net_investment_income, net_premiums_earned)

    def loss_ratio(self):
        net_claims = self.get_financial_statement_values_row("Net Claims")
        net_premiums_earned = self.get_financial_statement_values_row("Net Premiums Earned")

        return calculate_financial_ratio(net_claims, net_premiums_earned)

    def underwriting_expense_ratio(self):
        commission_expense = self.get_financial_statement_values_row("Commission Expense")
        interest_expense = self.get_financial_statement_values_row("Interest Expense")
        investment_expense = self.get_financial_statement_values_row("Investment Expense")
        management_expense = self.get_financial_statement_values_row("Management Expense")

        total_expense = commission_expense + interest_expense + investment_expense + management_expense

        net_premiums_earned = self.get_financial_statement_values_row("Net Premiums Earned")

        return calculate_financial_ratio(total_expense, net_premiums_earned)
