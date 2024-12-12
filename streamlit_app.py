import streamlit as st
import os
import base64
import google.generativeai as genai

st.title("GenAI Camp -> Roast my tree!")
st.write(
    "Share your Christmas tree photo and we'll give it a good ol' roasting!"
)
genai.configure(api_key=st.secrets['GEMINI_API_KEY'])
def upload_to_gemini(path, mime_type=None):
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

generation_config = {
  "temperature": 2,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 4192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
  system_instruction="You are a friendly but funny professional Christmas tree rater and roaster. You review pictures of Christmas trees, to rate how they are. You give funny, witty remarks similar to a roasting battle, from skinny trees to overdone, you scathingly but non-offensively roast them all.\nThings you might critique:\nToo skinny or too bushy. Too many lights, not enough lights. No decoration, too many decorations. Too focused colour scheme, no colour scheme, etc.",
)


my_file = st.file_uploader("Choose your christmas tree!", type=['jpg'], accept_multiple_files=False, label_visibility="visible")

if my_file is not None:
    col1, col2 = st.columns(2)
    with col1:
       st.image(my_file)

    with col2:
        gemfile = upload_to_gemini(my_file, 'image/jpeg')
        response = model.generate_content([gemfile, "Roast this tree!"])
        st.write(response.text)
