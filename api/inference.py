from PIL import Image
from datetime import datetime
from database.db_config import get_oracle_connection

def get_model():
    return None

def preprocess_image(image: Image.Image):
    return image

def fake_predict(image: Image.Image, filename: str):
    name = filename.lower()

    if "bike" in name or "bicicleta" in name:
        return "bike", 0.9

    if "bus" in name or "onibus" in name or "ônibus" in name:
        return "transporte_publico", 0.85

    if "car" in name or "carro" in name or "uber" in name or "taxi" in name:
        return "carona", 0.8

    if "copo" in name or "caneca" in name or "cup" in name or "mug" in name:
        return "reutilizavel", 0.75

    return "nao_sustentavel", 0.5


def class_to_eco_score_and_points(classe: str, prob: float):
    base_score = {
        "bike": 90,
        "transporte_publico": 80,
        "carona": 70,
        "reutilizavel": 60,
        "nao_sustentavel": 10,
    }.get(classe, 10)

    eco_score = int(base_score * float(prob))
    pontos = int(eco_score * 0.6)
    return eco_score, pontos


def save_action_to_db(user_id: str, classe: str, prob: float, eco_score: int, pontos: int) -> int:
    conn = get_oracle_connection()
    cur = conn.cursor()

    sql = """
        INSERT INTO ECO_ACTIONS (
            USER_ID, CLASS_NAME, PROBABILITY, ECO_SCORE, POINTS,
            IMAGE_SOURCE, CREATED_AT
        )
        VALUES (:u, :c, :p, :e, :pts, 'api', :dt)
        RETURNING ID INTO :id
    """

    id_var = cur.var(int)

    cur.execute(sql, {
        "u": user_id,
        "c": classe,
        "p": float(prob),
        "e": int(eco_score),
        "pts": int(pontos),
        "dt": datetime.now(),
        "id": id_var
    })

    conn.commit()
    cur.close()
    conn.close()

    return int(id_var.getvalue())


def get_user_history(user_id: str):
    conn = get_oracle_connection()
    cur = conn.cursor()

    sql = """
        SELECT CREATED_AT, CLASS_NAME, ECO_SCORE, POINTS
        FROM ECO_ACTIONS
        WHERE USER_ID = :id
        ORDER BY CREATED_AT DESC
    """

    cur.execute(sql, {"id": user_id})
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows
