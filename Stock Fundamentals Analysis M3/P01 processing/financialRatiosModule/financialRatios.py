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

class financialData_main:
    financialYears = []
    
    # Initialization
    def __init__(self, df_name, sheet_name, index_col_pos = None):
        print("Financial Data Object created")
        
        self.df_input = pd.read_excel(df_name, sheet_name, index_col = index_col_pos)
        self.df_input = (self.df_input).dropna() # Clean dataframe and remove any irrelevant data
        
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
            return [0, 0, 0, 0, 0]
        
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
    
    '''
    Input .xlsx file is expected to have "Items" index-column and a list of "5 Financial Years" columns.
    If format does not match, the getters will return errors.
    '''
    
    '''
    New system allows for direct calling of key data via indexing, no need for complex boolean steps. 
    
    In addition, it also allows for processing of five values at once.
    
    Legacy Codes:
    def getInputElement(self, itemName, financialYear): # Update to include failure to find item
        if (self.df_input[self.df_input.columns[0]] == itemName).any() == True:
            return (self.df_input.loc[self.df_input[self.df_input.columns[0]] == itemName, financialYear].values)[0]
        else:
            print(itemName, " not Found")
            return 0.0
    
    # Setters
    def setOutput_row(self, itemName): # Create Financial Ratio row to input values later on
        self.df_output = self.df_output.append({"Financial Ratios": itemName}, ignore_index = True, sort = False)
        
    def setOutput_element(self, itemName, financialYear, value): # Input value for a specific Financial Ratio row and financial year 
        self.df_output.loc[self.df_output[self.df_output.columns[0]] == itemName, financialYear] = value
    
    def setFinancialYears(self): # Reformat to remove Source Document column, keep as Raw Data reference.
        # Assuming consistent formatting of columns: items, source documents, year 00 -> year 05.
        self.financialYears = (self.df_input.columns.values)[2:(len(self.df_input.columns.values))]
    '''
    
    # Write to Excel
    def writeOut(self, doc_name):
        xlsx_name = doc_name + ".xlsx"
        
        # Reindex Financial Ratios as Index instead of numbers
        self.getFinancialRatios().set_index(self.getFinancialRatios().columns[0], inplace = True)
        
        #print(doc_name , xlsx_name)
        (self.getFinancialRatios()).to_excel(xlsx_name, sheet_name = 'output')