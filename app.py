import streamlit as st
from audiorecorder import audiorecorder
import pyperclip
import pyautogui
from PIL import Image
import io
import requests
import openai
from gtts import gTTS
import time

STT_API_KEY = "" #see discord
STT_URL = "" #see discord
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

if "images" not in st.session_state:
    st.session_state.images = 0

if "audio_output" not in st.session_state:
    st.session_state.audio_output = False

# Display chat messages from history on app rerun

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown(message["content"])
            st.image(Image.open(message["image"]))
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

    with st.chat_message("assistant"):
        with st.spinner('Let me cook...'):
            image_url = make_image_url(prompt)
            image= load_pil_image_from_link(image_url)
            st.session_state.images= st.session_state.images+1
            image_name= "image"+str(st.session_state.images)+".jpg"
            image.save(image_name)
            st.image(image)
            st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response, "image": image_name})
    st.session_state.audio_output = True


with st.sidebar:
    audio = audiorecorder("Click to record", "Click to stop recording")

    if st.session_state.duration!= audio.duration_seconds:

        audio.export("audio.flac", format="flac")
        headers = {"Content-Type": "audio/flac"}
        with open("audio.flac", "rb") as f:
            with st.spinner('Wait for it...'):
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

    if st.session_state.audio_output:
        tts_text = st.session_state.messages[-1]["content"]
        print(tts_text)
        tts = gTTS(tts_text)
        tts.save('hello.mp3')

        st.audio('hello.mp3', format='audio/mp3', start_time=0)
        st.session_state.audio_output = False
        time.sleep(0.5)
        x, y = pyautogui.position()
        pyautogui.click(56, 331)
        pyautogui.moveTo(x, y)
