import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

file_path = 'paracetamol_consumption_table.csv'
data = pd.read_csv(file_path)
print("Dataset Preview:")
print(data.head())
if 'Month' in data.columns and 'Year' in data.columns:
    data['Date'] = pd.to_datetime(data['Year'].astype(str) + '-' + data['Month'].astype(str))
else:
    data['Date'] = pd.to_datetime(data['Date'].astype(str))

fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlabel('Date')
ax.set_ylabel('Paracetamol Consumption')
ax.set_title('Paracetamol Consumption Over Time')
ax.grid(True)

line, = ax.plot([], [], marker='o', linestyle='-', color='b', label='Paracetamol Consumption')
ax.legend(loc='best')

def init():
    line.set_data([], [])
    return line,

def update(frame):
    x = data['Date'][:frame]
    y = data['Paracetamol_Consumption'][:frame]
    line.set_data(x, y)
    ax.relim()
    ax.autoscale_view()
    return line,

ani = FuncAnimation(fig, update, frames=len(data), init_func=init, blit=True, interval=200)

plt.show()
