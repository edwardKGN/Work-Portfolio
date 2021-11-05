from . import fundamentalsAnalysis

class FA_inventoryHolding(fundamentalsAnalysis.FA):
    
    def analyse_inventoryHolding(self):
        print("Checking for Inventory Ratios")
        
        if (self.df_financialRatios.index == "Stock Days").any(): # Check if Stock data is present.
            print("Analysing Inventory Ratios")
            
            self.analyse_stockDays()
            self.analyse_stockTurnover()
            self.analyse_quickRatio()
        
    """
    List of Financial Ratios
    
    # Effectiveness
    - Stock Days
    - Stock Turnover
    
    # Liquidity
    - Quick Ratio
    """
            
    def analyse_stockDays(self):
        self.setFinancialRatiosGrowth("Stock Days")
        
    def analyse_stockTurnover(self):
        self.setFinancialRatiosGrowth("Stock Turnover")
     
    def analyse_quickRatio(self):
        self.setFinancialRatiosGrowth("Quick Ratio")