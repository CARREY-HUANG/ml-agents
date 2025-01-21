import pandas as pd
import matplotlib.pyplot as plt

# Input file paths
marker_table = pd.read_csv('/Users/Carrey/Downloads/profile_withData/SoccerTwosIncreasedLR/higher_learning_rate_marker.csv', sep=';')
frame_table = pd.read_csv('/Users/Carrey/Downloads/profile_withData/SoccerTwosIncreasedLR/higher_learning_rate_frame.csv', sep=';')

# Output directory
output_dir = '/Users/Carrey/Downloads/no1'

# Clean column names
marker_table.columns = marker_table.columns.str.strip()
frame_table.columns = frame_table.columns.str.strip()

# Analyze marker data
top_markers = marker_table.sort_values(by='Mean Time', ascending=False).head(5)

# Display top 5 markers
print("Top 5 Markers by Mean Time:")
print(top_markers[['Name', 'Mean Time', 'Median Time', 'Count Total']])

# Generate bar chart for top 5 markers
plt.figure(figsize=(10, 6))
plt.bar(top_markers['Name'], top_markers['Mean Time'], color='orange')
plt.title('Top 5 Markers by Mean Time')
plt.xlabel('Marker Name')
plt.ylabel('Mean Time (ms)')
plt.xticks(rotation=10, ha='right')
plt.tight_layout()
plt.savefig(f'{output_dir}/top_5_markers.png')
plt.show()

# Frame time analysis
mean_frame_time = frame_table['Frame Time (ms)'].mean()
std_frame_time = frame_table['Frame Time (ms)'].std()
max_frame_time = frame_table['Frame Time (ms)'].max()
min_frame_time = frame_table['Frame Time (ms)'].min()

print("\nFrame Time Statistics:")
print(f"Mean Frame Time: {mean_frame_time:.2f} ms")
print(f"Standard Deviation: {std_frame_time:.2f} ms")
print(f"Max Frame Time: {max_frame_time:.2f} ms")
print(f"Min Frame Time: {min_frame_time:.2f} ms")

plt.figure(figsize=(10, 6))
plt.plot(frame_table['Frame Index'], frame_table['Frame Time (ms)'], color='blue')
plt.title('Frame Time Trend Over Frames')
plt.xlabel('Frame Index')
plt.ylabel('Frame Time (ms)')
plt.axhline(mean_frame_time, color='red', linestyle='--', label='Mean Frame Time')
plt.ylim(0, mean_frame_time * 2)
plt.legend()
plt.tight_layout()
plt.savefig(f'{output_dir}/frame_time_trend.png')
plt.show()

# Identify spike frame
max_frame = frame_table.loc[frame_table['Frame Time (ms)'].idxmax()]
print(f"Spike Frame: Index {max_frame['Frame Index']}, Time {max_frame['Frame Time (ms)']} ms")

# Analyze marker contributions
marker_contributions = marker_table.groupby('Name').agg({
    'Median Time': 'mean',
    'Min Time': 'mean',
    'Max Time': 'mean',
    'Total Time': 'sum',
    'Mean Time': 'mean',
    'Count Total': 'sum'
}).sort_values(by='Total Time', ascending=False)

top_contributors = marker_contributions.head(5)
print("\nTop Marker Contributors:")
print(top_contributors)

plt.figure(figsize=(12, 6))
top_contributors[['Median Time', 'Min Time', 'Max Time', 'Total Time', 'Mean Time']].plot(
    kind='bar',
    figsize=(12, 6),
    stacked=False,
    colormap='viridis'
)

plt.title('Top Marker Contributions by Key Metrics')
plt.xlabel('Marker Name')
plt.ylabel('Time (ms)')
plt.xticks(rotation=10, ha='right')
plt.tight_layout()
plt.savefig(f'{output_dir}/top_marker_contributions.png')
plt.show()

# Analyze GC.Collect markers (garbage collection)
gc_data = marker_table[marker_table['Name'] == 'GC.Collect']

if not gc_data.empty:
    gc_total_time = gc_data['Total Time'].sum()
    gc_mean_time = gc_data['Mean Time'].mean()
    gc_count = gc_data['Count Total'].sum()

    print(f"\nGC.Collect Analysis:")
    print(f"Total Time: {gc_total_time:.2f} ms")
    print(f"Mean Time: {gc_mean_time:.2f} ms")
    print(f"Total Count: {gc_count}")

    # Visualize garbage collection trends
    plt.figure(figsize=(10, 6))
    plt.bar(gc_data['Name'], gc_data['Total Time'], color='purple')
    plt.title('Garbage Collection Total Time')
    plt.xlabel('GC Marker')
    plt.ylabel('Total Time (ms)')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/gc_collect.png')
    plt.show()
else:
    print("No GC.Collect data found.")

# Combine frame time stats and marker contributions into a summary CSV
summary = {
    'Metric': ['Mean Frame Time', 'Std Frame Time', 'Max Frame Time', 'Min Frame Time'],
    'Value (ms)': [mean_frame_time, std_frame_time, max_frame_time, min_frame_time]
}
summary_df = pd.DataFrame(summary)

summary_df.to_csv(f'{output_dir}/performance_summary.csv', index=False)
marker_contributions.to_csv(f'{output_dir}/marker_contributions.csv')

print("\nPerformance summary saved as 'performance_summary.csv'")
print("Marker contributions saved as 'marker_contributions.csv'")
