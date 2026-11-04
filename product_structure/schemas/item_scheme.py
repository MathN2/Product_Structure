from pydantic import BaseModel, Field, field_validator


class ItemCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=150)
    descricao: str = ""
    preco: float = Field(ge=0)

    @field_validator("nome")
    @classmethod
    def nome_sem_espacos(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("O nome do item é obrigatório.")
        return value


class ItemUpdate(ItemCreate):
    pass
