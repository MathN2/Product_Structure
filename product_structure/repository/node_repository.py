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


def atualizar_quantidade_item_formula(formula_id, node_id, quantidade):
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                UPDATE item_formula
                SET quantidade = %s
                WHERE formula_id = %s AND id = %s
                RETURNING id;
            """,
            (quantidade, formula_id, node_id),
        )
        return cursor.fetchone()


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


def implosao_produto(formula_id, quantidade_producao=1):
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                WITH RECURSIVE explosao AS (
                    SELECT
                        id,
                        formula_id,
                        item_id,
                        parent_id,
                        quantidade * %s::numeric AS quantidade_total
                    FROM item_formula
                    WHERE formula_id = %s AND parent_id IS NULL

                    UNION ALL

                    SELECT
                        filho.id,
                        filho.formula_id,
                        filho.item_id,
                        filho.parent_id,
                        filho.quantidade * pai.quantidade_total
                    FROM item_formula AS filho
                    JOIN explosao AS pai
                      ON filho.parent_id = pai.id
                     AND filho.formula_id = pai.formula_id
                )
                SELECT COALESCE(
                    SUM(i.preco * e.quantidade_total)
                        FILTER (WHERE e.parent_id IS NOT NULL),
                    0
                ) AS total
                FROM explosao AS e
                JOIN itens AS i ON i.id = e.item_id;
            """,
            (quantidade_producao, formula_id),
        )
        return cursor.fetchone()
