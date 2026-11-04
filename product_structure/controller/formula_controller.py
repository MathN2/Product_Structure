from fastapi import APIRouter

from product_structure.dto.node_dto import NodeDTO

from product_structure.schemas.formula_scheme import FormulaCreate
from product_structure.schemas.node_schema import NodeCreate

from product_structure.services.formula_service import (
    buscar_todas_formulas,
    buscar_arvore_formula,
    criar_formula,
    criar_node as criar_node_formula,
    explosao,
)


router = APIRouter(
    prefix="/formulas",
    tags=["Fórmulas"]
)


# -----------------------------
#        ENDPOINT GET
# -----------------------------
@router.get("/")
def listar_formulas():
    return buscar_todas_formulas()

@router.get("/{formula_id}")
def buscar_formula(formula_id: int):
    arvore = buscar_arvore_formula(formula_id)
    return explosao(arvore)

# -----------------------------
#       ENDPOINT POST
# -----------------------------
@router.post("/", status_code=201)
def criar(formula: FormulaCreate):
    resultado = criar_formula(formula.nome)

    return {
        "id": resultado.id,
        "nome": resultado.nome
    }

@router.post("/{formula_id}/nodes", status_code=201)
def criar_node(formula_id: int, node: NodeCreate):
    dados = NodeDTO(
        formula_id=formula_id,
        item_id=node.item_id,
        quantidade=node.quantidade,
        parent_id=node.parent_id,
    )
    
    resultado = criar_node_formula(dados=dados)
    return {
        "node_id": resultado.node_id,
        "item_id": resultado.value.id,
        "parent_id": resultado.parent_id,
        "quantidade": resultado.quantidade
    }