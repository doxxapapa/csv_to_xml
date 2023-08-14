import sys
import os

# Get the path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
print(script_dir)
# Add the directory containing the 'core' module to sys.path
sys.path.append(os.path.join(script_dir, "core"))

from core.ui import ui
def main():
    try:
        ui()
    except Exception:
        pass

if __name__ == "__main__":
    main()