# Header Files
import pandas as pd # Pre-requisite to run Pandas
from pandas import Series, DataFrame
import numpy as np # Pre-requisite to run numpy

import datetime # Import date time for datetime data type
from datetime import timedelta
from datetime import date
from datetime import time
from datetime import datetime

import math # For isnan() function
import itertools

'''
Input .xlsx file is expected to have "Items" index-column and a list of "5 Financial Years" columns.
If format does not match, the getters will return errors.

New system allows for direct calling of key data via indexing, no need for complex boolean steps. 
    
In addition, it also allows for processing of five values at once.
'''

class financialData_main:
    financialYears = []
    
    # Initialization
    def __init__(self, xlsx_name, sheet_name, index_col_pos = None):
        print("Financial Data Object created")
        
        xlsx_file = xlsx_name + ".xlsx"
        self.df_input = pd.read_excel(xlsx_file, sheet_name, index_col = index_col_pos)
        (self.df_input).dropna(inplace = True) # Clean dataframe and remove any irrelevant data
        
        self.setFinancialYears()
        
        column_names =  list(itertools.chain(["Financial Ratios"], self.financialYears))
        self.df_financialRatios = pd.DataFrame(columns = column_names)

    # Raw Financial Data Methods
    def getInput(self):
        return self.df_input
    
    def getFinancialData_row(self, data_label): # Extract a row of information based on data_label string
        
        if (self.df_input.index == data_label).any():       
            return self.df_input.loc[data_label].values
        else:
            print(data_label, " not found.")
            return np.array([0, 0, 0, 0, 0]) # Use Array to ease later processing
        
    # Financial Ratio Methods
    def getFinancialRatios(self):
        return self.df_financialRatios
    
    def calculateFinancialRatios_row(self, numerators, denominators):
        financialRatios = []
        
        for index, numerator in enumerate(numerators):
            
            if denominators[index] == 0: # Avoid division by 0 which results in error.
                financialRatios.append(0)
            else:
                financialRatios.append(numerator/denominators[index])
                
        return financialRatios

    def setFinancialRatios_row(self, financialRatios_label, financialRatios_arr):
        self.df_financialRatios = self.df_financialRatios.append(
            {"Financial Ratios": financialRatios_label}, ignore_index = True, sort = False)
        
        for index, item in enumerate(financialRatios_arr):
            # print(index, item)
            self.df_financialRatios.loc[self.df_financialRatios[
                self.df_financialRatios.columns[0]] == financialRatios_label, 
                self.financialYears[index]] = item
    
    # Financial Years Methods
    def getFinancialYears(self):
        return self.financialYears
    
    # Setters
    def setFinancialYears(self):
        self.financialYears = self.df_input.columns.values
    
    # Write to Excel (Run Last)
    def writeOut(self, doc_name):
        xlsx_name = doc_name + ".xlsx"
        
        # Reindex Financial Ratios as Index instead of numbers
        df_output = self.getFinancialRatios()
        
        df_output.set_index(df_output.columns[0], inplace = True)
        
        #print(doc_name , xlsx_name)
        df_output.to_excel(xlsx_name, sheet_name = 'output')