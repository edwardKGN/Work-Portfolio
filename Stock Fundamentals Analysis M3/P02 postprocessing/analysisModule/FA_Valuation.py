from . import fundamentalsAnalysis

class FA_Valuation(fundamentalsAnalysis.FA):
    
    def analyse_valuation(self):
        print("Analysing Valuation Ratios")
        
        self.analyse_priceToBook()
        self.analyse_priceToEarnings()
        
    def analyse_priceToBook(self):
        self.setFinancialRatiosQuality("Price to Book Ratio", 4, 1.3)
        self.setFinancialRatiosGrowth("Price to Book Ratio")
       
    def analyse_priceToEarnings(self):
        self.setFinancialRatiosQuality("Price to Earnings Ratio", 2, 10)
        self.setFinancialRatiosGrowth("Price to Earnings Ratio")
    