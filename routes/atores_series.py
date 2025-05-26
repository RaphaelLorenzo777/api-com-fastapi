from fastapi import APIRouter, Response, status
from mysql.connector import Error
from models.models import Ator_Serie
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
def criar_ator_serie(ator_serie: Ator_Serie):
    query = "INSERT INTO ator_serie (id_ator, id_serie, personagem) VALUES (%s, %s, %s)"
    params = (ator_serie.id_ator, ator_serie.id_serie, ator_serie.personagem)
    cursor = executar_query(query, params)
    return {"id": cursor.lastrowid, "mensagem": "Ator_serie criado com sucesso"}

@router.get("/")
def listar_atores_series():
    query = "SELECT * FROM ator_serie"
    return executar_query(query, fetch=True, dictionary=True)

@router.put("/")
def atualizar_ator_serie(ator_serie: Ator_Serie):
    query = "UPDATE ator_serie SET personagem = %s WHERE id_ator = %s AND id_serie = %s"
    params = (ator_serie.personagem, ator_serie.id_ator, ator_serie.id_serie)
    cursor = executar_query(query, params)
    if isinstance(cursor, Response) or cursor.rowcount == 0:
        return Response(content="Ator_serie não encontrado", status_code=status.HTTP_404_NOT_FOUND)
    return {"mensagem": "Ator_serie atualizado com sucesso"}

@router.delete("/")
def deletar_ator_serie(id_ator: int, id_serie: int):
    query = "DELETE FROM ator_serie WHERE id_ator = %s AND id_serie = %s"
    params = (id_ator, id_serie)
    cursor = executar_query(query, params)
    if isinstance(cursor, Response) or cursor.rowcount == 0:
        return Response(content="Ator_serie não encontrado", status_code=status.HTTP_404_NOT_FOUND)
    return {"mensagem": "Ator_serie deletado com sucesso"}

