from . import FR_Valuation
from . import FR_Profitability
from . import FR_Efficiency
from . import FR_Liquidity
from . import FR_Solvency

from . import FR_sub_dividendPaying

from . import FR_sub_haveSales
from . import FR_sub_inventoryHolding

from . import financialRatios

import numpy as np

class financialData_REIT(FR_Valuation.valuation_gen, FR_Profitability.profitability_gen, FR_Efficiency.efficiency_gen, FR_Liquidity.liquidity_gen, FR_Solvency.solvency_gen, FR_sub_dividendPaying.dividendPaying, FR_sub_haveSales.haveSales, FR_sub_inventoryHolding.inventoryHolding, financialRatios.financialData_main):
    
    def analyze_REIT(self):
        print("Calculating REIT's Financial Ratios")
        
        self.analyzeEfficiency()
        self.analyzeLiquidity()
        self.analyzeSolvency()
        
        self.analyzeDividend()
        
        self.analyzeSales()
        self.analyzeInventory()
        
        self.setFinancialRatios_row("FFO", self.FFO())
        self.setFinancialRatios_row("AFFO", self.AFFO())
        
        self.setFinancialRatios_row("Net Asset Value", self.netAssetValue())
        
        self.setFinancialRatios_row("Price to FFO Ratio", self.priceToFFO())
        self.setFinancialRatios_row("Price to AFFO Ratio", self.priceToAFFO())
        
        self.setFinancialRatios_row("AFFO Yield", self.AFFOyield())
        
        self.setFinancialRatios_row("Capitalization Rate", self.capitalizationRate())
        
        self.setFinancialRatios_row("Management Expense to Profit Ratio", self.managementExToProfitRatio())
        
        
    def FFO(self): # Funds from Operations
        netIncome = self.getFinancialData_row("Net Income")
        depreciation = self.getFinancialData_row("Depreciation")
        amortization = self.getFinancialData_row("Amortization")
        propSalesLoss = self.getFinancialData_row("Losses on Property Sales")
        propSalesGain = self.getFinancialData_row("Gains on Property Sales")
        interestIncome = self.getFinancialData_row("Interest Income")
        otherIncome = self.getFinancialData_row("Other Income")
        
        return netIncome + depreciation + amortization + propSalesLoss - (propSalesGain + interestIncome + otherIncome)
        
    def AFFO(self): # Adjusted Funds from Operations
        capEx = self.getFinancialData_row("Capital Expenditure")
        rentIncreases = self.getFinancialData_row("Rent Increases")
        propOpsEx = self.getFinancialData_row("Property Operating Expenses")
        
        return self.FFO() + rentIncreases - capEx - propOpsEx
    
    ## Valuation
    
    def netAssetValue(self):
        totAssets = self.getFinancialData_row("Total Assets")
        totLiab = self.getFinancialData_row("Total Liabilities")
        
        netAsset = np.multiply((totAssets - totLiab), 1000) # Convert to Currency
        
        outstandingShares = self.getFinancialData_row("Outstanding Shares")
        
        return self.calculateFinancialRatios_row(netAsset, outstandingShares)
    
    def priceToFFO(self):
        unitPrice = self.getFinancialData_row("Unit Price (Currency)")
        outstandingShares = self.getFinancialData_row("Outstanding Shares")
        
        marketCap = (unitPrice * outstandingShares)/1000 # Currency -> Currency '000 <Standard Unit>

        return self.calculateFinancialRatios_row(marketCap, self.FFO())
        
    def priceToAFFO(self):
        unitPrice = self.getFinancialData_row("Unit Price (Currency)")
        outstandingShares = self.getFinancialData_row("Outstanding Shares")
        
        marketCap = (unitPrice * outstandingShares)/1000 # Currency -> Currency '000 <Standard Unit>
                
        return self.calculateFinancialRatios_row(marketCap, self.AFFO())
    
    ## Profitability
    
    def AFFOyield(self):
        unitPrice = self.getFinancialData_row("Unit Price (Currency)")
        outstandingShares = self.getFinancialData_row("Outstanding Shares")
        
        marketCap = (unitPrice * outstandingShares)/1000 # Currency -> Currency '000 <Standard Unit>

        return self.calculateFinancialRatios_row(self.AFFO(), marketCap)
    
    def capitalizationRate(self):
        unitPrice = self.getFinancialData_row("Unit Price (Currency)")
        outstandingShares = self.getFinancialData_row("Outstanding Shares")
        
        marketCap = (unitPrice * outstandingShares)/1000 # Currency -> Currency '000 <Standard Unit>
        
        netOpIncome = self.getFinancialData_row("Net Operating Income")
        
        return self.calculateFinancialRatios_row(netOpIncome, marketCap)
    
    ## Efficiency / Activity
        
    def managementExToProfitRatio(self):
        netIncome = self.getFinancialData_row("Net Income")
        managementEx = self.getFinancialData_row("Management Expense")
        
        return self.calculateFinancialRatios_row(managementEx, netIncome)