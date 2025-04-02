import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = dir_path.capitalize() + r"\battery-report\battery_capacity_history.csv"
data = pd.read_csv(file_path)

# Data Cleaning
data['START_DATE'] = data['PERIOD'].apply(lambda x: x.split(' - ')[0])  # Extract start date
data['START_DATE'] = pd.to_datetime(data['START_DATE'])  # Convert to datetime

data['FULL CHARGE CAPACITY'] = data['FULL CHARGE CAPACITY'].str.replace(',', '').str.replace(' mWh', '').astype(int)

# Set Seaborn style for aesthetics
sns.set_theme(style="darkgrid")

# Visualization
plt.figure(figsize=(12, 7))
sns.lineplot(x='START_DATE', y='FULL CHARGE CAPACITY', data=data, label='Full Charge Capacity', marker='o', linewidth=2.5, color='#4CAF50')


# Enhancements
plt.title('Battery Capacity Trends Over Time', fontsize=18, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Capacity (mWh)', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(rotation=45)
plt.tight_layout()

# Display the graph
plt.show()
