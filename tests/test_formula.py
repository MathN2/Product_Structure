from product_structure.core.formula import ArvoreFormula
from product_structure.core.node import Node


def test_tree_starts_empty():
    arvore = ArvoreFormula(1, "Caneta")

    assert arvore.root is None
    assert arvore.nodes == {}


def test_insert_child_to_root():
    arvore = ArvoreFormula(1, "Caneta")
    root = Node("Caneta", node_id=1, formula_id=1)
    child = Node("Tinta", node_id=2, formula_id=1, parent_id=1)

    arvore.inserir(root)
    arvore.inserir(child, root)

    assert arvore.root is root
    assert child in root.children
    assert child.parent is root
    assert arvore.nodes == {1: root, 2: child}
