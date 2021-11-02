from . import financialRatios
import numpy as np

class inventoryHolding(financialRatios.financialData_main): # Often Declared as "Stock" in Financial Reports
    
    """
    List of Financial Ratios
    
    # Effectiveness
    - Stock Days
    - Stock Turnover
    
    # Liquidity
    - Quick Ratio
    """
    
    # Main Analyzer
    def analyzeInventory(self):
        print("Analyze Inventory Holding")
        
        if (self.df_input.index == "Stock").any(): # Check if Stock data row is present.
            print("Stock data found.")
        
            self.setFinancialRatios_row("Stock Days", self.stockDays())
            self.setFinancialRatios_row("Stock Turnover", self.stockTurnover())
            
            self.setFinancialRatios_row("Quick Ratio", self.quickRatio())
        else:
            print("No Stock data found.")
    
    ## Efficicency
    
    ## Stock Days
    def stockDays(self):
        stock = self.getFinancialData_row("Stock")
        
        COGS = self.getFinancialData_row("Cost of Goods Sold") # Cost of Goods Sold
        
        return np.multiply(self.calculateFinancialRatios_row(stock, COGS), 365)
    
    ## Stock Turnover
    def stockTurnover(self):
        sales = self.getFinancialData_row("Sales")
        
        stock = self.getFinancialData_row("Stock")
            
        return self.calculateFinancialRatios_row(sales, stock)
    
    ## Liquidity
    
    ## Quick Ratio
    def quickRatio(self):
        curAssets = self.getFinancialData_row("Current Assets")
        stock = self.getFinancialData_row("Stock")
        
        quickValue = curAssets - stock
        
        curLiabilities = self.getFinancialData_row("Current Liabilities")
        
        return self.calculateFinancialRatios_row(quickValue, curLiabilities)