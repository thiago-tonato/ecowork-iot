from PIL import Image
from datetime import datetime

from transformers import pipeline

from database.db_config import get_oracle_connection

# Pipeline global de classificação de imagens
_classifier = None


def get_model():
    """
    Carrega o modelo pré-treinado da Hugging Face (Vision Transformer - ViT).
    O pipeline baixa automaticamente o modelo na primeira execução.
    """
    global _classifier
    if _classifier is None:
        _classifier = pipeline(
            "image-classification",
            model="google/vit-base-patch16-224",
            top_k=5
        )
    return _classifier


def preprocess_image(image: Image.Image):
    """
    Para o modelo Vision Transformer da Hugging Face, a imagem PIL já é suficiente.
    """
    return image


def map_predictions(preds):
    """
    Recebe as predições do modelo e converte para as classes do EcoWork.
    preds = [
       {"label": "bicycle-built-for-two", "score": 0.88},
       {"label": "mountain bike", "score": 0.76},
       ...
    ]
    """

    eco_class = "nao_sustentavel"
    best_score = 0.0

    for pred in preds:
        label = pred["label"].lower()
        score = pred["score"]

        # Bicicleta
        if "bicycle" in label or "bike" in label:
            if score > best_score:
                eco_class = "bike"
                best_score = score

        # Ônibus / transporte público
        elif "bus" in label or "trolleybus" in label:
            if score > best_score:
                eco_class = "transporte_publico"
                best_score = score

        # Trem / metrô / tram
        elif "train" in label or "tram" in label:
            if score > best_score:
                eco_class = "transporte_publico"
                best_score = score

        # Carro / táxi
        elif "car" in label or "cab" in label or "taxi" in label:
            if score > best_score:
                eco_class = "carona"
                best_score = score

        # Copo / caneca reutilizável
        elif "cup" in label or "mug" in label:
            if score > best_score:
                eco_class = "reutilizavel"
                best_score = score

    # Se nada bater, usa a probabilidade do top1 como fallback
    if best_score == 0.0 and preds:
        best_score = preds[0]["score"]

    return eco_class, best_score


def class_to_eco_score_and_points(classe: str, prob: float):
    base_score = {
        "bike": 90,
        "transporte_publico": 80,
        "carona": 70,
        "reutilizavel": 60,
        "economia_energia": 50,
        "nao_sustentavel": 10,
    }.get(classe, 10)

    eco_score = int(base_score * prob)
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
        "p": prob,
        "e": eco_score,
        "pts": pontos,
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
