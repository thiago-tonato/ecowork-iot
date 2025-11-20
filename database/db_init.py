from database.db_config import get_oracle_connection


# ---------------------------------------------------------------------------
# Criação automática da tabela ECO_ACTIONS
# ---------------------------------------------------------------------------
def init_database():
    """
    Cria a tabela ECO_ACTIONS caso ela ainda não exista.
    """
    conn = None
    try:
        conn = get_oracle_connection()
        cur = conn.cursor()

        sql = """
        BEGIN
            EXECUTE IMMEDIATE '
                CREATE TABLE ECO_ACTIONS (
                    ID NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    USER_ID VARCHAR2(100),
                    CLASS_NAME VARCHAR2(200),
                    PROBABILITY NUMBER,
                    ECO_SCORE NUMBER,
                    POINTS NUMBER,
                        IMAGE_SOURCE VARCHAR2(50),
                    CREATED_AT TIMESTAMP
                )
            ';
        EXCEPTION
            WHEN OTHERS THEN
                IF SQLCODE != -955 THEN
                    RAISE;
                END IF;
        END;
        """

        cur.execute(sql)
        conn.commit()
        cur.close()

    except Exception as e:
        print("Erro criando tabela:", e)

    finally:
        if conn:
            conn.close()


# ---------------------------------------------------------------------------
# Correção automática de registros inválidos
# ---------------------------------------------------------------------------
def fix_invalid_records():
    """
    Corrige registros antigos salvos incorretamente quando a IA retornava listas.
    Ajusta probabilidades, ecoScores e pontos que foram gravados como listas.
    """

    conn = None
    try:
        conn = get_oracle_connection()
        cur = conn.cursor()

        sql_select = """
            SELECT ID, PROBABILITY, ECO_SCORE, POINTS
            FROM ECO_ACTIONS
        """

        cur.execute(sql_select)
        rows = cur.fetchall()

        for row in rows:
            record_id = row[0]
            prob = row[1]
            eco_score = row[2]
            points = row[3]

            needs_fix = False

            # Correção automática — se algum campo for lista
            if isinstance(prob, list):
                prob = float(prob[0]) if prob else 0.5
                needs_fix = True

            if isinstance(eco_score, list):
                eco_score = int(eco_score[0]) if eco_score else 10
                needs_fix = True

            if isinstance(points, list):
                points = int(points[0]) if points else 5
                needs_fix = True

            # Atualiza SOMENTE se necessário
            if needs_fix:
                sql_update = """
                    UPDATE ECO_ACTIONS
                    SET PROBABILITY = :p,
                        ECO_SCORE = :e,
                        POINTS = :pt
                    WHERE ID = :id
                """
                cur.execute(sql_update, {
                    "p": prob,
                    "e": eco_score,
                    "pt": points,
                    "id": record_id
                })

        conn.commit()
        cur.close()

    except Exception as e:
        print("Erro ao corrigir registros inválidos:", e)

    finally:
        if conn:
            conn.close()


# ---------------------------------------------------------------------------
# Limpeza opcional (somente se quiser apagar tudo)
# ---------------------------------------------------------------------------
def wipe_database():
    """
    Apaga todos os registros (não utilizada automaticamente).
    """
    conn = get_oracle_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM ECO_ACTIONS")
    conn.commit()
    cur.close()
    conn.close()
