from . import financialRatios

class efficiency_gen(financialRatios.financialData_main):
    
    """
    List of Financial Ratios
    
    # Efficiency
    - EBITDA to Cash Conversion
    - Revenue to Expense Ratio
    """
    
    def analyzeEfficiency(self): # Equivalent to Run All
        print("Analyze Efficiency")
        
        self.setFinancialRatios_row("EBITDA to Cash Conversion Ratio", self.ebitdaToCashConversion())
        self.setFinancialRatios_row("Revenue to Expense Ratio", self.revenueToExpenseRatio())
        
    # Financial Ratio
    
    ## EBITDA to Cash Conversion
    def ebitdaToCashConversion(self):
        netCashOps = self.getFinancialData_row("Net Cash Flow from Operations")
        
        netIncome = self.getFinancialData_row("Net Income")
        depreciation = self.getFinancialData_row("Depreciation")
        amortization = self.getFinancialData_row("Amortization")
        interest = self.getFinancialData_row("Interest Expense")
        tax = self.getFinancialData_row("Tax")
        
        EBITDA = netIncome + interest + tax + depreciation + amortization

        return self.calculateFinancialRatios_row(netCashOps, EBITDA)
    
    ## Revenue to Expense Ratio
    def revenueToExpenseRatio(self):
        revenue = self.getFinancialData_row("Revenue")
        
        totalExpenses = self.getFinancialData_row("Total Expenses")
        
        return self.calculateFinancialRatios_row(revenue, totalExpenses)