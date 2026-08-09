import pandas as pd
import numpy as np

# Load collected data
data = pd.read_csv("gyro_data.csv")

# Normalize sensor values (typically in rad/s)
data[['x_axis', 'y_axis', 'z_axis']] = (
    data[['x_axis', 'y_axis', 'z_axis']] - data[['x_axis', 'y_axis', 'z_axis']].mean()
) / data[['x_axis', 'y_axis', 'z_axis']].std()

# Create sliding windows for time-series features
window_size = 20
X, y = [], []
for i in range(len(data) - window_size):
    X.append(data.iloc[i:i+window_size][['x_axis', 'y_axis', 'z_axis']].values)
    y.append(data.iloc[i+window_size]['label'])

X = np.array(X)  # Shape: (samples, window_size, 3)
y = np.array(y)  # Labels
