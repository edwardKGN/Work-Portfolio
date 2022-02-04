"""
Author: Edward KGN
Last Update: 29/01/2022

Sub-subclass of FR_main, specialized for banking industry

Dependent on FR_main
"""

from FR_main import *


class FR_banking(FR_valuation_general, FR_profitability_general, FR_efficiency_general, FR_liquidity_general,
                 FR_solvency_general, FR_dividend_paying, FR_main):
    """
    List of Unique Financial Ratios
    # Profitability
    - Net Interest Margin
    - Net Non-Interest Margin
    - CASA Ratio
    - Net Bank Operating Margin
    - Net Profit Margin
    - Asset Utilization
    # Efficiency
    - Efficiency Ratio
    - Operating Efficiency Ratio
    # Liquidity
    - Credit to Deposit
    # Solvency
    - Leverage Ratio
    - CET1 Ratio
    - Loan to Assets
    - Capital Adequacy
    - Bad Loan Ratio
    - Loan Loss Provision Coverage Ratio
    """

    def analyze_banking(self):
        self.analyze_valuation_gen()
        self.analyze_profitability_gen()
        self.analyze_efficiency_gen()
        self.analyze_liquidity_gen()
        # self.analyze_solvency_gen()  # Excluded as banking is the creditor of loans. Hence, not applicable

        self.analyze_dividend()

        self.set_financial_ratios("Net Interest Margin", self.net_interest_margin())
        self.set_financial_ratios("Net Non-Interest Margin", self.net_non_interest_margin())
        self.set_financial_ratios("CASA Ratio", self.casa_ratio())
        self.set_financial_ratios("Net Bank Operating Margin", self.net_bank_operating_margin())
        self.set_financial_ratios("Net Profit Margin", self.net_profit_margin())
        self.set_financial_ratios("Asset Utilization", self.asset_utilization())

        self.set_financial_ratios("Efficiency Ratio", self.efficiency_ratio())

        self.set_financial_ratios("Leverage Ratio", self.leverage_ratio())
        self.set_financial_ratios("CET-1 Ratio", self.cet1_ratio())
        self.set_financial_ratios("Loan to Assets Ratio", self.loan_to_assets())
        self.set_financial_ratios("Capital Adequacy Ratio", self.capital_adequacy())
        self.set_financial_ratios("Bad Loan Ratio", self.bad_loan_ratio())
        self.set_financial_ratios("Loan Loss Provision Coverage Ratio", self.loan_loss_provision_coverage_ratio())

    def net_interest_margin(self):
        interest_income = self.get_financial_statement_values_row("Interest Income")
        interest_expense = self.get_financial_statement_values_row("Interest Expense")
        total_assets = self.get_financial_statement_values_row("Total Assets")
        intangible_assets = self.get_financial_statement_values_row("Intangible Assets")

        net_interest_income = interest_income - interest_expense
        total_tangible_assets = total_assets - intangible_assets

        return calculate_financial_ratio(net_interest_income, total_tangible_assets)

    def net_non_interest_margin(self):
        non_interest_income = self.get_financial_statement_values_row("Non-Interest Income")
        non_interest_expense = self.get_financial_statement_values_row("Non-Interest Expense")
        total_assets = self.get_financial_statement_values_row("Total Assets")
        intangible_assets = self.get_financial_statement_values_row("Intangible Assets")

        net_non_interest_income = non_interest_income - non_interest_expense
        total_tangible_assets = total_assets - intangible_assets

        return calculate_financial_ratio(net_non_interest_income, total_tangible_assets)

    def casa_ratio(self):
        current_accounts_deposit = self.get_financial_statement_values_row("Current Accounts Deposit")
        savings_accounts_deposit = self.get_financial_statement_values_row("Savings Accounts Deposit")

        return calculate_financial_ratio(current_accounts_deposit, savings_accounts_deposit)

    def net_bank_operating_margin(self):
        operating_revenue = self.get_financial_statement_values_row("Operating Revenue")
        operating_expense = self.get_financial_statement_values_row("Operating Expense")
        total_assets = self.get_financial_statement_values_row("Total Assets")
        intangible_assets = self.get_financial_statement_values_row("Intangible Assets")

        net_operating_revenue = operating_revenue - operating_expense
        total_tangible_assets = total_assets - intangible_assets

        return calculate_financial_ratio(net_operating_revenue, total_tangible_assets)

    def net_profit_margin(self):
        net_income = self.get_financial_statement_values_row("Net Income")
        operating_revenue = self.get_financial_statement_values_row("Operating Revenue")

        return calculate_financial_ratio(net_income, operating_revenue)

    def asset_utilization(self):
        operating_revenue = self.get_financial_statement_values_row("Operating Revenue")
        total_assets = self.get_financial_statement_values_row("Total Assets")
        intangible_assets = self.get_financial_statement_values_row("Intangible Assets")

        total_tangible_assets = total_assets - intangible_assets

        return calculate_financial_ratio(operating_revenue, total_tangible_assets)

    def efficiency_ratio(self):
        non_interest_expense = self.get_financial_statement_values_row("Non-Interest Expense")
        revenue = self.get_financial_statement_values_row("Revenue")

        return calculate_financial_ratio(non_interest_expense, revenue)

    def leverage_ratio(self):
        t1_capital = self.get_financial_statement_values_row("Tier 1 Capital")

        total_assets = self.get_financial_statement_values_row("Total Assets")
        intangible_assets = self.get_financial_statement_values_row("Intangible Assets")

        total_tangible_assets = total_assets - intangible_assets

        return calculate_financial_ratio(t1_capital, total_tangible_assets)

    def cet1_ratio(self):
        cet1_capital = self.get_financial_statement_values_row("Common Equity Tier 1 Capital")
        risk_weighted_assets = self.get_financial_statement_values_row("Risk Weighted Assets")

        return calculate_financial_ratio(cet1_capital, risk_weighted_assets)

    def loan_to_assets(self):
        gross_loans_and_acceptance = self.get_financial_statement_values_row("Gross Loans and Acceptance")

        total_assets = self.get_financial_statement_values_row("Total Assets")
        intangible_assets = self.get_financial_statement_values_row("Intangible Assets")

        total_tangible_assets = total_assets - intangible_assets

        return calculate_financial_ratio(gross_loans_and_acceptance, total_tangible_assets)

    def capital_adequacy(self):
        t1_capital = self.get_financial_statement_values_row("Tier 1 Capital")
        t2_capital = self.get_financial_statement_values_row("Tier 2 Capital")

        total_capital = t1_capital + t2_capital

        risk_weighted_assets = self.get_financial_statement_values_row("Risk Weighted Assets")

        return calculate_financial_ratio(total_capital, risk_weighted_assets)

    def bad_loan_ratio(self):
        total_npa = self.get_financial_statement_values_row("Total Non-Performing Assets")
        gross_loans_and_acceptance = self.get_financial_statement_values_row("Gross Loans and Acceptance")

        return calculate_financial_ratio(total_npa, gross_loans_and_acceptance)

    def loan_loss_provision_coverage_ratio(self):
        total_npa = self.get_financial_statement_values_row("Total Non-Performing Assets")
        provision_for_credit_loss = self.get_financial_statement_values_row("Provision for Credit Loss")

        return calculate_financial_ratio(total_npa, provision_for_credit_loss)
