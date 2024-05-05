import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd  # Import pandas for Excel file saving

load_dotenv()  # Load environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Model Configuration
MODEL_CONFIG = {
  "temperature": 0.2,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}

## Safety Settings of Model
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  }
]

# LOAD GEMINI MODEL WITH MODEL CONFIGURATIONS
model = genai.GenerativeModel(model_name = "gemini-pro-vision",
                              generation_config = MODEL_CONFIG,
                              safety_settings = safety_settings)

## Function to get respones
def get_gemini_response(input, image, user_prompt):
    response = model.generate_content([input, image[0], user_prompt])
    return response.text

# FUNCTION TO DEFINE IMAGE FORMAT TO INPUT IN GEMINI
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# GEMINI MODEL OUTPUT- Function to extract the table from image
def gemini_output(image, system_prompt, user_prompt):

    image_info = input_image_details(image)
    input_prompt= [system_prompt, image_info[0], user_prompt]
    response = model.generate_content(input_prompt)
    return response.text

# Initializing streamlit app

st.set_page_config(page_title="DCI_PDFs_TABLE_DATA_EXTRACTOR")
st.header("PDF's Table Extractor")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Extract Table")

# System and User prompts
system_prompt = """
I am tasked with extracting tables from scanned images, even if cells are merged. 
Utilize your expertise in image understanding to accurately identify and extract all tables within the provided image.
Present each table clearly and orderly, maintaining the original cell structure and content. 
Handle merged cells effectively by combining their information seamlessly.
Ultimately, you should deliver well-defined tables with proper borders and accurate cell data.
"""
user_prompt = """
Please extract the table from the image, paying particular attention to any merged cells. 
Ensure the extracted table accurately reflects the original structure and content, 
combining information from merged cells appropriately. 
Maintain a clear and organized format with proper cell borders.
"""

if submit:
    # Extract tables using Gemini
    output = gemini_output(uploaded_file, system_prompt, user_prompt)  
    st.subheader("The Extracted Table:")
    st.write(output)
