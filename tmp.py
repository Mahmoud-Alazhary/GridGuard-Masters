import pandas as pd
import numpy as np

# Load the Excel file using pandas
data = pd.read_excel("D:/programming/GridMasters/GridGuard-Masters/Files/Actuals.xlsx")

# Select rows from 15783 to 15806 (inclusive)
#data = data.iloc[15783:15806+1, 1:]  # Adjust indexing as needed
print(data.iloc[15807])
# Exclude the first column and convert to NumPy array
