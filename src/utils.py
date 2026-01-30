"""
Funções auxiliares para processamento de dados de TPV e markup.

Este módulo contém funções para:
  - Carregar dados de múltiplas planilhas (CSV ou Excel) de um diretório.
  - Consolidar e combinar os dados em um DataFrame do pandas.
  - Calcular métricas como soma de TPV e média de markup por cliente.
"""

from __future__ import annotations

import os
from typing import List, Tuple, Optional

import pandas as pd


def load_data(data_dir: str, encoding: str | None = None) -> pd.DataFrame:
    """Carrega e consolida dados de todas as planilhas em `data_dir`.

    Aceita arquivos CSV e Excel (.xls ou .xlsx).  Espera colunas
    `Cliente`, `TPV` e `Markup`.  Uma coluna `Data` (com datas) é
    opcional e será convertida para dtype datetime se presente.

    Args:
        data_dir: caminho para a pasta contendo as planilhas.
        encoding: codificação opcional para arquivos CSV.

    Returns:
        DataFrame consolidado com todas as planilhas.
    """
    all_frames: List[pd.DataFrame] = []

    for filename in sorted(os.listdir(data_dir)):
        if filename.startswith("~"):  # ignora arquivos temporários
            continue
        filepath = os.path.join(data_dir, filename)
        if not os.path.isfile(filepath):
            continue
        ext = os.path.splitext(filename)[1].lower()
        try:
            if ext in {".csv"}:
                df = pd.read_csv(filepath, encoding=encoding or "utf-8", delimiter=",")
            elif ext in {".xlsx", ".xls"}:
                df = pd.read_excel(filepath)
            else:
                print(f"Ignorando arquivo não suportado: {filename}")
                continue
        except Exception as exc:
            print(f"Falha ao ler {filename}: {exc}")
            continue

        # Padroniza nomes de colunas (remove espaços extras e capitaliza)
        df = df.rename(columns={c: c.strip().title() for c in df.columns})

        # Garante que as colunas necessárias existam
        required_cols = {"Cliente", "Tpv", "Markup"}
        if not required_cols.issubset({c.title() for c in df.columns}):
            print(f"Arquivo {filename} ignorado: colunas necessárias não encontradas")
            continue

        # Converte 'Data' para datetime se existir
        if "Data" in {c.title() for c in df.columns}:
            df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

        # Assegura que TPV e markup são numéricos
        df["Tpv"] = pd.to_numeric(df["Tpv"], errors="coerce")
        df["Markup"] = pd.to_numeric(df["Markup"], errors="coerce")

        all_frames.append(df)

    if not all_frames:
        raise FileNotFoundError("Nenhum arquivo válido encontrado em data_dir")

    combined = pd.concat(all_frames, ignore_index=True)
    return combined


def compute_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Computa métricas de TPV e markup por cliente.

    Agrupa o DataFrame por coluna `Cliente` e calcula:
      * Soma de TPV
      * Média de markup (em percentuais)
      * Número de registros por cliente

    Args:
        df: DataFrame consolidado.

    Returns:
        DataFrame com colunas `Cliente`, `Tpv_Total`, `Markup_Medio`, `Registros`.
    """
    summary = (
        df.groupby("Cliente")
        .agg(
            Tpv_Total=("Tpv", "sum"),
            Markup_Medio=("Markup", "mean"),
            Registros=("Cliente", "count"),
        )
        .reset_index()
    )
    return summary
