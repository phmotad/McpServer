from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from fastapi_mcp import FastApiMCP
import secrets
from typing import Dict, Any
from config import settings
from models import SQLQueryRequest, SQLQueryResult, execute_sql

app = FastAPI(
    title="SQL Query MCP Server",
    description="Servidor MCP para execução de consultas SQL em banco Firebird",
    version="1.0.0"
)

# Configuração do MCP
mcp = FastApiMCP(
    app,
    name="SQL Query MCP",
    description="Servidor MCP para consultas SQL em banco Firebird via AI Agents",
    base_url="http://localhost:8000"
)

security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    """Validação de autenticação básica"""
    correct_username = secrets.compare_digest(credentials.username, settings.API_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, settings.API_PASSWORD)
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.post("/api/sql/execute", response_model=SQLQueryResult, tags=["SQL"], operation_id="execute_sql_query")
async def execute_sql_query(
    request: SQLQueryRequest,
    username: str = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Executa uma consulta SQL no banco Firebird.
    
    Este endpoint permite que AI Agents executem consultas SQL parametrizadas no banco de dados Firebird.
    As consultas são executadas com autenticação e proteção contra SQL injection.
    
    Args:
        request: Objeto contendo a consulta SQL e seus parâmetros
        username: Usuário autenticado (via Basic Auth)
        
    Returns:
        Resultado da consulta com colunas e dados, ou mensagem de erro
    """
    try:
        result = await execute_sql(request)
        return result
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": str(e)}
        )

@app.get("/", tags=["Health"], operation_id="health_check")
async def root():
    """
    Endpoint de verificação de saúde do servidor.
    Retorna o status atual do servidor e informações sobre o endpoint MCP.
    """
    return {
        "status": "ok", 
        "message": "SQL Query MCP Server está funcionando",
        "endpoint_mcp": "/mcp"
    }

# Montando o servidor MCP
mcp.mount()