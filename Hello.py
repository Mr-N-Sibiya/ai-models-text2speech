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
import streamlit_authenticator as stauch
import tempfile

import requests

LOGGER = get_logger(__name__)










def run():
    import replicate
    

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
        input_text=[]
        input_text = st.text_area("Please Enter Text to Convert to Speech", key="qw13")
        if st.button("Convert to Speech"):
            # Call function to convert input_text to speech
            pass
            # Authenticate replicate client
            replicate = replicate.Client(api_token='r8_FPd0TDjuTIaLK6pJ86sWou8rWBBD4oC1dzWt0')
            words=input_text.split()
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
            print(output)




    else: 
        file_up = st.file_uploader("Choose PDF File", type="pdf", key="qr")
        if st.button("Convert to Speech"):
            if file_up is not None:
                # Call function to convert file_up to speech
                pass
                print("code for uploading file")
            else:
                st.warning("Please upload a PDF file.")
                print(file_up)

    




if __name__ == "__main__":
    run()



