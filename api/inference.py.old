from PIL import Image
from datetime import datetime

from transformers import pipeline

from database.db_config import get_oracle_connection


# Pipeline global do modelo HuggingFace
_classifier = None


def get_model():
    """
    Carrega o modelo Vision Transformer (ViT) da Hugging Face.
    Garante instanciação única.
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
    O HuggingFace aceita diretamente a imagem PIL.
    """
    return image


def map_predictions(preds):
    """
    Mapeia as predições do modelo HuggingFace para as classes EcoWork.
    Corrige automaticamente casos onde o transformers retorna [[{...}]].

    preds esperado:
        [ {"label": "...", "score": 0.88}, {"label": "...", "score": 0.75}, ... ]

    OU (caso transformers retorne lista de listas):
        [[ {"label": "...", "score": 0.88}, ... ]]
    """

    # 🔧 CORREÇÃO AUTOMÁTICA SE FOR LISTA DE LISTAS
    if isinstance(preds, list) and len(preds) > 0 and isinstance(preds[0], list):
        preds = preds[0]

    # Segurança: se vier vazio
    if not preds:
        return "nao_sustentavel", 0.5

    eco_class = "nao_sustentavel"
    best_score = 0.0

    for pred in preds:
        label = str(pred.get("label", "")).lower()
        score = float(pred.get("score", 0.0))

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

        # Trem / metrô
        elif "train" in label or "tram" in label:
            if score > best_score:
                eco_class = "transporte_publico"
                best_score = score

        # Carro / táxi
        elif "car" in label or "cab" in label or "taxi" in label:
            if score > best_score:
                eco_class = "carona"
                best_score = score

        # Copos / canecas reutilizáveis
        elif "cup" in label or "mug" in label:
            if score > best_score:
                eco_class = "reutilizavel"
                best_score = score

    # Se nada foi encontrado, usa o top1
    if best_score == 0.0:
        best_score = float(preds[0].get("score", 0.5))

    return eco_class, best_score


def class_to_eco_score_and_points(classe: str, prob: float):
    """
    Converte classe e probabilidade em ecoScore e Pontos Verdes.
    """
    prob = float(prob)  # garante que prob não seja lista

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
    """
    Salva o registro no banco Oracle.
    Garante que nenhum campo seja lista (que causaria o erro int(list)).
    """
    prob = float(prob)
    eco_score = int(eco_score)
    pontos = int(pontos)

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
    """
    Retorna o histórico das ações do usuário.
    """
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
