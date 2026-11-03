from psycopg.rows import dict_row

from product_structure.database.connection import get_connection
from product_structure.dto.node_dto import NodeDTO


def inserir_item_formula(item: NodeDTO):
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                INSERT INTO item_formula (formula_id, item_id, parent_id, quantidade)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """,
            (item.formula_id, item.item_id, item.parent_id, item.quantidade),
        )

        item_id = cursor.fetchone()
        return item_id


def implosao_produto(formula_id):
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute(
            """
                SELECT SUM(preco) AS total
                FROM item_formula
                WHERE formula_id = %s
            """,
            (formula_id,)
        )

        return cursor.fetchone()