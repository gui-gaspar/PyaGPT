import os
import streamlit as st
from datetime import datetime
import pytz
from utils import (
    fetch_contatos, fetch_server_url, get_modelos_info, extract_model_names, get_openai_client
)

def chat_page():
    st.title("PyaGPT - Assistente Virtual do Instituto Piaget")
    st.subheader("Bem-vindo ao PyaGPT!", divider="red", anchor=False)

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
        user_label = f"**{st.session_state.username.capitalize()}**"
    else:
        user_label = "**Convidado**"

    if not st.session_state.welcome_message_added:
        if st.session_state.get('logged_in'):
            welcome_message = (
                f"Olá {user_label}! Eu sou o PyaGPT, o assistente virtual da Escola Superior de Tecnologia e Gestão Jean Piaget. "
                "Como posso ajudá-lo hoje?"
            )
        else:
            welcome_message = (
                "Olá **Convidado**! Eu sou o PyaGPT, o assistente virtual da Escola Superior de Tecnologia e Gestão Jean Piaget. "
                "Como posso ajudá-lo hoje?"
            )
        st.session_state.messages.insert(0, {  # Insert at the beginning
            "role": "assistant",
            "content": welcome_message
        })
        st.session_state.welcome_message_added = True
    else:
        if st.session_state.messages and st.session_state.messages[0]["role"] == "assistant":
            first_message = st.session_state.messages[0]
            if "Olá **Convidado**" in first_message["content"] and st.session_state.get('logged_in'):
                st.session_state.messages.pop(0)
                updated_welcome_message = (
                    f"Olá {user_label}! Eu sou o PyaGPT, o assistente virtual da Escola Superior de Tecnologia e Gestão Jean Piaget. "
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

    def get_current_time():
        tz = pytz.timezone('Europe/Lisbon')
        current_time_utc = datetime.now(pytz.utc)
        current_time_local = current_time_utc.astimezone(tz)
        # Print the local time to help diagnose the issue
        print(f"Hora Local Atual: {current_time_local.strftime('%H:%M:%S')}")
        return current_time_local.strftime('%H:%M')

    for message in st.session_state.messages:
        if message["role"] != "system":
            avatar = "🤖" if message["role"] == "assistant" else "😎"
            label = "PyaGPT" if message["role"] == "assistant" else capitalize_first_letter(st.session_state.username) if st.session_state.get('logged_in') else "**Convidado**"
            with message_container.chat_message(message["role"], avatar=avatar):
                time_stamp = get_current_time()
                st.markdown(f"**{label}:** {message['content']} <span style='float: right;'>{time_stamp}</span>", unsafe_allow_html=True)

    if prompt := st.chat_input("Introduza uma pergunta aqui..."):
        try:
            user_label = capitalize_first_letter(st.session_state.username) if st.session_state.get('logged_in') else "**Convidado**"
            st.session_state.messages.append({"role": "user", "content": prompt})
            with message_container.chat_message("user", avatar="😎"):
                time_stamp = get_current_time()
                st.markdown(f"**{user_label}:** {prompt} <span style='float: right;'>{time_stamp}</span>", unsafe_allow_html=True)

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

                        response_placeholder.markdown(f"**PyaGPT:** ", unsafe_allow_html=True)

                        for chunk in stream:
                            delta_content = chunk.choices[0].delta.content
                            response += delta_content
                            response_placeholder.markdown(f"**PyaGPT:** {response}▌", unsafe_allow_html=True)

                time_stamp = get_current_time()
                response_placeholder.markdown(f"**PyaGPT:** {response} <span style='float: right;'>{time_stamp}</span>", unsafe_allow_html=True)

            st.session_state.messages.append({"role": "assistant", "content": response})

            # Log the conversation
            log_message("user", prompt)
            log_message("assistant", response)

        except Exception as e:
            st.error(f"Ocorreu um erro: {e}", icon="⛔️")
            log_message("error", str(e))  # Log errors as well

def log_message(role, content):
    # Ensure logs directory exists
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, 'chat_log.txt')
    with open(log_file, 'a', encoding='utf-8') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{timestamp} - {role.capitalize()}: {content}\n")

def format_contatos(contatos_info):
    formatted_contacts = []
    for contato in contatos_info:
        formatted_contacts.append(
            f"**Instituto:** {contato.get('instituto', 'Informações não disponíveis')}\n"
            f"**Tipo:** {contato.get('tipo', 'Informações não disponíveis')}\n"
            f"**Nome:** {contato.get('nome', 'Informações não disponíveis')}\n"
            f"**Morada:** {contato.get('morada', 'Informações não disponíveis')}\n"
            f"**Código Postal:** {contato.get('codigo_postal', 'Informações não disponíveis')}\n"
            f"**Telefone:** {contato.get('telefone', 'Informações não disponíveis')}\n"
            f"**Fax:** {contato.get('fax', 'Informações não disponíveis')}\n"
            f"**Email:** {contato.get('email', 'Informações não disponíveis')}\n"
            f"**GPS:** {contato.get('gps', 'Informações não disponíveis')}\n"
            f"**Skype:** {contato.get('skype', 'Informações não disponíveis')}\n"
            f"**Horário:** {contato.get('horario', 'Informações não disponíveis')}\n"
        )
    return "\n".join(formatted_contacts)
