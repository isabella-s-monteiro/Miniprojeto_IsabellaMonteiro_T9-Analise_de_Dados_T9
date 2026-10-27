"""Limpeza e tratamento dos dados importados da base de varejo."""

import os
import shutil
import numpy as np
import pandas as pd

VALORES_NULOS = ["", "NULL", "NULO", "NAN", "NONE", "NA", "N/A", "-"]
COLUNAS_ID = ["CO_ID", "CL_ID", "PR_ID"]
COLUNAS_INTEIRAS = ["CO_ID", "CL_ID", "CL_EC", "CL_FHL", "PR_ID"]
COLUNAS_TEXTO = ["CL_GENERO", "CL_SEG", "PR_CAT", "PR_NOME"]

class LimpezaDados:
    def __init__(self, df):
        self.df = df.copy()
        self.relatorio = {"registros_iniciais": len(df)}

    def remover_colunas_vazias(self):
     
        colunas_unnamed = [c for c in self.df.columns if str(c).startswith("Unnamed")]
        self.df = self.df.drop(columns=colunas_unnamed).dropna(axis=1, how="all")
        self.relatorio["colunas_removidas"] = len(colunas_unnamed)
        return self

    def padronizar_textos(self):
        
        for coluna in COLUNAS_TEXTO + ["DATA"]:
            if coluna in self.df.columns:
                self.df[coluna] = self.df[coluna].astype("string").str.strip()
                if coluna != "DATA":
                    self.df[coluna] = self.df[coluna].str.upper()
                self.df[coluna] = self.df[coluna].replace(
                    {v: pd.NA for v in VALORES_NULOS}
                )
        return self

    def converter_tipos(self):
        
        self.df["DATA"] = pd.to_datetime(self.df["DATA"], dayfirst=True, errors="coerce")
        for coluna in COLUNAS_INTEIRAS:
            self.df[coluna] = pd.to_numeric(self.df[coluna], errors="coerce")
        return self

    def tratar_nulos(self):
        
        self.relatorio["nulos_encontrados"] = int(self.df.isna().sum().sum())

        antes = len(self.df)
        self.df = self.df.dropna(subset=COLUNAS_ID + ["DATA"])
        self.relatorio["removidos_sem_id_ou_data"] = antes - len(self.df)

        for coluna in ["CL_GENERO", "CL_EC", "CL_FHL", "CL_SEG"]:
            self.df[coluna] = self.df[coluna].fillna(
                self.df.groupby("CL_ID")[coluna].transform(
                    lambda s: s.mode().iloc[0] if not s.mode().empty else np.nan
                )
            )

        for coluna in ["PR_CAT", "PR_NOME"]:
            self.df[coluna] = self.df[coluna].fillna(
                self.df.groupby("PR_ID")[coluna].transform(
                    lambda s: s.mode().iloc[0] if not s.mode().empty else np.nan
                )
            )

        for coluna in ["CL_EC", "CL_FHL"]:
            self.df[coluna] = self.df[coluna].fillna(self.df[coluna].median())
        for coluna in COLUNAS_TEXTO:
            if self.df[coluna].isna().any():
                self.df[coluna] = self.df[coluna].fillna(self.df[coluna].mode().iloc[0])

        self.df[COLUNAS_INTEIRAS] = self.df[COLUNAS_INTEIRAS].round().astype("int64")
        self.df[COLUNAS_TEXTO] = self.df[COLUNAS_TEXTO].astype(str)
        return self

    def remover_duplicados(self):
       
        antes = len(self.df)
        self.df = self.df.drop_duplicates().reset_index(drop=True)
        self.relatorio["duplicados_removidos"] = antes - len(self.df)
        return self

    def executar(self):
       
        (
            self.remover_colunas_vazias()
            .padronizar_textos()
            .converter_tipos()
            .tratar_nulos()
            .remover_duplicados()
        )
        self.relatorio["registros_finais"] = len(self.df)
        return self.df

    def salvar_csv(self, caminho, fazer_backup=True):
        
        if fazer_backup:
            caminho_backup = caminho.replace(".csv", "_original.csv")
            if not os.path.exists(caminho_backup):
                shutil.copy(caminho, caminho_backup)
        self.df.to_csv(caminho, sep=";", index=False, date_format="%d/%m/%Y")

    def mostrar_relatorio(self):
       
        for chave, valor in self.relatorio.items():
            print(f"{chave.replace('_', ' ').capitalize()}: {valor}")

if __name__ == "__main__":
    from pipeline_dados_varejo import CAMINHO_CSV

    limpeza = LimpezaDados(pd.read_csv(CAMINHO_CSV, sep=";"))
    limpeza.executar()
    limpeza.mostrar_relatorio()
    limpeza.salvar_csv(CAMINHO_CSV)
    print(f"Base limpa salva em: {CAMINHO_CSV}")