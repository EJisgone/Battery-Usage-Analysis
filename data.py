import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Get the directory path
dir_path = os.path.dirname(os.path.abspath(__file__))

# Load datasets
battery_capacity_history = pd.read_csv(os.path.join(dir_path, 'battery-report', 'battery_capacity_history.csv'))
battery_details = pd.read_csv(os.path.join(dir_path, 'battery-report', 'battery_details.csv'))
battery_life_estimates = pd.read_csv(os.path.join(dir_path, 'battery-report', 'battery_life_estimates.csv'))
battery_usage = pd.read_csv(os.path.join(dir_path, 'battery-report', 'battery_usage.csv'))
recent_usage = pd.read_csv(os.path.join(dir_path, 'battery-report', 'recent_usage.csv'))
system_info = pd.read_csv(os.path.join(dir_path, 'battery-report', 'system_info.csv'))
usage_history = pd.read_csv(os.path.join(dir_path, 'battery-report', 'usage_history.csv'))

# Display the first few rows of each dataset
print("Battery Capacity History:")
print(battery_capacity_history.head())
print("\nBattery Details:")
print(battery_details)
print("\nBattery Life Estimates:")
print(battery_life_estimates.head())
print("\nBattery Usage:")
print(battery_usage.head())
print("\nRecent Usage:")
print(recent_usage.head())
print("\nSystem Info:")
print(system_info)
print("\nUsage History:")
print(usage_history.head())

# Visualize Battery Capacity History
plt.figure(figsize=(10, 6))
plt.plot(battery_capacity_history['PERIOD'], battery_capacity_history['FULL CHARGE CAPACITY'])
plt.xlabel('Period')
plt.ylabel('Full Charge Capacity')
plt.title('Battery Capacity History')
plt.xticks(rotation=45)
plt.show()

# Visualize Battery Life Estimates
plt.figure(figsize=(10, 6))
sns.barplot(x='PERIOD', y='AT FULL CHARGE ACTIVE', data=battery_life_estimates)
plt.xlabel('Period')
plt.ylabel('Life Estimate at Full Charge')
plt.title('Battery Life Estimates')
plt.xticks(rotation=45)
plt.show()

# Visualize Battery Usage
plt.figure(figsize=(10, 6))
sns.lineplot(x='DATE', y='ENERGY DRAINED', data=battery_usage)
plt.xlabel('Date')
plt.ylabel('Energy Drained')
plt.title('Battery Usage')
plt.xticks(rotation=45)
plt.show()

# Visualize Recent Usage
plt.figure(figsize=(10, 6))
sns.lineplot(x='DATE', y='CAPACITY REMAINING', data=recent_usage)
plt.xlabel('Date')
plt.ylabel('Capacity Remaining')
plt.title('Recent Usage')
plt.xticks(rotation=45)
plt.show()

# Visualize Usage History
plt.figure(figsize=(10, 6))
sns.lineplot(x='PERIOD', y='BATTERY DURATION ACTIVE', data=usage_history)
plt.xlabel('Period')
plt.ylabel('Battery Duration Active')
plt.title('Usage History')
plt.xticks(rotation=45)
plt.show()