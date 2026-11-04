from fastapi import APIRouter, HTTPException

from product_structure.core.exceptions import ItemBeingUsedError
from product_structure.dto.item_dto import ItemDTO
from product_structure.schemas.item_scheme import ItemCreate, ItemUpdate
from product_structure.services.item_service import (
    atualizar_item,
    buscar_item_id,
    buscar_todos_itens,
    cadastrar_item,
    remover_item,
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


@item_router.get("/{item_id}")
def buscar_item(item_id: int):
    item = buscar_item_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado.")
    return item


@item_router.patch("/{item_id}")
def editar_item(item_id: int, item: ItemUpdate):
    existente = buscar_item_id(item_id)
    if existente is None:
        raise HTTPException(status_code=404, detail="Item não encontrado.")

    dados = ItemDTO(
        nome=item.nome,
        descricao=item.descricao,
        preco=item.preco,
        item_id=item_id,
    )
    atualizar_item(dados)
    return {
        "id": item_id,
        "nome": dados.nome,
        "descricao": dados.descricao,
        "preco": dados.preco,
    }


@item_router.delete("/{item_id}")
def excluir_item(item_id: int):
    try:
        removido = remover_item(item_id)
    except ItemBeingUsedError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    if removido is None:
        raise HTTPException(status_code=404, detail="Item não encontrado.")
    return {"mensagem": "Item removido com sucesso.", "id": item_id}
