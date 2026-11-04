from pydantic import BaseModel


class FormulaCreate(BaseModel):
    nome: str