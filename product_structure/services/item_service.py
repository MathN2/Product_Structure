from product_structure.dto.item_dto import ItemDTO
from product_structure.models.item_formula import ItemFormula
from product_structure.repository.item_repository import inserir, atualizar, remover, buscar_todos, buscar_por_id, buscar_por_nome


def cadastrar_item(item_dto: ItemDTO):
    nome = item_dto.nome
    descricao = item_dto.descricao
    preco = item_dto.preco

    ItemFormula(nome, descricao, preco)
    inserir(item_dto)


def atualizar_item(item_dto: ItemDTO):
    atualizar(item_dto)


def remover_item(id):
    remover(id)


def buscar_todos_itens():
    return buscar_todos()

def buscar_item_nome(nome):
    return buscar_por_nome(nome)

def buscar_item_id(id):
    return buscar_por_id(id)