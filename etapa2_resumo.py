import pandas as pd
from rich.panel import Panel

from carrega_dados import carrega_dados
from limpa_dados import limpa_dados
from formatacao import console, numero_br


def mostrar_resultado(df):
    total_registros = len(df)
    total_produtos = pd.to_numeric(
        df["PR_ID"], errors="coerce"
    ).count()
    total_clientes = df["CL_ID"].nunique()
    total_categorias = df["PR_CAT"].nunique()

    texto = (
        f"[bold] Registros: [/] {numero_br(total_registros)}\n"
        f"[bold] Produtos registrados: [/] {numero_br(total_produtos)}\n"
        f"[bold] Clientes: [/] {numero_br(total_clientes)}\n"
        f"[bold] Categorias: [/] {numero_br(total_categorias)}\n"
    )

    console.print(
        Panel(texto, title="Painel de Varejo", expand=False)
    )


if __name__ == "__main__":
    df = carrega_dados()

    print("Registros originais:", len(df))
    print("Duplicatas exatas:", df.duplicated().sum())

    print("\nValores ausentes por coluna:")
    print(df.isnull().sum())

    df = limpa_dados(df)
    mostrar_resultado(df)
