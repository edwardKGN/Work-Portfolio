from . import financialRatios

class liquidity_gen(financialRatios.financialData_main):
    
    """
    List of Financial Ratios
    
    # Liquidity
    - Current Ratio
    - Cash Ratio
    - Operating Cash Flow Ratio
    - Cash Conversion Ratio
    """
    
    def analyzeLiquidity(self): # Equivalent to Run All
        print("Analyzing Liquidity Ratios")
        
        self.setFinancialRatios_row("Current Ratio", self.currentRatio())
        self.setFinancialRatios_row("Cash Ratio", self.cashRatio())
        self.setFinancialRatios_row("Operating Cash Flow Ratio", self.operatingCashFlowRatio())
        self.setFinancialRatios_row("Cash Conversion Ratio", self.cashConversionRatio())
    
    # Financial Ratio
    ## Current Ratio
    def currentRatio(self):
        curAssets = self.getFinancialData_row("Current Assets")
        
        curLiabilities = self.getFinancialData_row("Current Liabilities")
        
        return self.calculateFinancialRatios_row(curAssets, curLiabilities)
    
    ## Cash Ratio
    def cashRatio(self):
        cashAndCashEq = self.getFinancialData_row("Cash and Cash Equivalent")
        
        curLiabilities = self.getFinancialData_row("Current Liabilities")
        
        return self.calculateFinancialRatios_row(cashAndCashEq, curLiabilities)
    
    ## Operating Cash Flow Ratio
    def operatingCashFlowRatio(self):
        netCashOps = self.getFinancialData_row("Net Cash Flow from Operations")
        
        curLiabilities = self.getFinancialData_row("Current Liabilities")
       
        return self.calculateFinancialRatios_row(netCashOps, curLiabilities)
    
    ## Cash Conversion Ratio
    def cashConversionRatio(self):
        netCashOps = self.getFinancialData_row("Net Cash Flow from Operations")
        
        netIncome = self.getFinancialData_row("Net Income")
        
        return self.calculateFinancialRatios_row(netCashOps, netIncome)