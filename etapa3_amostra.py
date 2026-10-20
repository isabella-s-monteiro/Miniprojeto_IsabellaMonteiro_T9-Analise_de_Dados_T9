from rich import console
from rich.panel import Panel

from rich.table import Table

from carrega_dados import carrega_dados
from formatacao import console, numero_br

def mostrar_amostra(df, linha=4):

    colunas = [
    "DATA",
    "CO_ID",
    "CL_ID",
    "CL_GENERO",
    "CL_EC",
    "CL_FHL",
    "CL_SEG",
    "PR_ID",
    "PR_CAT",
    "PR_NOME"
]

    tabela = Table(title=f"Primeiras {linha} linhas", header_style="bold cyan")

    for coluna in colunas:
        tabela.add_column(coluna)

    for _, registro in df.head(linha).iterrows():
        valores = [str(registro[coluna]) for coluna in colunas]
        tabela.add_row(*valores)
    
    console.print(tabela)   

if __name__ == "__main__":
    df = carrega_dados()
    mostrar_amostra(df)
