#!/usr/bin/env python3
"""Script principal para processar planilhas de TPV e markup.

Este script lê todos os arquivos CSV e Excel da pasta `data/`,
consolida as informações em um único DataFrame, calcula métricas por
cliente e gera gráficos interativos usando a biblioteca Plotly.

Uso:
    python src/process_data.py [--data-dir PATH] [--report-dir PATH]

As dependências são pandas, openpyxl e plotly. Instale‑as com:
    pip install pandas openpyxl plotly

"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

import plotly.express as px
import pandas as pd

from utils import load_data, compute_summary


def main(data_dir: str, report_dir: str) -> None:
    # Garante que a pasta de relatórios exista
    Path(report_dir).mkdir(parents=True, exist_ok=True)

    # Carrega e consolida dados
    print(f"Lendo planilhas de {data_dir} ...")
    df = load_data(data_dir)

    # Calcula resumo por cliente
    summary = compute_summary(df)
    print("Resumo por cliente:")
    print(summary.head())

    # Ordena os dados para gráficos
    summary_sorted_tpv = summary.sort_values("Tpv_Total", ascending=False)
    summary_sorted_markup = summary.sort_values("Markup_Medio", ascending=False)

    # Gráfico de barras: TPV total por cliente
    fig_tpv = px.bar(
        summary_sorted_tpv,
        x="Cliente",
        y="Tpv_Total",
        title="TPV total por cliente",
        labels={"Cliente": "Cliente", "Tpv_Total": "TPV Total"},
    )
    fig_tpv.update_layout(xaxis_tickangle=-45)
    output_tpv = os.path.join(report_dir, "tpv_por_cliente.html")
    fig_tpv.write_html(output_tpv, include_plotlyjs="cdn")
    print(f"Gráfico salvo em {output_tpv}")

    # Gráfico de barras: markup médio por cliente
    fig_markup = px.bar(
        summary_sorted_markup,
        x="Cliente",
        y="Markup_Medio",
        title="Markup médio por cliente",
        labels={"Cliente": "Cliente", "Markup_Medio": "Markup médio"},
    )
    fig_markup.update_layout(xaxis_tickangle=-45)
    output_markup = os.path.join(report_dir, "markup_por_cliente.html")
    fig_markup.write_html(output_markup, include_plotlyjs="cdn")
    print(f"Gráfico salvo em {output_markup}")

    # Se houver coluna Data, gera gráfico temporal (soma de TPV por mês)
    if "Data" in df.columns:
        df_date = df.dropna(subset=["Data"]).copy()
        if not df_date.empty:
            # Normaliza a data para mês/ano
            df_date["AnoMes"] = df_date["Data"].dt.to_period("M").dt.to_timestamp()
            ts_summary = (
                df_date.groupby("AnoMes")
                .agg(Tpv_Total=("Tpv", "sum"), Markup_Medio=("Markup", "mean"))
                .reset_index()
            )
            # Gráfico de linha para TPV ao longo do tempo
            fig_tpv_ts = px.line(
                ts_summary,
                x="AnoMes",
                y="Tpv_Total",
                title="Evolução do TPV ao longo do tempo",
                labels={"AnoMes": "Data", "Tpv_Total": "TPV Total"},
            )
            output_ts = os.path.join(report_dir, "tpv_ao_longo_do_tempo.html")
            fig_tpv_ts.write_html(output_ts, include_plotlyjs="cdn")
            print(f"Gráfico temporal salvo em {output_ts}")

            # Gráfico de linha para markup médio ao longo do tempo
            fig_markup_ts = px.line(
                ts_summary,
                x="AnoMes",
                y="Markup_Medio",
                title="Evolução do markup médio ao longo do tempo",
                labels={"AnoMes": "Data", "Markup_Medio": "Markup médio"},
            )
            output_markup_ts = os.path.join(report_dir, "markup_ao_longo_do_tempo.html")
            fig_markup_ts.write_html(output_markup_ts, include_plotlyjs="cdn")
            print(f"Gráfico temporal salvo em {output_markup_ts}")

    print("Processamento concluído.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Processa planilhas de TPV e markup.")
    parser.add_argument(
        "--data-dir",
        default=os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"),
        help="Diretório onde estão as planilhas. Padrão: ./data",
    )
    parser.add_argument(
        "--report-dir",
        default=os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports"),
        help="Diretório onde os relatórios serão salvos. Padrão: ./reports",
    )
    args = parser.parse_args()
    main(args.data_dir, args.report_dir)
