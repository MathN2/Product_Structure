from product_structure.core.formula import ArvoreFormula
from product_structure.core.node import Node


def test_tree_star_empty():
    arvore = ArvoreFormula()

    assert arvore.root is None
    assert arvore.nodes == {}


def test_insert_child_to_root():
    arvore = ArvoreFormula()
    root = Node("Caneta")
    child = Node("Tinta")

    arvore.inserir(root)
    arvore.inserir(child, root)

    assert arvore.root is root
    assert child in root.children
    assert child.parent is root
    # assert root in arvore.nodes.values() Preciso encontrar uma forma de criar os ids
    # assert child in arvore.nodes.values()
