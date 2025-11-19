import os
from PIL import Image
import numpy as np

from transformers import pipeline

from database.db_config import get_oracle_connection
from datetime import datetime

# Carrega pipeline de classificação de imagens
_classifier = None

def get_model():
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
    O pipeline da HuggingFace já cuida do preprocessamento,
    então basta retornar a imagem original.
    """
    return image


def map_predictions(preds):
    """
    preds = lista de dicionários, ex:
    [{'label': 'bicycle', 'score': 0.88}, ...]
    """
    eco_class = "nao_sustentavel"
    best_score = 0.0

    for pred in preds:
        label = pred["label"].lower()
        score = pred["score"]

        if "bicycle" in label or "bike" in label:
            if score > best_score:
                eco_class = "bike"
                best_score = score

        elif "bus" in label or "trolleybus" in label:
            if score > best_score:
                eco_class = "transporte_publico"
                best_score = score

        elif "train" in label or "tram" in label:
            if score > best_score:
                eco_class = "transporte_publico"
                best_score = score

        elif "car" in label or "cab" in label or "taxi" in label:
            if score > best_score:
                eco_class = "carona"
                best_score = score

        elif "cup" in label or "mug" in label:
            if score > best_score:
                eco_class = "reutilizavel"
                best_score = score

    # Se nada bateu, usa a score do top1
    if best_score == 0.0:
        best_score = preds[0]["score"]

    return eco_class, best_score


def class_to_eco_score_and_points(classe, prob):
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


def save_action_to_db(user_id, classe, prob, eco_score, pontos):
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


def get_user_history(user_id):
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
