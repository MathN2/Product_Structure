from dataclasses import dataclass


@dataclass
class ItemDTO:
    nome: str
    descricao: str
    preco: float
    item_id: int | None = None
