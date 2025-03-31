import matplotlib

matplotlib.use('TkAgg')  # Switch the backend to TkAgg

import psutil
import time
import matplotlib.pyplot as plt

# Lists to store CPU and Memory usage
cpu_usage = []
memory_usage = []
timestamps = []

# Set the duration to monitor (in seconds)
duration = 5  # Monitor for 1 minute
interval = 0.05  # Check every 1 second

start_time = time.time()

# Collect data for the specified duration
while time.time() - start_time < duration:
    timestamp = time.time() - start_time
    cpu_percent = psutil.cpu_percent(interval=interval)
    memory_percent = psutil.virtual_memory().percent

    # Store the data
    cpu_usage.append(cpu_percent)
    memory_usage.append(memory_percent)
    timestamps.append(timestamp)

    print(f"Time: {timestamp:.2f}s - CPU Usage: {cpu_percent}% - Memory Usage: {memory_percent}%")

# Plotting the data
plt.figure(figsize=(10, 5))

# Plot CPU usage
plt.subplot(2, 1, 1)
plt.plot(timestamps, cpu_usage, label="CPU Usage", color='r')
plt.xlabel('Time (s)')
plt.ylabel('CPU Usage (%)')
plt.title('CPU Usage Over Time')
plt.grid(True)

# Plot Memory usage
plt.subplot(2, 1, 2)
plt.plot(timestamps, memory_usage, label="Memory Usage", color='b')
plt.xlabel('Time (s)')
plt.ylabel('Memory Usage (%)')
plt.title('Memory Usage Over Time')
plt.grid(True)

# Show the plots
plt.tight_layout()
plt.show()
