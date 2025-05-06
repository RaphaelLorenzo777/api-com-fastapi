from fastapi import APIRouter, Form, HTTPException
from mysql.connector import Error
from pydantic import BaseModel
from database import get_connection

router = APIRouter(prefix="/series")

class Serie(BaseModel):
    titulo: str
    descricao: str
    ano: int
    id_categoria: int

# POST via JSON
@router.post("/json")
def criar_serie_json(serie: Serie):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO serie (titulo, descricao, ano_lancamento, id_categoria) VALUES (%s, %s, %s, %s)",
            (serie.titulo, serie.descricao, serie.ano, serie.id_categoria)
        )
        conn.commit()
        novo_id = cursor.lastrowid

        return {"id": novo_id, "mensagem": "Série criada com sucesso (JSON)"}

    except Error as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

# POST via Form
@router.post("/form")
def criar_serie_form(
    titulo: str = Form(...),
    descricao: str = Form(...),
    ano: int = Form(...),
    id_categoria: int = Form(...)
):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO serie (titulo, descricao, ano_lancamento, id_categoria) VALUES (%s, %s, %s, %s)",
            (titulo, descricao, ano, id_categoria)
        )
        conn.commit()
        novo_id = cursor.lastrowid

        return {"id": novo_id, "mensagem": "Série criada com sucesso (Form)"}

    except Error as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

# GET - listar todas as séries
@router.get("/")
def listar_series():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM serie")
        series = cursor.fetchall()

        return series

    except Error as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass
