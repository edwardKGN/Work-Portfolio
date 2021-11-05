from . import FR_Valuation
from . import FR_Profitability
from . import FR_Efficiency
from . import FR_Liquidity
from . import FR_Solvency

from . import FR_sub_dividendPaying
from . import FR_sub_haveSales
from . import FR_sub_inventoryHolding

from . import financialRatios

class financialData_finance(FR_Valuation.valuation_gen, FR_Profitability.profitability_gen, FR_Efficiency.efficiency_gen, FR_Liquidity.liquidity_gen, FR_Solvency.solvency_gen, FR_sub_dividendPaying.dividendPaying, FR_sub_haveSales.haveSales, FR_sub_inventoryHolding.inventoryHolding, financialRatios.financialData_main):
    
    """
    # Financial Ratios Implemented
        
    # General
        
    ## Valuation
    - Price to Book
    - Price to Earnings
        
    ## Profitability
    - Return on Equity
    - Return on Capital Employed
    - EBITDA to Revenue
        
    ## Efficiency / Activity
    - EBITDA to Cash Conversion
    - Revenue to Expense Ratio
            
    ## Liquidity
    - Current Ratio
    - Cash Ratio
    - Operating Cash Flow Ratio
    - Cash Conversion Ratio

    # Dividend 
        
    ## Profitability
    - Dividend Yield
        
    ## Liquidity
    - Dividend Coverage
    - Dividend Payout Ratio
    
    # Unique
        
    ## Profitability
    - Net Interest Margin
    - Net Non-Interest Margin
    - Return on Assets
    - CASA Ratio
    - Net Bank Operating Margin
    - Net Profit Margin
    - Asset Utilization
        
    ## Efficiency / Activity
    - Efficiency Ratio
    - Operating Efficiency Ratio
        
    ## Liquidity
    - Credit to Deposit
        
    ## Leverage / Solvency / Gearing
    - Leverage Ratio
    - CET1 Ratio
    - Loans to Assets
    - Capital Adequacy
    - Bad Loan Ratio
    - Loan Loss Provision Coverage Ratio
    """
    
    def analyze_finance(self):
        print("Calculating Finance's Financial Ratios")
        
        self.analyzeValuation()
        self.analyzeProfitability()
        self.analyzeEfficiency()
        self.analyzeLiquidity()
        # self.analyzeSolvency() # Banking and Finance have unique Loan situation
        
        self.analyzeDividend()
        self.analyzeSales()
        self.analyzeInventory()
        
        self.setFinancialRatios_row("Net Interest Margin", self.netInterestMargin())
        self.setFinancialRatios_row("Net Non-Interest Margin", self.netNonInterestMargin())
        self.setFinancialRatios_row("Return on Assets", self.ROA())
        self.setFinancialRatios_row("CASA Ratio", self.casaRatio())
        self.setFinancialRatios_row("Net Bank Operating Margin", self.netBankOperatingMargin())
        self.setFinancialRatios_row("Net Profit Margin", self.netProfitMargin())
        self.setFinancialRatios_row("Asset Utilization Ratio", self.assetUtilization())
        
        self.setFinancialRatios_row("Efficiency Ratio", self.efficiencyRatio())
        self.setFinancialRatios_row("Operating Efficiency Ratio", self.operatingEfficiencyRatio())
        
        self.setFinancialRatios_row("Credit to Deposit Ratio", self.creditToDeposit())
        
        self.setFinancialRatios_row("Leverage Ratio", self.leverageRatio())
        self.setFinancialRatios_row("CET-1 Ratio", self.CET1Ratio())
        self.setFinancialRatios_row("Loans to Assets Ratio", self.loansToAssets())
        self.setFinancialRatios_row("Capital Adequacy Ratio", self.capitalAdequacy())
        self.setFinancialRatios_row("Bad Loan Ratio", self.badLoanRatio())
        self.setFinancialRatios_row("Loan Loss Provision Coverage Ratio", self.loanLossProvisionCoverageRatio())
        
    # Unique Financial Ratios
    
     # Profitability
    
    def netInterestMargin(self):
        intInc = self.getFinancialData_row("Interest Income")
        intExp = self.getFinancialData_row("Interest Expense")
        
        totAssets = self.getFinancialData_row("Total Assets")
        intAssets = self.getFinancialData_row("Intangible Assets")
        
        tangibleAssets = totAssets - intAssets
        
        return self.calculateFinancialRatios_row((intInc - intExp), tangibleAssets)
    
    def netNonInterestMargin(self):
        nonIntInc = self.getFinancialData_row("Non-Interest Income")
        nonIntExp = self.getFinancialData_row("Non-Interest Expense")
        totAssets = self.getFinancialData_row("Total Assets")
        intAssets = self.getFinancialData_row("Intangible Assets")
        
        tangibleAssets = totAssets - intAssets
        
        return self.calculateFinancialRatios_row((nonIntInc - nonIntExp), tangibleAssets)
    
    def ROA(self):
        netIncome = self.getFinancialData_row("Net Income")
        
        totAssets = self.getFinancialData_row("Total Assets")
        intAssets = self.getFinancialData_row("Intangible Assets")
        
        tangibleAssets = totAssets - intAssets

        return self.calculateFinancialRatios_row(netIncome, tangibleAssets)
    
    def casaRatio(self):
        currentAccounts = self.getFinancialData_row("Current Accounts Deposit")
        savingsAccounts = self.getFinancialData_row("Savings Accounts Deposit")
        
        return self.calculateFinancialRatios_row(currentAccounts, savingsAccounts)
    
    def netBankOperatingMargin(self):
        opRevenue = self.getFinancialData_row("Operating Revenue")
        opExpense = self.getFinancialData_row("Operating Expense")
        
        totAssets = self.getFinancialData_row("Total Assets")
        intAssets = self.getFinancialData_row("Intangible Assets")
        
        tangibleAssets = totAssets - intAssets
        
        return self.calculateFinancialRatios_row((opRevenue - opExpense), tangibleAssets)
    
    def netProfitMargin(self):
        netIncome = self.getFinancialData_row("Net Income")
        opRevenue = self.getFinancialData_row("Operating Revenue")
        
        return self.calculateFinancialRatios_row(netIncome, opRevenue)
    
    def assetUtilization(self):
        opRevenue = self.getFinancialData_row("Operating Revenue")
        
        totAssets = self.getFinancialData_row("Total Assets")
        intAssets = self.getFinancialData_row("Intangible Assets")
        
        tangibleAssets = totAssets - intAssets
        
        return self.calculateFinancialRatios_row(opRevenue, tangibleAssets)
        
    # Efficiency / Activity
    
    def efficiencyRatio(self):
        nonIntExp = self.getFinancialData_row("Non-Interest Expense")
        revenue = self.getFinancialData_row("Revenue")
        
        return self.calculateFinancialRatios_row(nonIntExp, revenue) 
    
    def operatingEfficiencyRatio(self):
        opExpense = self.getFinancialData_row("Operating Expense")
        opRevenue = self.getFinancialData_row("Operating Revenue")
        
        return self.calculateFinancialRatios_row(opExpense, opRevenue)
    
    # Liquidity
    
    def creditToDeposit(self):
        netLoanAndAcceptance = self.getFinancialData_row("Gross Loans and Acceptance")
        totalDeposits = self.getFinancialData_row("Total Deposits")
        
        return self.calculateFinancialRatios_row(netLoanAndAcceptance, totalDeposits)
        
    # Leverage / Gearing / Solvency
    
    def leverageRatio(self):
        tier1Cap = self.getFinancialData_row("Tier 1 Capital")
        totAssets = self.getFinancialData_row("Total Assets")
        intAssets = self.getFinancialData_row("Intangible Assets")
        
        tangibleAssets = totAssets - intAssets
        
        return self.calculateFinancialRatios_row(tier1Cap, tangibleAssets)
    
    def CET1Ratio(self):
        CET1Cap = self.getFinancialData_row("Common Equity Tier 1 Capital")
        RWA = self.getFinancialData_row("Risk Weighted Assets")
        
        return self.calculateFinancialRatios_row(CET1Cap, RWA)
    
    def loansToAssets(self):
        netLoansAndAcceptance = self.getFinancialData_row("Gross Loans and Acceptance")
        
        totAssets = self.getFinancialData_row("Total Assets")
        intAssets = self.getFinancialData_row("Intangible Assets")
        
        #print("Net Loans and Acceptance", netLoansAndAcceptance, " Total Assets: ", totAssets, " Intangible Assets: ", intAssets)
        
        tangibleAssets = totAssets - intAssets
        
        return self.calculateFinancialRatios_row(netLoansAndAcceptance, tangibleAssets)
    
    def capitalAdequacy(self):
        tier1Cap = self.getFinancialData_row("Tier 1 Capital")
        tier2Cap = self.getFinancialData_row("Tier 2 Capital")
        RWA = self.getFinancialData_row("Risk Weighted Assets")
        
        return self.calculateFinancialRatios_row((tier1Cap + tier2Cap), RWA)
    
    def badLoanRatio(self):
        totNPA = self.getFinancialData_row("Total NPA")
        netLoansAndAcceptance = self.getFinancialData_row("Gross Loans and Acceptance")
        
        return self.calculateFinancialRatios_row(totNPA, netLoansAndAcceptance)
    
    def loanLossProvisionCoverageRatio(self):
        totNPA = self.getFinancialData_row("Total NPA")
        creditLossProvision = self.getFinancialData_row("Provision for Credit Loss")
        
        return self.calculateFinancialRatios_row(creditLossProvision, totNPA)