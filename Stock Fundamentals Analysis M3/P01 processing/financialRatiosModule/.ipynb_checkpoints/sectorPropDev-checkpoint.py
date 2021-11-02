from . import fundamentalsAnalysis
from . import FA_Valuation_gen
from . import FA_Profitability_gen
from . import FA_Efficiency_gen
from . import FA_Liquidity_gen
from . import FA_Solvency_gen
from . import dividendPaying
from . import inventoryHolding

class financialData_propDev(FA_Valuation_gen.valuation_gen, FA_Profitability_gen.profitability_gen, FA_Efficiency_gen.efficiency_gen, FA_Liquidity_gen.liquidity_gen, FA_Solvency_gen.solvency_gen, dividendPaying.dividendPaying_general, fundamentalsAnalysis.financialData_sectorGeneral): # Method Resolution Order (MRO) second layer that inherit from first layer must be declared prior the first layer of inheritence. 
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
    
    def analyze_propDev(self):
        print("Analysis starting")
        
        self.analyzeValuation_gen()
        self.analyzeProfitability_gen()
        self.analyzeEfficiency_gen()
        self.analyzeLiquidity_gen()
        self.analyzeSolvency_gen()
        self.analyze_dividend()

    # Unique Financial Ratios
    # N/A