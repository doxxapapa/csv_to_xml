import os
from ..common.apply_schema import apply_schema
from ..common.create_zip import create_zip
from ..generators.generate_csv_from_xlsx import convert_xlsx_to_csv

def generate_output(schemaPath, input_file):
    
    #check file and convert it to csv if it is not
    if input_file.endswith(".xlsx") or input_file.endswith(".xls"):
        stem = input_file.split("/")[-1].rsplit(".", 1)[0]
        input_file = convert_xlsx_to_csv(input_file, stem)
    
    #run the logic that converts csv to xml based on a schema    
    apply_schema(schemaPath, input_file)
    
    #remove unnecesarry file
    try:
        os.remove(input_file)
    except OSError as e:
        print(e)
        
    #generate zip file from the output    
    create_zip()