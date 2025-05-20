from fastapi import APIRouter, HTTPException
from mysql.connector import Error
from models.models import Ator_Serie
from models.database import get_connection
from app.main import erro_404

router = APIRouter(prefix="/atores_series")

def executar_query(query, params=None, fetch=False, dictionary=False):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=dictionary)
        cursor.execute(query, params or ())
        if fetch:
            return cursor.fetchall()
        conn.commit()
        return cursor
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

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
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Ator_serie não encontrado")
    return {"mensagem": "Ator_serie atualizado com sucesso"}

@router.delete("/")
def deletar_ator_serie(id_ator: int, id_serie: int):
    query = "DELETE FROM ator_serie WHERE id_ator = %s AND id_serie = %s"
    params = (id_ator, id_serie)
    cursor = executar_query(query, params)
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Ator_serie não encontrado")
    return {"mensagem": "Ator_serie deletado com sucesso"}