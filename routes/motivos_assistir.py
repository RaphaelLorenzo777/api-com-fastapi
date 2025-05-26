from fastapi import APIRouter, Response, status
from mysql.connector import Error
from models.models import Motivo_Assistir
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
def criar_motivo_assistir(motivo_assistir: Motivo_Assistir):
    query = "INSERT INTO motivo_assistir (id, id_serie, motivo) VALUES (%s, %s, %s)"
    params = (motivo_assistir.id, motivo_assistir.id_serie, motivo_assistir.motivo)
    cursor = executar_query(query, params)
    return {"id": cursor.lastrowid, "mensagem": "Motivo_Assistir criado com sucesso"}

@router.get("/")
def listar_motivos_assistir():
    query = "SELECT * FROM motivo_assistir"
    return executar_query(query, fetch=True, dictionary=True)

@router.put("/")
def atualizar_motivo_assistir(motivo_assistir: Motivo_Assistir):
    query = "UPDATE motivo_assistir SET motivo = %s WHERE id = %s"
    params = (motivo_assistir.motivo, motivo_assistir.id)
    cursor = executar_query(query, params)
    if isinstance(cursor, Response) or cursor.rowcount == 0:
        return Response(content="Motivo_Assistir não encontrado", status_code=status.HTTP_404_NOT_FOUND)
    return {"mensagem": "Motivo_Assistir atualizado com sucesso"}

@router.delete("/")
def deletar_motivo_assistir(id: int):
    query = "DELETE FROM motivo_assistir WHERE id = %s"
    params = (id,)
    cursor = executar_query(query, params)
    if isinstance(cursor, Response) or cursor.rowcount == 0:
        return Response(content="Motivo_Assistir não encontrado", status_code=status.HTTP_404_NOT_FOUND)
    return {"mensagem": "Motivo_Assistir deletado com sucesso"}

