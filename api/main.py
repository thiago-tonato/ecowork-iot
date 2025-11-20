from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

from .models import EcoScanResponse, HealthResponse, HistoricoResponse, HistoricoItem
from .inference import (
    get_model,
    preprocess_image,
    fake_predict,
    class_to_eco_score_and_points,
    save_action_to_db,
    get_user_history,
    safe_int,
)

# -----------------------------------------------------------------------------
# Criação da aplicação FastAPI
# -----------------------------------------------------------------------------
app = FastAPI(title="EcoWork IA - API de Visão Computacional (Simulada, em memória)")

# -----------------------------------------------------------------------------
# Middleware CORS
# -----------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção, restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------------------------------
# ENDPOINT: /api/v1/ecoscan  -> Análise da imagem + "gravação"
# -----------------------------------------------------------------------------
@app.post("/api/v1/ecoscan", response_model=EcoScanResponse)
async def ecoscan(
    image: UploadFile = File(...),
    user_id: str = Form(...)
):
    """
    Recebe uma imagem, executa análise simulada de IA,
    calcula ecoScore e pontos e grava em memória.
    """
    try:
        contents = await image.read()
        img = Image.open(io.BytesIO(contents))

        _ = get_model()
        _ = preprocess_image(img)

        # IA simulada
        classe_predita, prob = fake_predict(img, image.filename)

        eco_score, pontos = class_to_eco_score_and_points(classe_predita, prob)

        registro_id = save_action_to_db(
            user_id=user_id,
            classe=classe_predita,
            prob=prob,
            eco_score=eco_score,
            pontos=pontos,
        )

        mensagem = f"Ação reconhecida: {classe_predita}."

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


# -----------------------------------------------------------------------------
# ENDPOINT: /api/v1/health  -> Status da API
# -----------------------------------------------------------------------------
@app.get("/api/v1/health", response_model=HealthResponse)
def health():
    """
    Verifica se a 'IA' está disponível.
    Banco, neste modo, é em memória.
    """
    # IA simulada = sempre disponível
    model_loaded = True
    model_name = "EcoWork Simulated Vision Model (In-Memory Storage)"

    # Banco em memória = sempre ok
    database_status = "ok"

    status = "ok" if model_loaded else "error"

    return HealthResponse(
        status=status,
        model_loaded=model_loaded,
        model_name=model_name,
        database_connection=database_status,
    )


# -----------------------------------------------------------------------------
# ENDPOINT: /api/v1/users/{user_id}/historico  -> Histórico de ações
# -----------------------------------------------------------------------------
@app.get("/api/v1/users/{user_id}/historico", response_model=HistoricoResponse)
def historico(user_id: str):
    """
    Retorna o histórico de ações sustentáveis registradas para um usuário
    usando somente o armazenamento em memória.
    """
    try:
        rows = get_user_history(user_id)

        historico_items = []
        for r in rows:
            data_hora = r[0]
            classe = r[1]
            eco = safe_int(r[2], 0)
            pts = safe_int(r[3], 0)

            historico_items.append(
                HistoricoItem(
                    data_hora=data_hora.isoformat(),
                    classe=classe,
                    ecoScore=eco,
                    pontos=pts,
                )
            )

        return HistoricoResponse(
            user_id=user_id,
            historico=historico_items
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
