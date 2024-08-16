import streamlit as st
from pages.chat import chat_page
from pages.login import logout, main as login_main
from pages.multimodal import main as multimodal_main
from pages.settings import main as settings_main

# Set page configuration
st.set_page_config(
    page_title="PyaGPT",
    page_icon=":guardsman:",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.sidebar.title("Navegação")

    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Chat"  # Default to Chat page

    pages = {
        "Chat": chat_page,
        "Teste menu": multimodal_main,
        "Teste menu 2": settings_main,
        "Login": login_main
    }

    for page_name in ["Chat", "Teste menu", "Teste menu 2"]:
        if st.sidebar.button(page_name, key=f"sidebar_button_{page_name}"):
            st.session_state.current_page = page_name
            st.rerun()

    st.sidebar.divider()

    if st.session_state.get('logged_in'):
        username = st.session_state.username.capitalize()
        st.sidebar.markdown(f"Bem-vindo, **{username}**!")
        if st.sidebar.button("Logout", key="logout_sidebar_button"):
            st.session_state.logged_in = False
            st.session_state.username = None
            logout()
            st.rerun()
    else:
        if st.sidebar.button("Login", key="login_sidebar_button"):
            st.session_state.current_page = "Login"
            st.rerun()

    page = pages.get(st.session_state.current_page, chat_page)
    page()

if __name__ == "__main__":
    main()
