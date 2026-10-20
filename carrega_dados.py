
import pandas as pd
from rich.panel import Panel
from rich.console import Console

console = Console()

# Caminho do arquivo CSV
CAMINHO_CSV = "dados_csv.csv"


def carrega_dados():
    """Carrega a base de dados de varejo."""
    df = pd.read_csv(CAMINHO_CSV, sep=";")
    return df


if __name__ == "__main__":
    df = carrega_dados()
    print(df.head())
