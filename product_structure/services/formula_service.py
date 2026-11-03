from product_structure.core.exceptions import *
from product_structure.core.formula import ArvoreFormula
from product_structure.core.node import Node
from product_structure.dto.item_dto import ItemDTO
from product_structure.dto.node_dto import NodeDTO
from product_structure.repository.formula_repository import (
    buscar_formula_por_id_bd,
    buscar_formula_por_nome_bd,
    buscar_todas_formulas_bd,
    criar_formula_bd,
)
from product_structure.repository.item_repository import (
    buscar_item_por_id_bd,
    buscar_item_por_nome_bd,
)
from product_structure.repository.node_repository import inserir_item_formula
from product_structure.services.item_service import criar_item


# ====================================
#       FUNÇOES BANCO DE DADOS
# ====================================
def criar_formula(nome_formula):
    # Coleta de dados
    if nome_formula is None:
        raise NodeEmptyError("Node não pode estar vazio.")

    resultado_busca = buscar_formula_por_nome(nome_formula)

    if resultado_busca is not None and resultado_busca["nome"] == nome_formula:
        raise FormulaAlreadyExistsError("Já existe uma fórmula com esse nome.")

    item = buscar_item_por_nome_bd(nome_formula)

    if item is None:
        raise ItemError(
            "Não foi possivel criar a formula porque o produto não existe em `itens`."
        )

    # Criaçao de dados
    formula_bd = criar_formula_bd(nome_formula)

    if formula_bd is None:
        raise TreeError("Falha durante a criação da arvore.")

    formula_arvore = ArvoreFormula(formula_bd["id"], formula_bd["nome"])

    node_dto = NodeDTO(formula_bd["id"], item["id"], 1)
    node = inserir_node(node_dto)

    inserir_node_arvore(formula_arvore, node)

    return formula_arvore


def criar_node(node_dto: NodeDTO):
    item_dict = buscar_item_por_id_bd(node_dto.item_id)

    if item_dict is None:
        raise NodeEmptyError(
            "Não será possivel criar o Node porque o valor está vazio."
        )

    item_dto = ItemDTO(
        item_dict["nome"],
        item_dict["descricao"],
        item_dict["preco"],
        item_dict["id"],
    )
    item = criar_item(item_dto)

    return Node(
        value=item,
        node_id=node_dto.node_id,
        formula_id=node_dto.formula_id,
        parent_id=node_dto.parent_id,
        quantidade=node_dto.quantidade,
    )


def inserir_node(node_dto: NodeDTO):
    result_id = inserir_item_formula(node_dto)

    if result_id is None:
        raise NodeValueError("Não foi possivel encontrar um ID.")

    node_dto.node_id = result_id["id"]
    node = criar_node(node_dto)

    return node


def atualizar_formula():
    pass


def remover_formula():
    pass


def buscar_todas_formulas():
    return buscar_todas_formulas_bd()


def buscar_formula_por_nome(nome):
    return buscar_formula_por_nome_bd(nome)


def buscar_formula_por_id(id):
    return buscar_formula_por_id_bd(id)


# ====================================
#          FUNÇOES DA ARVORE
# ====================================
def inserir_node_arvore(arvore: ArvoreFormula, node: Node):
    if node.node_id in arvore.nodes:
        raise NodeAlreadyExistsError(
            "Falha ao inserir item na arvore. Esse Node já existe."
        )

    arvore.inserir(node)


# FUNÇOES COMPLEMENTARES
def explosao(formula: ArvoreFormula):
    if formula.root is None:
        raise TreeEmptyError("Árvore vazia.")

    root = formula.root

    resultado = {
        "nome": root.value.nome,
        "descricao": root.value.descricao,
        "preco": implosao(formula),
        "componentes": [],
    }

    for child in root.children:
        resultado["componentes"].append(_formatacao_explosao(child))

    return resultado


def _formatacao_explosao(node: Node):
    resultado = {
        "nome": node.value.nome,
        "descricao": node.value.descricao,
        "quantidade": node.quantidade,
        "preco": node.value.preco,
        "componentes": [],
    }

    for child in node.children:
        resultado["componentes"].append(_formatacao_explosao(child))

    return resultado


def implosao(formula: ArvoreFormula):
    pass
