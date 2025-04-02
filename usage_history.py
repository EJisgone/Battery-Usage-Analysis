import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Get the directory path
dir_path = os.path.dirname(os.path.abspath(__file__))

# Load dataset
usage_history = pd.read_csv(os.path.join(dir_path, 'battery-report', 'usage_history.csv'))

# Display the first few rows
print("Usage History:")
print(usage_history.head())

# Visualization: Comparison of Battery Duration Active and AC Duration Active
plt.figure(figsize=(50, 30))
sns.lineplot(x='PERIOD', y='BATTERY DURATION ACTIVE', data=usage_history, label='Battery Duration Active')
sns.lineplot(x='PERIOD', y='AC DURATION ACTIVE', data=usage_history, label='AC Duration Active')
plt.xlabel('Period')
plt.ylabel('Duration')
plt.title('Comparison of Battery Duration Active and AC Duration Active')
plt.xticks(rotation=45)
plt.legend(title='Duration Type')
plt.show()