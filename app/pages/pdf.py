import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO
import json
from pdfminer.high_level import extract_text
from utils import fetch_server_url, fetch_server_url_generate, get_modelos_info, extract_model_names

def img_to_base64(image: Image.Image) -> str:
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

def extract_text_from_pdf(file_upload) -> str:
    """
    Extract text from a PDF file using pdfminer.six.

    Args:
        file_upload (st.UploadedFile): Streamlit file upload object containing the PDF.

    Returns:
        str: The extracted text from the PDF.
    """
    pdf_bytes = file_upload.read()
    text = extract_text(BytesIO(pdf_bytes))
    return text

def main():
    st.title("LLaVA Playground")
    st.subheader("Interact with LLaVA models", divider="red", anchor=False)

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

    # Extract model names from the fetched model information
    if not isinstance(modelos_info, dict) or "data" not in modelos_info:
        st.warning("Invalid model information format.")
        return

    if not isinstance(modelos_info["data"], list):
        st.warning("The 'data' field in model information is not a list.")
        return

    available_models = [model.get("id") for model in modelos_info["data"] if isinstance(model, dict)]
    if not available_models:
        st.warning("No available models found.")
        return

    selected_model = st.selectbox("Pick a model available locally on your system ↓", available_models, key=1)

    if "chats" not in st.session_state:
        st.session_state.chats = []

    if "uploaded_file_state" not in st.session_state:
        st.session_state.uploaded_file_state = None

    uploaded_file = st.file_uploader("Upload a PDF file for analysis", type=["pdf"])

    col1, col2 = st.columns(2)

    with col2:
        if uploaded_file is not None:
            st.session_state.uploaded_file_state = uploaded_file.getvalue()
            pdf_text = extract_text_from_pdf(uploaded_file)
            st.text_area("Extracted Text", pdf_text, height=300)

    with col1:
        if uploaded_file is not None:
            for message in st.session_state.chats:
                avatar = "🌋" if message["role"] == "assistant" else "🫠"
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])

            if user_input := st.chat_input("Question about the document...", key="chat_input"):
                st.session_state.chats.append({"role": "user", "content": user_input})
                with st.chat_message("user", avatar="🫠"):
                    st.markdown(user_input)

                API_URL = api_url_generate
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                }
                # Combine the extracted text and the user query
                combined_prompt = f"Document text: {pdf_text}\n\nQuestion: {user_input}"
                data = {
                    "model": selected_model,
                    "prompt": combined_prompt,  # Send both the text and the question in the prompt
                }

                llava_response = ""

                with st.chat_message("assistant", avatar="🌋"):
                    with st.spinner(":blue[processing...]"):
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
