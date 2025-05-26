from fastapi import APIRouter, Response, status
from mysql.connector import Error
from models.models import Ator
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
def criar_ator(ator: Ator):
    query = "INSERT INTO ator (id, nome) VALUES (%s, %s)"
    params = (ator.id, ator.nome)
    cursor = executar_query(query, params)
    return {"id": cursor.lastrowid, "mensagem": "Ator criado com sucesso"}

@router.get("/")
def listar_atores():
    query = "SELECT * FROM ator"
    return executar_query(query, fetch=True, dictionary=True)

@router.put("/")
def atualizar_ator(ator: Ator):
    query = "UPDATE ator SET nome = %s WHERE id = %s"
    params = (ator.nome, ator.id)
    cursor = executar_query(query, params)
    if isinstance(cursor, Response) or cursor.rowcount == 0:
        return Response(content="Ator não encontrado", status_code=status.HTTP_404_NOT_FOUND)
    return {"mensagem": "Ator atualizado com sucesso"}

@router.delete("/")
def deletar_ator(id: int):
    query = "DELETE FROM ator WHERE id = %s"
    params = (id,)
    cursor = executar_query(query, params)
    if isinstance(cursor, Response) or cursor.rowcount == 0:
        return Response(content="Ator não encontrado", status_code=status.HTTP_404_NOT_FOUND)
    return {"mensagem": "Ator deletado com sucesso"}
