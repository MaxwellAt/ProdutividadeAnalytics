from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db.sqlite3"
TABLE_NAME = "dados_produtividade_task"


def carregar_tarefas(db_path: Path = DB_PATH) -> pd.DataFrame:
    if not db_path.exists():
        raise FileNotFoundError(f"Banco não encontrado em: {db_path}")

    with sqlite3.connect(db_path) as conn:
        query = f"SELECT * FROM {TABLE_NAME};"
        df = pd.read_sql_query(query, conn)

    return df


def tarefas_por_dia(df: pd.DataFrame) -> pd.DataFrame:
    if "created_at" not in df.columns:
        return pd.DataFrame(columns=["dia", "tarefas_criadas"])

    datas = pd.to_datetime(df["created_at"], errors="coerce").dt.date
    resultado = (
        df.assign(dia=datas)
        .dropna(subset=["dia"])
        .groupby("dia", as_index=False)
        .size()
        .rename(columns={"size": "tarefas_criadas"})
        .sort_values("dia")
    )
    return resultado


def media_tempo_conclusao(df: pd.DataFrame) -> pd.Timedelta | None:
    if "created_at" not in df.columns or "completed_at" not in df.columns:
        return None

    df_local = df.copy()
    df_local["created_at"] = pd.to_datetime(df_local["created_at"], errors="coerce")
    df_local["completed_at"] = pd.to_datetime(df_local["completed_at"], errors="coerce")

    concluidas = df_local.dropna(subset=["created_at", "completed_at"])
    if concluidas.empty:
        return None

    tempos = concluidas["completed_at"] - concluidas["created_at"]
    return tempos.mean()


def main() -> None:
    df = carregar_tarefas()

    print("\n--- Estatísticas de Produtividade ---\n")

    por_dia = tarefas_por_dia(df)
    if por_dia.empty:
        print("Quantas tarefas são criadas por dia? -> Sem dados suficientes.")
    else:
        print("Quantas tarefas são criadas por dia?")
        print(por_dia.to_string(index=False))

    media_tempo = media_tempo_conclusao(df)
    if media_tempo is None:
        print("\nQual a média de tempo para concluir uma tarefa? -> Sem dados suficientes.")
    else:
        print(
            "\nQual a média de tempo para concluir uma tarefa? -> "
            f"{media_tempo}"
        )


if __name__ == "__main__":
    main()
