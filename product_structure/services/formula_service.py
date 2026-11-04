from product_structure.core.exceptions import *
from product_structure.core.formula import ArvoreFormula
from product_structure.core.node import Node
from product_structure.dto.item_dto import ItemDTO
from product_structure.dto.node_dto import NodeDTO
from product_structure.repository.formula_repository import (
    atualizar_nome_formula_bd,
    buscar_formula_por_id_bd,
    buscar_formula_por_nome_bd,
    buscar_todas_formulas_bd,
    criar_formula_bd,
    remover_formula_bd,
)
from product_structure.repository.item_repository import (
    buscar_item_por_id_bd,
    buscar_item_por_nome_bd,
)
from product_structure.repository.node_repository import (
    buscar_itens_formula_bd,
    implosao_produto,
    inserir_item_formula,
    remover_item_formula_bd,
    verificar_item_formula_existe,
)
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


def inserir_node(node_dto: NodeDTO):
    result_id = inserir_item_formula(node_dto)

    if result_id is None:
        raise NodeValueError("Não foi possivel encontrar um ID.")

    node_dto.node_id = result_id["id"]
    node = criar_node(node_dto)

    return node


def atualizar_nome_formula(formula_id, novo_nome):
    atualizar_nome_formula_bd(formula_id, novo_nome)


def remover_formula(formula_id):
    resultado_busca = buscar_formula_por_id(formula_id)

    if resultado_busca is None:
        raise TreeEmptyError("A arvore não foi encontrada.")

    remover_formula_bd(formula_id)


def remover_item_formula(node_id):
    resultado_busca = verificar_item_formula_existe(node_id)

    if resultado_busca is None:
        raise ItemError("Erro na verificação de existencia do item.")

    if not resultado_busca["exists"]:
        raise ItemError("Item nâo existe.")

    remover_item_formula_bd(node_id)


def buscar_todas_formulas():
    return buscar_todas_formulas_bd()


def buscar_formula_por_nome(nome):
    return buscar_formula_por_nome_bd(nome)


def buscar_formula_por_id(id):
    return buscar_formula_por_id_bd(id)


def buscar_itens_formula(formula_id):
    return buscar_itens_formula_bd(formula_id)


# ====================================
#          FUNÇOES DA ARVORE
# ====================================
def criar_node(dados: NodeDTO | dict):
    if isinstance(dados, NodeDTO):
        return _criar_node_dto(dados)

    elif isinstance(dados, dict):
        return _criar_node_dict(dados)

    raise TypeError("Tipo de dado não suportado.")

def _criar_node_dto(node_dto: NodeDTO):
    item_dict = buscar_item_por_id_bd(node_dto.item_id)
    
    if item_dict is None:
        raise NodeEmptyError("Não será possivel criar o Node porque o valor está vazio.")

    return _criar_node_dict(item_dict)

def _criar_node_dict(item_dict: dict):
    item = criar_item(item_dict)

    return Node(
        value = item,
        node_id = item_dict["id"],
        formula_id = item_dict["formula_id"],
        parent_id = item_dict["parent_id"],
        quantidade = item_dict["quantidade"],
    )


def inserir_node_arvore(arvore: ArvoreFormula, node: Node):
    if node.node_id in arvore.nodes:
        raise NodeAlreadyExistsError(
            "Falha ao inserir item na arvore. Esse Node já existe."
        )

    arvore.inserir(node)


def atualizar_nome_formula_arvore(arvore: ArvoreFormula, novo_nome):
    arvore.nome = novo_nome


def remover_node_arvore(arvore: ArvoreFormula, node: Node):
    if not node.node_id in arvore.nodes:
        raise NodeError("Este node não está presente na arvore.")

    arvore.remover(node)


def buscar_node_por_nome(arvore: ArvoreFormula, nome: str):
    nodes = arvore.get_nodes()

    for n in nodes:
        if n.value.nome == nome:
            return n


def buscar_arvore_formula(formula_id):
    formula = buscar_formula_por_id(formula_id)

    if formula is None:
        raise FormulaNotFoundError("Formula não encontrada.")

    itens = buscar_itens_formula(formula_id)

    arvore = ArvoreFormula(formula["id"], formula["nome"])

    nodes: dict[int | None, Node] = {}

    for item in itens:
        node = criar_node(item)
        nodes[node.node_id] = node

    for node in nodes.values():
        if node.parent_id is None:
            arvore.inserir(node)
        else:
            parent = nodes[node.parent_id]
            parent.children.append(node)

    return arvore


# FUNÇOES COMPLEMENTARES
def explosao(formula: ArvoreFormula):
    if formula.root is None:
        raise TreeEmptyError("Árvore vazia.")

    root = formula.root

    resultado = {
        "nome": root.value.nome,
        "descricao": root.value.descricao,
        "preco": implosao(formula.id),
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


def implosao(formula_id):
    resultado_busca = buscar_formula_por_id(formula_id)

    if resultado_busca is None:
        raise FormulaNotFoundError(
            "Não foi possivel encontrar a formula no sistema."
        )

    return implosao_produto(formula_id)
