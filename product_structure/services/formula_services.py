from product_structure.core.generic_tree import ArvoreFormula
from product_structure.core.node import Node
from product_structure.core.exceptions import *


def explosao(produto: ArvoreFormula):
    if produto.root is None:
        raise TreeEmptyError("Árvore vazia.")

    root = produto.root

    resultado = {
        "nome": root.value.nome,
        "preco": produto.implosao(),
        "componentes": [],
    }

    for child in root.children:
        resultado["componentes"].append(_formatacao_explosao(child))

    return resultado


def _formatacao_explosao(node: Node):
    resultado = {
        "nome": node.value.nome,
        "quantidade": node.value.quantidade,
        "preco": node.value.preco,
        "componentes": [],
    }

    for child in node.children:
        resultado["componentes"].append(_formatacao_explosao(child))

    return resultado
