import os
import tkinter as tk
from tkinter import filedialog
from ..generators.generate_output import generate_output

def open_xlsx_csv():
    file_path = filedialog.askopenfilename(filetypes=[("Excel/CSV Files", "*.xlsx *.csv")])
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

def open_xsd():
    xsd_path = filedialog.askopenfilename(filetypes=[("XSD Files", "*.xsd")])
    xsd_path_entry.delete(0, tk.END)
    xsd_path_entry.insert(0, xsd_path)

def process_files():
    xlsx_csv_path = file_path_entry.get()
    xsd_path =xsd_path_entry.get()
    
    # Assuming the generated files are in a folder named "output"
    output_folder = "outputs"
    os.makedirs(output_folder, exist_ok=True)
    
    generate_output(xsd_path,xlsx_csv_path )
        
    # Open the folder after generating files
    folder_path = os.path.abspath(output_folder)
    os.startfile(folder_path)

# Create the main window
root = tk.Tk()
root.title("Simple Frontend")

# Labels
file_path_label = tk.Label(root, text="Select XLSX/CSV File:")
xsd_path_label = tk.Label(root, text="Select XSD File:")

# Entry widgets
file_path_entry = tk.Entry(root, width=50)
xsd_path_entry = tk.Entry(root, width=50)

# Buttons
open_xlsx_csv_button = tk.Button(root, text="Browse", command=open_xlsx_csv)
open_xsd_button = tk.Button(root, text="Browse", command=open_xsd)
process_button = tk.Button(root, text="Process Files", command=process_files)

# Layout using grid
file_path_label.grid(row=0, column=0, padx=10, pady=5)
file_path_entry.grid(row=0, column=1, padx=10, pady=5)
open_xlsx_csv_button.grid(row=0, column=2, padx=5, pady=5)

xsd_path_label.grid(row=1, column=0, padx=10, pady=5)
xsd_path_entry.grid(row=1, column=1, padx=10, pady=5)
open_xsd_button.grid(row=1, column=2, padx=5, pady=5)

process_button.grid(row=2, columnspan=3, padx=10, pady=10)

root.mainloop()