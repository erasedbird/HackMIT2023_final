import streamlit as st
from audiorecorder import audiorecorder
import pyperclip
import pyautogui
from PIL import Image
import io
import requests
import openai

STT_API_KEY = "" #see discord
STT_URL = "" #see discord

image_test_link= "https://cdn.discordapp.com/attachments/1152649972517453844/1152765018807468092/img-LNt9zeZT68IiNZXeGcAZb56O.png"

openai.api_key = 0 #KEY HERE

def question_response(prompt):
    question_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "You are providing a reflective question less than 15 words on the following journal entry."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7
    )

    return question_response['choices'][0]['message']['content']

def make_image_url(prompt):
    summary_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are providing 5 words summarizing the following journal entry."},
            {"role": "user", "content": prompt},
        ]
    )

    summary = summary_response['choices'][0]['message']['content']

    response = openai.Image.create(
        prompt=summary + " abstract painting",
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']

    return image_url

def load_pil_image_from_link(image_url):
    response = requests.get(image_url)
    image_data = response.content
    image_file = io.BytesIO(image_data)
    image = Image.open(image_file)
    return image

st.write('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)

st.title("Reflexion Buddy")

if "duration" not in st.session_state:
    st.session_state.duration = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown(message["content"])
            st.image(load_pil_image_from_link(message["image"]))
        else:
            st.markdown(message["content"])
    

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = question_response(prompt)
    # Display assistant response in chat message container

    image_url = make_image_url(prompt)
    with st.chat_message("assistant"):
        st.markdown(response)
        st.image(load_pil_image_from_link(image_url))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response, "image": image_test_link})

with st.sidebar:
    audio = audiorecorder("Click to record", "Click to stop recording")

    if st.session_state.duration!= audio.duration_seconds:

        audio.export("audio.flac", format="flac")
        headers = {"Content-Type": "audio/flac"}
        with open("audio.flac", "rb") as f:
            response = requests.post(STT_URL, auth=("apikey", STT_API_KEY), headers=headers, files={'audio.flac': f})
            response_json = response.json()
            if response_json["results"]:
                response_text = response_json["results"][0]["alternatives"][0]["transcript"]
            else:
                response_text = "No audio detected"

        x, y = pyautogui.position()
        pyautogui.click(758, 912)
        pyautogui.moveTo(x, y)
        pyperclip.copy(response_text)
        pyautogui.press('end')
        pyautogui.press('space')
        pyautogui.hotkey('ctrl', 'v')
        st.session_state.duration = audio.duration_seconds
