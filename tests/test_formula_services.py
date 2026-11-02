from product_structure.core.formula import ArvoreFormula
from product_structure.core.node import Node
from product_structure.models.item_formula import ItemFormula
from product_structure.services.formula_service import explosao


def test_explosao():
    a = ArvoreFormula()
    item1 = ItemFormula("a", "", 1)
    n1 = Node(item1, 1)

    item2 = ItemFormula("b", "", 1, 1)
    n2 = Node(item2, 2)

    item3 = ItemFormula("c", "", 1, 1)
    n3 = Node(item3, 3)

    item4 = ItemFormula("d", "", 1, 1)
    n4 = Node(item4, 4)

    a.inserir(n1)
    a.inserir(n2, n1)
    a.inserir(n3, n1)
    a.inserir(n4, n2)

    resultado_explosao = explosao(a)
    gabarito_explosao = {
        "nome": "a",
        "descricao": "",
        "preco": 3,
        "componentes": [
            {
                "nome": "b",
                "descricao": "",
                "quantidade": 1,
                "preco": 1,
                "componentes": [
                    {
                        "nome": "d",
                        "descricao": "",
                        "quantidade": 1,
                        "preco": 1,
                        "componentes": [],
                    }
                ],
            },
            {
                "nome": "c",
                "descricao": "",
                "quantidade": 1,
                "preco": 1,
                "componentes": [],
            },
        ],
    }

    assert resultado_explosao == gabarito_explosao
