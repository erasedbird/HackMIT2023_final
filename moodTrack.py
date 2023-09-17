import matplotlib.pyplot as plt

# Emotions data
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

# Prepare data for plotting
days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]
morning_emotions = []
afternoon_emotions = []
evening_emotions = []

for day in days:
    morning_emotions.append(emotions_data[f"{day} - Morning"][0])
    afternoon_emotions.append(emotions_data[f"{day} - Afternoon"][0])
    evening_emotions.append(emotions_data[f"{day} - Evening"][0])

# Emotion mapping for colors (you can customize this)
emotion_colors = {
    'anger': 'red',
    'sadness': 'blue',
    'fear': 'green',
    'disgust': 'yellow',
    'joy': 'orange'
    
}

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(days, morning_emotions, marker='o', label='Morning', color='orange')
plt.plot(days, afternoon_emotions, marker='o', label='Afternoon', color='green')
plt.plot(days, evening_emotions, marker='o', label='Evening', color='purple')

# Customize plot
plt.title('Mood Over 5 Days')
plt.xlabel('Days')
plt.ylabel('Emotion')
plt.legend(loc='upper right')
plt.grid(True)

# Show the plot
plt.show()
