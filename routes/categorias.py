from fastapi import APIRouter, Response, status
from mysql.connector import Error
from models.models import Categoria
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
def criar_categoria(categoria: Categoria):
    query = "INSERT INTO categoria (id, nome) VALUES (%s, %s)"
    params = (categoria.id, categoria.nome)
    cursor = executar_query(query, params)
    return {"id": cursor.lastrowid, "mensagem": "Categoria criada com sucesso"}

@router.get("/")
def listar_categorias():
    query = "SELECT * FROM categoria"
    return executar_query(query, fetch=True, dictionary=True)

@router.put("/")
def atualizar_categoria(categoria: Categoria):
    query = "UPDATE categoria SET nome = %s WHERE id = %s"
    params = (categoria.nome, categoria.id)
    cursor = executar_query(query, params)
    if isinstance(cursor, Response) or cursor.rowcount == 0:
        return Response(content="Categoria não encontrada", status_code=status.HTTP_404_NOT_FOUND)
    return {"mensagem": "Categoria atualizada com sucesso"}

@router.delete("/")
def deletar_categoria(id: int):
    query = "DELETE FROM categoria WHERE id = %s"
    params = (id,)
    cursor = executar_query(query, params)
    if isinstance(cursor, Response) or cursor.rowcount == 0:
        return Response(content="Categoria não encontrada", status_code=status.HTTP_404_NOT_FOUND)
    return {"mensagem": "Categoria deletada com sucesso"}


