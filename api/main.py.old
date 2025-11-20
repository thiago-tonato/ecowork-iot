from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

from .models import EcoScanResponse, HealthResponse, HistoricoResponse, HistoricoItem
from .inference import (
    get_model,
    preprocess_image,
    map_predictions,
    class_to_eco_score_and_points,
    save_action_to_db,
    get_user_history,
)
from database.db_init import init_database
from database.db_config import test_connection

# ------------------------------------------------------------------------------------
# Inicializa tabelas ao subir a API
# ------------------------------------------------------------------------------------
init_database()

# ------------------------------------------------------------------------------------
# Configuração da API
# ------------------------------------------------------------------------------------
app = FastAPI(title="EcoWork IA - API de Visão Computacional")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # pode ajustar depois
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------------------
# ENDPOINT: IA - /api/v1/ecoscan
# ------------------------------------------------------------------------------------
@app.post("/api/v1/ecoscan", response_model=EcoScanResponse)
async def ecoscan(
    image: UploadFile = File(...),
    user_id: str = Form(...)
):
    """
    Recebe uma imagem, executa classificação com HuggingFace ViT e grava no Oracle.
    """

    try:
        # Lê a imagem enviada
        contents = await image.read()
        img = Image.open(io.BytesIO(contents))

        # Carrega o modelo e pré-processa
        model = get_model()
        img_proc = preprocess_image(img)

        # Predição (HuggingFace)
        preds = model(img_proc)

        # Converte predições para uma classe EcoWork
        classe_predita, prob = map_predictions(preds)

        # Calcula ecoScore e pontos verdes
        eco_score, pontos = class_to_eco_score_and_points(classe_predita, prob)

        # Salva no Oracle
        registro_id = save_action_to_db(
            user_id, classe_predita, prob, eco_score, pontos
        )

        mensagem = f"Ação sustentável reconhecida: {classe_predita}."

        # Retorna JSON
        return EcoScanResponse(
            user_id=user_id,
            classe_predita=classe_predita,
            probabilidade=prob,
            ecoScore=eco_score,
            pontos_verdes=pontos,
            mensagem=mensagem,
            registro_id=registro_id,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------------------------------------
# ENDPOINT: Healthcheck - /api/v1/health
# ------------------------------------------------------------------------------------
@app.get("/api/v1/health", response_model=HealthResponse)
def health():
    """
    Verifica:
    - Carregamento do modelo HuggingFace
    - Conexão com o banco Oracle
    """
    try:
        _ = get_model()
        model_loaded = True
        model_name = "google/vit-base-patch16-224"
    except Exception:
        model_loaded = False
        model_name = "erro"

    database_status = "ok" if test_connection() else "error"

    api_status = "ok" if (model_loaded and database_status == "ok") else "error"

    return HealthResponse(
        status=api_status,
        model_loaded=model_loaded,
        model_name=model_name,
        database_connection=database_status,
    )


# ------------------------------------------------------------------------------------
# ENDPOINT: Histórico - /api/v1/users/{user_id}/historico
# ------------------------------------------------------------------------------------
@app.get("/api/v1/users/{user_id}/historico", response_model=HistoricoResponse)
def historico(user_id: str):
    try:
        rows = get_user_history(user_id)

        # DEBUG OBRIGATÓRIO
        print("DEBUG ROWS FROM ORACLE:", rows)

        historico_items = [
            HistoricoItem(
                data_hora=r[0].isoformat(),
                classe=r[1],
                ecoScore=int(r[2]),
                pontos=int(r[3]),
            )
            for r in rows
        ]

        return HistoricoResponse(
            user_id=user_id,
            historico=historico_items
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
