from fastapi import APIRouter, Response, status
from mysql.connector import Error
from models.models import Avaliacao_Serie
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
def criar_avaliacao_serie(avaliacao_serie: Avaliacao_Serie):
    query = "INSERT INTO avaliacao_serie (id, id_serie, nota, comentario, data_avaliacao) VALUES (%s, %s, %s, %s, %s)"
    params = (avaliacao_serie.id, avaliacao_serie.id_serie, avaliacao_serie.nota, avaliacao_serie.comentario, avaliacao_serie.data_avaliacao)
    cursor = executar_query(query, params)
    return {"id": cursor.lastrowid, "mensagem": "Avaliacao_Serie criado com sucesso"}

@router.get("/")
def listar_avaliacoes_series():
    query = "SELECT * FROM avaliacao_serie"
    return executar_query(query, fetch=True, dictionary=True)

@router.put("/")
def atualizar_avaliacao_serie(avaliacao_serie: Avaliacao_Serie):
    query = "UPDATE avaliacao_serie SET nota = %s, comentario = %s, data_avaliacao = %s WHERE id = %s AND id_serie = %s"
    params = (avaliacao_serie.nota, avaliacao_serie.comentario, avaliacao_serie.data_avaliacao, avaliacao_serie.id, avaliacao_serie.id_serie)
    cursor = executar_query(query, params)
    if isinstance(cursor, Response) or cursor.rowcount == 0:
        return Response(content="Avaliacao_Serie não encontrado", status_code=status.HTTP_404_NOT_FOUND)
    return {"mensagem": "Avaliacao_Serie atualizado com sucesso"}

@router.delete("/")
def deletar_avaliacao_serie(id: int):
    query = "DELETE FROM avaliacao_serie WHERE id = %s"
    params = (id,)
    cursor = executar_query(query, params)
    if isinstance(cursor, Response) or cursor.rowcount == 0:
        return Response(content="Avaliacao_Serie não encontrado", status_code=status.HTTP_404_NOT_FOUND)
    return {"mensagem": "Avaliacao_Serie deletado com sucesso"}
