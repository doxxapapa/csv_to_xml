import os
import pandas as pd

def convert_xlsx_to_csv(file, output_name):
    # Read and store content
    # of an excel file 
    read_file = pd.read_excel(file)
    
    # Write the dataframe object
    # into csv file
    path = os.path.join(os.getcwd(),f"outputs/{output_name}.csv")
    read_file.to_csv(path, 
                    index = None,
                    header=True)
    return path