from . import financialRatios

class profitability_gen(financialRatios.financialData_main):
    
    """
    List of Financial Ratios
    
    # Profitability
    - Return on Equity
    - Return on Capital Employed
    - EBITDA to Revenue Ratio
    """
    
    def analyzeProfitability(self): # Equivalent to Run All
        print("Analyzing Profitability")
        
        self.setFinancialRatios_row("Return on Equity", self.ROE())
        self.setFinancialRatios_row("Return on Capital Employed", self.ROCE())
        self.setFinancialRatios_row("EBITDA to Revenue Ratio", self.ebitdaToRevenueRatio())
        
    # Financial Ratios
    ## Return on Equity # TAG for future search
    def ROE(self):         
        netIncome = self.getFinancialData_row("Net Income")
        shareholderEquity = self.getFinancialData_row("Shareholders Equity")

        return self.calculateFinancialRatios_row(netIncome, shareholderEquity)
    
    ## Return on Capital Employed
    def ROCE(self):
        operatingProfit = self.getFinancialData_row("Operating Profit")
        capitalEmployed = self.getFinancialData_row("Total Assets") - self.getFinancialData_row("Current Liabilities")

        return self.calculateFinancialRatios_row(operatingProfit, capitalEmployed)
    
    ## EBITDA to Revenue Ratio  
    def ebitdaToRevenueRatio(self):        
        netIncome = self.getFinancialData_row("Net Income")
        depreciation = self.getFinancialData_row("Depreciation")
        amortization = self.getFinancialData_row("Amortization")
        interest = self.getFinancialData_row("Interest Expense")
        tax = self.getFinancialData_row("Tax")
        
        EBITDA = netIncome + interest + tax + depreciation + amortization
        
        revenue = self.getFinancialData_row("Revenue")
        
        return self.calculateFinancialRatios_row(EBITDA, revenue)