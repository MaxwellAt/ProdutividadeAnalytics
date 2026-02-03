# ProdutividadeAnalytics

Sistema de Gestão e Análise de Dados de Produtividade.

## Funcionalidades

As principais funcionalidades deste aplicativo são:

- Adicionar uma nova tarefa;
- Editar uma tarefa existente;
- Remover uma tarefa;
- Visualizar todas as tarefas cadastradas.
- Gerar estatísticas de produtividade (via análise em dados).

## Como utilizar

Para utilizar este aplicativo, siga os passos abaixo:

1. Clone este repositório em seu computador:
>git clone https://github.com/MaxwellAt/ProdutividadeAnalytics.git

2. Acesse a pasta do projeto:
>cd ProdutividadeAnalytics

3. Instale as dependências:
>pip install -r requeriments.txt

### Configuração automatizada do ambiente

Se preferir, use o script de setup:

>chmod +x scripts/setup_env.sh
>./scripts/setup_env.sh

4. Crie o banco de dados:
>python manage.py migrate

5. Inicie o servidor:
>python manage.py runserver


6. Acesse o aplicativo no seu navegador, através do endereço http://localhost:8000/.

## Análise de produtividade

Para gerar estatísticas a partir das tarefas cadastradas:

>python analise_produtividade.py

## Tecnologias utilizadas

Este projeto foi desenvolvido com as seguintes tecnologias:

- Python
- Django
- HTML
- Pandas

##
<div align="center">
  <img alt="ko4la" src="https://media.tenor.com/FTZx57BugI4AAAAC/koala-sleeping.gif" width="90">
</div>
