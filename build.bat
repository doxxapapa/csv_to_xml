pyinstaller --noconsole --add-data "./core;core" --hidden-import=tkinter --hidden-import=tkinter.filedialog --hidden-import=lxml --hidden-import=openpyxl --hidden-import=pandas --hidden-import=xmlschema --hidden-import=tkinter.ttk --hidden-import=dict2xml main.py