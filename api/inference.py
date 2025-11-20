from PIL import Image
from datetime import datetime

# "Banco de dados" em memória
ACTIONS = []
NEXT_ID = 1


def safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return float(default)


def safe_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return int(default)


# ----------------- "IA" SIMULADA ----------------------

def get_model():
    # Mantido apenas para manter a arquitetura
    return None


def preprocess_image(image: Image.Image):
    return image


def fake_predict(image: Image.Image, filename: str):
    """
    IA simulada baseada no NOME DO ARQUIVO.
    """
    name = filename.lower()

    if "bike" in name or "bicicleta" in name:
        return "bike", 0.9

    if "bus" in name or "onibus" in name or "ônibus" in name:
        return "transporte_publico", 0.85

    if "car" in name or "carro" in name or "uber" in name or "taxi" in name:
        return "carona", 0.8

    if "copo" in name or "caneca" in name or "cup" in name or "mug" in name:
        return "reutilizavel", 0.75

    # Trem
    if "trem" in name or "train" in name:
        return "trem", 0.88

    # Metrô
    if "metro" in name or "subway" in name:
        return "metro", 0.87

    # Navio
    if "navio" in name or "ship" in name or "boat" in name or "cruise" in name:
        return "navio", 0.70

    # Helicóptero
    if "helicoptero" in name or "helicopter" in name or "heli" in name:
        return "helicoptero", 0.65

    # Avião
    if "aviao" in name or "airplane" in name or "plane" in name or "flight" in name:
        return "aviao", 0.60

    # Moto
    if "moto" in name or "motocicleta" in name or "motorcycle" in name:
        return "moto", 0.78


    return "nao_sustentavel", 0.5


def class_to_eco_score_and_points(classe: str, prob: float):
    base_score = {
        "bike": 90,
        "transporte_publico": 80,
        "trem": 88,
        "metro": 87,
        "carona": 70,
        "reutilizavel": 60,
        "moto": 50,
        "navio": 30,
        "helicoptero": 20,
        "aviao": 15,
        "nao_sustentavel": 10,
    }.get(classe, 10)


    prob = safe_float(prob, 0.5)
    eco_score = int(base_score * prob)
    pontos = int(eco_score * 0.6)
    return eco_score, pontos


def save_action_to_db(user_id: str, classe: str, prob: float, eco_score: int, pontos: int) -> int:
    """
    Simula salvamento em banco, usando uma lista em memória.
    """
    global NEXT_ID

    prob = safe_float(prob, 0.5)
    eco_score = safe_int(eco_score, 0)
    pontos = safe_int(pontos, 0)

    action = {
        "id": NEXT_ID,
        "user_id": user_id,
        "class_name": classe,
        "probability": prob,
        "eco_score": eco_score,
        "points": pontos,
        "image_source": "api",
        "created_at": datetime.now(),
    }

    ACTIONS.append(action)
    NEXT_ID += 1

    return action["id"]


def get_user_history(user_id: str):
    """
    Retorna uma lista de tuplas no formato:
    (created_at, class_name, eco_score, points)
    """
    rows = []
    for action in ACTIONS:
        if action["user_id"] == user_id:
            rows.append(
                (
                    action["created_at"],
                    action["class_name"],
                    action["eco_score"],
                    action["points"],
                )
            )
    # Ordena por data decrescente
    rows.sort(key=lambda r: r[0], reverse=True)
    return rows
