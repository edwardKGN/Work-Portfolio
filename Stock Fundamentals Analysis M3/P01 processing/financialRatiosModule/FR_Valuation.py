from . import financialRatios

class valuation_gen(financialRatios.financialData_main):
                
    """
    List of Financial Ratios
    
    # Valuation
    - Price to Book
    - Price to Earnings
    """
    
    def analyzeValuation(self): # Equivalent to Run All  
        print("Analyzing Valuation")
        
        self.setFinancialRatios_row("Price to Book Ratio", self.priceToBook())
        self.setFinancialRatios_row("Price to Earnings Ratio", self.priceToEarnings())
    
    # Financial Ratios
    ## Price to Book
    def priceToBook(self):        
        marketCap = (self.getFinancialData_row("Unit Price (Currency)") 
                     * self.getFinancialData_row("Outstanding Shares") ) / 1000
        
        bookVal = self.getFinancialData_row("Total Assets") - (self.getFinancialData_row("Total Liabilities")
                                                               + self.getFinancialData_row("Intangible Assets"))
        
        return self.calculateFinancialRatios_row(marketCap, bookVal)

    
    ## Price to Earnings
    def priceToEarnings(self):
        marketCap = (self.getFinancialData_row("Unit Price (Currency)") 
                     * self.getFinancialData_row("Outstanding Shares") ) / 1000
        
        netIncome = self.getFinancialData_row("Net Income")
        
        return self.calculateFinancialRatios_row(marketCap, netIncome)