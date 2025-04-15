from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from database import execute_query

class SQLQueryRequest(BaseModel):
    query: str
    parameters: Optional[List[Any]] = None

class SQLQueryResult(BaseModel):
    columns: Optional[List[str]] = None
    results: Optional[List[Dict[str, Any]]] = None
    message: Optional[str] = None
    error: Optional[str] = None

async def execute_sql(request: SQLQueryRequest) -> SQLQueryResult:
    try:
        result = execute_query(request.query, tuple(request.parameters) if request.parameters else None)
        return SQLQueryResult(**result)
    except Exception as e:
        return SQLQueryResult(error=str(e))