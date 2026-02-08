# 📊 ProdutividadeAnalytics

Plataforma de **Quantified Self** para gestão e análise de produtividade pessoal. Transforme logs de tempo brutos em insights acionáveis, agora com uma **API Restful** completa.

![CI Status](https://github.com/MaxwellAt/ProdutividadeAnalytics/actions/workflows/ci.yml/badge.svg) ![badge](https://img.shields.io/badge/Python-3.10+-blue) ![badge](https://img.shields.io/badge/Django-Full_Stack-green) ![badge](https://img.shields.io/badge/API-Restful-orange)

## ✨ Funcionalidades

### 🌐 API Restful (Novo)
- **Endpoints Completos**: `/api/v1/tasks`, `/api/v1/activities`.
- **Documentação Automática**: Swagger UI (`/swagger`) e Redoc (`/redoc`).
- **Autenticação**: Segura e pronta para integração com Mobile/React.

### 📈 Painel de Controle (Dashboard)
- **KPIs em Tempo Real**: Total de horas focadas, categorias dominantes e média diária.
- **Visualização Rica**: Gráficos interativos (Plotly) para tendências semanais.
- **Design Moderno**: Interface "Midnight Blue" com efeitos Glassmorphism.

### 🧠 Inteligência de Dados
- **Ingestão de CSV**: Importe dados de ferramentas como Toggl, RescueTime ou Clockify.
- **Auto-Classificação**: Motor de regras (Regex/Keywords) para categorização automática.

---

## 🚀 Como Rodar

### Comandos Rápidos (Makefile)
Para facilitar sua vida, incluímos um `Makefile`:
```bash
make setup       # Instala dependências
make migrate     # Configura o banco
make admin       # Cria usuário admin (admin/admin)
make run         # Roda o servidor
make test        # Roda os testes automatizados
```

### Docker (Recomendado)
```bash
docker-compose up -d --build
```
Acesse:
*   **Web**: [localhost:8000](http://localhost:8000)
*   **API Docs**: [localhost:8000/swagger](http://localhost:8000/swagger)
*   **Adminer**: [localhost:8080](http://localhost:8080)

---

## 📂 Arquitetura do Projeto

```text
/
├── dados_produtividade/    # Core da Aplicação
│   ├── api/                # [Novo] Serializers e ViewSets da API
│   ├── services/           # Lógica de Analytics e Ciência de Dados
│   ├── etl/                # Scripts de Ingestão e Processamento
│   └── tests/              # Testes Automatizados (Pytest)
├── requirements/           # Gestão de dependências (base vs local)
└── .github/workflows/      # CI/CD Pipeline (Automated Tests)
```

## 🛠️ Tecnologias
- **Backend**: Django 4, DRF (Rest Framework)
- **Docs**: Swagger/OpenAPI (drf-yasg)
- **Data**: Pandas, Plotly, PostgreSQL
- **QA**: Pytest, GitHub Actions

---
MaxwellAt © 2026

##
<div align="center">
  <img alt="ko4la" src="https://media.tenor.com/FTZx57BugI4AAAAC/koala-sleeping.gif" width="90">
</div>
