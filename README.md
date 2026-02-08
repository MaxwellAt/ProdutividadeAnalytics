# 📊 ProdutividadeAnalytics

Plataforma de **Quantified Self** para gestão e análise de produtividade pessoal. Transforme logs de tempo brutos em insights acionáveis através de dashboards modernos e classificação inteligente.

![badge](https://img.shields.io/badge/Status-Completed-success) ![badge](https://img.shields.io/badge/Python-3.10+-blue) ![badge](https://img.shields.io/badge/Django-4.0+-green) ![badge](https://img.shields.io/badge/Docker-Ready-blue)

## ✨ Funcionalidades

### 📈 Painel de Controle (Dashboard)
- **KPIs em Tempo Real**: Total de horas focadas, categorias dominantes e média diária.
- **Visualização Rica**: Gráficos interativos (Plotly) para tendências semanais, distribuição por fonte e categorias.
- **Design Moderno**: Interface "Midnight Blue" com efeitos Glassmorphism.

### 🧠 Inteligência de Dados
- **Ingestão de CSV**: Importe dados de ferramentas como Toggl, RescueTime ou Clockify.
- **Auto-Classificação**: Motor de regras (Regex/Keywords) que categoriza automaticamente atividades novas com base na descrição.
- **Dimensões**: Análise por Categoria, Fonte e Projetos.

### 🛠️ Gestão de Tarefas
- CRUD completo de tarefas diárias.
- Associação de tarefas a categorias de produtividade.

## 🚀 Como Rodar

### Opção 1: Docker (Recomendado)
Ambiente completo isolado com Banco de Dados PostgreSQL e Adminer.

```bash
# 1. Subir os containers
docker-compose up -d --build

# 2. Acessar a aplicação
# Web: http://localhost:8000
# Adminer (DB GUI): http://localhost:8080
```

### Opção 2: Instalação Manual
```bash
# 1. Criar ambiente virtual e instalar dependências
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configurar variáveis de ambiente (Opte por copiar o .env.example)
# Certifique-se de configurar o DATABASE_URL se não for usar SQLite

# 3. Executar migrações
python manage.py makemigrations
python manage.py migrate

# 4. Iniciar servidor
python manage.py runserver
```

### 📚 Guia de Uso

- **Admin**: Acesse `/admin` para criar Categorias e Regras de Classificação.
- **Importação**: Use a aba "Importar CSV" para carregar seus dados históricos.

## 🛠️ Tecnologias Utilizadas
- **Backend / Web**: Django, Gunicorn, WhiteNoise
- **Data Science**: Pandas, Plotly (Visualização)
- **Frontend**: Bootstrap 5, Custom CSS (Glassmorphism)
- **Infraestrutura**: Docker, Docker Compose, PostgreSQL

---
MaxwellAt © 2026

##
<div align="center">
  <img alt="ko4la" src="https://media.tenor.com/FTZx57BugI4AAAAC/koala-sleeping.gif" width="90">
</div>
