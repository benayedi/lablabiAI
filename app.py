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
import speech2text as s2t
import wave 

def main():
    st.title("Breaking down barriers")
    st.write("Please create a report")
    with open('output.wav', 'wb') as w:
        
        w.write(st_audiorec())
        w.close()
    speech= s2t.speech_to_text("fr-FR", "output.wav")
    st.write(speech)
    translatedspeech= s2t.translate_text(speech,"fr")
    st.write(translatedspeech)
    st.write(s2t.answer_question("when were the tasks done? give me the date in dd/mm/yyyy format",translatedspeech))
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

    pdf = canvas.Canvas("report.pdf")
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, "Report")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 700, "Emplyee name:")
    pdf.drawString(100, 680, "Location:")
    pdf.drawString(100, 660, "Task:")
    pdf.drawString(100, 640, "Task finished:")
    pdf.drawString(100, 620, "Date:")
    pdf.drawString(100, 600, "Description:")
    pdf.drawString(100, 580, "Image:")
    pdf.drawString(120, 560, text_input)
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
            mime="application/pdf",
        )

    download_report()


if __name__ == "__main__":
    main()