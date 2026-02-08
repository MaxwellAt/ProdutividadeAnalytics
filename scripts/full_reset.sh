#!/bin/bash
rm -f db.sqlite3
rm -f dados_produtividade/migrations/0*.py
touch dados_produtividade/migrations/__init__.py
python manage.py makemigrations dados_produtividade
python manage.py migrate
python manage.py run_etl
echo "Reset complete. Logs generated."
