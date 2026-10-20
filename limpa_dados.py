
import pandas as pd
from carrega_dados import carrega_dados


def limpa_dados(df):
    """Limpa a base de dados de varejo."""

    # Remover colunas sem nome
    colunas_para_remover = [
        "Unnamed: 10",
        "Unnamed: 11",
        "Unnamed: 12",
        "Unnamed: 13"
    ]
    df = df.drop(columns=colunas_para_remover, errors="ignore")

    # Tratar valores ausentes
    # O tratamento será definido após verificar os dados.

    # Remover duplicatas
    df = df.drop_duplicates()

    return df
