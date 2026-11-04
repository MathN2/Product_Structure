from psycopg.rows import dict_row

from product_structure.database.connection import get_connection
from product_structure.dto.node_dto import NodeDTO


def inserir_item_formula(item: NodeDTO):
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                INSERT INTO item_formula (formula_id, item_id, parent_id, quantidade)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """,
            (item.formula_id, item.item_id, item.parent_id, item.quantidade),
        )

        item_id = cursor.fetchone()
        return item_id


def remover_item_formula_bd(node_id):
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                DELETE FROM item_formula
                WHERE id = %s
                RETURNING id;
            """,
            (node_id,)
        )

        return cursor.fetchone()


def buscar_item_formula_bd(node_id):
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                SELECT * FROM item_formula
                WHERE id = %s;
            """,
            (node_id,)
        )

        return cursor.fetchone()


def buscar_itens_formula_bd(formula_id):
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                SELECT * FROM item_formula
                WHERE formula_id = %s;
            """,
            (formula_id,),
        )

        return cursor.fetchall()


def verificar_item_formula_existe(item_formula_id):
    with get_connection().cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                SELECT EXISTS (
                    SELECT 1
                    FROM item_formula
                    WHERE id = %s;
                )
            """,
            (item_formula_id,),
        )

        return cursor.fetchone()


def implosao_produto(formula_id):
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                SELECT SUM(i.preco * if.quantidade) AS total
                FROM item_formula AS if
                JOIN itens AS i ON i.id = if.item_id
                WHERE if.formula_id = %s;
            """,
            (formula_id,),
        )

        return cursor.fetchone()
