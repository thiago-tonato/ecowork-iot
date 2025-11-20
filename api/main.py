@app.post("/api/v1/ecoscan", response_model=EcoScanResponse)
async def ecoscan(
    image: UploadFile = File(...),
    user_id: str = Form(...)
):
    try:
        contents = await image.read()
        img = Image.open(io.BytesIO(contents))

        _ = get_model()
        _ = preprocess_image(img)

        # IA Simulada
        classe_predita, prob = fake_predict(img, image.filename)

        eco_score, pontos = class_to_eco_score_and_points(classe_predita, prob)
        registro_id = save_action_to_db(user_id, classe_predita, prob, eco_score, pontos)

        return EcoScanResponse(
            user_id=user_id,
            classe_predita=classe_predita,
            probabilidade=prob,
            ecoScore=eco_score,
            pontos_verdes=pontos,
            mensagem=f"Ação reconhecida: {classe_predita}.",
            registro_id=registro_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
