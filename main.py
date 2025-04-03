import os
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
from gemini_utility import (load_gemini_pro_model, gemini_pro_response, gemini_pro_vision_response, embeddings_model_response)
import google.generativeai as genai

working_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="The Birder AI",
    page_icon=":bird:",
    layout="centered",
)

with st.sidebar:
    selected = option_menu('The Birder AI',['Home','Chat with me','Send me an image',],menu_icon='bird', icons=['house-fill','chat-dots-fill', 'image-fill'],default_index=0)


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

if selected == 'Home':

    col1,col2,col3=st.columns(3)
    with col2:
        st.image("data/logo.png", width=200)
    st.title("The Birder AI")
    st.markdown(f'<p style="font-size:25px; text-align:left; "><br></p>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:35px; text-align:left; ">Welcome to <b>The Birder</b> -- Your Intelligent Online Ornithologist</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:15px; text-align:left; ">You are now able to access the most incredible information about birds</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:25px; text-align:left; "><br></p>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:20px; text-align:left; "><b>The Birder</b> is a cutting-edge, AI-driven bird companion that will make sure you get the best experience in the ornithology sector. The Birder will guide you through this incredible world letting you know the best curiosities of every bird, along with whre to find it and how to get there. This experience includes the best flight and hotel recommendations to make it the easiest possible for you to make your dream come true. You are one step away to achieve real happiness!</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:25px; text-align:left; "><br></p>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:25px; text-align:left; font-weight:bold;">But why The Birder?</p>', unsafe_allow_html=True)
    st.markdown("""
    - **Bird Information** – In this tab you will find the most interesting and precise information of any bird you want, just by uploading the image of the bird you want to know more about. You will also be able to ask any intricate question you might think of and The Birder will answer you as best as it knows.
    - **Flights** – Once you know where this particular bird is usually located, your companion will recommend the three best flight options for you to get to live the experience with your own eyes.
    - **Hotels** – The last thing you need to live the full experience is a good hotel to stay in and enjoy the best days of your life. The Birder will help you choose the best staying places you can think of to have a good rest after a long day of spotting your favourite birds.
    - **Team** – In here you can have an inside look at our incredible and hard-working team that made all this possible.
    """)
    st.markdown(f'<p style="font-size:25px; text-align:left; "><br></p>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:25px; text-align:left; "><br></p>', unsafe_allow_html=True)

    cola,colb,colc=st.columns(3)
    with cola:
        st.image("data/bird5.jpg", width=205)
        st.image("data/bird4.jpg", width=205)
        st.image("data/bird7.jpg", width=205)
    with colb:
        st.image("data/bird2.jpg", width=205)
        st.image("data/bird1.jpg", width=205)
        st.image("data/bird8.jpg", width=205)
    with colc:
        st.image("data/bird3.jpg", width=205)
        st.image("data/bird6.jpg", width=205)
        st.image("data/bird9.jpg", width=205)

# chatbot page
if selected == 'Chat with me':
    genai.configure(api_key='AIzaSyC7PQIrRQbjbf-EKZcTIm3zTM9gHipMsuM')
    model = genai.GenerativeModel("gemini-1.5-pro")

    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    col1,col2,col3=st.columns(3)
    with col2:
        st.image("data/logo.png", width=200)
    st.title("Chat with me")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.chat_input("Ask Gemini-Pro...")  # Renamed for clarity
    if user_prompt:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)  # Renamed for clarity

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)


# Image captioning page
if selected == "Image Captioning":

    st.title("📷 Snap Narrate")

    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    if st.button("Generate Caption"):
        image = Image.open(uploaded_image)

        col1, col2 = st.columns(2)

        with col1:
            resized_img = image.resize((800, 500))
            st.image(resized_img)

        default_prompt = "write a short caption for this image"  # change this prompt as per your requirement

        # get the caption of the image from the gemini-pro-vision LLM
        caption = gemini_pro_vision_response(default_prompt, image)

        with col2:
            st.info(caption)


# text embedding model
if selected == "Embed text":

    st.title("🔡 Embed Text")

    # text box to enter prompt
    user_prompt = st.text_area(label='', placeholder="Enter the text to get embeddings")

    if st.button("Get Response"):
        response = embeddings_model_response(user_prompt)
        st.markdown(response)


# text embedding model
if selected == "Ask me anything":

    st.title("❓ Ask me a question")

    # text box to enter prompt
    user_prompt = st.text_area(label='', placeholder="Ask me anything...")

    if st.button("Get Response"):
        response = gemini_pro_response(user_prompt)
        st.markdown(response)
