from dataclasses import dataclass


@dataclass
class ItemDTO():
    node_id: int
    tree_id: int
    parent_id: int
    nome: str
    quantidade: int
    preco: float