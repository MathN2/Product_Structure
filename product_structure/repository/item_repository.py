from product_structure.database.connection import get_connection
from product_structure.dto.item_dto import ItemDTO


def inserir(item: ItemDTO):
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute(
            """
                INSERT INTO itens (nome, descricao, preco)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
            (item.nome, item.descricao, item.preco),
        )

        result = cursor.fetchone()

        if result is None:
            raise RuntimeError("Não foi possivel recuperar o ID do item.")

        item_id = result[0]
        return item_id


def buscar_todos():
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute("SELECT * FROM itens")
        result = cursor.fetchall()
        
        return result
