import streamlit as st
from audiorecorder import audiorecorder
import pyperclip
import pyautogui
from PIL import Image
import io
import requests

image_test_link= "https://cdn.discordapp.com/attachments/1152649972517453844/1152765018807468092/img-LNt9zeZT68IiNZXeGcAZb56O.png"

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

    response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
        st.image(load_pil_image_from_link(image_test_link))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response, "image": image_test_link})

with st.sidebar:
    audio = audiorecorder("Click to record", "Click to stop recording")

    if st.session_state.duration!= audio.duration_seconds:
        x, y = pyautogui.position()
        pyautogui.click(758, 912)
        pyautogui.moveTo(x, y)
        pyperclip.copy("text_to_copy")
        pyautogui.press('end')
        pyautogui.press('space')
        pyautogui.hotkey('ctrl', 'v')
        st.session_state.duration = audio.duration_seconds
