import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO
import json
from utils import fetch_server_url, fetch_server_url_generate, get_modelos_info, extract_model_names

def img_to_base64(image):
    """
    Convert an image to base64 format.

    Args:
        image: PIL.Image - The image to be converted.
    Returns:
        str: The base64 encoded image.
    """
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def get_allowed_model_names(modelos_info):
    """
    Extract allowed model names from the fetched model information.

    Args:
        modelos_info: dict - Dictionary containing model information.
    Returns:
        tuple: A tuple of allowed model names.
    """
    allowed_models = ["bakllava:latest", "llava:latest"]
    
    # Check if the modelos_info dictionary has a "data" key and that it's a list
    if not isinstance(modelos_info, dict) or "data" not in modelos_info:
        st.warning("Invalid model information format.")
        return tuple()  # Return an empty tuple if the format is incorrect

    # Ensure 'data' key is a list
    if not isinstance(modelos_info["data"], list):
        st.warning("The 'data' field in model information is not a list.")
        return tuple()

    model_names = [model.get("id") for model in modelos_info["data"] if isinstance(model, dict)]
    return tuple(
        model
        for model in allowed_models
        if model in model_names
    )

def main():
    st.title("PyaGPT - Análise de Imagens")
    st.subheader("Faça o upload de imagens para serem interpretadas pelo PyaGPT!", divider="red", anchor=False)

    server_url = fetch_server_url()
    if not server_url:
        st.error("Failed to fetch the server URL.")
        return

    api_url_generate = fetch_server_url_generate()
    if not api_url_generate:
        st.error("Failed to fetch the server URL for generation.")
        return

    modelos_info = get_modelos_info(server_url)
    if not modelos_info:
        st.error("Failed to fetch model list.")
        return

    available_models = get_allowed_model_names(modelos_info)
    if not available_models:
        st.warning("No available models found.")
        return

    selected_model = st.selectbox("Escolha um modelo disponível localmente no seu sistema ↓", available_models, key=1)

    if "chats" not in st.session_state:
        st.session_state.chats = []

    if "uploaded_file_state" not in st.session_state:
        st.session_state.uploaded_file_state = None

    uploaded_file = st.file_uploader("Faça upload de uma imagem para análise:", type=["png", "jpg", "jpeg"])

    col1, col2 = st.columns(2)

    with col2:
        if uploaded_file is not None:
            st.session_state.uploaded_file_state = uploaded_file.getvalue()
            image = Image.open(BytesIO(st.session_state.uploaded_file_state))
            st.image(image, caption="Imagem Carregada")

    with col1:
        if uploaded_file is not None:
            for message in st.session_state.chats:
                avatar = "🤖" if message["role"] == "assistant" else "😎"
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])

            if user_input := st.chat_input("Escreva uma pergunta sobre a imagem...", key="chat_input"):
                st.session_state.chats.append({"role": "user", "content": user_input})
                with st.chat_message("user", avatar="😎"):
                    st.markdown(user_input)

                image_base64 = img_to_base64(image)
                API_URL = api_url_generate  # Use the URL fetched from the server
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                }
                data = {
                    "model": selected_model,
                    "prompt": user_input,
                    "images": [image_base64],
                }

                llava_response = ""  # Initialize llava_response to an empty string

                with st.chat_message("assistant", avatar="🤖"):
                    with st.spinner(":blue[Aguarde enquanto o PyaGPT genera uma resposta...]"):
                        try:
                            response = requests.post(API_URL, json=data, headers=headers)
                            response.raise_for_status()
                            response_lines = response.text.split("\n")
                            
                            for line in response_lines:
                                if line.strip():
                                    try:
                                        response_data = json.loads(line)
                                        if "response" in response_data:
                                            llava_response += response_data["response"]
                                    except json.JSONDecodeError:
                                        st.warning("Received invalid JSON from the server.")
                            if llava_response:
                                st.markdown(llava_response)
                            else:
                                st.warning("No response received from the API.")
                        except requests.exceptions.RequestException as e:
                            st.error(f"Request failed: {e}")

                st.session_state.chats.append({"role": "assistant", "content": llava_response})

if __name__ == "__main__":
    main()
