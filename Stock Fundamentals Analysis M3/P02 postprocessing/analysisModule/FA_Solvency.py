from . import fundamentalsAnalysis

class FA_Solvency(fundamentalsAnalysis.FA):
    
    def analyse_solvency(self):
        print("Analysing Solvency Ratios")
        
        self.analyse_debtRatio()
        self.analyse_debtToEquityRatio()
        self.analyse_interestCoverageRatio()
        self.analyse_yearsToRepayDebt()
        self.analyse_averageInterestRate()
        
    def analyse_debtRatio(self):
        self.setFinancialRatiosQuality("Debt Ratio", 4, 0.5)
        self.setFinancialRatiosGrowth("Debt Ratio")
    
    def analyse_debtToEquityRatio(self):
        self.setFinancialRatiosQuality("Debt to Equity Ratio", 4, 0.33)
        self.setFinancialRatiosGrowth("Debt to Equity Ratio")
        
    def analyse_interestCoverageRatio(self):
        self.setFinancialRatiosQuality("Interest Coverage Ratio", 2, 1)
        self.setFinancialRatiosGrowth("Interest Coverage Ratio")
        
    def analyse_yearsToRepayDebt(self):
        self.setFinancialRatiosGrowth("Years to Repay Debt")
        
    def analyse_averageInterestRate(self):
        self.setFinancialRatiosQuality("Average Interest Rate", 4, 0.03) # 3% Below Interest Rate 
        self.setFinancialRatiosGrowth("Average Interest Rate")
