import os
import subprocess
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime, timedelta

dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = dir_path.capitalize() + r"\battery-report\battery-report.html"

command = f'powercfg /batteryreport /output "{file_path}"'
subprocess.run(command, shell=True)

with open(file_path, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

def fill_missing_dates(times):
    last_date = None
    new_times = []

    for time in times:
        if " " in time:  # Full timestamp present
            last_date = time.split(" ")[0]  # Extract date part
            new_times.append(time)
        else:  # Only time is present, prepend last known date
            new_times.append(f"{last_date} {time}" if last_date else time)

    return new_times

def extract_time_percentage(column):
    time_values = []
    percent_values = []
    
    for value in column.astype(str):
        match = re.search(r"(\d{1,2}:\d{2}:\d{2})\s*(\d+)%?", value)
        if match:
            time_values.append(match.group(1))  # Extract time
            percent_values.append(match.group(2))  # Extract percentage
        else:  # If no match, default to empty values
            time_values.append("")
            percent_values.append("")
    
    return time_values, percent_values

def find_table_value(label):
    """Finds the value next to a label in a table, handling missing elements safely."""
    cell = soup.find("td", string=lambda text: text and label.lower() in text.lower())
    return cell.find_next_sibling("td").text.strip() if cell else "N/A"

system_info = {
    "Computer Name": find_table_value("COMPUTER NAME"),
    "System Product Name": find_table_value("SYSTEM PRODUCT NAME"),
    "OS Build": find_table_value("OS BUILD"),
    "BIOS": find_table_value("BIOS"),
    "Report Time": find_table_value("REPORT TIME")
}

battery_details = {
    "Battery Name": find_table_value("NAME"),
    "Manufacturer": find_table_value("MANUFACTURER"),
    "Chemistry": find_table_value("CHEMISTRY"),
    "Design Capacity": find_table_value("DESIGN CAPACITY"),
    "Full Charge Capacity": find_table_value("FULL CHARGE CAPACITY"),
}

def extract_table(section_header):
    """Extracts table data under a given section header."""
    section = soup.find("h2", string=lambda text: text and section_header.lower() in text.lower())
    if not section:
        return pd.DataFrame()  
    
    table = section.find_next("table")
    if not table:
        return pd.DataFrame()

    rows = []
    for row in table.find_all("tr", class_=["even", "odd"]):
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if cols:  
            rows.append(cols)

    first_row = table.find("tr")
    headers = [th.get_text(strip=True) for th in first_row.find_all("th")]

    max_columns = max(len(row) for row in rows) if rows else 0
    if not headers or len(headers) != max_columns:
        headers = [f"Column_{i+1}" for i in range(max_columns)]

    return pd.DataFrame(rows, columns=headers)

def clean_energy_value(value):
    """Cleans energy values by removing 'mWh', commas, and converting to numeric."""
    if isinstance(value, str):
        # Remove 'mWh', commas, and spaces
        value = value.replace('mWh', '').replace(',', '').strip()
        # Remove any surrounding quotes
        value = value.strip('"')
        # Try to convert to float, return 0 if not possible
        try:
            return float(value)
        except ValueError:
            return 0
    return value


recent_usage = extract_table("Recent usage")
battery_usage = extract_table("Battery usage")
usage_history = extract_table("Usage history")
battery_capacity_history = extract_table("Battery capacity history")
battery_life_estimates = extract_table("Battery life estimates")

pd.DataFrame([system_info]).to_csv(dir_path.capitalize() + r"\battery-report\system_info.csv", index=False)
pd.DataFrame([battery_details]).to_csv(dir_path.capitalize() + r"\battery-report\battery_details.csv", index=False)

recent_usage.columns = [
    "START TIME",
    "STATE",
    "SOURCE",
    "CAPACITY REMAINING PERCENT",
    "CAPACITY REMAINING"
]

# Fix missing spaces between date and time
recent_usage["START TIME"] = recent_usage["START TIME"].astype(str).apply(
    lambda x: re.sub(r'(\d{4}-\d{2}-\d{2})(\d{2}:\d{2}:\d{2})', r'\1 \2', x)
)

# Apply the function
recent_usage["START TIME"] = fill_missing_dates(recent_usage["START TIME"])

# Convert to proper datetime format
recent_usage["START TIME"] = pd.to_datetime(recent_usage["START TIME"], errors="coerce")

# Split 'START TIME' into separate 'DATE' and 'TIME' columns
recent_usage["DATE"] = recent_usage["START TIME"].dt.date
recent_usage["TIME"] = recent_usage["START TIME"].dt.time

# Remove 'START TIME' and reorder columns
recent_usage = recent_usage.drop(columns=["START TIME"])
recent_usage = recent_usage[["DATE", "TIME"] + [col for col in recent_usage.columns if col not in ["DATE", "TIME"]]]
recent_usage["CAPACITY REMAINING"] = recent_usage["CAPACITY REMAINING"].apply(clean_energy_value)

recent_usage.to_csv(dir_path.capitalize() + r"\battery-report\recent_usage.csv", index=False)

battery_usage.columns = [
    "START TIME",
    "STATE",
    "DURATION",
    "ENERGY DRAINED PERCENT",
    "ENERGY DRAINED"
]
# Fix missing spaces between date and time
battery_usage["START TIME"] = battery_usage["START TIME"].astype(str).apply(
    lambda x: re.sub(r'(\d{4}-\d{2}-\d{2})(\d{2}:\d{2}:\d{2})', r'\1 \2', x)
)

# Apply the function
battery_usage["START TIME"] = fill_missing_dates(battery_usage["START TIME"])

# Convert to proper datetime format
battery_usage["START TIME"] = pd.to_datetime(battery_usage["START TIME"], errors="coerce")

# Split 'START TIME' into separate 'DATE' and 'TIME' columns
battery_usage["DATE"] = battery_usage["START TIME"].dt.date
battery_usage["TIME"] = battery_usage["START TIME"].dt.time

battery_usage = battery_usage.drop(columns=["START TIME"])
battery_usage = battery_usage[["DATE", "TIME"] + [col for col in battery_usage.columns if col not in ["DATE", "TIME"]]]
battery_usage["ENERGY DRAINED"] = battery_usage["ENERGY DRAINED"].apply(clean_energy_value)

battery_usage.to_csv(dir_path.capitalize() + r"\battery-report\battery_usage.csv", index=False)

usage_history.drop(usage_history.columns[3], axis=1, inplace=True)
usage_history.columns = [
    "PERIOD",
    "BATTERY DURATION ACTIVE",
    "BATTERY DURATION CONNECTED STANDBY",
    "AC DURATION ACTIVE",
    "AC DURATION CONNECTED STANDBY",
]
def clean_and_fix_period(df, period_column="PERIOD"):
    # Clean up the PERIOD column by removing extra newlines and spaces
    df[period_column] = df[period_column].str.replace(r"\s*\n+\s*", " ", regex=True).str.strip()

    # Identify rows where PERIOD has only one date
    single_date_rows = df[period_column].str.match(r"^\d{4}-\d{2}-\d{2}$", na=False)

    # Fill in missing end dates by using the next row's start date, if available
    for i in df[single_date_rows].index:
        if i + 1 in df.index:  # Ensure the next row exists
            next_date = df.loc[i + 1, period_column].split(" - ")[0]  # Get start date of next period
            df.loc[i, period_column] = f"{df.loc[i, period_column]} - {next_date}"

    # Recalculate the last index
    last_index = df.index[-1]

    # Extract the last start date from the PERIOD column (handling cases with ranges)
    last_date_str = df.loc[last_index, period_column].split(" - ")[0]  # Take only the first date

    # Function to manually increment a date
    def increment_date(date_str):
        year, month, day = map(int, date_str.split("-"))
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            days_in_month[1] = 29  # Leap year adjustment
        day += 1
        if day > days_in_month[month - 1]:
            day = 1
            month += 1
            if month > 12:
                month = 1
                year += 1
        return f"{year:04d}-{month:02d}-{day:02d}"

    # Compute the next day manually
    next_day_str = increment_date(last_date_str)

    # Update the last row with the calculated next day
    df.loc[last_index, period_column] = f"{last_date_str} - {next_day_str}"

    return df
usage_history = clean_and_fix_period(usage_history)
usage_history.to_csv(dir_path.capitalize() + r"\battery-report\usage_history.csv", index=False)

battery_capacity_history.columns = ["PERIOD", "FULL CHARGE CAPACITY", "DESIGN CAPACITY"]
battery_capacity_history = clean_and_fix_period(battery_capacity_history)
battery_capacity_history["FULL CHARGE CAPACITY"] = battery_capacity_history["FULL CHARGE CAPACITY"].apply(clean_energy_value)
battery_capacity_history["DESIGN CAPACITY"] = battery_capacity_history["DESIGN CAPACITY"].apply(clean_energy_value)


battery_capacity_history.to_csv(dir_path.capitalize() + r"\battery-report\battery_capacity_history.csv", index=False)

battery_life_estimates.drop(battery_life_estimates.columns[3], axis=1, inplace=True)
battery_life_estimates.columns = [
    "PERIOD",
    "AT FULL CHARGE ACTIVE",
    "AT FULL CONNECTED STANDBY",
    "AT DESIGN CAPACITY ACTIVE",
    "AT DESIGN CAPACITY CONNECTED STANDBY"
]
battery_life_estimates = clean_and_fix_period(battery_life_estimates)
battery_life_estimates["CONNECTED_STANDBY_TIME"], battery_life_estimates["CONNECTED_STANDBY_PERCENT"] = extract_time_percentage(
    battery_life_estimates["AT FULL CONNECTED STANDBY"]
)
battery_life_estimates["DESIGN_CONNECTED_STANDBY_TIME"], battery_life_estimates["DESIGN_CONNECTED_STANDBY_PERCENT"] = extract_time_percentage(
    battery_life_estimates["AT DESIGN CAPACITY CONNECTED STANDBY"]
)
battery_life_estimates.drop(['AT FULL CONNECTED STANDBY', 'AT DESIGN CAPACITY CONNECTED STANDBY'], axis=1, inplace=True)

# Reorder the columns as requested
new_column_order = [
    'PERIOD',
    'AT FULL CHARGE ACTIVE',
    'CONNECTED_STANDBY_TIME',
    'CONNECTED_STANDBY_PERCENT',
    'AT DESIGN CAPACITY ACTIVE',
    'DESIGN_CONNECTED_STANDBY_TIME',
    'DESIGN_CONNECTED_STANDBY_PERCENT'
]
battery_life_estimates = battery_life_estimates[new_column_order]

battery_life_estimates.to_csv(dir_path.capitalize() + r"\battery-report\battery_life_estimates.csv", index=False)

print("Extraction Complete! Data Saved as CSV Files.")
print(system_info)
print(battery_details)