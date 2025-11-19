# EcoWork IoT - Sistema de Reconhecimento de Ações Sustentáveis

Sistema de visão computacional que utiliza inteligência artificial para reconhecer e pontuar ações sustentáveis através de análise de imagens.

## 📋 Sobre o Projeto

O EcoWork IoT é uma solução que combina visão computacional e machine learning para identificar ações sustentáveis em imagens, atribuindo pontuações e scores ecológicos aos usuários. O sistema reconhece diferentes categorias de ações sustentáveis como uso de bicicletas, transporte público, caronas, uso de materiais reutilizáveis, entre outras.

## 🏗️ Arquitetura

O projeto está organizado nas seguintes estruturas:

```
ecowork-iot/
├── api/                 # API FastAPI com endpoints de inferência
│   ├── main.py         # Endpoints principais da API
│   ├── inference.py    # Lógica de inferência e processamento de imagens
│   ├── models.py       # Modelos Pydantic para validação
│   └── requirements.txt # Dependências Python
├── database/            # Configuração e schema do banco de dados
│   ├── db_config.py    # Configuração de conexão Oracle
│   └── schema_oracle.sql # Schema do banco de dados
├── ml/                  # Modelos e treinamento
│   ├── train.py        # Script de treinamento do modelo
│   ├── dataset/        # Dataset de imagens para treinamento
│   └── saved_models/   # Modelos treinados salvos
└── devops/              # Configurações de deployment
    └── Dockerfile      # Containerização da aplicação
```

## 🚀 Funcionalidades

- **EcoScan**: Endpoint que recebe imagens e identifica ações sustentáveis
- **Sistema de Pontuação**: Atribui scores ecológicos e pontos verdes baseados nas ações identificadas
- **Histórico de Usuário**: Consulta de histórico de ações sustentáveis por usuário
- **Health Check**: Endpoint para verificar status do modelo e conexão com banco de dados

## 🛠️ Tecnologias Utilizadas

- **FastAPI**: Framework web para construção da API
- **TensorFlow/Keras**: Framework de deep learning
- **MobileNetV2**: Modelo pré-treinado para classificação de imagens
- **Oracle Database**: Banco de dados para armazenamento de ações e usuários
- **PIL/Pillow**: Processamento de imagens
- **Docker**: Containerização da aplicação

## 📦 Instalação

### Pré-requisitos

- Python 3.10+
- Oracle Database (ou Oracle Cloud Autonomous Database)
- Docker (opcional, para containerização)

### Configuração Local

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd ecowork-iot
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
cd api
pip install -r requirements.txt
```

4. Execute a API (na raiz do projeto):
```bash
uvicorn api.main:app --reload
```

A API estará disponível em `http://localhost:8000`

### Documentação da API

Após iniciar a API, acesse:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🐳 Docker

Para executar com Docker:

1. Construa a imagem:
```bash
docker build -t ecowork-iot -f devops/Dockerfile .
```

2. Execute o container:
```bash
docker run -p 8000:8000 \
  -e ORACLE_USER=seu_usuario \
  -e ORACLE_PASSWORD=sua_senha \
  -e ORACLE_DSN=seu_dsn \
  ecowork-iot
```

## 📡 Endpoints da API

### POST `/api/v1/ecoscan`
Analisa uma imagem e identifica ações sustentáveis.

**Parâmetros:**
- `image`: Arquivo de imagem (multipart/form-data)
- `user_id`: ID do usuário (form data)

**Resposta:**
```json
{
  "user_id": "string",
  "classe_predita": "string",
  "probabilidade": 0.0,
  "ecoScore": 0,
  "pontos_verdes": 0,
  "mensagem": "string",
  "registro_id": 0
}
```

### GET `/api/v1/health`
Verifica o status da API, modelo e conexão com banco de dados.

**Resposta:**
```json
{
  "status": "ok",
  "model_loaded": true,
  "model_name": "string",
  "database_connection": "ok"
}
```

### GET `/api/v1/users/{user_id}/historico`
Retorna o histórico de ações sustentáveis de um usuário.

**Resposta:**
```json
{
  "user_id": "string",
  "historico": [
    {
      "data_hora": "string",
      "classe": "string",
      "ecoScore": 0,
      "pontos": 0
    }
  ]
}
```

## 🎯 Classes Reconhecidas

O sistema reconhece as seguintes classes de ações sustentáveis:

- `bike`: Uso de bicicleta
- `transporte_publico`: Uso de transporte público
- `carona`: Compartilhamento de carona
- `reutilizavel`: Uso de materiais reutilizáveis
- `economia_energia`: Ações de economia de energia
- `nao_sustentavel`: Ações não sustentáveis

## 🤖 Treinamento do Modelo

Para treinar um modelo customizado:

1. Organize seu dataset em `ml/dataset/` com subpastas por classe
2. Execute o script de treinamento:
```bash
cd ml
python train.py
```

O modelo treinado será salvo em `ml/saved_models/ecowork_mobilenet.h5`

