from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=150)
    descricao: str = ""
    preco: float = Field(ge=0)
