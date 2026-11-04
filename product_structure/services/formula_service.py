from product_structure.core.exceptions import *
from product_structure.core.formula import ArvoreFormula
from product_structure.core.node import Node
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
    atualizar_quantidade_item_formula,
    buscar_item_formula_bd,
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
    arvore = buscar_arvore_formula(node_dto.formula_id)
    _validar_item_raiz(arvore, node_dto.item_id)

    result_id = inserir_item_formula(node_dto)

    if result_id is None:
        raise NodeValueError("Não foi possivel encontrar um ID.")

    node_dto.node_id = result_id["id"]
    node = criar_node(node_dto)

    return node


def atualizar_nome_formula(formula_id, novo_nome):
    atualizar_nome_formula_bd(formula_id, novo_nome)


def mover_node(node_id, novo_pai_id):
    node_dict = buscar_item_formula(node_id)

    if node_dict is None:
        raise NodeValueError("Node não encontrado.")
    
    node_pai_dict = buscar_item_formula(novo_pai_id)

    if not node_pai_dict is None:
        arvore = buscar_arvore_formula(node_dict.get("formula_id"))
        node = criar_node(node_dict)
        node_pai = criar_node(node_pai_dict)

        _validar_ancestralidade(arvore, node, node_pai)

        node.parent_id = node_pai.node_id
        node_pai.children.append(node)

        return node

    raise NodeValueError("O novo pai não existe.")
    

def remover_formula(formula_id):
    resultado_busca = buscar_formula_por_id(formula_id)

    if resultado_busca is None:
        raise TreeEmptyError("A arvore não foi encontrada.")

    remover_formula_bd(formula_id)


def atualizar_quantidade_node(formula_id, node_id, quantidade):
    arvore = buscar_arvore_formula(formula_id)
    if node_id not in arvore.nodes:
        raise NodeValueError("Componente não encontrado nesta fórmula.")

    atualizado = atualizar_quantidade_item_formula(
        formula_id, node_id, quantidade
    )
    if atualizado is None:
        raise NodeValueError("Não foi possível atualizar a quantidade.")
    return atualizado


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


def buscar_item_formula(item_id):
    return buscar_item_formula_bd(item_id)


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
    dados = {
        "id": node_dto.node_id,
        "formula_id": node_dto.formula_id,
        "item_id": node_dto.item_id,
        "parent_id": node_dto.parent_id,
        "quantidade": node_dto.quantidade
    }

    return _criar_node_dict(dados)

def _criar_node_dict(item_dict: dict):
    item_preparado = item_dict

    if "item_id" in item_dict:
        item_preparado = buscar_item_por_id_bd(item_dict.get("item_id"))
        
        if item_preparado is None:
            raise NodeEmptyError("Não será possivel criar o Node porque o valor está vazio.")
    
    item = criar_item(item_preparado)

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
def explosao(formula: ArvoreFormula, quantidade_producao: int = 1):
    if formula.root is None:
        raise TreeEmptyError("Árvore vazia.")

    root = formula.root

    if quantidade_producao < 1:
        raise NodeValueError("A quantidade a produzir deve ser maior que zero.")

    custo = implosao(formula.id, quantidade_producao)
    resultado = {
        "node_id": root.node_id,
        "nome": root.value.nome,
        "descricao": root.value.descricao,
        "quantidade_producao": quantidade_producao,
        "preco": custo,
        "custo_aquisicao": custo["total"],
        "componentes": [],
    }

    for child in root.children:
        resultado["componentes"].append(
            _formatacao_explosao(child, quantidade_producao)
        )

    return resultado


def _formatacao_explosao(node: Node, multiplicador: int = 1):
    quantidade_total = node.quantidade * multiplicador
    preco_unitario = float(node.value.preco)
    resultado = {
        "node_id": node.node_id,
        "nome": node.value.nome,
        "descricao": node.value.descricao,
        "quantidade": quantidade_total,
        "quantidade_por_unidade": node.quantidade,
        "preco": preco_unitario,
        "preco_unitario": preco_unitario,
        "custo_aquisicao": preco_unitario * quantidade_total,
        "componentes": [],
    }

    for child in node.children:
        resultado["componentes"].append(
            _formatacao_explosao(child, quantidade_total)
        )

    return resultado


def implosao(formula_id, quantidade_producao: int = 1):
    resultado_busca = buscar_formula_por_id(formula_id)

    if resultado_busca is None:
        raise FormulaNotFoundError(
            "Não foi possivel encontrar a formula no sistema."
        )

    return implosao_produto(formula_id, quantidade_producao)


# VALIDAÇAO
def _validar_item_raiz(arvore: ArvoreFormula, novo_item_id: int):
    if arvore.root and novo_item_id == arvore.root.value.id:
        raise NodeValueError(
            "O item raiz não pode ser inserido como componente."
        )

def _validar_ancestralidade(
    arvore: ArvoreFormula,
    node: Node,
    novo_pai: Node
):
    atual: Node | None = novo_pai

    while atual is not None:
        if atual.node_id == node.node_id:
            raise NodeValueError(
                "A definição do parent_id criaria um ciclo."
            )

        if atual.parent_id is None:
            break

        atual = arvore.nodes.get(atual.parent_id)