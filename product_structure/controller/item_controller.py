from fastapi import APIRouter

from product_structure.dto.item_dto import ItemDTO
from product_structure.schemas.item_scheme import ItemCreate
from product_structure.services.item_service import (
    buscar_todos_itens,
    cadastrar_item,
)

item_router = APIRouter(prefix="/itens", tags=["Itens"])


@item_router.get("/")
def listar_itens():
    return buscar_todos_itens()


@item_router.post("/", status_code=201)
def criar_item(item: ItemCreate):
    criado = cadastrar_item(
        ItemDTO(nome=item.nome, descricao=item.descricao, preco=item.preco)
    )
    return {
        "id": criado.item_id,
        "nome": criado.nome,
        "descricao": criado.descricao,
        "preco": criado.preco,
    }
