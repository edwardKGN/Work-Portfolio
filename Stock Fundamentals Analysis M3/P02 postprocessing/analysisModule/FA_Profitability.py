from . import fundamentalsAnalysis

class FA_Profitability(fundamentalsAnalysis.FA):
    
    def analyse_profitability(self):
        print("Analyse Profitability Ratios")
        
        self.analyse_returnOnEquity()
        self.analyse_returnOnCapitalEmployed()
        self.analyse_ebitdaToRevenueRatio()
    
    def analyse_returnOnEquity(self):
        self.setFinancialRatiosGrowth("Return on Equity")
    
    def analyse_returnOnCapitalEmployed(self):
        self.setFinancialRatiosGrowth("Return on Capital Employed")
    
    def analyse_ebitdaToRevenueRatio(self):
        self.setFinancialRatiosGrowth("EBITDA to Revenue Ratio")
    