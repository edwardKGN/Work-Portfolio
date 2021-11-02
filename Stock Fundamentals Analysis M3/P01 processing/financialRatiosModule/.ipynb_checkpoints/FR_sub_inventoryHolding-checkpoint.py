from . import fundamentalsAnalysis

class inventoryHolding_general(fundamentalsAnalysis.financialData_sectorGeneral):
    
    # Main Analyzer
    def analyze_inventory(self):
        print("Analyze Inventory Holding")
        
        self.setOutput_row("Stock Days")
        self.setOutput_row("Stock Turnover")
        
        self.setOutput_row("Quick Ratio")
        
        self.setFinancialYears()
        
        for year in self.getFinancialYears(): # Return Financial Ratios as fractions
            self.setOutput_element("Stock Days", year, self.stockDays(year))
            self.setOutput_element("Stock Turnover", year, self.stockTurnover(year))
            
            self.setOutput_element("Quick Ratio", year, self.quickRatio(year))
        
        
    """
    List of Financial Ratios
    - Stock Days
    - Stock Turnover
    
    - Quick Ratio
    """
    
    # Unique
    
    ## Efficicency
    
    ## Stock Days
    def stockDays(self, year):
        stock = self.getInputElement("Stock", year)
        COGS = self.getInputElement("Cost of Goods Sold", year) # Cost of Goods Sold
        
        if COGS == 0:
            print("ERROR - Stock Days: denominator is zero")
            return 0
        
        return stock/COGS * 365
    
    ## Stock Turnover
    def stockTurnover(self, year):
        sales = self.getInputElement("Sales" , year)
        stock = self.getInputElement("Stock", year)
        
        if stock == 0:
            print("ERROR - Stock Turnover: denominator is zero")
            return 0
            
        return sales/stock
    
    ## Liquidity
    
    ## Quick Ratio
    def quickRatio(self, year):
        curAssets = self.getInputElement("Current Assets", year)
        stock = self.getInputElement("Stock", year)
        curLiabilities = self.getInputElement("Current Liabilities", year)
        
        if curLiabilities == 0:
            print("ERROR - Quick Ratio: denominator is zero")
            return 0.0
        
        return (curAssets - stock)/curLiabilities