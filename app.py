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
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors


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
    # Employee name
    employee_name = st.text_input("Employee Name:")

    # Location
    location = st.text_input("Location:")

    # Task
    task = st.text_input("Task:")

    # Task Finished
    task_finished = st.radio("Task Finished:", options=["Yes", "No"])

    # Date
    date = st.date_input("Date:")

    # Description
    description = []
    for i in range(2):
        description.append(st.text_input(f"Description {i+1}:"))

    # Media/Images
    #media_images = st.file_uploader("Media/Images:")

    # Generate PDF report using ReportLab
    c = canvas.Canvas("employee_report.pdf", pagesize=letter)
    # Set the font size and position of the title
    c.setFont("Helvetica-Bold", 16)
    title_x, title_y = 1*inch, 10.5*inch

    # Draw the title on the first page
    c.drawString(title_x, title_y, "Employee Report: Task Completion")
    # Employee Information
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 700, "Emplyee name:")
    c.setFont("Helvetica", 12)
    c.drawString(100, 680, "{employee_name}")
    c.drawString(100, 660, "Location:")
    c.drawString(100, 640, "{location}")
    
    # Task Information
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 620, "Task Information")
    c.setFont("Helvetica", 12)
    c.drawString(100, 600, "Task:")
    c.drawString(100, 580, "{task}")
    c.drawString(100, 560, "Date:")
    c.drawString(100, 540, "{date}")
    c.drawString(100, 520, "Description:")
    for i, text in enumerate(description):
        c.drawString(100, 500 - i * 20, f"{i+1}. {text}")
    c.showPage()
    c.save()

    # Stream generated PDF to user
    def download_report():
        with open("employee_report.pdf", "rb") as f:
            data = f.read()
        st.download_button(
            label="Download Report",
            data=data,
            file_name="employee_report.pdf",
            mime="application/pdf",
        )


    download_report()

if __name__ == "__main__":
    main()
