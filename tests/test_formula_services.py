from product_structure.core.formula import ArvoreFormula
from product_structure.core.node import Node
from product_structure.models.item_formula import ItemFormula
from product_structure.services import formula_service


def test_explosao_scales_nested_requirements_and_cost(monkeypatch):
    arvore = ArvoreFormula(7, "Caneta")
    raiz = Node(ItemFormula("Caneta", "", 0), node_id=1, formula_id=7)
    tinta = Node(
        ItemFormula("Tinta", "", 1),
        node_id=2,
        formula_id=7,
        parent_id=1,
        quantidade=2,
    )
    corpo = Node(
        ItemFormula("Corpo", "", 1),
        node_id=3,
        formula_id=7,
        parent_id=1,
        quantidade=1,
    )
    pigmento = Node(
        ItemFormula("Pigmento", "", 1),
        node_id=4,
        formula_id=7,
        parent_id=2,
        quantidade=3,
    )

    arvore.inserir(raiz)
    arvore.inserir(tinta, raiz)
    arvore.inserir(corpo, raiz)
    arvore.inserir(pigmento, tinta)
    monkeypatch.setattr(
        formula_service,
        "implosao",
        lambda formula_id, quantidade_producao: {"total": 18},
    )

    resultado = formula_service.explosao(arvore, quantidade_producao=2)

    assert resultado["quantidade_producao"] == 2
    assert resultado["custo_aquisicao"] == 18
    assert resultado["componentes"][0]["quantidade"] == 4
    assert resultado["componentes"][0]["custo_aquisicao"] == 4
    assert resultado["componentes"][0]["componentes"][0]["quantidade"] == 12
    assert resultado["componentes"][0]["componentes"][0]["custo_aquisicao"] == 12
    assert resultado["componentes"][1]["quantidade"] == 2


def test_implosao_passes_requested_quantity_to_repository(monkeypatch):
    calls = {}
    monkeypatch.setattr(
        formula_service,
        "buscar_formula_por_id",
        lambda formula_id: {"id": formula_id},
    )
    monkeypatch.setattr(
        formula_service,
        "implosao_produto",
        lambda formula_id, quantidade: calls.update(
            formula_id=formula_id, quantidade=quantidade
        ) or {"total": 42},
    )

    assert formula_service.implosao(7, quantidade_producao=3) == {"total": 42}
    assert calls == {"formula_id": 7, "quantidade": 3}
