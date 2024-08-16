import streamlit as st
from utils import (
    get_models_info, extract_model_names, fetch_escola_info,
    fetch_personal_info, fetch_server_url, format_personal_info,
    format_escola_info, get_openai_client
)

def chat_page():
    st.title("PyaGPT - Assistente Virtual do Instituto Piaget")
    st.subheader("Bem-vindo ao PyaGPT!")

    server_url = fetch_server_url()  # Fetch server URL dynamically
    if not server_url:
        st.error("Não foi possível obter o URL do servidor.")
        return

    try:
        models_info = get_models_info(server_url)
        available_models = extract_model_names(models_info)
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
                "Você é o assistente virtual PyaGPT da Escola Superior de Tecnologia e Gestão Jean Piaget. "
                "Utilize as informações detalhadas sobre a Escola e informações pessoais do utilizador, se disponíveis. "
                "Responda apenas a perguntas sobre a Escola Superior de Tecnologia e Gestão Jean Piaget em Almada e forneça informações "
                "precisas e detalhadas com base nas informações fornecidas. Responda em Português de Portugal. "
                "Apenas responde ao que for perguntado e não divulgue informação se essa não for pedida."
            )
        }
        st.session_state.welcome_message_added = False

    st.session_state.escola_info = fetch_escola_info()

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

    for message in st.session_state.messages:
        if message["role"] != "system":
            avatar = "🤖" if message["role"] == "assistant" else "😎"
            label = "PyaGPT" if message["role"] == "assistant" else capitalize_first_letter(st.session_state.username) if st.session_state.get('logged_in') else "**Convidado**"
            with message_container.chat_message(message["role"], avatar=avatar):
                st.markdown(f"**{label}:** {message['content']}")

    if prompt := st.chat_input("Introduza uma pergunta aqui..."):
        try:
            user_label = capitalize_first_letter(st.session_state.username) if st.session_state.get('logged_in') else "**Convidado**"
            st.session_state.messages.append({"role": "user", "content": prompt})
            with message_container.chat_message("user", avatar="😎"):
                st.markdown(f"**{user_label}:** {prompt}")

            context = ""

            if st.session_state.get('logged_in'):
                personal_info = fetch_personal_info(st.session_state.username)
                if personal_info:
                    context += format_personal_info(personal_info) + "\n"
                else:
                    st.warning("Informações pessoais não carregadas.", icon="⚠️")

            escola_info = st.session_state.escola_info
            if escola_info:
                context += format_escola_info(escola_info)
            else:
                st.warning("Informações da escola não carregadas.", icon="⚠️")

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

                response_placeholder.markdown(f"**PyaGPT:** {response}", unsafe_allow_html=True)

            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"Ocorreu um erro: {e}", icon="⛔️")
