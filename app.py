import streamlit as st
import tempfile
from audio_recorder_streamlit import audio_recorder
from PIL import Image
import os
import base64


def main():
    st.title("Simple Web App")
    st.write("Welcome to my simple web app!")

    # Get user input
    text_input = st.text_input("Enter some text:")
    file_input = st.file_uploader("Upload an image:", type=["jpg", "png"])
    voice_input = st.button("Record voice note")
    camera_input = st.button("Take a picture")

    # Handle voice note recording
    if voice_input:
        st.write("Recording voice note...")
        audio_bytes = audio_recorder()
        if audio_bytes:
            # Save the voice note to a file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
                fp.write(audio_bytes)
                st.write(f"Voice note saved to {fp.name}")

                # Display the voice note playback button
                play_button = st.audio(audio_bytes, format="audio/wav")

                # Allow the user to download the voice note file
                download_button = st.download_button(
                    label="Download voice note",
                    data=audio_bytes,
                    file_name=os.path.basename(fp.name),
                    mime="audio/wav",
                )

    # Handle camera input
    if camera_input:
        st.write("Taking picture...")
        image = take_picture()
        st.image(image, caption="Taken picture", use_column_width=True)

    # Handle file upload
    if file_input is not None:
        st.write("Image uploaded!")
        image = Image.open(file_input)
        st.image(image, caption="Uploaded image", use_column_width=True)

    # Show user input
    if text_input:
        st.write("You entered:", text_input)


def take_picture():
    # TODO: Implement this function to take a picture using the user's camera and return the image
    pass


if __name__=='__main__':
    main()