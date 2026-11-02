from product_structure.core.exceptions import *
from product_structure.core.formula import ArvoreFormula
from product_structure.core.node import Node


def explosao(produto: ArvoreFormula):
    if produto.root is None:
        raise TreeEmptyError("Árvore vazia.")

    root = produto.root

    resultado = {
        "nome": root.value.nome,
        "descricao": root.value.descricao,
        "preco": produto.implosao(),
        "componentes": [],
    }

    for child in root.children:
        resultado["componentes"].append(_formatacao_explosao(child))

    return resultado


def _formatacao_explosao(node: Node):
    resultado = {
        "nome": node.value.nome,
        "descricao": node.value.descricao,
        "quantidade": node.value.quantidade,
        "preco": node.value.preco,
        "componentes": [],
    }

    for child in node.children:
        resultado["componentes"].append(_formatacao_explosao(child))

    return resultado
