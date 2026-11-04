from typing import Annotated

from fastapi import APIRouter, Query

from product_structure.dto.node_dto import NodeDTO
from product_structure.schemas.formula_scheme import FormulaCreate
from product_structure.schemas.node_schema import NodeCreate, NodeUpdate
from product_structure.services.formula_service import (
    atualizar_nome_formula,
    atualizar_quantidade_node,
    buscar_arvore_formula,
    buscar_todas_formulas,
    criar_formula,
    explosao,
    remover_formula,
    remover_item_formula,
)
from product_structure.services.formula_service import (
    inserir_node as inserir_node_formula,
)

router = APIRouter(
    prefix="/formulas",
    tags=["Fórmulas"]
)


# ====================================
#               GET
# ====================================
@router.get("/")
def listar_formulas():
    return buscar_todas_formulas()

@router.get("/{formula_id}")
def buscar_formula(
    formula_id: int, quantidade_producao: Annotated[int, Query(ge=1)] = 1
):
    arvore = buscar_arvore_formula(formula_id)
    return explosao(arvore, quantidade_producao)

# ====================================
#               POST
# ====================================
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
    
    resultado = inserir_node_formula(dados)
    return {
        "node_id": resultado.node_id,
        "item_id": resultado.value.id,
        "parent_id": resultado.parent_id,
        "quantidade": resultado.quantidade
    }


# ====================================
#               PATCH
# ====================================

@router.patch("/{formula_id}/nodes/{node_id}")
def atualizar_node(
    formula_id: int, node_id: int, node: NodeUpdate
):
    atualizar_quantidade_node(formula_id, node_id, node.quantidade)
    return {
        "mensagem": "Quantidade do componente atualizada com sucesso.",
        "node_id": node_id,
        "quantidade": node.quantidade,
    }


@router.patch("/{formula_id}")
def atualizar_formula(formula_id: int, formula: FormulaCreate):
    atualizar_nome_formula(formula_id, formula.nome)

    return {
        "mensagem": "Fórmula atualizada com sucesso.",
        "id": formula_id,
        "nome": formula.nome
    }


# ====================================
#              DELETE
# ====================================

@router.delete("/{formula_id}")
def excluir_formula(formula_id: int):
    remover_formula(formula_id)

    return {
        "mensagem": "Fórmula removida com sucesso."
    }


@router.delete("/{formula_id}/nodes/{node_id}")
def excluir_node(formula_id: int, node_id: int):
    # Verifica se o nó pertence à fórmula informada.
    arvore = buscar_arvore_formula(formula_id)

    if node_id not in arvore.nodes:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail="Componente não encontrado nesta fórmula."
        )

    remover_item_formula(node_id)

    return {
        "mensagem": "Componente removido com sucesso.",
        "node_id": node_id
    }
