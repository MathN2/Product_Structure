from psycopg.rows import dict_row

from product_structure.database.connection import get_connection


def criar_formula_bd(nome):
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                INSERT INTO formula (nome)
                VALUES (%s)
                RETURNING *
            """,
            (nome,),
        )

        formula = cursor.fetchone()

        return formula


def inserir_formula_bd():
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                INSERT INTO item_formula (formula_id, item_id, parent_id, quantidade)
                VALUES (%s, %s, %s, %s)
                RETURNING *
            """,
            (),
        )


# FUNÇOES DE BUSCA
def buscar_todas_formulas_bd():
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute("SELECT * FROM formula")

        return cursor.fetchall()


def buscar_formula_por_nome_bd(nome):
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                SELECT * FROM formula
                WHERE nome = %s
                RETURNING *
            """,
            (nome,),
        )

        return cursor.fetchone()


def buscar_formula_por_id_bd(id):
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                SELECT * FROM formula
                WHERE id = %s
                RETURNING *
            """,
            (id,),
        )

        return cursor.fetchone()
