import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv() ## load all the environment variables from .env

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Load Gemini pro vision model
model=genai.GenerativeModel('gemini-pro-vision')

## Function to get respones
def get_gemini_response(input,image,user_prompt):
    response=model.generate_content([input,image[0],user_prompt])
    return response.text

## Function to read image and convert it to bytes
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


##initialize our streamlit app

st.set_page_config(page_title="MultiLanguage Image's data Extractor")

st.header("MultiLanguage Image's data Extractor")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image ...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit=st.button("Tell me about the image")

input_prompt="""
You are an expert in understanding images. We will upload an image
and you will have to answer any questions based on the uploaded image
"""

## if submit button is clicked

if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Rresponse is")
    st.write(response)