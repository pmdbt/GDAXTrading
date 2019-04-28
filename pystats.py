import statsmodels.api
from math import log
import numpy as np
import pandas as pd
#This file contains the code for using PCAF time series analysis function on financial data using python
#packages and not relying on python interfacing with R. This code is ideal for quantopian's dev
#environment

def py_calc(python_price_list, time_differential):
    lag_chosen = int(0.1*time_differential) #currently set to 10 percent of data length
    logged_prices = []
    for values in python_price_list:
        logged_prices.append(log(values))
    pacf_results = statsmodels.tsa.stattools.pacf(logged_prices, lag_chosen)
    pacf_results = pacf_results[1:]
    lags = []
    """Want this loop to cycle through the pacf_results, the ith term + 1
    should be the day lag from the pacf analysis, since loop starts at value 0, ie 0th term is the 1 day lag"""
    for i in range(len(pacf_results)):
        lags.append(i+1)
    regression_matrix = [[]] * (len(lags)+1) #dynamically create number of empty lists that corresponds to the number of lags
    for i in range(len(regression_matrix)):
        #we want to truncate the days lag data so they all line up for regression
        #len(lags)-i seems to be the formula to truncate the top of the list, while len(logged_prices)-1-i
        #truncates from the bottom. The columns should be each of length of original price list - number of lags
        #so, 100 days of data with 2 days of lag should have each column length at 98
        #The -1-i at the end is because python lists start at index 0 insted of at 1
        regression_matrix[i] = logged_prices[(len(lags)-i):(len(logged_prices)-1-i)]
    #the code below splits the large formatted matrix to exogenous and endogenous variables y and x
    reg_y = regression_matrix[0]
    reg_x = np.transpose(regression_matrix[1:]) #transpose the matrix to get the dimensions to be correct
    reg_y = pd.DataFrame(reg_y, columns=["logged_prices"])
    #need to create a list of column names as a vector of string variables
    variable_names = []
    for lag in lags:
        variable_names.append("lag" + str(lag))
    reg_x = pd.DataFrame(reg_x, columns=variable_names)
    reg_x = statsmodels.tools.tools.add_constant(reg_x) #this adds constant to the regression
    model = statsmodels.regression.linear_model.OLS(reg_y, reg_x)
    results = model.fit()
    #for debugging
    #print(results.summary())
    #print(results.params)
    #using loops to strip away parameters that have bad t values, usually lower than absolute value of 1.70
    which_lags = []
    for counter, value in enumerate(results.tvalues):
        if abs(value) >= 1.70:
            which_lags.append(counter) #the counter corresponds to the columns of the reg_x dataframe
    print(which_lags)
    filtered_results = []
    #checks if there is a constant present in the significant results
    for counter, lag in enumerate(which_lags):
        if lag == 0: #checking if there is a significant const returned by regression
            filtered_results.append("const")
        else:
            filtered_results.append("lag" + str(lag)) #creates vector of new significant columns
    #resetting reg_x so that it only includes columns that were signifcant after first regression
    reg_x = reg_x[filtered_results]
    #second regression using only significant variables
    model = statsmodels.regression.linear_model.OLS(reg_y, reg_x)
    results = model.fit()
    print(results.summary())
    const = False
    if filtered_results[0].lower() == "const":
        const = True
    return results.params, results.rsquared_adj, const
