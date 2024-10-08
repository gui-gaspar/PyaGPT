import streamlit as st
import requests
import time  # Import time for delay
from utilities.icon import page_icon

# FastAPI URL
FASTAPI_URL = "http://fastapi:8000"  # Update to match your FastAPI server URL

# Validate login credentials via FastAPI
def validate_login(username, password):
    try:
        response = requests.post(f"{FASTAPI_URL}/login", json={"username": username, "password": password})
        response.raise_for_status()
        data = response.json()
        return {"valid": data.get("valid", False), "username": username}  # Garantimos o retorno de um dicionário
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"An error occurred: {req_err}")
    return {"valid": False, "username": None}  # Sempre retorna um dicionário

# Get full name from FastAPI using the username
def get_nome_completo(username):
    try:
        response = requests.get(f"{FASTAPI_URL}/nome_completo/{username}")
        response.raise_for_status()
        return response.json().get("nome_completo")
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"An error occurred: {req_err}")
    return None

# Clear session state
def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Main function for the Streamlit app
def main():
    st.title("PyaGPT - Página de Login")
    st.subheader("Inicie sessão na sua conta do Instituto Piaget!", divider="red", anchor=False)

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.write(f"Welcome, {st.session_state.nome_completo}!")
        st.button("Logout", key="logout_button", on_click=logout)
        st.rerun()
    else:
        with st.form(key='login_form'):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label="Login")

            if submit_button:
                result = validate_login(username, password)  # Chamamos validate_login
                if result["valid"]:  # Agora result sempre será um dicionário
                    st.session_state.logged_in = True
                    st.session_state.username = result["username"]

                    # Agora vamos buscar o nome completo
                    nome_completo = get_nome_completo(st.session_state.username)
                    if nome_completo:
                        st.session_state.nome_completo = nome_completo
                    else:
                        st.error("Não foi possível obter o nome completo.")

                    st.success("Login bem-sucedido!")
                    time.sleep(1)  # Add delay to show the success message
                    st.session_state.current_page = "Chat"  # Redirect to chat page
                    st.rerun()
                else:
                    st.error("Username ou password inválidos.")


if __name__ == "__main__":
    main()
