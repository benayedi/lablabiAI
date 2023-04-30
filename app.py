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
    
    q_name = s2t.answer_question("what is the name of the speaker?", translatedspeech)
    q_location = s2t.answer_question("where was the task done?", translatedspeech) 
    q_task_name = s2t.answer_question("what is the name of the task?", translatedspeech) 
    q_task_id = s2t.answer_question("what is the task id?", translatedspeech)
    q_finished  = s2t.answer_question("was the task finished successfully?", translatedspeech)
    q_process = s2t.answer_question("what is the process of the task?", translatedspeech)    
    
    st.write(q_task_name)
    # st.write("what is the name of the speaker?")
    # st.write(q_name)
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
    employee_name = q_name

    # Location
    location = q_location

    # Task
    task = q_task_name

    # Task Finished
    task_finished = q_finished

    # Date
    date = st.date_input("Date:")

    # Description
    description = q_process

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
    c.drawString(100, 680, "{}".format(q_name))
    c.drawString(100, 660, "Location:")
    c.drawString(100, 640, "{}".format(q_location))
    
    # Task Information
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 620, "Task Information")
    c.setFont("Helvetica", 12)
    c.drawString(100, 600, "Task:")
    c.drawString(100, 580, "{}".format(q_task_name))

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