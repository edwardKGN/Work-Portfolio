from . import fundamentalsAnalysis

class FA_Efficiency(fundamentalsAnalysis.FA):
    
    def analyse_efficiency(self):
        print("Analysing Efficiency Ratios")
        
        self.analyse_ebidtdaToCashConversion()
        self.analyse_revenueToExpenseRatio()
        
    def analyse_ebidtdaToCashConversion(self):
        self.setFinancialRatiosGrowth("EBITDA to Cash Conversion Ratio")
        
    def analyse_revenueToExpenseRatio(self):
        self.setFinancialRatiosGrowth("Revenue to Expense Ratio")