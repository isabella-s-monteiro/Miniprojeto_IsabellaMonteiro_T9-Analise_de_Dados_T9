"""Etapa de Formatação do Meus dados que serão exibidos"""

from rich.console import Console    

console = Console()

def numero_br (valor, casas_decimais=0):
    texto = f"{valor:,.{casas_decimais}f}"
    texto =texto.replace(",", "X")
    texto = texto.replace(".", ",")
    texto = texto.replace("X", ".")
    return texto
