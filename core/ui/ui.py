import os
import platform
import subprocess
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading
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
    try:
        shutil.rmtree("outputs")
    except Exception:
        pass
    xlsx_csv_path = file_path_entry.get()
    xsd_path =xsd_path_entry.get()
    
    # Disable the process button during processing
    process_button.config(state=tk.DISABLED)
    
    # Create a progress bar
    progress_bar = ttk.Progressbar(root, mode='determinate', maximum=100, length=5)
    progress_bar.grid(row=2, columnspan=1, padx=5, pady=5, sticky='we')
    progress_bar.start()
    
    # Assuming the generated files are in a folder named "output"
    output_folder = "outputs"
    os.makedirs(output_folder, exist_ok=True)
    
    # Create a new thread to run generate_output
    thread = threading.Thread(target=generate_output, args=(xsd_path, xlsx_csv_path))
    
    # Start the thread
    thread.start()
    
    progress_bar['value'] = 0
    root.update_idletasks()  # Force GUI update
    
    is_output_generated = False
    while not is_output_generated:
        progress_bar['value'] += 0.06
        root.update_idletasks()  # Force GUI update
        if os.path.exists("outputs/output.zip"):
            # Open the folder after generating files
            folder_path = os.path.abspath(output_folder)
            if platform.system() == "Windows":
                os.startfile(folder_path)
            elif platform.system() == "Darwin":
                subprocess.check_call(["open", folder_path])
            else:
                subprocess.check_call(["xdg-open", folder_path])
            os.startfile(folder_path)
            progress_bar['value'] = 100
            root.update_idletasks()  # Force GUI update
            progress_bar.grid_remove()  # Remove the progress bar from the layout
            process_button.config(state=tk.NORMAL)
            succeded_label = tk.Label(root, text="Succesful Generation")
            succeded_label.grid(row=2, column=0, padx=10, pady=5)
            thread.join()
            is_output_generated = True
    

# Create the main window
root = tk.Tk()
root.title("XML2CSV")

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