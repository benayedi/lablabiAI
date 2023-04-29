import streamlit as st
import tempfile
from PIL import Image
import os
import base64
import numpy as np
from io import BytesIO
import streamlit.components.v1 as components
from st_custom_components import st_audiorec
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileMerger

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

    pdf = canvas.Canvas("report.pdf")
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, "Report")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 700, "Section 1")
    pdf.drawString(100, 680, "Description:")
    pdf.drawString(120, 660, text_input)
    pdf.showPage()
    pdf.save()

   
    # Stream generated PDF to user
    def download_report():
        with open("report.pdf", "rb") as f:
            data = f.read()
        st.download_button(
            label="Download Report",
            data=data,
            file_name="report.pdf",
            mime="application/pdf"
    )

    download_report()
if __name__ == "__main__":
    main()

