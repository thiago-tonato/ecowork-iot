import oracledb

ORACLE_USER = "rm99404"
ORACLE_PASSWORD = "220205"
ORACLE_DSN = "oracle.fiap.com.br:1521/ORCL"

# Exemplo de DSN:
# host:porta/nome_do_servico
# Em Oracle Cloud Autonomous DB:
# "xxxxxx.adb.sa-saopaulo-1.oraclecloud.com:1522/xxxxxx_high"


# ---------------------------------------------------------
# Função de conexão
# ---------------------------------------------------------

def get_oracle_connection():
    """
    Retorna uma conexão ativa com o banco Oracle usando valores fixos.
    Adequado para protótipos e projetos acadêmicos.
    """
    conn = oracledb.connect(
        user=ORACLE_USER,
        password=ORACLE_PASSWORD,
        dsn=ORACLE_DSN
    )
    return conn


# ---------------------------------------------------------
# Teste de conexão (opcional)
# ---------------------------------------------------------

def test_connection():
    """
    Faz um teste rápido de conexão com o Oracle.
    Usado no endpoint /health.
    """
    try:
        conn = get_oracle_connection()
        conn.close()
        return True
    except Exception:
        return False
