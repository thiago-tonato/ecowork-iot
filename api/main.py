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

init_database()

app = FastAPI(title="EcoWork IA - API de Visão Computacional")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/v1/ecoscan", response_model=EcoScanResponse)
async def ecoscan(
    image: UploadFile = File(...),
    user_id: str = Form(...)
):
    try:
        contents = await image.read()
        img = Image.open(io.BytesIO(contents))

        model = get_model()
        preds = model(img)   # retorna top-5 já prontinho
        classe, prob = map_predictions(preds)

        decoded = decode_predictions(preds, top=5)
        classe_predita, prob = map_imagenet_to_eco_class(decoded)

        eco_score, pontos = class_to_eco_score_and_points(classe_predita, prob)
        registro_id = save_action_to_db(user_id, classe_predita, prob, eco_score, pontos)

        mensagem = f"Ação sustentável reconhecida: {classe_predita}."

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


@app.get("/api/v1/health", response_model=HealthResponse)
def health():
    # Testa carregamento do modelo
    try:
        model = get_model()
        model_loaded = True
        model_name = "MobileNetV2 (ImageNet pré-treinado)"
    except Exception:
        model_loaded = False
        model_name = "unknown"

    # Testa conexão com DB
    db_status = "ok" if test_connection() else "error"

    return HealthResponse(
        status="ok" if model_loaded and db_status == "ok" else "error",
        model_loaded=model_loaded,
        model_name=model_name,
        database_connection=db_status,
    )


@app.get("/api/v1/users/{user_id}/historico", response_model=HistoricoResponse)
def historico(user_id: str):
    try:
        rows = get_user_history(user_id)
        historico_items = [
            HistoricoItem(
                data_hora=r[0].isoformat(),
                classe=r[1],
                ecoScore=int(r[2]),
                pontos=int(r[3]),
            )
            for r in rows
        ]
        return HistoricoResponse(user_id=user_id, historico=historico_items)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
