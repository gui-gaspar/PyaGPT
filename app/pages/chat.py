import os
import streamlit as st
from datetime import datetime
from utils import (
    fetch_contatos, fetch_server_url, get_modelos_info, extract_model_names, get_openai_client
)

def chat_page():
    st.title("PyaGPT - Assistente Virtual do Instituto Piaget")
    st.subheader("Bem-vindo ao PyaGPT!")

    server_url = fetch_server_url()  # Fetch server URL dynamically
    if not server_url:
        st.error("Não foi possível obter o URL do servidor.")
        return

    try:
        modelos_info = get_modelos_info(server_url)
        available_models = extract_model_names(modelos_info)
    except Exception as e:
        st.error(f"Falha ao recuperar modelos: {e}")
        return

    if available_models:
        selected_model = st.selectbox(
            "Escolha um modelo disponível localmente no seu sistema ↓", available_models
        )
    else:
        st.warning("Ainda não descarregou nenhum modelo da Ollama!", icon="⚠️")
        if st.button("Ir para as definições para descarregar um modelo"):
            st.session_state.current_page = "Settings"
            st.experimental_rerun()  # Rerun to navigate to the "Settings" page

    message_container = st.container()

    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.system_message = {
            "role": "system",
            "content": (
                "Você é o assistente virtual PyaGPT do Instituto Piaget. "
                "Responda em Português de Portugal. "
                "Utilize as informações detalhadas sobre a Escola e informações pessoais do utilizador, se disponíveis. "
                "Responda apenas a perguntas sobre a Escola Superior de Tecnologia e Gestão Jean Piaget em Almada e forneça informações precisas e detalhadas com base nas informações fornecidas. "
                "Apenas responde ao que for perguntado e não divulgue informação se essa não for pedida."
            )
        }
        st.session_state.welcome_message_added = False

    if "contatos_info" not in st.session_state:
        st.session_state.contatos_info = fetch_contatos()

    if st.session_state.get('logged_in') and st.session_state.get('username'):
        user_label = f"{st.session_state.username.capitalize()}"
    else:
        user_label = "Convidado"

    if not st.session_state.welcome_message_added:
        if st.session_state.get('logged_in'):
            welcome_message = (
                f"Olá <strong>{user_label}</strong>! Eu sou o PyaGPT, o assistente virtual da Escola Superior de Tecnologia e Gestão Jean Piaget. "
                "Como posso ajudá-lo hoje?"
            )
        else:
            welcome_message = (
                "Olá <strong>Convidado</strong>! Eu sou o PyaGPT, o assistente virtual da Escola Superior de Tecnologia e Gestão Jean Piaget. "
                "Como posso ajudá-lo hoje?"
            )
        st.session_state.messages.insert(0, {
            "role": "assistant",
            "content": welcome_message
        })
        st.session_state.welcome_message_added = True
    else:
        if st.session_state.messages and st.session_state.messages[0]["role"] == "assistant":
            first_message = st.session_state.messages[0]
            if "Olá <strong>Convidado</strong>" in first_message["content"] and st.session_state.get('logged_in'):
                st.session_state.messages.pop(0)
                updated_welcome_message = (
                    f"Olá <strong>{user_label}</strong>! Eu sou o PyaGPT, o assistente virtual da Escola Superior de Tecnologia e Gestão Jean Piaget. "
                    "Como posso ajudá-lo hoje?"
                )
                st.session_state.messages.insert(0, {
                    "role": "assistant",
                    "content": updated_welcome_message
                })

    if st.session_state.system_message not in st.session_state.messages:
        st.session_state.messages.insert(1, st.session_state.system_message)  # Insert after the welcome message

    def capitalize_first_letter(text):
        return text.capitalize() if text else text

    for message in st.session_state.messages:
        if message["role"] != "system":
            avatar = "🤖" if message["role"] == "assistant" else "😎"
            label = "PyaGPT" if message["role"] == "assistant" else capitalize_first_letter(st.session_state.username) if st.session_state.get('logged_in') else "Convidado"
            with message_container.chat_message(message["role"], avatar=avatar):
                st.markdown(
                    f"<div style='display: flex; align-items: center; width: 100%;'>"
                    f"<span style='margin-right: 8px;'><strong>{label}:</strong></span>"
                    f"<span style='flex-grow: 1;'>{message['content']}</span></div>",
                    unsafe_allow_html=True
                )

    if prompt := st.chat_input("Introduza uma pergunta aqui..."):
        try:
            user_label = capitalize_first_letter(st.session_state.username) if st.session_state.get('logged_in') else "Convidado"
            st.session_state.messages.append({"role": "user", "content": prompt})
            with message_container.chat_message("user", avatar="😎"):
                st.markdown(
                    f"<div style='display: flex; align-items: center; width: 100%;'>"
                    f"<span style='margin-right: 8px;'><strong>{user_label}:</strong></span>"
                    f"<span style='flex-grow: 1;'>{prompt}</span></div>",
                    unsafe_allow_html=True
                )

            context = ""

            # Fetch and format contacts information
            if "contatos_info" in st.session_state:
                contatos_info = st.session_state.contatos_info
                context += format_contatos(contatos_info) + "\n"

            # Update system message content
            st.session_state.system_message["content"] = context

            combined_messages = [
                {"role": "system", "content": st.session_state.system_message["content"]},
                {"role": "user", "content": prompt}
            ] + st.session_state.messages

            client = get_openai_client(server_url)

            with message_container.chat_message("assistant", avatar="🤖"):
                response_placeholder = st.empty()
                spinner_placeholder = st.empty()
                response = ""

                with spinner_placeholder:
                    with st.spinner("Aguarde um pouco enquanto o PyaGPT gera uma resposta..."):
                        stream = client.chat.completions.create(
                            model=selected_model,
                            messages=combined_messages,
                            stream=True
                        )
                        spinner_placeholder.empty()

                        response_placeholder.markdown(
                            f"<div style='display: flex; align-items: center; width: 100%;'>"
                            f"<span style='margin-right: 8px;'><strong>PyaGPT:</strong></span>"
                            f"<span style='flex-grow: 1;'></span></div>",
                            unsafe_allow_html=True
                        )

                        for chunk in stream:
                            delta_content = chunk.choices[0].delta.content
                            response += delta_content
                            response_placeholder.markdown(
                                f"<div style='display: flex; align-items: center; width: 100%;'>"
                                f"<span style='margin-right: 8px;'><strong>PyaGPT:</strong></span>"
                                f"<span style='flex-grow: 1;'>{response}▌</span></div>",
                                unsafe_allow_html=True
                            )

                response_placeholder.markdown(
                    f"<div style='display: flex; align-items: center; width: 100%;'>"
                    f"<span style='margin-right: 8px;'><strong>PyaGPT:</strong></span>"
                    f"<span style='flex-grow: 1;'>{response}</span></div>",
                    unsafe_allow_html=True
                )

            st.session_state.messages.append({"role": "assistant", "content": response})

            # Log the conversation
            log_message("user", prompt)
            log_message("assistant", response)

        except Exception as e:
            st.error(f"Ocorreu um erro: {e}", icon="⛔️")
            log_message("error", str(e))  # Log errors as well

def log_message(role, content):
    log_path = "chat_log.txt"
    with open(log_path, "a") as log_file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_file.write(f"{timestamp} [{role.upper()}]: {content}\n")

def format_contatos(contatos_info):
    formatted_contatos = "Contatos Importantes:\n"
    for contact in contatos_info:
        formatted_contatos += f"- {contact['name']}: {contact['phone']} ({contact['email']})\n"
    return formatted_contatos
