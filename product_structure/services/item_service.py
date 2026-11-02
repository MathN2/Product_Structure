from product_structure.dto.item_dto import ItemDTO
from product_structure.models.item_formula import ItemFormula
from product_structure.repository.item_repository import inserir, buscar_todos


def cadastrar_item(item_dto: ItemDTO):
    nome = item_dto.nome
    descricao = item_dto.descricao
    preco = item_dto.preco

    ItemFormula(nome, descricao, preco)
    inserir(item_dto)


def buscar_item(item_dto: ItemDTO):
    pass


def buscar_todos_itens():
    lista_itens = buscar_todos()
    return lista_itens