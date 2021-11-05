# Header Files
import pandas as pd # Pre-requisite to run Pandas
from pandas import Series, DataFrame
import numpy as np # Pre-requisite to run numpy

import datetime # Import date time for datetime data type
from datetime import timedelta
from datetime import date
from datetime import time
from datetime import datetime

from analysisModule.statisticsModule.statisticsMod import linReg # Apparently it's read from the calling page
from scipy import stats

import math # For isnan() function
import itertools

class FA:
    financialYears = []
    
    def __init__(self, xlsx_name, sheet_name, index_col_pos = None):
        
        xlsx_name = xlsx_name + ".xlsx"
        self.df_financialRatios = pd.read_excel(xlsx_name, sheet_name, index_col = index_col_pos)
        (self.df_financialRatios).dropna(inplace = True) # Clean dataframe and remove any irrelevant data
        
        self.setFinancialYears()
        
        column_names =  list(itertools.chain(["Financial Ratios", "Condition"], self.financialYears))
        self.df_quality = pd.DataFrame(columns = column_names)
        
        self.df_growth = pd.DataFrame(columns = ["Financial Ratios", "Growth", "Intercept", "Correlation Coefficient", "Growth Uncertainty", "Intercept Uncertainty"])
    
    # Financial Ratios Methods
    def getFinancialRatios(self):
        return self.df_financialRatios
    
    def getFinancialRatios_row(self, data_label):
        if (self.df_financialRatios.index == data_label).any():       
            return self.df_financialRatios.loc[data_label].values
        else:
            print(data_label, " not found.")
            return np.array([0, 0, 0, 0, 0])
    
    # General Output Setters
    def setFirstColumn_element(self, item, df_option):
        if df_option == 0:
            #print("Setting First Column Element:", item)
            self.df_quality = self.df_quality.append({"Financial Ratios": item}, ignore_index = True, sort = False)
        elif df_option == 1:
            #print("Setting First Column Element:", item)
            self.df_growth = self.df_growth.append({"Financial Ratios": item}, ignore_index = True, sort = False)
        else:
            print("ERROR - Option not recognized")
            return 
        
    def getAnalysis(self, df_option):  
        if df_option == 0:
            return self.df_quality
        elif df_option == 1:
            return self.df_growth
        else:
            print("ERROR - Option not recognized")
            return 
    
    # Financial Ratios Quality Methods
    
    def setCondition_element(self, item, element): 
        self.df_quality.loc[self.df_quality[self.df_quality.columns[0]] == item, "Condition"] = element
    
    def setFinancialRatiosQuality(self, financialRatio_label, condition_option, condition_value):
        self.setFirstColumn_element(financialRatio_label, 0)
        
        FR_row = self.getFinancialRatios_row(financialRatio_label)
        
        if condition_option == 0:
            ls_quality = FR_row == condition_value
            self.setCondition_element(financialRatio_label, ("==" + str(condition_value)))
        elif condition_option == 1:
            ls_quality = FR_row > condition_value
            self.setCondition_element(financialRatio_label, (">" + str(condition_value)))
        elif condition_option == 2:
            ls_quality = FR_row >= condition_value
            self.setCondition_element(financialRatio_label, (">=" + str(condition_value)))
        elif condition_option == 3:
            ls_quality = FR_row < condition_value
            self.setCondition_element(financialRatio_label, ("<" + str(condition_value)))
        elif condition_option == 4:
            ls_quality = FR_row <= condition_value
            self.setCondition_element(financialRatio_label, ("<=" + str(condition_value)))
        else: 
            print("ERROR - Option not recognized")
            return
        
        # print(ls_quality)
        ls_met = []
        
        for result in ls_quality:
            if result:
                ls_met.append("Met")
            else: 
                ls_met.append("Not Met")
                
        # print(ls_met)
        
        for index, year in enumerate(self.getFinancialYears()):
            #print(index, year)
            self.df_quality.loc[self.df_quality[self.df_quality.columns[0]] == financialRatio_label, year] = ls_met[index]
   
    # Financial Ratios Growth Methods   
    def setFinancialRatiosGrowth(self, financialRatio_label):
        self.setFirstColumn_element(financialRatio_label, 1)
        
        FR_row = self.getFinancialRatios_row(financialRatio_label)
        years = self.getFinancialYears()
        
        #print("Type Financial Ratios ", type(FR_row), "Items: ", FR_row)
        #print("Type Financial Years ", type(years), "Years: ", years)
        
        #linReg_out = linReg(years, input_row)
        #print(linReg_out, type(linReg_out), linReg_out[0])
        
        linReg_result = stats.linregress(list(years), list(FR_row)) # Use Scipy.stats Linear Regression method       
        linReg_out = (linReg_result.slope, linReg_result.intercept, linReg_result.rvalue, linReg_result.stderr, linReg_result.intercept_stderr)
        
        #print(self.getOutput(1).columns[1:])
        for index, column_name in enumerate(self.getAnalysis(1).columns[1:]):
            #print(index, column_name)
            self.df_growth.loc[self.df_growth[self.df_growth.columns[0]] == financialRatio_label, column_name] = linReg_out[index]
    
    # Financial Years Methods
    def getFinancialYears(self): # Getter
        return self.financialYears
 
    def setFinancialYears(self): # Setter
        self.financialYears = self.df_financialRatios.columns.values
        
    # Write to Excel
    def writeOut(self, doc_name):
        xlsx_name = doc_name + ".xlsx"
        
        df_quality = self.getAnalysis(0)
        df_growth = self.getAnalysis(1)
        
        df_quality.set_index(df_quality.columns[0], inplace = True)
        df_growth.set_index(df_growth.columns[0], inplace = True)
        
        #print(doc_name , xlsx_name)
        df_quality.to_excel(("quality_" + xlsx_name), sheet_name = 'output')
        df_growth.to_excel(("growth_" + xlsx_name), sheet_name = 'output')