"""
Run this file to generate your own dataset for Star Type Predictor App
- Just change the number of samples as per your wish and run this file
- You will have a csv file ready with the name "input_star_data.csv" 
"""

# Change the number of samples based on how much data you want to generate
N_SAMPLES = 436

# Imports
import numpy as np
import pandas as pd

##############################################################################

""" DO NOT CHANGE THE CODE BELOW """

"""
Training was done based on this model
So if you change the code below, it may not work as expected
"""

##############################################################################

# Define a seed value (other than 100 as 100 was used for training)
np.random.seed(5007) 

# Generate Data
X_test = 3*np.random.rand(N_SAMPLES,1)
y_test = 9 + 2*X_test + np.random.rand(N_SAMPLES,1)

# Convert arrays into dict
dict_info = {'Brightness' : X_test.reshape(-1,),
             'True Size' : y_test.reshape(-1,)}

# Convert dict to pandas dataframe and save the csv
input_df = pd.DataFrame(dict_info)
input_df.to_csv('input_star_data.csv', index=False)