# 📊 ProdutividadeAnalytics API

Backend robusto para **Quantified Self** com foco em Engenharia de Dados e API-First Design.
Este projeto demonstra arquitetura modular em Django, separação de camadas de serviço, ingestão de dados e testes automatizados.

![CI Status](https://github.com/MaxwellAt/ProdutividadeAnalytics/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/badge/Coverage-92%25-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Django REST](https://img.shields.io/badge/Django_REST-API_First-red)

---

<<<<<<< HEAD

- **Views / ViewSets**: Camada de Interface (HTTP/HTML/JSON).
- **Services**: Camada de Lógica de Negócios (Ex: `TaskService`, `AnalyticsService`).
- **Models**: Camada de Dados e Definições de Schema.
- **API (DRF)**: Exposição RESTful independente para consumo externo.
=======
## 🏗️ Arquitetura de Software

O projeto segue padrões de **Clean Architecture** adaptados ao Django, evitando o anti-padrão de "Fat Models/Views".
>>>>>>> bb9a095 (docs: atualização do README.md com melhorias na descrição da API e estrutura do projeto)

### 1. **Service Layer** (Regra de Negócio Pura)
A lógica não vive nas Views nem nos Models, mas em serviços testáveis e desacoplados.
- `TaskService`: Centraliza operações CRUD, garantindo que API e Web interface usem a mesma lógica.
- `AnalyticsService`: Motor de processamento de dados com Pandas, gerando insights estatísticos.

### 2. **API-First Design** (Django Rest Framework)
Exposição de dados via JSON com documentação automática.
- Endpoints RESTful completos (`/api/v1/`).
- Documentação **Swagger/OpenAPI** embutida (`/swagger`).

### 3. **Engenharia de Dados & ETL**
- **Ingestão**: Módulos para processamento de CSV (Toggl, RescueTime).
- **Auto-Classificação**: Algoritmos (Services) que categorizam logs de tempo automaticamente com base em regras regex.

### 4. **Qualidade de Código**
- **Testes Automatizados**: Pytest cobrindo Models, Services e Integração de API.
- **CI/CD**: Pipeline de integração contínua via GitHub Actions.

---

## 🌐 Endpoints Principais (API)

Acesse a documentação interativa em `/swagger` para testar os endpoints.

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/v1/analytics/` | KPIs agregados (JSON puro) com métricas de produtividade. |
| `GET` | `/api/v1/tasks/` | Lista tarefas com paginação e filtros. |
| `POST` | `/api/v1/activities/` | Log de nova atividade temporal. |
| `GET` | `/api/v1/analytics/weekly_trend/` | Dados processados para plotagem de gráficos. |

#### Exemplo de Resposta (Analytics):
```json
{
  "total_tasks": 24,
  "completed_tasks": 18,
  "completion_rate": 75.0,
  "focus_score": 82,
  "top_category": "Deep Work"
}
```

---

## 🚀 Como Rodar

### Comandos de Engenharia (Makefile)
Utilize o `Makefile` para rotinas padronizadas:

```bash
make setup       # Instala dependências e ambiente
make migrate     # Aplica migrações de banco
make admin       # Cria superusuário (admin/admin)
make test        # Executa suíte de testes (Pytest)
make run         # Inicia o servidor de desenvolvimento
```

### via Docker
Ambiente isolado com PostgreSQL e Adminer.
```bash
docker-compose up -d --build
```
- **API Docs**: [localhost:8000/swagger](http://localhost:8000/swagger)
- **Adminer (DB)**: [localhost:8080](http://localhost:8080)

---

## 📂 Estrutura de Pastas

```text
/
├── dados_produtividade/    # Módulo Principal
│   ├── api/                # Camada de Interface (Serializers, ViewSets)
│   ├── services/           # Camada de Domínio (Business Logic)
│   ├── etl/                # Camada de Processamento de Dados
│   └── tests/              # Teste e QA
├── requirements/           # Dependências Modulares
└── .github/workflows/      # CI Pipeline
```

## 🛠️ Stack Tecnológico
- **Core**: Python 3.10+, Django 4.2
- **API**: Django Rest Framework (DRF), drf-yasg (Swagger)
- **Data**: Pandas, NumPy (Processamento), Plotly (Viz engine)
- **Infra**: Docker, PostgreSQL, Gunicorn
- **QA**: Pytest, GitHub Actions

---
MaxwellAt © 2026
