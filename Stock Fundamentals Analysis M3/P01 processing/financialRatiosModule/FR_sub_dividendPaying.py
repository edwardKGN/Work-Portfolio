from . import financialRatios

class dividendPaying(financialRatios.financialData_main):
    
    """
    List of Financial Ratios
    
    # Profitability
    - Dividend Yield
    
    # Liquidity
    - Dividend Coverage
    - Dividend Payout Ratio
    """
    
    # Main Analyzer
    def analyzeDividend(self):
        print("Analyzing Dividend Financial Ratios")
        
        if (self.df_input.index == "Gross Dividend Payout (Currency per Unit)").any(): # Check if Stock data row is present.
            print("Dividend data found")
            
            self.setFinancialRatios_row("Dividend Yield", self.dividendYield())
            self.setFinancialRatios_row("Dividend Coverage Ratio", self.dividendCoverage())
            self.setFinancialRatios_row("Dividend Payout Ratio", self.dividendPayoutRatio())
            
        else:
            print("No dividend data available")
   
    # Unique
    
    ## Profitability
    
        ## Dividend Yield
    def dividendYield(self):
        grossDivPayout = self.getFinancialData_row("Gross Dividend Payout (Currency per Unit)")
        
        unitPrice = self.getFinancialData_row("Unit Price (Currency)")
        
        return self.calculateFinancialRatios_row(grossDivPayout, unitPrice)
    
    ## Liquidity
    
        ## Dividend Coverage
    def dividendCoverage(self):
        netIncome = self.getFinancialData_row("Net Income")
        
        grossDivPayout = self.getFinancialData_row("Gross Dividend Payout (Currency per Unit)")
        outstandingShares = self.getFinancialData_row("Outstanding Shares")
        
        totalDividendPayout = (grossDivPayout * outstandingShares)/1000 # Currency -> Currency '000 <Standard Unit>
        
        return self.calculateFinancialRatios_row(netIncome, totalDividendPayout)
    
        ## Dividend Payout Ratio
    def dividendPayoutRatio(self):  
        grossDivPayout = self.getFinancialData_row("Gross Dividend Payout (Currency per Unit)")
        outstandingShares = self.getFinancialData_row("Outstanding Shares")
        
        totalDividendPayout = (grossDivPayout * outstandingShares)/1000 # Currency -> Currency '000 <Standard Unit>
        
        netIncome = self.getFinancialData_row("Net Income")
        
        return self.calculateFinancialRatios_row(totalDividendPayout, netIncome) 