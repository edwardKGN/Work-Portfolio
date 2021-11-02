from . import FR_Valuation
from . import FR_Profitability
from . import FR_Efficiency
from . import FR_Liquidity
from . import FR_Solvency

from . import FR_sub_dividendPaying
from . import FR_sub_haveSales
from . import FR_sub_inventoryHolding

from . import financialRatios

class financialData_retail(FR_Valuation.valuation_gen, FR_Profitability.profitability_gen, FR_Efficiency.efficiency_gen, FR_Liquidity.liquidity_gen, FR_Solvency.solvency_gen, FR_sub_dividendPaying.dividendPaying, FR_sub_haveSales.haveSales, FR_sub_inventoryHolding.inventoryHolding, financialRatios.financialData_main):
    
    """
    # Financial Ratios Implemented
        
    # General
    ## Valuation
    - Price to Book
    - Price to Earnings
        
    ## Profitability
    - Return on Equity
    - Return on Capital Employed
    - Gross Margin
    - EBITDA to Revenue Ratio
        
    ## Efficiency / Activity
    - EBITDA to Cash Conversion
    
    - Revenue to Expense Ratio
    - Capital Productivity

    - COGS per Sale

    - Working Capital Productivity

    - Trade Debtor Productivity
    - Trade Debtor Days

    - Trade Creditor Productivity
    - Trade Creditor Days

    - Fixed Assets Productivity
        
    ## Liquidity
    - Current Ratio
    - Cash Ratio
    - Operating Cash Flow Ratio
    - Cash Conversion Ratio
        
    ## Leverage / Solvency / Gearing
    - Debt Ratio
    - Debt to Equity Ratio
        
    - Interest Coverage Ratio
        
    - Years to Repay Debt
        
    - Average Interest Rate
        
    # Dividend 
        
    ## Profitability
    - Dividend Yield
        
    ## Liquidity
    - Dividend Coverage
    - Dividend Payout Ratio
    """
    
    def analyze_retail(self):
        print("Analyzing Retail Sector's Financial Ratios")
        
        self.analyzeValuation()
        self.analyzeProfitability()
        self.analyzeEfficiency()
        self.analyzeLiquidity()
        self.analyzeSolvency()
        
        self.analyzeDividend()
        self.analyzeSales()
        self.analyzeInventory()