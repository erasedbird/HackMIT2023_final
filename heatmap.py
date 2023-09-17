import matplotlib.pyplot as plt
import numpy as np

# Define your emotions data
emotions_data = {
    "Day 1 - Morning": ['joy'],
    "Day 1 - Afternoon": ['sadness'],
    "Day 1 - Evening": ['anger'],
    "Day 2 - Morning": ['fear'],
    "Day 2 - Afternoon": ['disgust'],
    "Day 2 - Evening": ['sadness'],
    "Day 3 - Morning": ['joy'],
    "Day 3 - Afternoon": ['sadness'],
    "Day 3 - Evening": ['fear'],
    "Day 4 - Morning": ['anger'],
    "Day 4 - Afternoon": ['joy'],
    "Day 4 - Evening": ['anger'],
    "Day 5 - Morning": ['joy'],
    "Day 5 - Afternoon": ['anger'],
    "Day 5 - Evening": ['disgust']
}

# Define emotions mapping for colors
emotions_mapping = {
    'joy': 1,
    'sadness': 2,
    'anger': 3,
    'fear': 4,
    'disgust': 5
}

# Create a matrix to represent the heatmap
heatmap_matrix = np.zeros((5, 3))

for day in range(1, 6):
    for time_idx, time in enumerate(["Morning", "Afternoon", "Evening"]):
        key = f"Day {day} - {time}"
        emotion = emotions_data[key][0]
        heatmap_matrix[day - 1, time_idx] = emotions_mapping[emotion]

# Create a heatmap
plt.figure(figsize=(8, 6))
plt.imshow(heatmap_matrix, cmap='coolwarm', aspect='auto')

# Customize the heatmap
plt.colorbar(label='Emotion Level')
plt.title('Mood Heatmap Over 5 Days')
plt.xticks(np.arange(3), ["Morning", "Afternoon", "Evening"])
plt.yticks(np.arange(5), ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"])

# Display the plot
plt.show()
