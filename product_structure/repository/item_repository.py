from psycopg.rows import dict_row

from product_structure.core.exceptions import ItemBeingUsedError
from product_structure.database.connection import get_connection
from product_structure.dto.item_dto import ItemDTO


def inserir_item_bd(item: ItemDTO):
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                INSERT INTO itens (nome, descricao, preco)
                VALUES (%s, %s, %s)
                RETURNING id;
            """,
            (item.nome, item.descricao, item.preco),
        )

        result = cursor.fetchone()

        if result is None:
            raise RuntimeError("Não foi possivel recuperar o ID do item.")

        item_id = result["id"]
        return item_id


def atualizar_item_bd(item_dto: ItemDTO):
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                UPDATE itens
                SET nome = %s,
                    descricao = %s,
                    preco = %s
                WHERE id = %s;
            """,
            (
                item_dto.nome,
                item_dto.descricao,
                item_dto.preco,
                item_dto.item_id,
            ),
        )

        return cursor.rowcount > 0


def remover_item_bd(id):
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                SELECT EXISTS (
                    SELECT 1
                    FROM item_formula
                    WHERE item_id = %s;
                )
            """,
            (id,),
        )

        item_sendo_usado = cursor.fetchone()

        if item_sendo_usado is None:
            raise RuntimeError(
                "Não foi possivel realizar a verificaçao do item em `item_formula`."
            )

        if item_sendo_usado["exists"]:
            raise ItemBeingUsedError(
                "Falha ao remover item. "
                "O item está sendo utilizado em `item_formula`."
            )

        cursor.execute(
            """
                DELETE FROM itens
                WHERE id = %s
                RETURNING *;
            """,
            (id,),
        )

        resultado = cursor.fetchone()
        return resultado


def buscar_todos_itens_bd():
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute("SELECT * FROM itens;")
        result = cursor.fetchall()

        return result


def buscar_item_por_nome_bd(nome):
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                SELECT * FROM itens
                WHERE nome = %s;
            """,
            (nome,),
        )

        result = cursor.fetchone()
        return result


def buscar_item_por_id_bd(id):
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                SELECT * FROM itens
                WHERE id = %s;
            """,
            (id,),
        )

        return cursor.fetchone()
