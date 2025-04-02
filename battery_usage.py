import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Get the directory path
dir_path = os.path.dirname(os.path.abspath(__file__))

# Load dataset
battery_usage = pd.read_csv(os.path.join(dir_path, 'battery-report', 'battery_usage.csv'))

# Display the first few rows
print("Battery Usage:")
print(battery_usage.head())

# Visualization
plt.figure(figsize=(10, 6))
sns.lineplot(x='DATE', y='ENERGY DRAINED', data=battery_usage)
plt.xlabel('Date')
plt.ylabel('Energy Drained')
plt.title('Battery Usage')
plt.xticks(rotation=45)
plt.show()