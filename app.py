import io
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
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

def main():
    st.title("Breaking down barriers")
    st.write("Please create a report")
    with open('output.wav', 'wb') as w:
        af =st_audiorec()
        h= af is not None
        if h:
            w.write(af)
        w.close()
        if not h:
            return
        speech= s2t.speech_to_text("fr-FR", "output.wav")
        st.write(speech)

    translatedspeech= s2t.translate_text(speech,"fr")
    
    st.write(translatedspeech)
    q_name = s2t.answer_question("what is the name of the speaker?", translatedspeech)
    q_employer_id = s2t.answer_question("what is the speaker id?", translatedspeech)
    q_location = s2t.answer_question("where was the task done?", translatedspeech)
    q_date = s2t.answer_question("when was the task done?", translatedspeech) 
    q_task_name = s2t.answer_question("what is the name of the task?", translatedspeech) 
    q_task_id = s2t.answer_question("what is the task id?", translatedspeech)
    q_finished  = s2t.answer_question("was the task finished successfully?", translatedspeech)
    q_process = s2t.answer_question("what is the process of the task?", translatedspeech)    
    
    # INFO: by calling the function an instance of the audio recorder is created
    # INFO: once a recording is completed, audio data will be saved to wav_audio_data

    # Get user input
    #text_input = st.text_input("Enter some text:")
    
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
        image_bytes = img_file_buffer.read()
        st.write(s2t.analyze_image(image_bytes))

    # Display saved image
    if st.session_state.img_file_buffer is not None:
        st.write("Saved image:")
        image = Image.open(st.session_state.img_file_buffer)
        st.image(image, caption="Saved image", use_column_width=True)

    # Handle file upload
    if file_input is not None:
        st.write("Image uploaded!")
        image = Image.open(file_input)
        with io.BytesIO() as output:
            image.save(output, format= image.format)
            image_bytes = output.getvalue()
        st.write(s2t.analyze_image(image_bytes))
        st.image(image, caption="Uploaded image", use_column_width=True)


    # Date
    date = st.date_input("Date:")


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
    c.drawString(100, 700, "Employee Information:")
    c.setFont("Helvetica", 12)
    c.drawString(100, 680, "Name:")
    c.drawString(100, 660, "{}".format(q_name))
    c.drawString(100, 640, "Employee ID:")
    c.drawString(100, 620, "{}".format(q_employer_id))
    c.drawString(100, 600, "Location:")
    c.drawString(100, 580, "{}".format(q_location))
    
    # Task Information
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 560, "Task Information")
    c.setFont("Helvetica", 12)
    c.drawString(100, 540, "Task:")
    c.drawString(100, 520, "{}".format(q_task_name))
    c.drawString(100, 500, "TaskID:")
    c.drawString(100, 480, "{}".format(q_task_id))
    c.drawString(100, 460, "Description:")
    c.drawString(100, 440, "{}".format(q_process))
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