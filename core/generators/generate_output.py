import os
from ..common.apply_schema import apply_schema
from ..generators.generate_csv_from_xlsx import convert_xlsx_to_csv

def generate_output(schemaPath, input_file):
    
    if input_file.endswith(".xlsx") or input_file.endswith(".xls"):
        stem = input_file.split("/")[-1].rsplit(".", 1)[0]
        input_file = convert_xlsx_to_csv(input_file, stem)
        
    apply_schema(schemaPath, input_file)
    
    #remove unnecesarry file
    try:
        os.remove(input_file)
    except OSError as e:
        print(e)