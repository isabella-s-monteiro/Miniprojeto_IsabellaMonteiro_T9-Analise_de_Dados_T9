"""Módulo de carregamento e integração do pipeline de dados."""

import os
import pandas as pd
from limpeza_dados import LimpezaDados


CAMINHO_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "base_varejo.csv")

def importar_dados(limpar=True, mostrar_relatorio=False):
   
    df = pd.read_csv(CAMINHO_CSV, sep=";")
    if limpar:
        limpeza = LimpezaDados(df)
        df = limpeza.executar()
        if mostrar_relatorio:
            limpeza.mostrar_relatorio()
    return df

if __name__ == "__main__":
    df = importar_dados(mostrar_relatorio=True)
    print(f"{len(df)} registros carregados.")
    print(df.head())