import subprocess
import os
import pandas as pd

dir_path = os.path.dirname(os.path.abspath(__file__))
report_folder = os.path.join(dir_path, "battery-report")

# Step 1: Run extract.py
print("Running extract.py to extract battery data...")
subprocess.run(["python", os.path.join(dir_path, "extract.py")])

# Step 2: Load and analyze datasets
print("Analyzing extracted battery data...")

# Load all available CSV files
csv_files = [
    "system_info.csv",
    "battery_details.csv",
    "recent_usage.csv",
    "battery_usage.csv",
    "usage_history.csv",
    "battery_capacity_history.csv",
    "battery_life_estimates.csv",
]

dfs = {}

for file in csv_files:
    file_path = os.path.join(report_folder, file)
    if os.path.exists(file_path):
        dfs[file] = pd.read_csv(file_path)
        print(f"Loaded {file} with {len(dfs[file])} records.")

# Example Analysis
if "battery_capacity_history.csv" in dfs:
    df_capacity = dfs["battery_capacity_history.csv"]
    df_capacity["CAPACITY LOSS (%)"] = (
        (df_capacity["DESIGN CAPACITY"] - df_capacity["FULL CHARGE CAPACITY"]) / df_capacity["DESIGN CAPACITY"]
    ) * 100

    print("\nBattery Capacity Loss Over Time:")
    print(df_capacity[["PERIOD", "CAPACITY LOSS (%)"]].head())

if "battery_usage.csv" in dfs:
    df_usage = dfs["battery_usage.csv"]
    print("\nBattery Usage Summary:")
    print(df_usage.describe())

# Step 3: Run gone.py to delete extracted data
print("Running gone.py to delete extracted files...")
subprocess.run(["python", os.path.join(dir_path, "gone.py")])

print("Process Complete!")
