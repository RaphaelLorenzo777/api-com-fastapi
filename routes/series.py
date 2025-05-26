from fastapi import APIRouter, Response, status
from mysql.connector import Error
from models.models import Serie
from database import get_connection

router = APIRouter()

def executar_query(query, params=None, fetch=False, dictionary=False):
    try:
        with get_connection() as conn:
            with conn.cursor(dictionary=dictionary) as cursor:
                cursor.execute(query, params or ())
                if fetch:
                    return cursor.fetchall()
                conn.commit()
                return cursor
    except Error as e:
        return Response(
            content=f"Erro de banco de dados: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.post("/")
def criar_serie(serie: Serie):
    query = "INSERT INTO serie (id, titulo, descricao, ano_lancamento, id_categoria) VALUES (%s, %s, %s, %s, %s)"
    params = (serie.id, serie.titulo, serie.descricao, serie.ano_lancamento, serie.id_categoria)
    cursor = executar_query(query, params)
    return {"id": cursor.lastrowid, "mensagem": "Serie criada com sucesso"}

@router.get("/")
def listar_series():
    query = "SELECT * FROM serie"
    return executar_query(query, fetch=True, dictionary=True)

@router.put("/")
def atualizar_serie(serie: Serie):
    query = "UPDATE serie SET titulo = %s, descricao = %s, ano_lancamento = %s, id_categoria = %s WHERE id = %s"
    params = (serie.titulo, serie.descricao, serie.ano_lancamento, serie.id_categoria, serie.id)
    cursor = executar_query(query, params)
    if isinstance(cursor, Response) or cursor.rowcount == 0:
        return Response(content="Serie não encontrada", status_code=status.HTTP_404_NOT_FOUND)
    return {"mensagem": "Serie atualizada com sucesso"}

@router.delete("/")
def deletar_serie(id: int):
    query = "DELETE FROM serie WHERE id = %s"
    params = (id,)
    cursor = executar_query(query, params)
    if isinstance(cursor, Response) or cursor.rowcount == 0:
        return Response(content="Serie não encontrada", status_code=status.HTTP_404_NOT_FOUND)
    return {"mensagem": "Serie deletada com sucesso"}
