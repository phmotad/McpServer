import fdb
from contextlib import contextmanager
from config import settings

@contextmanager
def get_db_connection():
    conn = fdb.connect(
        host=settings.FIREBIRD_HOST,
        database=settings.FIREBIRD_DATABASE,
        user=settings.FIREBIRD_USER,
        password=settings.FIREBIRD_PASSWORD,
        charset=settings.FIREBIRD_CHARSET,
        port=settings.FIREBIRD_PORT
    )
    try:
        yield conn
    finally:
        conn.close()

def execute_query(query: str, params: tuple = None):
    with get_db_connection() as conn:
        cur = conn.cursor()
        try:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            
            if cur.description:
                columns = [desc[0] for desc in cur.description]
                results = [dict(zip(columns, row)) for row in cur.fetchall()]
                return {"columns": columns, "results": results}
            
            conn.commit()
            return {"message": "Query executed successfully"}
            
        except Exception as e:
            conn.rollback()
            raise e