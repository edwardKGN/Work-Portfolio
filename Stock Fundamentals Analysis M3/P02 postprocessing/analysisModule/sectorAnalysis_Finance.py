from . import FA_Valuation
from . import FA_Profitability
from . import FA_Efficiency
from . import FA_Liquidity
from . import FA_Solvency

from . import FA_sub_dividendPaying
from . import FA_sub_haveSales
from . import FA_sub_inventoryHolding

from . import fundamentalsAnalysis

class sectorAnalysis_finance(FA_Valuation.FA_Valuation, FA_Profitability.FA_Profitability, FA_Efficiency.FA_Efficiency, FA_Liquidity.FA_Liquidity, FA_Solvency.FA_Solvency, FA_sub_dividendPaying.FA_dividendPaying, FA_sub_haveSales.FA_haveSales, FA_sub_inventoryHolding.FA_inventoryHolding, fundamentalsAnalysis.FA):
    
    def analyse_finance(self):
        print("Analysing Finance's Fundamentals")
        
        self.analyse_valuation()
        self.analyse_profitability()
        self.analyse_efficiency()
        self.analyse_liquidity()
        #self.analyse_solvency() # No Solvency / Debt. Unique Calculation Required.
        
        self.analyse_dividendPaying()
        self.analyse_haveSales()
        self.analyse_inventoryHolding()
        
        self.analyse_netInterestMargin()
        self.analyse_netNonInterestMargin()
        self.analyse_ROA()
        self.analyse_casaRatio()
        self.analyse_netProfitMargin()
        self.analyse_assetUtilization()
        
        self.analyse_efficiencyRatio()
        self.analyse_operatingEfficiencyRatio()
        
        self.analyse_creditToDepositRatio()
        
        self.analyse_leverageRatio()
        self.analyse_cet1Ratio()
        self.analyse_loanToAssetsRatio()
        self.analyse_capitalAdequacyRatio()
        self.analyse_badLoanRatio()
        self.analyse_loanLossProvisionCoverageRatio()
        
    # Unique
    ## Profitability Ratios
        
    def analyse_netInterestMargin(self):
        self.setFinancialRatiosGrowth("Net Interest Margin")
        
    def analyse_netNonInterestMargin(self):
        self.setFinancialRatiosGrowth("Net Non-Interest Margin")
    
    def analyse_ROA(self):
        self.setFinancialRatiosQuality("Return on Assets", 2, 0.01)
        self.setFinancialRatiosGrowth("Return on Assets")
        
    def analyse_casaRatio(self):
        self.setFinancialRatiosGrowth("CASA Ratio")
     
    def analyse_netBankOperatingMargin(self):
        self.setFinancialRatiosGrowth("Net Bank Operating Margin")
        
    def analyse_netProfitMargin(self):
        self.setFinancialRatiosGrowth("Net Profit Margin")
    
    def analyse_assetUtilization(self):
        self.setFinancialRatiosGrowth("Asset Utilization Ratio")
        
    ## Efficiency Ratios
    
    def analyse_efficiencyRatio(self):
        self.setFinancialRatiosGrowth("Efficiency Ratio")
        
    def analyse_operatingEfficiencyRatio(self):
        self.setFinancialRatiosGrowth("Operating Efficiency Ratio")
        
    ## Liquidity
    def analyse_creditToDepositRatio(self):
        self.setFinancialRatiosGrowth("Credit to Deposit Ratio")
        
    ## Solvency
    def analyse_leverageRatio(self):
        self.setFinancialRatiosQuality("Leverage Ratio", 2, 0.03)
        self.setFinancialRatiosGrowth("Leverage Ratio")
    
    def analyse_cet1Ratio(self):
        self.setFinancialRatiosGrowth("CET-1 Ratio")
    
    def analyse_loanToAssetsRatio(self):
        self.setFinancialRatiosGrowth("Loans to Assets Ratio")
    
    def analyse_capitalAdequacyRatio(self):
        self.setFinancialRatiosQuality("Capital Adequacy Ratio", 2, 0.08)
        self.setFinancialRatiosGrowth("Capital Adequacy Ratio")
        
    def analyse_badLoanRatio(self):
        self.setFinancialRatiosGrowth("Bad Loan Ratio")
        
    def analyse_loanLossProvisionCoverageRatio(self):
        self.setFinancialRatiosGrowth("Loan Loss Provision Coverage Ratio")