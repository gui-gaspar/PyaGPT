import requests
import toml
import streamlit as st
from openai import OpenAI
import os

# FastAPI server URL
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://fastapi:8000")

# Load API key from configuration file
def load_api_key():
    try:
        config = toml.load('.streamlit/config.toml')
        return config['openai']['api_key']
    except FileNotFoundError:
        st.error("Config file not found.")
        return None
    except toml.TomlDecodeError:
        st.error("Error decoding config file.")
        return None

api_key = load_api_key()

def fetch_server_url():
    try:
        response = requests.get(f"{FASTAPI_URL}/server_url")
        response.raise_for_status()
        data = response.json()
        return data.get("server_url")
    except requests.exceptions.RequestException as err:
        st.error(f"An error occurred: {err}")
    return ""

def fetch_server_url_generate():
    try:
        response = requests.get(f"{FASTAPI_URL}/server_url_generate")
        response.raise_for_status()
        data = response.json()
        return data.get("server_url_generate")
    except requests.exceptions.RequestException as err:
        st.error(f"An error occurred: {err}")
    return ""

def get_openai_client(server_url):
    return OpenAI(
        base_url=server_url,
        api_key=api_key,
    )

def get_models_info(server_url):
    try:
        response = requests.get(f"{server_url}/models")
        response.raise_for_status()
        models_info = response.json()
        if models_info is None:
            st.error("Recebido JSON vazio do servidor.")
            return {}
        return models_info
    except requests.exceptions.RequestException as err:
        st.error(f"An error occurred: {err}")
    return {}

def extract_model_names(models_info: dict) -> tuple:
    return tuple(model["id"] for model in models_info.get("data", []))

def fetch_escola_info():
    try:
        response = requests.get(f"{FASTAPI_URL}/escola_info")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        st.error(f"An error occurred: {err}")
    return {}

def fetch_personal_info(username):
    try:
        response = requests.get(f"{FASTAPI_URL}/personal_info/{username}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        st.error(f"An error occurred: {err}")
    return {}

def format_escola_info(escola_info: dict) -> str:
    return (
        f"**Nome da Escola:** {escola_info.get('nome', 'Informações não disponíveis')}\n"
        f"**História:** {escola_info.get('historia', 'Informações não disponíveis')}\n"
        f"**Cursos oferecidos:** {', '.join(escola_info.get('cursos', []))}\n"
        f"**Contato:**\n"
        f"  - **Telefone:** {escola_info.get('telefone', 'Informações não disponíveis')}\n"
        f"  - **Email:** {escola_info.get('email', 'Informações não disponíveis')}\n"
        f"  - **Endereço:** {escola_info.get('endereco', 'Informações não disponíveis')}\n"
    )

def format_personal_info(personal_info: dict) -> str:
    courses_enrolled = personal_info.get('courses_enrolled', [])
    grades = personal_info.get('grades', {})
    
    if not isinstance(courses_enrolled, list):
        courses_enrolled = []

    if not isinstance(grades, dict):
        grades = {}

    return (
        f"**Nome Completo:** {personal_info.get('full_name', 'N/A')}\n"
        f"**Email:** {personal_info.get('email', 'N/A')}\n"
        f"**Telefone:** {personal_info.get('phone', 'N/A')}\n"
        f"**Endereço:** {personal_info.get('address', 'N/A')}\n"
        f"**Cursos Inscritos:** {', '.join(courses_enrolled)}\n"
        f"**Notas:**\n" + "\n".join([f"  - **{course}:** {grade}" for course, grade in grades.items()]) + "\n"
        f"**Informações Adicionais:** {personal_info.get('additional_info', 'N/A')}"
    )

