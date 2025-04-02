import os
import pandas as pd
import matplotlib.pyplot as plt

# Get the directory path
dir_path = os.path.dirname(os.path.abspath(__file__))

# Load dataset
battery_capacity_history = pd.read_csv(os.path.join(dir_path, 'battery-report', 'battery_capacity_history.csv'))

# Visualization
plt.figure(figsize=(20, 6))
plt.plot(battery_capacity_history['PERIOD'], battery_capacity_history['FULL CHARGE CAPACITY'])
plt.xlabel('Period')
plt.ylabel('Full Charge Capacity')
plt.title('Battery Capacity History')
plt.xticks(rotation=45)
plt.show()