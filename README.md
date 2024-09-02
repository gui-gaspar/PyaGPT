# PyaGPT

O projeto **PyaGPT** é uma aplicação inovadora que utiliza diversas tecnologias para criar um assistente virtual especializado em fornecer informações sobre o Instituto Piaget. A interface de utilizador é desenvolvida em Streamlit, enquanto o backend é gerido pelo FastAPI, garantindo uma comunicação eficiente entre os diversos componentes do sistema. A base de dados gráfica Neo4j armazena todas as informações essenciais sobre o instituto, como contatos e cursos, e ao mesmo tempo, informações especificas para os utilizadores conectados, como as suas informações básicas e horários do curso, permitindo assim obter sempre respostas contextuais e personalizadas. A integração com a API da Ollama permite o uso de modelos de linguagem avançados para responder às perguntas dos utilizadores de forma mais precisa e relevante. O PyaGPT é, assim, uma ferramenta interativa, fácil e eficiente, ideal para facilitar o acesso a informações institucionais do Piaget.

## Tecnologias Utilizadas

- **Interface do Utilizador**: Desenvolvida em **Streamlit**, proporcionando uma interface interativa e fácil de utilizar.
- **Backend**: Gerido pelo **FastAPI**, garantindo uma comunicação rápida e eficaz entre os diferentes componentes do sistema.
- **Base de Dados**: Utiliza a base de dados gráfica **Neo4j** para armazenar informações essenciais sobre o Instituto, como contactos e cursos, bem como dados específicos dos utilizadores, como informações pessoais e horários dos cursos. Isto permite que o sistema forneça respostas contextuais e personalizadas.
- **Modelos de Linguagem**: Integrado com a **API do Ollama** para utilizar modelos de linguagem avançados, oferecendo respostas precisas e relevantes às questões dos utilizadores.

## Instalação dos Modelos Ollama

Os modelos da Ollama devem ser instalados previamente para garantir o correto funcionamento do PyaGPT. Recomendamos a instalação dos seguintes modelos:

- [**Llama 3.1**](https://ollama.com/library/llama3.1): Para interações gerais no chat.
- [**Llava**](https://ollama.com/library/llava): Para análise de imagens e PDFs.

### Comandos de Instalação:

Para instalar os modelos, utilize os seguintes comandos:

```bash
ollama run llama3.1
ollama run llava
```

Após a instalação, localize o diretório onde os modelos foram instalados no seu sistema:

- **Windows**: `C:\Users\USER\.ollama\models` (substitua "USER" pelo nome do seu utilizador).
- **Linux**: `/usr/share/ollama/.ollama/models`

Copie as pastas `blobs` e `manifests` para o diretório do projeto, em `ollama\models`. Este diretório deve ser criado na raiz do projeto PyaGPT, caso ainda não exista. Esta etapa é essencial para que o modelo seja corretamente carregado durante a execução do projeto.

## Execução do Projeto

Para executar o PyaGPT, siga um dos seguintes procedimentos:

1. No diretório principal do projeto, execute o comando:
   ```bash
   docker-compose up --build
   ```

2. Alternativamente, utilize o script localizado na `root` do projeto:
   ```bash
   run_docker.bat
   ```

## Importar dados para a Base de Dados Neo4j

Os dados do Neo4j devem ser carregados utilizando os scripts SQL disponíveis na pasta `sql`:

1. `importar_dados.sql`
2. `importar_relacoes.sql`

Apenas é necessário copiar o seu conteúdo para a `prompt` do Neo4j para serem importados todos os dados referentes ao Instituto Piaget e informações pessoais dos utilizadores.