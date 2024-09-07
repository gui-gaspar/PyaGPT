import os
import streamlit as st
from datetime import datetime
import pytz
from utils import (
    fetch_contatos, fetch_cursos, fetch_server_url, get_modelos_info, extract_model_names, get_openai_client
)

# Clear cached data if necessary
st.cache_data.clear()

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
        st.session_state.welcome_message_added = False

    if "contatos_info" not in st.session_state:
        st.session_state.contatos_info = fetch_contatos()

    if "cursos_info" not in st.session_state:
        st.session_state.cursos_info = fetch_cursos()

    # Adicionar as informações de contato na mensagem do sistema
    if st.session_state.get("contatos_info"):
        contatos_info = st.session_state.contatos_info
        contatos_formatted = (
            "Aqui estão os contatos atuais do Instituto Piaget:\n"
            f"**Instituto:** {contatos_info[0].get('instituto', 'Informações não disponíveis')}\n"
            f"**Tipo:** {contatos_info[0].get('tipo', 'Informações não disponíveis')}\n"
            f"**Morada:** {contatos_info[0].get('morada', 'Informações não disponíveis')}\n"
            f"**Código Postal:** {contatos_info[0].get('codigo_postal', 'Informações não disponíveis')}\n"
            f"**Telefone:** {contatos_info[0].get('telefone', 'Informações não disponíveis')}\n"
            f"**Fax:** {contatos_info[0].get('fax', 'Informações não disponíveis')}\n"
            f"**Email:** {contatos_info[0].get('email', 'Informações não disponíveis')}\n"
            f"**GPS:** {contatos_info[0].get('gps', 'Informações não disponíveis')}\n"
            f"**Skype:** {contatos_info[0].get('skype', 'Informações não disponíveis')}\n"
            f"**Horário:** {contatos_info[0].get('horario', 'Informações não disponíveis')}\n"
        )
        system_message_content = (
            "Você é o assistente virtual PyaGPT do Instituto Piaget. "
            "Responda em Português de Portugal e utilize as informações detalhadas sobre o Instituto Piaget. "
            f"{contatos_formatted}\n"
        )
    else:
        system_message_content = (
            "Você é o assistente virtual PyaGPT do Instituto Piaget. "
            "Responda em Português de Portugal."
        )

    # Adicionar as informações dos cursos na mensagem do sistema
    if st.session_state.get("cursos_info"):
        cursos_info = st.session_state.cursos_info
        cursos_formatted = (
            "Aqui estão os cursos atuais do Instituto Piaget:\n"
            + "\n".join([f"**{curso['tipo']}**, **{curso['curso']}**, **{curso['escola']}**" for curso in cursos_info])
        )
        system_message_content += f"\n{cursos_formatted}"

    st.session_state.system_message = {
        "role": "system",
        "content": system_message_content
    }

    # Assign user label based on login status, showing nome_completo if available
    if st.session_state.get('logged_in') and st.session_state.get('nome_completo'):
        user_label = f"**{st.session_state['nome_completo']}**"
    else:
        user_label = f"**{st.session_state.get('username', 'Convidado').capitalize()}**"

    # Handle welcome message logic
    if not st.session_state.welcome_message_added:
        welcome_message = (
            f"Olá {user_label}! Eu sou o PyaGPT, o assistente virtual do Instituto Piaget. "
            "Como posso ajudá-lo hoje?"
        )
        st.session_state.messages.insert(0, {
            "role": "assistant",
            "content": welcome_message
        })
        st.session_state.welcome_message_added = True
    else:
        # Update welcome message if login state changes
        if st.session_state.messages and st.session_state.messages[0]["role"] == "assistant":
            first_message = st.session_state.messages[0]
            if "Olá **Convidado**" in first_message["content"] and st.session_state.get('logged_in'):
                st.session_state.messages.pop(0)
                updated_welcome_message = (
                    f"Olá {user_label}! Eu sou o PyaGPT, o assistente virtual do Instituto Piaget. "
                    "Como posso ajudá-lo hoje?"
                )
                st.session_state.messages.insert(0, {
                    "role": "assistant",
                    "content": updated_welcome_message
                })

    # Ensure system message is always in messages
    if st.session_state.system_message not in st.session_state.messages:
        st.session_state.messages.insert(1, st.session_state.system_message)

    def get_current_time():
        tz = pytz.timezone('Europe/Lisbon')
        current_time_utc = datetime.now(pytz.utc)
        current_time_local = current_time_utc.astimezone(tz)
        return current_time_local.strftime('%H:%M')

    # Render all messages with avatars and timestamps
    for message in st.session_state.messages:
        if message["role"] != "system":
            avatar = "🤖" if message["role"] == "assistant" else "😎"
            label = "PyaGPT" if message["role"] == "assistant" else user_label
            with message_container.chat_message(message["role"], avatar=avatar):
                time_stamp = get_current_time()
                st.markdown(f"**{label}:** {message['content']} <span style='float: right;'>{time_stamp}</span>", unsafe_allow_html=True)

    # Handle user input
    if prompt := st.chat_input("Introduza uma pergunta aqui..."):
        try:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with message_container.chat_message("user", avatar="😎"):
                time_stamp = get_current_time()
                st.markdown(f"**{user_label}:** {prompt} <span style='float: right;'>{time_stamp}</span>", unsafe_allow_html=True)

            # Prepare messages for the AI API
            combined_messages = [
                {"role": "system", "content": st.session_state.system_message["content"]},
                {"role": "user", "content": prompt}
            ] + st.session_state.messages

            client = get_openai_client(server_url)

            # Get AI response with a loading spinner
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

                        # Display streaming AI response
                        for chunk in stream:
                            delta_content = chunk.choices[0].delta.content
                            response += delta_content
                            response_placeholder.markdown(f"**PyaGPT:** {response}▌", unsafe_allow_html=True)

                time_stamp = get_current_time()
                response_placeholder.markdown(f"**PyaGPT:** {response} <span style='float: right;'>{time_stamp}</span>", unsafe_allow_html=True)

            # Add AI response to session state
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Log conversation
            log_message("user", prompt)
            log_message("assistant", response)

        except Exception as e:
            st.error(f"Ocorreu um erro: {e}", icon="⛔️")
            log_message("error", str(e))

# Function to log conversation
def log_message(role, content):
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, 'chat_log.txt')
    with open(log_file, 'a', encoding='utf-8') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{timestamp} - {role.capitalize()}: {content}\n")
