import streamlit as st
import tempfile
from PIL import Image
import os
import base64
import numpy as np
from io import BytesIO
import streamlit.components.v1 as components
from st_custom_components import st_audiorec


def main():
    st.title("Breaking down barriers")
    st.write("Welcome to my simple web app!")
    wav_audio_data = st_audiorec()

    if wav_audio_data is not None:
        # display audio data as received on the backend
        st.audio(wav_audio_data, format="audio/wav")

    # INFO: by calling the function an instance of the audio recorder is created
    # INFO: once a recording is completed, audio data will be saved to wav_audio_data

    # Get user input
    text_input = st.text_input("Enter some text:")
    file_input = st.file_uploader("Upload an image:", type=["jpg", "png"])
    camera_input = st.button("Take a picture")

    # Handle camera input
    if camera_input:
        st.write("Taking picture...")
        image = st.camera_input(label="Click the camera button to take a picture")
        if image is not None:
            st.image(image, caption="Taken picture", use_column_width=True)

    # Handle file upload
    if file_input is not None:
        st.write("Image uploaded!")
        image = Image.open(file_input)
        st.image(image, caption="Uploaded image", use_column_width=True)

    # Show user input
    if text_input:
        st.write("You entered:", text_input)


if __name__ == "__main__":
    main()

