from . import FR_Valuation
from . import FR_Profitability
from . import FR_Efficiency
from . import FR_Liquidity
from . import FR_Solvency

from . import FR_sub_dividendPaying
from . import FR_sub_haveSales
from . import FR_sub_inventoryHolding

from . import financialRatios

class financialData_insurance(FR_Valuation.valuation_gen, FR_Profitability.profitability_gen, FR_Efficiency.efficiency_gen, FR_Liquidity.liquidity_gen, FR_Solvency.solvency_gen, FR_sub_dividendPaying.dividendPaying, FR_sub_haveSales.haveSales, FR_sub_inventoryHolding.inventoryHolding, financialRatios.financialData_main):
    
    """
    # Financial Ratios Implemented
        
    # General
    ## Valuation
    - Price to Book
    - Price to Earnings
        
    ## Profitability
    - Return on Equity
    - Return on Capital Employed
    - Gross Margin
    - EBITDA to Revenue Ratio
        
    ## Efficiency / Activity
    - EBITDA to Cash Conversion
    
    - Revenue to Expense Ratio
    - Capital Productivity

    - COGS per Sale

    - Working Capital Productivity

    - Trade Debtor Productivity
    - Trade Debtor Days

    - Trade Creditor Productivity
    - Trade Creditor Days

    - Fixed Assets Productivity
        
    ## Liquidity
    - Current Ratio
    - Cash Ratio
    - Operating Cash Flow Ratio
    - Cash Conversion Ratio
        
    ## Leverage / Solvency / Gearing
    - Debt Ratio
    - Debt to Equity Ratio
        
    - Interest Coverage Ratio
        
    - Years to Repay Debt
        
    - Average Interest Rate
        
    # Dividend 
        
    ## Profitability
    - Dividend Yield
        
    ## Liquidity
    - Dividend Coverage
    - Dividend Payout Ratio
    
    # Insurance
    
    ## Profitability
    - Investment Return
    - Net Investment Income Ratio
    
    ## Efficiency / Activity
    - Loss Ratio
    - Underwriting Expense Ratio
    """
    
    def analyze_insurance(self):
        print("Calculating Insurance's Financial Ratios")
        
        self.analyzeValuation()
        self.analyzeProfitability()
        self.analyzeEfficiency()
        self.analyzeLiquidity()
        self.analyzeSolvency()
        
        self.analyzeDividend()
        self.analyzeSales()
        self.analyzeInventory()
        
        self.setFinancialRatios_row("Investment Return", self.investmentReturn())
        self.setFinancialRatios_row("Net Investment Income Ratio", self.netInvestmentIncomeRatio())
        
        self.setFinancialRatios_row("Loss Ratio", self.lossRatio())
        self.setFinancialRatios_row("Underwriting Expense Ratio", self.underwritingExpenseRatio())
   
    def investmentReturn(self):
        investmentIncome = self.getFinancialData_row("Investment Income")
        investmentExpense = self.getFinancialData_row("Investment Expense")
        
        netInvestmentIncome = investmentIncome - investmentExpense
        
        gainInvestmentAssets = self.getFinancialData_row("Gains on Investment Assets")
        lossInvestmentAssets = self.getFinancialData_row("Losses on Investment Assets")
        
        netGainsInvestmentAssets = gainInvestmentAssets - lossInvestmentAssets
        
        investmentAssets = self.getFinancialData_row("Investment Assets")
        
        return self.calculateFinancialRatios_row((netInvestmentIncome + netGainsInvestmentAssets), investmentAssets)
    
    def netInvestmentIncomeRatio(self):
        investmentIncome = self.getFinancialData_row("Investment Income")
        investmentExpense = self.getFinancialData_row("Investment Expense")
        
        netInvestmentIncome = investmentIncome - investmentExpense
        
        netPremiumsEarned = self.getFinancialData_row("Net Premiums Earned")
        
        return self.calculateFinancialRatios_row(netInvestmentIncome, netPremiumsEarned)
    
    ## Efficiency / Activity
    
    def lossRatio(self):
        netClaims = self.getFinancialData_row("Net Claims")
        netPremiumsEarned = self.getFinancialData_row("Net Premiums Earned")
        
        return self.calculateFinancialRatios_row(netClaims, netPremiumsEarned)
    
    def underwritingExpenseRatio(self):
        commExp = self.getFinancialData_row("Commission Expense")
        interestExp = self.getFinancialData_row("Interest Expense")
        investmentExp = self.getFinancialData_row("Investment Expenses")
        mgmtExp = self.getFinancialData_row("Management Expense")
        
        underWritingExp = commExp + interestExp + investmentExp + mgmtExp
        
        netPremiumsEarned = self.getFinancialData_row("Net Premiums Earned")
        
        return self.calculateFinancialRatios_row(underWritingExp, netPremiumsEarned)         