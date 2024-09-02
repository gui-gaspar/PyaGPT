O projeto PyaGPT é uma aplicação inovadora que utiliza diversas tecnologias para criar um assistente virtual especializado em fornecer informações sobre o Instituto Piaget. A interface de utilizador é desenvolvida em Streamlit, enquanto o backend é gerido pelo FastAPI, garantindo uma comunicação eficiente entre os diversos componentes do sistema. A base de dados gráfica Neo4j armazena todas as informações essenciais sobre o instituto, como contatos e cursos, e ao mesmo tempo, informações especificas para os utilizadores conectados, como as suas informações básicas e horários do curso, permitindo assim obter sempre respostas contextuais e personalizadas. A integração com a API da Ollama permite o uso de modelos de linguagem avançados para responder às perguntas dos utilizadores de forma mais precisa e relevante. O PyaGPT é, assim, uma ferramenta interativa, fácil e eficiente, ideal para facilitar o acesso a informações institucionais do Piaget.


Os modelos do Ollama devem ser previamente instalados.

É recomendado utilizar os seguintes modelos:

•   https://ollama.com/library/llama3.1 (para o chat em geral)
•   https://ollama.com/library/llava (para a análise de imagens e pdfs)

Podem ser instalados através dos comandos:

•   ollama run llama3.1
•   ollama run llava

Após a instalação do modelo, aceda ao diretório onde os modelos foram instalados no seu computador, geralmente no Windows encontram-se no diretório: 

•	“C:\Users\USER\.ollama\models” (em que “USER” corresponde ao utilizador do sistema) 

Se optar por Linux, terá de entrar no diretório: 

•	“/usr/share/ollama/.ollama/models”

Feito isso, apenas tem de copiar as pastas “blobs” e “manifests” para o diretório do projeto, especificamente “ollama\models”, que devem ser previamente criadas a partir da pasta “root” do projeto PyaGPT, isto caso ainda não estejam. Esta etapa é completamente essencial para garantir que o modelo seja corretamente carregado pelo sistema durante a execução do projeto.


Para executar o PyaGPT, é necessário executar o comando "docker-compose up --build" na pasta principal ou o script "run_docker.bat".

Na base de dados Neo4j, os dados devem ser copiados atraves dos ficheiros da pasta "sql" pela ordem que aparecem:
1_importar_dados.sql
2_importar_relacoes.sql
