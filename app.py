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
    st.write("Please create a report")
    wav_audio_data = st_audiorec()

    if wav_audio_data is not None:
        # display audio data as received on the backend
        st.audio(wav_audio_data, format="audio/wav")

    # INFO: by calling the function an instance of the audio recorder is created
    # INFO: once a recording is completed, audio data will be saved to wav_audio_data

    # Get user input
    text_input = st.text_input("Enter some text:")
    file_input = st.file_uploader("Upload an image:", type=["jpg", "png"])

    # taking photo with the camera functionality:
    # Initialize session state variables
    if "camera_enabled" not in st.session_state:
        st.session_state.camera_enabled = False
    if "img_file_buffer" not in st.session_state:
        st.session_state.img_file_buffer = None

    # Add enable/disable camera button
    if st.button("Enable/Disable Camera"):
        st.session_state.camera_enabled = not st.session_state.camera_enabled

    # Check if camera is enabled
    if st.session_state.camera_enabled:
        st.write("Taking picture...")
        img_file_buffer = st.camera_input("Take a picture")

        # If an image was taken, display its type
        if img_file_buffer is not None:
            st.session_state.img_file_buffer = img_file_buffer
            img = Image.open(img_file_buffer)
            # To convert PIL Image to numpy array:
            img_array = np.array(img)
            # Check the type of img_array:
            # Should output: <class 'numpy.ndarray'>
            st.write(type(img_array))
            # Check the shape of img_array:
            # Should output shape: (height, width, channels)
            st.write(img_array.shape)

    # Display saved image
    if st.session_state.img_file_buffer is not None:
        st.write("Saved image:")
        image = Image.open(st.session_state.img_file_buffer)
        st.image(image, caption="Saved image", use_column_width=True)

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
