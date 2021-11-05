from . import fundamentalsAnalysis 

class FA_Liquidity(fundamentalsAnalysis.FA):
    
    def analyse_liquidity(self):
        print("Analysing Liquidity Ratios")
        
        self.analyse_currentRatio()
        self.analyse_cashRatio()
        self.analyse_operatingCashFlowRatio()
        self.analyse_cashConversionRatio()
    
    def analyse_currentRatio(self):
        self.setFinancialRatiosQuality("Current Ratio", 2, 2)
        self.setFinancialRatiosGrowth("Current Ratio")
        
    def analyse_cashRatio(self):
        self.setFinancialRatiosGrowth("Cash Ratio")
        
    def analyse_operatingCashFlowRatio(self):
        self.setFinancialRatiosGrowth("Operating Cash Flow Ratio")
        
    def analyse_cashConversionRatio(self):
        self.setFinancialRatiosQuality("Cash Conversion Ratio", 2, 1)
        self.setFinancialRatiosGrowth("Cash Conversion Ratio")