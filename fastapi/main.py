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
    
@app.get("/models")
async def get_models():
    try:
        # Fetch models from the OpenAI endpoint
        openai_url = f"{server_url}/models"
        headers = {
            "Authorization": f"Bearer {api_key}"  # Use the API key from the client configuration
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(openai_url, headers=headers)
            response.raise_for_status()
            models_info = response.json()
            return models_info
    except httpx.HTTPStatusError as http_err:
        raise HTTPException(status_code=response.status_code, detail=str(http_err))
    except httpx.RequestError as req_err:
        raise HTTPException(status_code=500, detail=str(req_err))

@app.post("/login")
async def login(request: LoginRequest):
    query = """
    MATCH (u:User {username: $username, password: $password})
    RETURN u
    """
    with driver.session() as session:
        result = session.run(query, username=request.username, password=request.password)
        user = result.single()
        if user:
            return {"valid": True}
        return {"valid": False}

@app.get("/escola_info")
async def get_escola_info():
    query = """
    MATCH (e:Escola {nome: 'Escola Superior de Tecnologia e Gestão Jean Piaget'})
    RETURN e.nome AS nome, e.historia AS historia, e.telefone AS telefone, e.email AS email, e.endereco AS endereco, e.cursos AS cursos
    """
    with driver.session() as session:
        result = session.run(query)
        record = result.single()
        if record:
            return {
                "nome": record["nome"],
                "historia": record["historia"],
                "telefone": record["telefone"],
                "email": record["email"],
                "endereco": record["endereco"],
                "cursos": record["cursos"]
            }
        raise HTTPException(status_code=404, detail="Escola info not found")

@app.get("/personal_info/{username}")
async def get_personal_info(username: str):
    query = """
    MATCH (u:User {username: $username})
    RETURN u.username AS username, u.full_name AS full_name, u.email AS email,
           u.phone AS phone, u.address AS address, u.courses_enrolled AS courses_enrolled,
           u.grades AS grades, u.additional_info AS additional_info
    """
    with driver.session() as session:
        result = session.run(query, username=username)
        record = result.single()
        if record:
            grades_str = record.get("grades", "{}")
            try:
                grades = json.loads(grades_str) if grades_str else {}  # Ensure it's a dictionary
            except json.JSONDecodeError:
                grades = {}  # Default to an empty dictionary if parsing fails
            return {
                "username": record["username"],
                "full_name": record["full_name"],
                "email": record["email"],
                "phone": record["phone"],
                "address": record["address"],
                "courses_enrolled": record["courses_enrolled"],
                "grades": grades,  # Ensure it's a dictionary
                "additional_info": record["additional_info"]
            }
        raise HTTPException(status_code=404, detail="Personal info not found")


