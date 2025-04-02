import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Get the directory path
dir_path = os.path.dirname(os.path.abspath(__file__))

# Load dataset
recent_usage = pd.read_csv(os.path.join(dir_path, 'battery-report', 'recent_usage.csv'))

# Display the first few rows
print("Recent Usage:")
print(recent_usage.head())

# Visualization
plt.figure(figsize=(10, 6))
sns.lineplot(x='DATE', y='CAPACITY REMAINING', data=recent_usage)
plt.xlabel('Date')
plt.ylabel('Capacity Remaining')
plt.title('Recent Usage')
plt.xticks(rotation=45)
plt.show()