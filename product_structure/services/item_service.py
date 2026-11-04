from product_structure.dto.item_dto import ItemDTO
from product_structure.models.item_formula import ItemFormula
from product_structure.repository.item_repository import (
    atualizar_item_bd,
    buscar_item_por_id_bd,
    buscar_item_por_nome_bd,
    buscar_todos_itens_bd,
    inserir_item_bd,
    remover_item_bd,
)


# ====================================
#       FUNÇOES BANCO DE DADOS
# ====================================
def cadastrar_item(item_dto: ItemDTO):
    item = criar_item(item_dto)
    inserir_item_bd(item_dto)

    return item


def atualizar_item(item_dto: ItemDTO):
    atualizar_item_bd(item_dto)


def remover_item(id):
    remover_item_bd(id)


def buscar_todos_itens():
    return buscar_todos_itens_bd()


def buscar_item_nome(nome):
    return buscar_item_por_nome_bd(nome)


def buscar_item_id(id):
    return buscar_item_por_id_bd(id)


# ====================================
#          FUNÇOES DA ARVORE
# ====================================
def criar_item(dados: ItemDTO | dict):
    if isinstance(dados, ItemDTO):
        return _criar_item_dto(dados)

    elif isinstance(dados, dict):
        return _criar_item_dict(dados)

    raise TypeError("Tipo de dado não suportado.")

def _criar_item_dto(item_dto: ItemDTO):
    return ItemFormula(
        item_dto.nome,
        item_dto.descricao,
        item_dto.preco
    )

def _criar_item_dict(item_dict: dict):
    return ItemFormula(
        item_dict["nome"],
        item_dict["descricao"],
        item_dict["preco"]
    )
