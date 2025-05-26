from pydantic import BaseModel, conint
import datetime
from typing import Optional

class Serie(BaseModel):
    id: Optional[int] = None
    titulo: str
    descricao: str
    ano: int
    id_categoria: int

class Categoria(BaseModel):
    id: Optional[int] = None
    nome: str

class Ator(BaseModel):
    id: Optional[int] = None
    nome: str

class Ator_Serie(BaseModel):
    id_serie: int
    id_ator: int
    personagem: str

class Avaliacao_Serie(BaseModel):
    id: Optional[int] = None
    id_serie: int
    nota: conint(ge=0, le=10)  
    comentario: str
    data_avaliacao: datetime.datetime

class Motivo_Assistir(BaseModel):
    id: Optional[int] = None
    id_serie: int
    motivo: str
