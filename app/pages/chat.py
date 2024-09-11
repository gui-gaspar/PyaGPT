import os
import pandas as pd
import streamlit as st
from datetime import datetime
import pytz
import requests
from utils import (
    fetch_contatos, fetch_cursos, fetch_server_url, get_modelos_info, extract_model_names, get_openai_client,
    fetch_curso_info, fetch_horarios, fetch_plano_estudos, fetch_escolas, fetch_institutos, fetch_orgaos_gestao
)

# Clear cached data if necessary
st.cache_data.clear()

def get_current_time():
    tz = pytz.timezone('Europe/Lisbon')
    current_time_utc = datetime.now(pytz.utc)
    current_time_local = current_time_utc.astimezone(tz)
    return current_time_local.strftime('%H:%M')

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

    # Fetch informações
    if "contatos_info" not in st.session_state:
        st.session_state.contatos_info = fetch_contatos()
        
    if "cursos_info" not in st.session_state:
        st.session_state.cursos_info = fetch_cursos()
    
    if "curso_info" not in st.session_state:
        st.session_state.curso_info = fetch_curso_info()
        
    if "plano_estudos" not in st.session_state:
        st.session_state.plano_estudos = fetch_plano_estudos()
        
    if "escolas" not in st.session_state:
        st.session_state.escolas = fetch_escolas()
        
    if "institutos" not in st.session_state:
        st.session_state.institutos = fetch_institutos()
        
    if "orgaos_gestao" not in st.session_state:
        st.session_state.orgaos_gestao = fetch_orgaos_gestao()

    if st.session_state.get('logged_in') and "horarios" not in st.session_state:
        st.session_state.horarios = fetch_horarios()

    # Formatting functions

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
    
    def format_horarios(horarios: list) -> pd.DataFrame:
        if not horarios:
            return pd.DataFrame(columns=['Ano Acadêmico', 'Curso', 'Cadeira', 'Dia do Mês', 'Mês', 'Ano', 'Dia', 'Hora Início', 'Hora Fim'])
        formatted_horarios = []
        for horario in horarios:
            if isinstance(horario, dict):
                formatted_horarios.append({
                    'Ano Acadêmico': horario.get('ano_academico', 'Informações não disponíveis'),
                    'Curso': horario.get('curso', 'Informações não disponíveis'),
                    'Cadeira': horario.get('cadeira', 'Informações não disponíveis'),
                    'Dia do Mês': horario.get('dia_do_mes', 'Informações não disponíveis'),
                    'Mês': horario.get('mes', 'Informações não disponíveis'),
                    'Ano': horario.get('ano', 'Informações não disponíveis'),
                    'Dia': horario.get('dia', 'Informações não disponíveis'),
                    'Hora Início': horario.get('hora_inicio', 'Informações não disponíveis'),
                    'Hora Fim': horario.get('hora_fim', 'Informações não disponíveis')
                })
            else:
                formatted_horarios.append({
                    'Ano Acadêmico': 'Informações não disponíveis',
                    'Curso': 'Informações não disponíveis',
                    'Cadeira': 'Informações não disponíveis',
                    'Dia do Mês': 'Informações não disponíveis',
                    'Mês': 'Informações não disponíveis',
                    'Ano': 'Informações não disponíveis',
                    'Dia': 'Informações não disponíveis',
                    'Hora Início': 'Informações não disponíveis',
                    'Hora Fim': 'Informações não disponíveis'
                })
        return pd.DataFrame(formatted_horarios)

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
        st.session_state.system_message = {
            "role": "system",
            "content": (
                "Você é o assistente virtual PyaGPT do Instituto Piaget. "
                "Responda em Português de Portugal e utilize as informações detalhadas sobre o Instituto Piaget. "
                f"{contatos_formatted}\n"
                "Responda a perguntas sobre a escola usando as informações fornecidas."
            )
        }
    elif st.session_state.get("cursos_info"):
        cursos_info = st.session_state.cursos_info
        cursos_formatted = format_cursos(cursos_info)
        st.session_state.system_message = {
            "role": "system",
            "content": (
                "Você é o assistente virtual PyaGPT do Instituto Piaget. "
                "Responda em Português de Portugal e utilize as informações detalhadas sobre os cursos oferecidos. "
                f"{cursos_formatted}\n"
                "Responda a perguntas sobre a escola usando as informações fornecidas."
            )
        }
    elif st.session_state.get("curso_info"):
        curso_info = st.session_state.curso_info
        curso_info_formatted = format_curso_info(curso_info)
        st.session_state.system_message = {
            "role": "system",
            "content": (
                "Você é o assistente virtual PyaGPT do Instituto Piaget. "
                "Responda em Português de Portugal e utilize as informações detalhadas sobre o curso oferecido. "
                f"{curso_info_formatted}\n"
                "Responda a perguntas sobre a escola usando as informações fornecidas."
            )
        }
    elif st.session_state.get("plano_estudos"):
        plano_estudos = st.session_state.plano_estudos
        plano_estudos_formatted = format_plano_estudos(plano_estudos)
        st.session_state.system_message = {
            "role": "system",
            "content": (
                "Você é o assistente virtual PyaGPT do Instituto Piaget. "
                "Responda em Português de Portugal e utilize as informações detalhadas sobre o plano de estudos. "
                f"{plano_estudos_formatted}\n"
                "Responda a perguntas sobre a escola usando as informações fornecidas."
            )
        }
    elif st.session_state.get("escolas"):
        escolas = st.session_state.escolas
        escolas_formatted = format_escolas(escolas)
        st.session_state.system_message = {
            "role": "system",
            "content": (
                "Você é o assistente virtual PyaGPT do Instituto Piaget. "
                "Responda em Português de Portugal e utilize as informações detalhadas sobre as escolas. "
                f"{escolas_formatted}\n"
                "Responda a perguntas sobre a escola usando as informações fornecidas."
            )
        }
    elif st.session_state.get("institutos"):
        institutos = st.session_state.institutos
        institutos_formatted = format_institutos(institutos)
        st.session_state.system_message = {
            "role": "system",
            "content": (
                "Você é o assistente virtual PyaGPT do Instituto Piaget. "
                "Responda em Português de Portugal e utilize as informações detalhadas sobre os institutos. "
                f"{institutos_formatted}\n"
                "Responda a perguntas sobre a escola usando as informações fornecidas."
            )
        }
    elif st.session_state.get("orgaos_gestao"):
        orgaos_gestao = st.session_state.orgaos_gestao
        orgaos_gestao_formatted = format_orgaos_gestao(orgaos_gestao)
        st.session_state.system_message = {
            "role": "system",
            "content": (
                "Você é o assistente virtual PyaGPT do Instituto Piaget. "
                "Responda em Português de Portugal e utilize as informações detalhadas sobre os órgãos de gestão. "
                f"{orgaos_gestao_formatted}\n"
                "Responda a perguntas sobre a escola usando as informações fornecidas."
            )
        }
    elif st.session_state.get("horarios_info"):
        horarios_info = st.session_state.horarios_info
        horarios_formatted = format_horarios(horarios_info)
        st.session_state.system_message = {
            "role": "system",
            "content": (
                "Você é o assistente virtual PyaGPT do Instituto Piaget. "
                "Responda em Português de Portugal e utilize as informações detalhadas sobre os horários. "
                f"{horarios_formatted}\n"
                "Responda a perguntas sobre a escola usando as informações fornecidas."
            )
        }
    else:
        st.session_state.system_message = {
            "role": "system",
            "content": (
                "Você é o assistente virtual PyaGPT do Instituto Piaget. "
                "Responda em Português de Portugal."
            )
        }

    # Assign user label based on login status, showing nome_completo if available
    if st.session_state.get('logged_in') and st.session_state.get('nome_completo'):
        user_label = f"**{st.session_state['nome_completo']}**"
    else:
        user_label = "Convidado"

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