from . import FA_Valuation
from . import FA_Profitability
from . import FA_Efficiency
from . import FA_Liquidity
from . import FA_Solvency

from . import FA_sub_dividendPaying
from . import FA_sub_haveSales
from . import FA_sub_inventoryHolding

from . import fundamentalsAnalysis

class sectorAnalysis_insurance(FA_Valuation.FA_Valuation, FA_Profitability.FA_Profitability, FA_Efficiency.FA_Efficiency, FA_Liquidity.FA_Liquidity, FA_Solvency.FA_Solvency, FA_sub_dividendPaying.FA_dividendPaying, FA_sub_haveSales.FA_haveSales, FA_sub_inventoryHolding.FA_inventoryHolding, fundamentalsAnalysis.FA):
    
    def analyse_insurance(self):
        self.analyse_valuation()
        self.analyse_profitability()
        self.analyse_efficiency()
        self.analyse_liquidity()
        self.analyse_solvency()
        
        self.analyse_dividendPaying()
        self.analyse_haveSales()
        self.analyse_inventoryHolding()
        
        self.analyse_investmentReturn()
        self.analyse_netInvestmentIncomeRatio()
        self.analyse_lossRatio()
        self.analyse_underwritingExpenseRatio()
        
        """
        # Insurance
    
        ## Profitability
        - Investment Return
        - Net Investment Income Ratio
    
        ## Efficiency / Activity
        - Loss Ratio
        - Underwriting Expense Ratio
    
        """
        
    def analyse_investmentReturn(self):
        self.setFinancialRatiosGrowth("Investment Return")
            
    def analyse_netInvestmentIncomeRatio(self):
        self.setFinancialRatiosGrowth("Net Investment Income Ratio")
            
    def analyse_lossRatio(self):
        self.setFinancialRatiosGrowth("Loss Ratio")
        
    def analyse_underwritingExpenseRatio(self):
        self.setFinancialRatiosGrowth("Underwriting Expense Ratio")