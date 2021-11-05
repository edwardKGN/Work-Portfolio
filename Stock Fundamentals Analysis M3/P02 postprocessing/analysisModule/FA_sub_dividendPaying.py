from . import fundamentalsAnalysis

class FA_dividendPaying(fundamentalsAnalysis.FA):
    
    def analyse_dividendPaying(self):
        print("Checking for Dividend Paying Ratios")

        if (self.df_financialRatios.index == "Dividend Yield").any(): # Check if Dividend Financial Ratios are present
            print("Analyising Dividend Paying Ratios")
        
            self.analyse_dividendYield()
            self.analyse_dividendCoverage()
            self.analyse_dividendPayoutRatio()
        
    def analyse_dividendYield(self):
        self.setFinancialRatiosQuality("Dividend Yield", 2, 0.03) # >= 3% 
        self.setFinancialRatiosGrowth("Dividend Yield")
        
    def analyse_dividendCoverage(self):
        self.setFinancialRatiosQuality("Dividend Coverage Ratio", 2, 1) # >= 1 
        self.setFinancialRatiosGrowth("Dividend Coverage Ratio")
        
    def analyse_dividendPayoutRatio(self):
        self.setFinancialRatiosQuality("Dividend Payout Ratio", 4, 1) # <= 1
        self.setFinancialRatiosGrowth("Dividend Payout Ratio")