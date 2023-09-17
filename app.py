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
from datetime import date
import markdown
import pdfkit
import plotly.express as px
from translations import english, spanish, chinese

STT_API_KEY = "" #see discord
STT_URL = "" #see discord
openai.api_key = 0 #KEY HERE

config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

if "text" not in st.session_state:
    st.session_state.text = english

if "lang_changed" not in st.session_state:
    st.session_state.lang_changed = True

def question_response(prompt):
    question_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system",
            "content": st.session_state.text["prompt1"]},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7
    )

    return question_response['choices'][0]['message']['content']

def make_image_url(prompt):
    summary_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": st.session_state.text["prompt2"]},
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

st.title(st.session_state.text["name"])

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
if prompt := st.chat_input(st.session_state.text["greeting"]):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = question_response(prompt)
    # Display assistant response in chat message container

    with st.chat_message("assistant"):
        with st.spinner(st.session_state.text["think"]):
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

    st.header(st.session_state.text["options"])

    option = st.selectbox(
    st.session_state.text["select_language"],
    st.session_state.text["languages"])

    if option == "English":
        st.session_state.text = english
    elif option == "Spanish":
        st.session_state.text = spanish
    elif option == "Chinese":
        st.session_state.text = chinese


    audio = audiorecorder(st.session_state.text["record"], st.session_state.text["stop"])

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
        tts = gTTS(tts_text)
        tts.save('hello.mp3')
        st.audio('hello.mp3', format='audio/mp3', start_time=0)
        st.session_state.audio_output = False
        time.sleep(1)
        x, y = pyautogui.position()
        pyautogui.click(51, 503)
        pyautogui.moveTo(x, y)

    if st.button(st.session_state.text["pdf"]):
        pdf_content = "# Journal\n### " + date.today().strftime("%B %d, %Y")
        entrance= 1
        for mess in st.session_state.messages:
            if mess["role"] == "user":
                pdf_content += "\n#### " +str(entrance)+"\n" + mess["content"]
            elif mess["role"] == "assistant":
                pdf_content += "\n" + "![Alt text](image"+str(entrance)+".jpg)"
                pdf_content += "\n" + mess["content"] + "\n\n"
            entrance+=1

        print(pdf_content)
        html_content = markdown.markdown(pdf_content)
        with open("output.html", "w") as html_file:
            html_file.write(html_content)

        # Convert HTML to PDF
        #pdfkit.from_file("output.html", "output.pdf")
        pdf_options = {
            "page-size": "A4",
            "margin-top": "10mm",
            "margin-right": "5mm",
            "margin-bottom": "10mm",
            "margin-left": "5mm",
            "enable-local-file-access": ""
        }

        # Convert HTML to PDF
        pdfkit.from_file("output.html", "output.pdf", options=pdf_options, configuration=config)

    st.subheader(st.session_state.text["Vibe"])
    
    fig= px.pie(values=[43, 17, 31, 9], names=['Happy', 'Sad', 'Surprise', 'Angry'])
    fig.update_layout(
        legend=dict(
            yanchor="top",
            y=0.001,
            xanchor="left",
            x=0.01,
            bgcolor=None
        )
    )
    st.plotly_chart(fig, use_container_width=True)
        
