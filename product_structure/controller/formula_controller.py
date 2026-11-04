from fastapi import APIRouter

from product_structure.schemas.formula_scheme import FormulaCreate
from product_structure.schemas.node_schema import NodeCreate


router = APIRouter(
    prefix="/formulas",
    tags=["Fórmulas"]
)

@router.get("/")
def listar_formulas():
    return {"mensagem": "Listagem de formulas"}

@router.get("/{formula_id}")
def buscar_formula(formula_id: int):
    return {
        "id": formula_id,
        "mensagem": "Formula encontrada."
    }

@router.post("/")
def criar_formula(formula: FormulaCreate):
    return {
        "mensagem": "Formula recebida!",
        "nome": formula.nome
    }

@router.post("/formulas/{formula_id}/nodes")
def criar_node(node: NodeCreate):
    return {
        "mensagem": "Node recebido!",
        "item_id": node.item_id,
        "parent_id": node.parent_id,
        "quantidade": node.quantidade
    }