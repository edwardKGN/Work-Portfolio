from . import financialRatios

class solvency_gen(financialRatios.financialData_main):
    
    """
    List of Financial Ratios
    
    # Solvency
    - Debt Ratio
    - Debt to Equity Ratio
    - Interest Coverage Ratio
    - Years to Repay Debt
    - Average Interest Rate
    """
    
    def analyzeSolvency(self):
        print("Analyzing Solvency")
        
        self.setFinancialRatios_row("Debt Ratio", self.debtRatio())
        self.setFinancialRatios_row("Debt to Equity Ratio", self.debtToEquityRatio())
        self.setFinancialRatios_row("Interest Coverage Ratio", self.interestCoverageRatio())
        self.setFinancialRatios_row("Years to Repay Debt", self.yearsToRepayDebt())
        self.setFinancialRatios_row("Average Interest Rate", self.averageInterestRate())

    # Financial Ratio
    ## Debt Ratio
    def debtRatio(self):
        totDebt = self.getFinancialData_row("Total Debt")
        
        totAssets = self.getFinancialData_row("Total Assets")
        
        return self.calculateFinancialRatios_row(totDebt, totAssets)
    
    ## Debt to Equity Ratio
    def debtToEquityRatio(self):
        totDebt = self.getFinancialData_row("Total Debt")
        
        totEquity = self.getFinancialData_row("Total Assets") - self.getFinancialData_row("Total Liabilities")
           
        return self.calculateFinancialRatios_row(totDebt, totEquity)
    
    ## Interest Coverage Ratio
    def interestCoverageRatio(self):
        netIncome = self.getFinancialData_row("Net Income")
        depreciation = self.getFinancialData_row("Depreciation")
        amortization = self.getFinancialData_row("Amortization")
        interest = self.getFinancialData_row("Interest Expense")
        tax = self.getFinancialData_row("Tax")
        
        EBITDA = netIncome + interest + tax + depreciation + amortization
        
        interest = self.getFinancialData_row("Interest Expense")
        
        return self.calculateFinancialRatios_row(EBITDA, interest)
    
    # Years to Repay Debt
    def yearsToRepayDebt(self):
        totDebt = self.getFinancialData_row("Total Debt")
        
        netIncome = self.getFinancialData_row("Net Income")
        depreciation = self.getFinancialData_row("Depreciation")
        amortization = self.getFinancialData_row("Amortization")
        interest = self.getFinancialData_row("Interest Expense")
        tax = self.getFinancialData_row("Tax")
        
        EBITDA = netIncome + interest + tax + depreciation + amortization
        
        return self.calculateFinancialRatios_row(totDebt, EBITDA)
        
    ## Average Interest Rate
    def averageInterestRate(self):
        totDebt = self.getFinancialData_row("Total Debt")
        
        interest = self.getFinancialData_row("Interest Expense")
        
        return self.calculateFinancialRatios_row(interest, totDebt)