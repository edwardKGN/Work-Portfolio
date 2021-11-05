from . import FA_Valuation
from . import FA_Profitability
from . import FA_Efficiency
from . import FA_Liquidity
from . import FA_Solvency

from . import FA_sub_dividendPaying
from . import FA_sub_haveSales
from . import FA_sub_inventoryHolding

from . import fundamentalsAnalysis

class sectorAnalysis_REIT(FA_Valuation.FA_Valuation, FA_Profitability.FA_Profitability, FA_Efficiency.FA_Efficiency, FA_Liquidity.FA_Liquidity, FA_Solvency.FA_Solvency, FA_sub_dividendPaying.FA_dividendPaying, FA_sub_haveSales.FA_haveSales, FA_sub_inventoryHolding.FA_inventoryHolding, fundamentalsAnalysis.FA):
    
    def analyse_REIT(self):
        print("Analysing REIT's Fundamentals")
        
        self.analyse_efficiency()
        self.analyse_liquidity()
        self.analyse_solvency()
        
        self.analyse_dividendPaying()
        self.analyse_haveSales()
        self.analyse_inventoryHolding()
        
        self.analyse_FFO()
        self.analyse_AFFO()
        
        self.analyse_netAssetValue()
        self.analyse_priceToFFO()
        self.analyse_priceToAFFO()
        self.analyse_affoYield()
        self.analyse_capitalizationRate()
        self.analyse_managementExpenseToProfitRatio()
    
    """
    # Unique
        
    ## Derived
    - Funds from Operations (FFO)
    - Adjusted Funds from Operations (AFFO)
        
    ## Valuation
    - Net Asset Value
    - Price to FFO
    - Price to AFFO
        
    ## Profitability
    - AFFO Yield
    - Capitalization Rate
        
    ## Efficiency
    - Management Expense to Profit Ratio
    """
    
    def analyse_FFO(self):
        self.setFinancialRatiosGrowth("FFO")
        
    def analyse_AFFO(self):
        self.setFinancialRatiosGrowth("AFFO")
        
    def analyse_netAssetValue(self):
        self.setFinancialRatiosGrowth("Net Asset Value")
        
    def analyse_priceToFFO(self):
        self.setFinancialRatiosGrowth("Price to FFO Ratio")
        
    def analyse_priceToAFFO(self):
        self.setFinancialRatiosGrowth("Price to AFFO Ratio")
        
    def analyse_affoYield(self):
        self.setFinancialRatiosGrowth("AFFO Yield")
        
    def analyse_capitalizationRate(self):
        self.setFinancialRatiosGrowth("Capitalization Rate")
        
    def analyse_managementExpenseToProfitRatio(self):
        self.setFinancialRatiosGrowth("Management Expense to Profit Ratio")