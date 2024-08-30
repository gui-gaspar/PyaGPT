from fastapi import FastAPI, HTTPException
from neo4j import GraphDatabase
from pydantic import BaseModel
import toml
import json
import httpx
from openai import OpenAI

app = FastAPI()

# Load secrets from secrets.toml
def load_secrets():
    try:
        secrets = toml.load('.secrets/secrets.toml')
        neo4j_secrets = secrets['neo4j']
        openai_secrets = secrets['openai']
        return neo4j_secrets, openai_secrets
    except FileNotFoundError:
        raise RuntimeError("Secrets file not found.")
    except toml.TomlDecodeError:
        raise RuntimeError("Error decoding secrets file.")

neo4j_secrets, openai_secrets = load_secrets()
NEO4J_URI = neo4j_secrets.get("uri")
NEO4J_USER = neo4j_secrets.get("user")
NEO4J_PASSWORD = neo4j_secrets.get("password")

# Create a Neo4J driver instance
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Initialize OpenAI client
server_url = openai_secrets.get("server_url")
server_url_generate = openai_secrets.get("server_url_generate")
api_key = openai_secrets.get("api_key")
client = OpenAI(
    base_url=server_url,
    api_key=api_key,
)

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/")
async def root():
    return {
        "message": "Bem-vindo ao backend FastAPI do PyaGPT!",
        "description": "Este backend fornece APIs para interagir com uma base de dados Neo4j, autenticação de utilizadores, e integração com modelos da OpenAI. "
                       "Utilize as várias rotas disponíveis para obter informações sobre a escola, dados pessoais, e muito mais.",
        "endpoints": {
            "/server_url": "Obtém o URL do servidor usado para inicializar o cliente OpenAI.",
            "/server_url_generate": "Obtém o URL usado para requisições de geração de texto via API.",
            "/modelos": "Lista os modelos disponíveis no servidor OpenAI configurado.",
            "/login": "Autentica um utilizador com nome de utilizador e senha.",
            "/escola_info": "Obtém informações detalhadas sobre a escola específica.",
            "/personal_info/{username}": "Obtém informações pessoais detalhadas para um utilizador específico."
        }

    }


@app.get("/server_url")
async def get_server_url():
    try:
        # Return server URL and additional info
        return {
            "server_url": server_url,
            "message": "This endpoint returns the server URL used for OpenAI client initialization.",
            "status": "success"
        }
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
@app.get("/server_url_generate")
async def get_server_url():
    try:
        # Return server URL and additional info
        return {
            "server_url_generate": server_url_generate,
            "message": "This endpoint provides the URL used for making generation API requests.",
            "status": "success"
        }
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
@app.get("/modelos")
async def get_modelos():
    try:
        # Fetch models from the OpenAI endpoint
        openai_url = f"{server_url}/models"
        headers = {
            "Authorization": f"Bearer {api_key}"  # Use the API key from the client configuration
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(openai_url, headers=headers)
            response.raise_for_status()
            modelos_info = response.json()
            return modelos_info
    except httpx.HTTPStatusError as http_err:
        raise HTTPException(status_code=response.status_code, detail=str(http_err))
    except httpx.RequestError as req_err:
        raise HTTPException(status_code=500, detail=str(req_err))

@app.post("/login")
async def login(request: LoginRequest):
    query = """
    MATCH (u:Utilizadores {username: $username, password: $password})
    RETURN u
    """
    with driver.session() as session:
        result = session.run(query, username=request.username, password=request.password)
        user = result.single()
        if user:
            return {"valid": True}
        return {"valid": False}

# Endpoints para Nodes

@app.get("/contatos")
async def get_contatos():
    query = """
    MATCH (c:Contato)
    RETURN c.instituto AS instituto, c.tipo AS tipo, c.morada AS morada, 
           c.codigo_postal AS codigo_postal, c.telefone AS telefone, c.fax AS fax, 
           c.email AS email, c.gps AS gps, c.nome AS nome, c.skype AS skype, 
           c.horario AS horario
    """
    with driver.session() as session:
        result = session.run(query)
        records = [record.data() for record in result]
        if records:
            return records
        raise HTTPException(status_code=404, detail="Contatos not found")

@app.get("/cursos")
async def get_cursos():
    query = """
    MATCH (c:Curso)
    RETURN c.tipo AS tipo, c.curso AS curso, c.escola AS escola
    """
    with driver.session() as session:
        result = session.run(query)
        records = [record.data() for record in result]
        if records:
            return records
        raise HTTPException(status_code=404, detail="Cursos not found")


@app.get("/curso_info")
async def get_curso_info():
    query = """
    MATCH (c:CursoInfo)
    RETURN c.curso AS curso, c.saídas_profissionais AS saídas_profissionais, 
           c.estatuto_profissional AS estatuto_profissional, c.apresentação AS apresentação,
           c.acesso_a_outros_ciclos AS acesso_a_outros_ciclos, c.área_de_estudo AS área_de_estudo,
           c.regras_de_avaliação AS regras_de_avaliação, c.acesso AS acesso, c.diploma AS diploma
    """
    with driver.session() as session:
        result = session.run(query)
        records = [record.data() for record in result]
        if records:
            return records
        raise HTTPException(status_code=404, detail="No curso info found")

@app.get("/plano_estudos")
async def get_plano_estudos():
    query = """
    MATCH (p:PlanoEstudos)
    RETURN p.tipo AS tipo, p.curso AS curso, p.ano AS ano, p.semestre AS semestre,
           p.unidade_curricular AS unidade_curricular, p.ch AS ch, p.ects AS ects
    ORDER BY p.curso, p.ano, p.semestre
    """
    with driver.session() as session:
        result = session.run(query)
        records = [record.data() for record in result]
        if records:
            return records
        raise HTTPException(status_code=404, detail="No plano de estudos found")


@app.get("/escolas")
async def get_escolas():
    query = """
    MATCH (e:Escola)
    RETURN e.nome AS escola, e.descricao AS descricao
    """
    with driver.session() as session:
        result = session.run(query)
        records = [record.data() for record in result]
        if records:
            return records
        raise HTTPException(status_code=404, detail="Escolas not found")

@app.get("/institutos")
async def get_institutos():
    query = """
    MATCH (i:Instituto)
    RETURN i.nome AS instituto
    """
    with driver.session() as session:
        result = session.run(query)
        records = [record.data() for record in result]
        if records:
            return records
        raise HTTPException(status_code=404, detail="Institutos not found")


@app.get("/orgaos_de_gestao")
async def get_orgaos_gestao():
    query = """
    MATCH (o:OrgaosGestao)
    RETURN o.escola AS escola, o.função AS função, o.nome AS nome
    """
    with driver.session() as session:
        result = session.run(query)
        records = [record.data() for record in result]
        if records:
            return records
        raise HTTPException(status_code=404, detail="Órgãos de gestão not found")

@app.get("/utilizadores")
async def get_utilizadores():
    query = "MATCH (u:Utilizadores) RETURN u"
    with driver.session() as session:
        result = session.run(query)
        records = [dict(record["u"]) for record in result]
        return {"utilizadores": records}

@app.get("/utilizadores/{username}")
async def get_utilizador(username: str):
    query = "MATCH (u:Utilizadores {username: $username}) RETURN u"
    with driver.session() as session:
        result = session.run(query, username=username)
        user = result.single()
        if user:
            return {"utilizador": dict(user["u"])}
        raise HTTPException(status_code=404, detail=f"Utilizador com username '{username}' não encontrado.")

# Endpoints para Relações

@app.get("/relacoes/oferece_curso")
async def relacao_oferece_curso():
    query = """
    MATCH (e:Escola)-[:OFERECE]->(c:Curso)
    RETURN e.nome AS Escola, c.curso AS Curso
    """
    with driver.session() as session:
        result = session.run(query)
        records = [record.data() for record in result]
        return {"relacoes": records}

@app.get("/relacoes/tem_info")
async def relacao_tem_info():
    query = """
    MATCH (c:Curso)-[:TEM_INFO]->(ci:CursoInfo)
    RETURN c.curso AS Curso, ci.curso AS CursoInfo
    """
    with driver.session() as session:
        result = session.run(query)
        records = [record.data() for record in result]
        return {"relacoes": records}

@app.get("/relacoes/tem_horario")
async def relacao_tem_horario():
    query = """
    MATCH (c:Curso)-[:TEM_HORARIO]->(h:Horarios)
    RETURN c.curso AS Curso, h.cadeira AS Cadeira, h.hora_inicio AS HoraInicio, h.hora_fim AS HoraFim
    """
    with driver.session() as session:
        result = session.run(query)
        records = [record.data() for record in result]
        return {"relacoes": records}

@app.get("/relacoes/gerido_por")
async def relacao_gerido_por():
    query = """
    MATCH (e:Escola)-[:GERIDO_POR]->(o:OrgaosGestao)
    RETURN e.nome AS Escola, o.nome AS OrgãoGestão
    """
    with driver.session() as session:
        result = session.run(query)
        records = [record.data() for record in result]
        return {"relacoes": records}

@app.get("/relacoes/tem_plano_de_estudos")
async def relacao_tem_plano_de_estudos():
    query = """
    MATCH (c:Curso)-[:TEM_PLANO_DE_ESTUDOS]->(p:PlanoEstudos)
    RETURN c.curso AS Curso, p.unidade_curricular AS UnidadeCurricular, p.ch AS CH
    """
    with driver.session() as session:
        result = session.run(query)
        records = [record.data() for record in result]
        return {"relacoes": records}

@app.get("/relacoes/oferece")
async def relacao_oferece():
    query = """
    MATCH (i:Instituto)-[:OFERECE]->(e:Escola)
    RETURN i.nome AS Instituto, e.nome AS Escola
    """
    with driver.session() as session:
        result = session.run(query)
        records = [record.data() for record in result]
        return {"relacoes": records}

@app.get("/relacoes/tem_contato_instituto")
async def relacao_tem_contato_instituto():
    query = """
    MATCH (i:Instituto)-[:TEM_CONTATO]->(c:Contato)
    RETURN i.nome AS Instituto, c.nome AS ContatoNome
    """
    with driver.session() as session:
        result = session.run(query)
        records = [record.data() for record in result]
        return {"relacoes": records}

@app.get("/relacoes/tem_contato_escola")
async def relacao_tem_contato_escola():
    query = """
    MATCH (e:Escola)-[:TEM_CONTATO]->(c:Contato)
    RETURN e.nome AS Escola, c.nome AS ContatoNome
    """
    with driver.session() as session:
        result = session.run(query)
        records = [record.data() for record in result]
        return {"relacoes": records}
    
@app.get("/relacoes/inscrito_em/{username}")
async def relacao_inscrito_em(username: str):
    query = """
    MATCH (u:Utilizadores {username: $username})-[:INSCRITO_EM]->(c:Curso)
    RETURN u.username AS Utilizador, c.curso AS Curso
    """
    with driver.session() as session:
        result = session.run(query, username=username)
        records = [record.data() for record in result]
        return {"relacoes": records}

@app.get("/relacoes/pertence_a/{username}")
async def relacao_pertence_a(username: str):
    query = """
    MATCH (u:Utilizadores {username: $username})-[:PERTENCE_A]->(e:Escola)
    RETURN u.username AS Utilizador, e.nome AS Escola
    """
    with driver.session() as session:
        result = session.run(query, username=username)
        records = [record.data() for record in result]
        return {"relacoes": records}

@app.get("/relacoes/pertence_a_instituto/{username}")
async def relacao_pertence_a_instituto(username: str):
    query = """
    MATCH (u:Utilizadores {username: $username})-[:PERTENCE_A_INSTITUTO]->(i:Instituto)
    RETURN u.username AS Utilizador, i.nome AS Instituto
    """
    with driver.session() as session:
        result = session.run(query, username=username)
        records = [record.data() for record in result]
        return {"relacoes": records}


