

from flask import Flask, render_template, request, jsonify
import openai
import random
import openai
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions

# Replace with your OpenAI API key
openai_api_key = "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"
openai.api_key = openai_api_key

# Initialize IBM Watson NLU with your credentials
ibm_watson_api_key = "tyTHkHJgT-AnY1zO7Sl0ReJz7HzP_NKtHPHkq5EcGI1h"
ibm_watson_service_url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/7f8bd212-8cc2-4bf2-a1e4-61ea4ca96bd7"
ibm_authenticator = IAMAuthenticator(ibm_watson_api_key)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=ibm_authenticator
)
natural_language_understanding.set_service_url(ibm_watson_service_url)

"""emotion_response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are providing a 1-sentence emotion that describes the following journal entry."},
        {"role": "user", "content": "I went to MIT and won second place in the hackathon. It was an amazing experience."},
    ]
)

generated_sentence = emotion_response['choices'][0]['message']['content']

# Analyze the emotion of the sentence using IBM Watson NLU
ibm_response = natural_language_understanding.analyze(
    text=generated_sentence,
    features=Features(emotion=EmotionOptions(targets=[generated_sentence]))
).get_result()

# Extract the dominant emotion and its score
emotion_scores = ibm_response['emotion']['document']
print(emotion_scores)
#dominant_emotion = max(emotion_scores, key=emotion_scores.get)

dominant_emotion = max(emotion_scores['emotion'], key=emotion_scores['emotion'].get)

print(f"Generated Sentence: {generated_sentence}")
print(f"Dominant Emotion: {dominant_emotion}")"""

# Initialize a dictionary to store emotions for 5 days




emotions_data = {
    "Day 1 - Morning": [],
    "Day 1 - Afternoon": [],
    "Day 1 - Evening": [],
    "Day 2 - Morning": [],
    "Day 2 - Afternoon": [],
    "Day 2 - Evening": [],
    "Day 3 - Morning": [],
    "Day 3 - Afternoon": [],
    "Day 3 - Evening": [],
    "Day 4 - Morning": [],
    "Day 4 - Afternoon": [],
    "Day 4 - Evening": [],
    "Day 5 - Morning": [],
    "Day 5 - Afternoon": [],
    "Day 5 - Evening": [],
}

# Define different messages for user role and time of the day
message_pools = [
    # Morning
    [{"role": "system", "content": "You give me a paragraph of description based on this."},
    {"role": "user", "content": "I went to MIT and won second place in the hackathon. It was an amazing experience. I felt so very happy and shouted with happiness. Everyone praised me so much and I felt so proud of myself"}],
    # Afternoon
     [{"role": "system", "content": "You give me a paragraph of description based on this"},
    {"role": "user", "content": "Surrounded by loved ones on my birthday, I felt an overwhelming sense of happiness that filled my heart with warmth and laughter because all my friends gave me gifts and we played a lot of games and had good food"}],
    # Afternoon
    [{"role": "system", "content": "You give me a paragraph of description based on this"},
    {"role": "user", "content": "I had a very bad break up with the person I loved the most and I feel so lonely because I miss that person very much and I want that person back in my life. I really miss the person very much. I am always thinking about this person"}],
    # Evening
    [{"role": "system", "content": "You give me a paragraph of description based on this."},
    {"role": "user", "content": "I really want to smash all the things in my room because I was feeling so very bad and my mood was so spoiled by someone in my office yellat at me. I was feeling very frustratedand did not know what I am supposed to do. This incident is a very bad experience for me and I regret all this"}]
]

# Loop through 5 days and 3 times of the day
for day in range(1, 6):
    for time in ["Morning", "Afternoon", "Evening"]:
        # Set the user content based on the time of the day
   

        message_pool = random.choice(message_pools)
        print(message_pool)

        # Select a random message from the pool
        #random_message = random.choice(message_pool)
        #print(random_message)

        # Generate a sentence using ChatGPT with the random message
        emotion_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=message_pool
        )

        generated_sentence = emotion_response['choices'][0]['message']['content']
        print("****")
        print(generated_sentence)

        # Analyze the emotion of the sentence using IBM Watson NLU
        ibm_response = natural_language_understanding.analyze(
            text=generated_sentence,
            features=Features(emotion=EmotionOptions(targets=[generated_sentence]))
        ).get_result()

        # Extract the dominant emotion and its score
        emotion_scores = ibm_response['emotion']['document']
        print(emotion_scores)
        print("*****")
       # dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        dominant_emotion = max(emotion_scores['emotion'], key=emotion_scores['emotion'].get)

        # Store the dominant emotion for the day and time
        emotions_data[f"Day {day} - {time}"].append(dominant_emotion)

# Print the emotions data
for day_time, emotions in emotions_data.items():
    print(f"{day_time}: {emotions}")

print(emotions_data)
