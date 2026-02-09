# ProdutividadeAnalytics

![CI](https://github.com/MaxwellAt/ProdutividadeAnalytics/actions/workflows/ci.yml/badge.svg) ![Coverage](https://img.shields.io/badge/Coverage-92%25-green) ![Python](https://img.shields.io/badge/Python-3.10-blue)

**Quantified Self Analytics Platform**. A robust backend for aggregating, classifying, and visualizing personal productivity metrics. Features a decoupled Service Layer architecture and a Pandas-powered analytics engine.

## 🛠 Tech Stack

| Category | Technologies |
|----------|--------------|
| **Core** | Python 3.10, Django 4.2, DRF |
| **Data** | Pandas, NumPy, Plotly JSON |
| **Infra** | Docker Compose, PostgreSQL 15, Gunicorn |
| **QA**      | Pytest, Flake8, GitHub Actions |

## 🏗 Architecture

This project implements a **Service-Oriented** pattern to decouple business logic from the framework:

- **API Layer (`/api`)**: Thin DRF ViewSets responsible strictly for serialization and HTTP handling.
- **Service Layer (`/services`)**: Encapsulates domain logic and data processing:
    - `TaskService`: Handles transactional logic, validation, and side-effects.
    - `AnalyticsService`: Performs OLAP-style aggregations using Pandas DataFrames.
- **Data Layer**: PostgreSQL optimized for time-series queries.

## 🔌 API Specification

Full OpenAPI 3.0 documentation available at `/swagger`.

- `GET /api/v1/analytics/` : Real-time KPI generation via Pandas.
- `GET /api/v1/tasks/` : Resource management with extensive filtering.

## 🚀 Setup & Deployment

### Docker (Production)

```bash
docker-compose up -d --build
```

### Local Development

```bash
make setup
make run
```

### Testing

```bash
pytest
```
