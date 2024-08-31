import streamlit as st
from pages.chat import chat_page
from pages.login import logout, main as login_page
from pages.img import main as img_page
from pages.settings import main as settings_main
from pages.pdf import main as pdf_page 

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
        "Teste menu 2": settings_main,
        "Login": login_page
    }

    # Add conditional pages based on login status
    if st.session_state.get('logged_in'):
        pages.update({
            "Imagem": img_page,
            "PDF": pdf_page
        })

    # Sidebar navigation buttons
    for page_name in pages:
        if page_name != "Login":
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

    # Display the current page
    page = pages.get(st.session_state.current_page, chat_page)
    page()

    # Add space at the bottom to ensure the footer is visible
    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)

    # Add footer
    st.markdown("""
        <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            background-color: #262730;
            color: white;
            border-top: 1px solid #ddd;
            z-index: 1000; /* Ensures the footer is in front of other content */
        }
        .footer b {
            font-weight: bold;
        }
        </style>
        <div class="footer">
            <b>PyaGPT</b> - &copy; 2024 Todos os direitos reservados.
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
