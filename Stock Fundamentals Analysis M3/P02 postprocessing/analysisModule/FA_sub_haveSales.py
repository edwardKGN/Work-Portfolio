from . import fundamentalsAnalysis

class FA_haveSales(fundamentalsAnalysis.FA):
    
    def analyse_haveSales(self):
        print("Checking for Sales Ratios")
        
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
    
        - Trade Creditors Productivity
        - Trade Creditors Days
    
        - Fixed Assets Productivity
        """
        
        if (self.df_financialRatios.index == "Gross Margin").any(): # Will return True if there is a matching value
            print("Analyising Sales Ratios")
            
            self.analyse_grossMargin()
            self.analyse_capitalProductivity()
            self.analyse_cogsPerSale()
            self.analyse_workingCapitalProductivity()
            self.analyse_tradeDebtorsProductivity()
            self.analyse_tradeDebtorsDays()
            self.analyse_tradeCreditorsProductivity()
            self.analyse_tradeCreditorsDays()
            self.analyse_fixedAssetsProductivity()

    def analyse_grossMargin(self):
        self.setFinancialRatiosGrowth("Gross Margin")
    
    def analyse_capitalProductivity(self):
        self.setFinancialRatiosGrowth("Capital Productivity")
        
    def analyse_cogsPerSale(self):
        self.setFinancialRatiosGrowth("COGS per Sale")
        
    def analyse_workingCapitalProductivity(self):
        self.setFinancialRatiosGrowth("Working Capital Productivity")
        
    def analyse_tradeDebtorsProductivity(self):
        self.setFinancialRatiosGrowth("Trade Debtors Productivity")
        
    def analyse_tradeDebtorsDays(self):
        self.setFinancialRatiosGrowth("Trade Debtors Days")
        
    def analyse_tradeCreditorsProductivity(self):
        self.setFinancialRatiosGrowth("Trade Creditors Productivity")
        
    def analyse_tradeCreditorsDays(self):
        self.setFinancialRatiosGrowth("Trade Creditors Days")
        
    def analyse_fixedAssetsProductivity(self):
        self.setFinancialRatiosGrowth("Fixed Assets Productivity")
        