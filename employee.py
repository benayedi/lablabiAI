import streamlit as st
from PIL import Image
import os
import base64
import numpy as np
from io import BytesIO
import streamlit.components.v1 as components
from st_custom_components import st_audiorec
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileMerger


def employee_page(username):
    st.title(f"Employee Page ({username})")
    st.write("Please create a report")

    # Get user input
    text_input = st.text_input("Enter some text:")
    file_input = st.file_uploader("Upload an image:", type=["jpg", "png"])

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

    # Generate report PDF
    pdf = canvas.Canvas("report.pdf")
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, "Report")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 700, "Employee name:")
    pdf.drawString(100, 680, "Location:")
    pdf.drawString(100, 660, "Task:")
    pdf.drawString(100, 640, "Task finished:")
    pdf.drawString(100, 620, "Date:")
    pdf.drawString(100, 600, "Description:")
    pdf.drawString(100, 580, "Image:")
    pdf.drawString(120, 560, username)
    pdf.showPage()
    pdf.save()

    # Display audio recording component
    wav_audio_data = st_audiorec()

    if wav_audio_data is not None:
        # Display audio data as received on the backend
        st.audio(wav_audio_data, format="audio/wav")

        # Merge audio with report PDF
        merger = PdfFileMerger()
        with open("report.pdf", "rb") as f:
            pdf_data = BytesIO(f.read())
        merger.append(pdf_data)
        audio_data = BytesIO(wav_audio_data)
        merger.append(audio_data)
        merged_file_name = "report_with_audio.pdf"
        merger.write(merged_file_name)

        # Display download button for report with audio
        def download_report():
            with open(merged_file_name, "rb") as f:
                data = f.read()
            st.download_button(
                label="Download Report with Audio",
                data=data,
                file_name=merged_file_name,
                mime="application/pdf",
            )

        st.button("Generate Report with Audio", on_click=download_report)
