import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO
import json

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

def get_models_info(server_url):
    """
    Fetch the list of models from the server.

    Args:
        server_url: str - The base URL of the server.
    Returns:
        dict or None: A dictionary with model information or None if there's an error.
    """
    try:
        # Attempt fetching models from different possible endpoints
        model_endpoints = [
            "/models",          # Original endpoint
            "/list/models",     # Alternative possible endpoint
            "/available-models" # Another possible endpoint
        ]
        
        for endpoint in model_endpoints:
            full_url = f"{server_url}{endpoint}"
            try:
                response = requests.get(full_url)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as http_err:
                st.write(f"Failed with endpoint {endpoint}: {http_err}")  # Debugging line

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        st.write(f"URL tried: {server_url}")  # Debugging line
    return None

def get_allowed_model_names(models_info):
    """
    Extract allowed model names from the fetched model information.

    Args:
        models_info: dict - Dictionary containing model information.
    Returns:
        tuple: A tuple of allowed model names.
    """
    allowed_models = ["bakllava:latest", "llava:latest"]
    model_names = [m["id"] for m in models_info.get("data", [])]
    return tuple(
        model
        for model in allowed_models
        if model in model_names
    )

def main():
    st.title("LLaVA Playground")
    st.subheader("Interact with LLaVA models", divider="red", anchor=False)

    server_url = "http://host.docker.internal:11434/v1"  # Updated URL

    models_info = get_models_info(server_url)
    if models_info is None:
        st.error("Failed to fetch model list.")
        return

    available_models = get_allowed_model_names(models_info)
    missing_models = set(["bakllava:latest", "llava:latest"]) - set(available_models)

    if not available_models:
        return

    selected_model = st.selectbox("Pick a model available locally on your system ↓", available_models, key=1)

    if "chats" not in st.session_state:
        st.session_state.chats = []

    if "uploaded_file_state" not in st.session_state:
        st.session_state.uploaded_file_state = None

    uploaded_file = st.file_uploader("Upload an image for analysis", type=["png", "jpg", "jpeg"])

    col1, col2 = st.columns(2)

    with col2:
        if uploaded_file is not None:
            st.session_state.uploaded_file_state = uploaded_file.getvalue()
            image = Image.open(BytesIO(st.session_state.uploaded_file_state))
            st.image(image, caption="Uploaded image")

    with col1:
        if uploaded_file is not None:
            for message in st.session_state.chats:
                avatar = "🌋" if message["role"] == "assistant" else "🫠"
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])

            if user_input := st.chat_input("Question about the image...", key="chat_input"):
                st.session_state.chats.append({"role": "user", "content": user_input})
                with st.chat_message("user", avatar="🫠"):
                    st.markdown(user_input)

                image_base64 = img_to_base64(image)
                API_URL = f"http://host.docker.internal:11434/api/generate"
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                }
                data = {
                    "model": selected_model,
                    "prompt": user_input,
                    "images": [image_base64],
                }

                with st.chat_message("assistant", avatar="🌋"):
                    with st.spinner(":blue[processing...]"):
                        try:
                            response = requests.post(API_URL, json=data, headers=headers)
                            response.raise_for_status()
                            response_lines = response.text.split("\n")
                            llava_response = ""
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
