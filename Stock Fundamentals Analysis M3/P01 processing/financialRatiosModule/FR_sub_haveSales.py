from . import financialRatios
import numpy as np

class haveSales(financialRatios.financialData_main): # Declared as Sales in Financial Report
    
    """
    List of Financial Ratios
    
    # Profitability
    - Gross Margin
    
    # Efficiency
    - Capital Productivity
    
    - COGS per Sale
    
    - Working Capital Productivity
    
    - Trade Debtors Productivity
    - Trade Debtors Days
    
    - Trade Creditor Productivity
    - Trade Creditor Days
    
    - Fixed Assets Productivity
    """
    
    def analyzeSales(self):
        print("Analyzing Sales-related Financial Ratios") # Mostly related to effectiveness
        
        if (self.df_input.index == "Sales").any(): # Check if Sales data row is present
            print("Sales data available")
            
            self.setFinancialRatios_row("Gross Margin", self.grossMargin())
            
            self.setFinancialRatios_row("Capital Productivity", self.capitalProductivity())
            self.setFinancialRatios_row("COGS per Sale", self.cogsPerSale())
            self.setFinancialRatios_row("Working Capital Producitivy", self.workingCapitalProductivity())
            
            self.setFinancialRatios_row("Trade Debtors Productivity", self.tradeDebtorProductivity())
            self.setFinancialRatios_row("Trade Debtors Days", self.tradeDebtorDays())
            
            self.setFinancialRatios_row("Trade Creditors Productivity", self.tradeCreditorProductivity())
            self.setFinancialRatios_row("Trade Creditors Days", self.tradeCreditorDays())
            
            self.setFinancialRatios_row("Fixed Assets Productivity", self.fixedAssetsProductivity())
        else:
            print("No sales data available")
    
    # Profitability
    ## Gross Margin
    def grossMargin(self):
        revenue = self.getFinancialData_row("Revenue")
        COGS = self.getFinancialData_row("Cost of Goods Sold") # Cost of Goods Sold
        
        grossProfit = revenue - COGS
        
        sales = self.getFinancialData_row("Sales")
        
        return self.calculateFinancialRatios_row(grossProfit, sales)
            
    ## Capital Productivity
    def capitalProductivity(self):
        operatingProfit = self.getFinancialData_row("Operating Profit")
        
        sales = self.getFinancialData_row("Sales")
        
        return self.calculateFinancialRatios_row(operatingProfit, sales)
   
    ## COGS per Sale
    def cogsPerSale(self):
        COGS = self.getFinancialData_row("Cost of Goods Sold") # Cost of Goods Sold
        
        sales = self.getFinancialData_row("Sales")
        
        return self.calculateFinancialRatios_row(COGS, sales)
   
    ## Working Capital Productivity
    def workingCapitalProductivity(self):
        sales = self.getFinancialData_row("Sales")
        
        currAssets = self.getFinancialData_row("Current Assets")
        currLiabilities = self.getFinancialData_row("Current Liabilities")
        
        workingCap = currAssets - currLiabilities
        
        return self.calculateFinancialRatios_row(sales, workingCap)
    
    ## Trade Debtor Productivity
    def tradeDebtorProductivity(self):
        sales = self.getFinancialData_row("Sales")
        
        tradeDebtors = self.getFinancialData_row("Trade Debtors")
        
        # print(self.calculateFinancialRatios_row(sales, tradeDebtors))
        
        return self.calculateFinancialRatios_row(sales, tradeDebtors)
    
    ## Trade Debtor Days
    def tradeDebtorDays(self):
        tradeDebtors = self.getFinancialData_row("Trade Debtors")
        
        sales = self.getFinancialData_row("Sales")
        
        # print(self.calculateFinancialRatios_row(tradeDebtors, sales) * 365) # This appears to duplicate the results 365 times
        # print(np.multiply(self.calculateFinancialRatios_row(tradeDebtors, sales), 365))
        
        return np.multiply(self.calculateFinancialRatios_row(tradeDebtors, sales), 365)
    
    ## Trade Creditor Productivity
    def tradeCreditorProductivity(self):
        sales = self.getFinancialData_row("Sales")
        
        tradeCreditors = self.getFinancialData_row("Trade Creditors")
        
        return self.calculateFinancialRatios_row(sales, tradeCreditors)

    ## Trade Creditor Days
    def tradeCreditorDays(self):
        tradeCreditors = self.getFinancialData_row("Trade Creditors")
        
        sales = self.getFinancialData_row("Sales")
        
        return np.multiply(self.calculateFinancialRatios_row(tradeCreditors, sales), 365)   
        
    ## Fixed Asset Productivity
    def fixedAssetsProductivity(self):
        sales = self.getFinancialData_row("Sales")
        
        fixedAssets = self.getFinancialData_row("Fixed Assets")
        
        return self.calculateFinancialRatios_row(sales, fixedAssets)      