# 📘 EcoWork – API de Visão Computacional (Simulada)
> **FIAP – Projeto Integrado | Deep Learning + DevOps + Banco de Dados**

## 📝 Descrição do Projeto
O **EcoWork** é uma solução de sustentabilidade corporativa que permite que funcionários registrem ações sustentáveis por meio de fotos enviadas à API.

A API:
1. Recebe a imagem  
2. Executa uma análise de “visão computacional simulada”  
3. Classifica a ação como sustentável ou não  
4. Calcula um **ecoScore**  
5. Gera **pontos verdes**  
6. Registra tudo no **Banco Oracle Cloud**  
7. Permite consultar o histórico  

## 🚫 Sobre a IA Simulada
O ambiente local impediu o download do modelo via HTTPS (erro de certificado SSL).  
Portanto, a IA foi simulada, mantendo toda a arquitetura Deep Learning-ready.

No vídeo, deverá ser dito:

> “A arquitetura está preparada para modelos reais, mas o ambiente bloqueou o download do modelo. Por isso, utilizamos IA simulada para demonstração.”

## 🧱 Arquitetura da Solução
```
Usuário → Swagger → API → IA Simulada → ecoScore → Oracle → Histórico
```

## 🧰 Tecnologias
- Python
- FastAPI
- Uvicorn
- Pillow
- Oracle Database
- Mock AI
- Docker (opcional)

## 📂 Estrutura
```
ecowork/
│ api/
│   main.py
│   inference.py
│   models.py
│ database/
│   db_config.py
│   db_init.py
│ requirements.txt
│ README.md
```

## ⚙️ Instalação

### 1️⃣ Criar ambiente virtual
```
python -m venv venv
```

Ativar:

Windows:
```
venv\Scripts\activate
```

Linux/Mac:
```
source venv/bin/activate
```

### 2️⃣ Instalar dependências
```
pip install -r requirements.txt
```

### 3️⃣ Configurar Oracle
Editar:
```
database/db_config.py
```

### 4️⃣ Rodar API
```
uvicorn api.main:app --reload
```

Acessar:
```
http://127.0.0.1:8000/docs
```

## 🧪 Testes

### 🔹 Healthcheck
```
GET /api/v1/health
```

Resposta:
```json
{
  "status": "ok",
  "model_loaded": true,
  "model_name": "EcoWork Simulated Vision Model",
  "database_connection": "ok"
}
```

### 🔹 IA Simulada
```
POST /api/v1/ecoscan
```

Exemplo de resposta:
```json
{
  "user_id": "luciana",
  "classe_predita": "bike",
  "probabilidade": 0.9,
  "ecoScore": 81,
  "pontos_verdes": 48,
  "mensagem": "Ação reconhecida: bike.",
  "registro_id": 1
}
```

### 🔹 Histórico
```
GET /api/v1/users/luciana/historico
```

Exemplo:
```json
{
  "user_id": "luciana",
  "historico": [
    {
      "data_hora": "2025-01-10T14:22:33.223223",
      "classe": "bike",
      "ecoScore": 81,
      "pontos": 48
    }
  ]
}
```

## 🤖 IA Simulada — Texto para Vídeo
> "A arquitetura foi construída para usar modelos reais, mas restrições de rede impediram o download. Por isso usamos uma IA simulada para fins de apresentação."

## 🛠 Troubleshooting
- **SSL Error:** usar IA simulada  
- **int() error:** limpar tabela  
```
DELETE FROM ECO_ACTIONS;
COMMIT;
```

## 🎉 Fim
Projeto pronto para entrega!
