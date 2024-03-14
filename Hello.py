# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
from moviepy.editor import concatenate_audioclips, AudioFileClip
from replicate.client import Client
from replicate import Client
from PyPDF2 import PdfReader
import tempfile
import PyPDF2 

import requests

LOGGER = get_logger(__name__)

def read_pdf(file):
    text = ""
    print("this is inside the function")
    pdf_reader = PdfReader(file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
        print("this is inside the for loop")
    return text

def split_text_into_words(text):
    words = text.split()
    return [words[i:i+40] for i in range(0, len(words), 40)]

def run():
    import replicate
    
    # Initialize session_state
    session_state = st.session_state
    
    st.set_page_config(
        page_title="2 SpeechTTS",
        page_icon="👋",
    )

    st.write("# Welcome to TTSModel 👋")
    genre = st.radio(
        "**How do you want to use 2_SpeechTTS**",
        ["Write Text", "Upload PDF",],
        captions = ["Enter Text to convert to speech", "Upload PDF file to convert to speech"],
        key="qe12"
    )

    if genre == 'Write Text':
        input_text = st.text_area("Please Enter Text to Convert to Speech", key="qw13")
        if st.button("Convert to Speech"):
            # Call function to convert input_text to speech
            # Authenticate replicate client
            replicate = replicate.Client(api_token='r8_FPd0TDjuTIaLK6pJ86sWou8rWBBD4oC1dzWt0')
            words = input_text.split()
            api_input_text = " ".join(words)

            output = replicate.run(
                "adirik/styletts2:989cb5ea6d2401314eb30685740cb9f6fd1c9001b8940659b406f952837ab5ac",
                input={
                    "beta": 0.7,
                    "seed": 0,
                    "text": api_input_text,
                    "alpha": 0.3,
                    "diffusion_steps": 10,
                    "embedding_scale": 1.5
                }
            )
            st.audio(output, format='audio/mp3', start_time=0)
            # Set session_state variable to trigger rerun
            session_state.button_triggered = True
            
    else: 
        file_up = st.file_uploader("Choose PDF File", type="pdf", key="qr")
        if st.button("Convert to Speech"):
            if file_up is not None:     
                print("where the magic happens")
                st.text("Uploaded successfully!")
                st.text("Converting PDF to audio...")
                text = read_pdf(file_up)
                st.write(text)

                # Split the passage into words
                words_list = split_text_into_words(text)
                # Create a list to store all the converted words
                #st.write("the following is words_list")
                #st.write(words_list)
                all_words = []

                # Display words in batches of 15 until all words are depleted
                # Display words in batches of 15 until all words are depleted
                replicate = replicate.Client(api_token='r8_FPd0TDjuTIaLK6pJ86sWou8rWBBD4oC1dzWt0')
                for batch in words_list:
                    batch = words_list.pop(0)
                    #st.write("the batch before extend on all words")
                    #st.write(batch)
                    
                    all_words.extend(batch)
                    #st.write("all_words extendend with batch")
                    #st.write(all_words)
                    api_input_text = ' '.join(map(str, all_words))  # Join all words, converting each to a string
                    #st.write(batch)
                    #print(batch)
                    
                    output = replicate.run(
                        "adirik/styletts2:989cb5ea6d2401314eb30685740cb9f6fd1c9001b8940659b406f952837ab5ac",
                        input={
                            "beta": 0.7,
                            "seed": 5,
                            "text": api_input_text,
                            "alpha": 0.3,
                            "diffusion_steps": 10,
                            "embedding_scale": 1.5
                        }
                    )
                    st.audio(output, format='audio/mp3', start_time=0)
                    #output
                    
            else:
                st.warning("Please upload a PDF file.")
                print(file_up)
            # Set session_state variable to trigger rerun
            session_state.button_triggered = True

    # Check if button has triggered and rerun if True
    if session_state.get('button_triggered'):
        st.rerun()
    

if __name__ == "__main__":
    run()
