from . import fundamentalsAnalysis

class Analysis_Valuation(fundamentalsAnalysis.FA):
    
    def analyse_valuation(self):
        print("Analyising Valuation Ratios")
        
        self.analyse_priceToBook()
        self.analyse_priceToEarnings()
        
    def analyse_priceToBook(self):
        self.setFinancialRatiosQuality("Price to Book Ratio", 2, 1.3)
        self.setFinancialRatiosGrowth("Price to Book Ratio")
       
    def analyse_priceToEarnings(self):
        self.setFinancialRatiosQuality("Price to Earnings", 10, 2)
        self.setFinancialRatiosGrowth("Price to Earnings")