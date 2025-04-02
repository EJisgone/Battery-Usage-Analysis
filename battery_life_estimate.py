import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Get the directory path
dir_path = os.path.dirname(os.path.abspath(__file__))

# Load dataset
battery_life_estimates = pd.read_csv(os.path.join(dir_path, 'battery-report', 'battery_life_estimates.csv'))

# Visualization
plt.figure(figsize=(40, 25))
sns.barplot(x='PERIOD', y='AT FULL CHARGE ACTIVE', data=battery_life_estimates)
plt.xlabel('Period')
plt.ylabel('Life Estimate at Full Charge')
plt.title('Battery Life Estimates')
plt.xticks(rotation=45)
plt.show()