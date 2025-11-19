from pydantic import BaseModel
from typing import Optional, List


class EcoScanResponse(BaseModel):
    user_id: str
    classe_predita: str
    probabilidade: float
    ecoScore: int
    pontos_verdes: int
    mensagem: str
    registro_id: Optional[int]


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_name: str
    database_connection: str


class HistoricoItem(BaseModel):
    data_hora: str
    classe: str
    ecoScore: int
    pontos: int


class HistoricoResponse(BaseModel):
    user_id: str
    historico: List[HistoricoItem]
