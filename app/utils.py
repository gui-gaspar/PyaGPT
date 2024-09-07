import requests
import toml
import streamlit as st
from openai import OpenAI
import os

# FastAPI server URL
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://fastapi:8000")
st.cache_data.clear()
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
        return data.get("server_url", "")
    except requests.exceptions.RequestException as err:
        st.error(f"An error occurred: {err}")
    return ""

def fetch_server_url_generate():
    try:
        response = requests.get(f"{FASTAPI_URL}/server_url_generate")
        response.raise_for_status()
        data = response.json()
        return data.get("server_url_generate", "")
    except requests.exceptions.RequestException as err:
        st.error(f"An error occurred: {err}")
    return ""

def get_openai_client(server_url):
    return OpenAI(
        base_url=server_url,
        api_key=api_key,
    )

def get_modelos_info(server_url):
    try:
        response = requests.get(f"{server_url}/models")
        response.raise_for_status()
        modelos_info = response.json()
        if not modelos_info:
            st.error("Received empty JSON from server.")
            return {}
        return modelos_info
    except requests.exceptions.RequestException as err:
        st.error(f"An error occurred: {err}")
    return {}

def extract_model_names(modelos_info: dict) -> tuple:
    return tuple(model["id"] for model in modelos_info.get("data", []))

def fetch_contatos():
    try:
        response = requests.get(f"{FASTAPI_URL}/contatos")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        st.error(f"An error occurred: {err}")
    return []

def format_contatos(contatos: list) -> str:
    if not contatos:
        return "Não há informações de contatos disponíveis."

    formatted_contatos = []
    for contato in contatos:
        formatted_contatos.append(
            f"**Instituto:** {contato.get('instituto', 'Informações não disponíveis')}\n"
            f"**Tipo:** {contato.get('tipo', 'Informações não disponíveis')}\n"
            f"**Morada:** {contato.get('morada', 'Informações não disponíveis')}\n"
            f"**Código Postal:** {contato.get('codigo_postal', 'Informações não disponíveis')}\n"
            f"**Telefone:** {contato.get('telefone', 'Informações não disponíveis')}\n"
            f"**Fax:** {contato.get('fax', 'Informações não disponíveis')}\n"
            f"**Email:** {contato.get('email', 'Informações não disponíveis')}\n"
            f"**GPS:** {contato.get('gps', 'Informações não disponíveis')}\n"
            f"**Skype:** {contato.get('skype', 'Informações não disponíveis')}\n"
            f"**Horário:** {contato.get('horario', 'Informações não disponíveis')}\n"
        )
    return "\n".join(formatted_contatos)


def fetch_cursos():
    try:
        response = requests.get(f"{FASTAPI_URL}/cursos")
        response.raise_for_status()
        data = response.json()
        print("Fetched Cursos:", data)  # Debugging line
        return data
    except requests.exceptions.RequestException as err:
        st.error(f"An error occurred: {err}")
        return []

def fetch_curso_info():
    try:
        response = requests.get(f"{FASTAPI_URL}/curso_info")
        response.raise_for_status()
        data = response.json()
        print("Fetched Curso Info:", data)  # Debugging line
        return data
    except requests.exceptions.RequestException as err:
        st.error(f"An error occurred: {err}")
        return []

def fetch_plano_estudos():
    try:
        response = requests.get(f"{FASTAPI_URL}/plano_estudos")
        response.raise_for_status()
        data = response.json()
        print("Fetched Plano Estudos:", data)  # Debugging line
        return data
    except requests.exceptions.RequestException as err:
        st.error(f"An error occurred: {err}")
        return []

def fetch_escolas():
    """
    Fetch the list of schools from the FastAPI backend.
    """
    try:
        response = requests.get(f"{FASTAPI_URL}/escolas")
        response.raise_for_status()
        data = response.json()
        print("Fetched Escolas:", data)  # Debugging line
        return data
    except requests.exceptions.RequestException as err:
        st.error(f"An error occurred while fetching schools: {err}")
        return []

def fetch_institutos():
    """
    Fetch the list of institutes from the FastAPI backend.
    """
    try:
        response = requests.get(f"{FASTAPI_URL}/institutos")
        response.raise_for_status()
        data = response.json()
        print("Fetched Institutos:", data)  # Debugging line
        return data
    except requests.exceptions.RequestException as err:
        st.error(f"An error occurred while fetching institutes: {err}")
        return []

def fetch_orgaos_gestao():
    try:
        response = requests.get(f"{FASTAPI_URL}/orgaos_de_gestao")
        response.raise_for_status()
        data = response.json()
        print("Fetched Órgãos de Gestão:", data)  # Debugging line
        return data
    except requests.exceptions.RequestException as err:
        st.error(f"An error occurred: {err}")
        return []
    
def format_cursos(cursos: list) -> str:
    if not cursos:
        return "Não há informações de cursos disponíveis."

    formatted_cursos = []
    for curso in cursos:
        if isinstance(curso, dict):
            formatted_cursos.append(
                f"**Tipo:** {curso.get('tipo', 'Informações não disponíveis')}\n"
                f"**Curso:** {curso.get('curso', 'Informações não disponíveis')}\n"
                f"**Escola:** {curso.get('escola', 'Informações não disponíveis')}\n"
            )
        else:
            formatted_cursos.append("Informação de curso inválida.")
    return "\n".join(formatted_cursos)

def format_curso_info(curso_info: dict) -> str:
    if not curso_info or not isinstance(curso_info, dict):
        return "Informações do curso não disponíveis."

    return (
        f"**Curso:** {curso_info.get('curso', 'Informações não disponíveis')}\n"
        f"**Saídas Profissionais:** {curso_info.get('saídas_profissionais', 'Informações não disponíveis')}\n"
        f"**Estatuto Profissional:** {curso_info.get('estatuto_profissional', 'Informações não disponíveis')}\n"
        f"**Apresentação:** {curso_info.get('apresentação', 'Informações não disponíveis')}\n"
        f"**Acesso a Outros Ciclos:** {curso_info.get('acesso_a_outros_ciclos', 'Informações não disponíveis')}\n"
        f"**Área de Estudo:** {curso_info.get('área_de_estudo', 'Informações não disponíveis')}\n"
        f"**Regras de Avaliação:** {curso_info.get('regras_de_avaliação', 'Informações não disponíveis')}\n"
        f"**Acesso:** {curso_info.get('acesso', 'Informações não disponíveis')}\n"
        f"**Diploma:** {curso_info.get('diploma', 'Informações não disponíveis')}\n"
    )

def format_plano_estudos(plano_estudos: list) -> str:
    if not plano_estudos:
        return "Não há informações sobre o plano de estudos disponíveis."

    formatted_plano_estudos = []
    for unidade in plano_estudos:
        if isinstance(unidade, dict):
            formatted_plano_estudos.append(
                f"**Ano:** {unidade.get('ano', 'Informações não disponíveis')}\n"
                f"**Semestre:** {unidade.get('semestre', 'Informações não disponíveis')}\n"
                f"**Unidade Curricular:** {unidade.get('unidade_curricular', 'Informações não disponíveis')}\n"
                f"**CH:** {unidade.get('ch', 'Informações não disponíveis')}\n"
                f"**ECTS:** {unidade.get('ects', 'Informações não disponíveis')}\n"
            )
        else:
            formatted_plano_estudos.append("Informação de plano de estudos inválida.")
    return "\n".join(formatted_plano_estudos)

def format_escolas(escolas: list) -> str:
    if not escolas:
        return "Nenhuma escola encontrada."

    formatted_schools = []
    for escola in escolas:
        if isinstance(escola, dict):
            formatted_schools.append(
                f"**Nome da Escola:** {escola.get('escola', 'N/A')}\n"
                f"**Descrição:** {escola.get('descricao', 'Descrição não disponível')}\n"
            )
        else:
            formatted_schools.append("Informação de escola inválida.")
    return "\n\n".join(formatted_schools)

def format_institutos(institutos: list) -> str:
    if not institutos:
        return "Nenhum instituto encontrado."

    formatted_institutes = []
    for instituto in institutos:
        if isinstance(instituto, dict):
            formatted_institutes.append(
                f"**Nome do Instituto:** {instituto.get('instituto', 'N/A')}\n"
            )
        else:
            formatted_institutes.append("Informação de instituto inválida.")
    return "\n\n".join(formatted_institutes)

def format_orgaos_gestao(orgaos_gestao: list) -> str:
    if not orgaos_gestao:
        return "Não há informações sobre órgãos de gestão disponíveis."

    formatted_orgaos_gestao = []
    for orgao in orgaos_gestao:
        if isinstance(orgao, dict):
            formatted_orgaos_gestao.append(
                f"**Escola:** {orgao.get('escola', 'Informações não disponíveis')}\n"
                f"**Função:** {orgao.get('função', 'Informações não disponíveis')}\n"
                f"**Nome:** {orgao.get('nome', 'Informações não disponíveis')}\n"
            )
        else:
            formatted_orgaos_gestao.append("Informação de órgão de gestão inválida.")
    return "\n".join(formatted_orgaos_gestao)



