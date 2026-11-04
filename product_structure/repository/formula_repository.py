from psycopg.rows import dict_row

from product_structure.database.connection import get_connection


def criar_formula_bd(nome):
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                INSERT INTO formula (nome)
                VALUES (%s)
                RETURNING *;
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
                RETURNING *;
            """,
            (),
        )


def atualizar_nome_formula_bd(formula_id, novo_nome):
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                UPDATE formula
                SET nome = %s
                WHERE id = %s
                RETURNING *;
            """,
            (novo_nome, formula_id),
        )

        return cursor.fetchone()


def remover_formula_bd(formula_id):
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute(
            "DELETE FROM item_formula WHERE formula_id = %s;", (formula_id,)
        )

        cursor.execute("DELETE FROM formula WHERE id = %s;", (formula_id,))

        if cursor.rowcount == 0:
            raise RuntimeError("Falha em apagar formula.")


# FUNÇOES DE BUSCA
def buscar_todas_formulas_bd():
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute("SELECT * FROM formula;")

        return cursor.fetchall()


def buscar_formula_por_nome_bd(nome):
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                SELECT * FROM formula
                WHERE nome = %s;
            """,
            (nome,)
        )

        return cursor.fetchone()


def buscar_formula_por_id_bd(id):
    with get_connection() as conn, conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            """
                SELECT * FROM formula
                WHERE id = %s;
            """,
            (id,),
        )

        return cursor.fetchone()
