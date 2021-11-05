from . import FA_Valuation
from . import FA_Profitability
from . import FA_Efficiency
from . import FA_Liquidity
from . import FA_Solvency

from . import FA_sub_dividendPaying
from . import FA_sub_haveSales
from . import FA_sub_inventoryHolding

from . import fundamentalsAnalysis

class sectorAnalysis_retail(FA_Valuation.FA_Valuation, FA_Profitability.FA_Profitability, FA_Efficiency.FA_Efficiency, FA_Liquidity.FA_Liquidity, FA_Solvency.FA_Solvency, FA_sub_dividendPaying.FA_dividendPaying, FA_sub_haveSales.FA_haveSales, FA_sub_inventoryHolding.FA_inventoryHolding, fundamentalsAnalysis.FA):
    
    def analyse_retail(self):
        print("Analyzing Retail Sector's Fundamentals Analysis")
        
        self.analyse_valuation()
        self.analyse_profitability()
        self.analyse_efficiency()
        self.analyse_liquidity()
        self.analyse_solvency()
        
        self.analyse_dividendPaying()
        self.analyse_haveSales()
        self.analyse_inventoryHolding()