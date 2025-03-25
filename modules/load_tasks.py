import pandas as pd
import os

def load_tasks():
    """Load tasks from CSV, converting from Excel if necessary"""
    excel_file = "data/unit3_tasks.xlsx"
    csv_file = "data/unit3_tasks.csv"

    # Convert Excel to CSV if CSV does not exist
    if not os.path.exists(csv_file) and os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
        df.to_csv(csv_file, index=False)
        print(f"✅ Converted '{excel_file}' to '{csv_file}'")

    # Load CSV
    return pd.read_csv(csv_file)

