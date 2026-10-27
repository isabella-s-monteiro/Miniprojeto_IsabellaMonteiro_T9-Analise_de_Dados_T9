"""Cálculo, estatísticas descritivas, agrupamentos e conclusões da base de varejo."""

import pandas as pd
from rich.panel import Panel

from pipeline_dados_varejo import importar_dados
from formatacao import console, numero_br

def calcular_estatisticas_filhos(df):

    df_clientes = (
        df.assign(DATA=pd.to_datetime(df["DATA"], dayfirst=True))
        .sort_values("DATA")
        .drop_duplicates(subset="CL_ID", keep="last")
    )
    s_filhos = df_clientes["CL_FHL"]
    
    return {
        "contagem": int(s_filhos.count()),
        "media": float(s_filhos.mean()),
        "mediana": float(s_filhos.median()),
        "desvio_padrao": float(s_filhos.std()),
        "moda": int(s_filhos.mode().iloc[0]),
        "minimo": int(s_filhos.min()),
        "maximo": int(s_filhos.max()),
        "q1_25": float(s_filhos.quantile(0.25)),
        "q3_75": float(s_filhos.quantile(0.75)),
    }

def mostrar_resumo(df):
    
    total_registros = len(df)
    total_compras = df["CO_ID"].nunique()
    total_clientes = df["CL_ID"].nunique()
    
    estat_fhl = calcular_estatisticas_filhos(df)
    
    compras_por_genero = df.groupby("CL_GENERO")["CO_ID"].nunique()
    itens_por_genero = df.groupby("CL_GENERO").size()
    
    itens_por_categoria = df.groupby("PR_CAT").size().sort_values(ascending=False)
    categoria_top = itens_por_categoria.index[0]
    

    compras_por_classe = df.groupby("CL_SEG")["CO_ID"].nunique()

    texto = (
        f"[bold yellow]1. VISÃO GERAL DA BASE[/]\n"
        f" • Total de registros limpos: {numero_br(total_registros)}\n"
        f" • Total de compras únicas: {numero_br(total_compras)}\n"
        f" • Total de clientes únicos: {numero_br(total_clientes)}\n\n"
        
        f"[bold yellow]2. ITEM 3 - ESTATÍSTICA DESCRITIVA DE FILHOS (CL_FHL)[/]\n"
        f" • Contagem de clientes: {numero_br(estat_fhl['contagem'])}\n"
        f" • Média: {estat_fhl['media']:.2f}\n"
        f" • Mediana: {estat_fhl['mediana']:.1f}\n"
        f" • Desvio Padrão: {estat_fhl['desvio_padrao']:.2f}\n"
        f" • Moda: {estat_fhl['moda']}\n"
        f" • Mínimo: {estat_fhl['minimo']} | Máximo: {estat_fhl['maximo']}\n"
        f" • 1º Quartil (Q1 - 25%): {estat_fhl['q1_25']:.1f}\n"
        f" • 3º Quartil (Q3 - 75%): {estat_fhl['q3_75']:.1f}\n\n"
        
        f"[bold yellow]3. ITEM 4 - ANÁLISES POR AGRUPAMENTO (groupby)[/]\n"
        f" • Agrupamento 1 (Gênero):\n"
        f"   - Feminino: {numero_br(compras_por_genero.get('F', 0))} compras | {numero_br(itens_por_genero.get('F', 0))} itens\n"
        f"   - Masculino: {numero_br(compras_por_genero.get('M', 0))} compras | {numero_br(itens_por_genero.get('M', 0))} itens\n"
        f" • Agrupamento 2 (Categoria de Produto):\n"
        f"   - Categoria Líder: {categoria_top} ({numero_br(itens_por_categoria.iloc[0])} itens vendidos)\n"
        f"   - Total de Categorias: {len(itens_por_categoria)}\n"
        f" • Agrupamento 3 (Classe / Segmento):\n"
        f"   - Classe A: {numero_br(compras_por_classe.get('A', 0))} compras | Classe B: {numero_br(compras_por_classe.get('B', 0))} compras | Classe C: {numero_br(compras_por_classe.get('C', 0))} compras\n\n"
        
        f"[bold yellow]4. ITEM 5 - BLOCO DE CONCLUSÕES & INSIGHTS[/]\n"
        f" 1. Higienização Eficiente: Foram removidas 4 colunas nulas ('Unnamed') e eliminadas 96.553 duplicatas, restando 733.447 registros válidos.\n"
        f" 2. Perfil Demográfico Familiar: A coluna de filhos apresenta média de {estat_fhl['media']:.2f} e mediana {estat_fhl['mediana']:.0f}, indicando perfil predominante de famílias com 1 filho.\n"
        f" 3. Distribuicão de Vendas por Gênero: Há equilíbrio entre o público feminino e masculino, com leve vantagem do público feminino em volume de compras.\n"
        f" 4. Concentração em Alimentos: A categoria '{categoria_top}' responde pelo maior volume absoluto de movimentação da base.\n"
        f" 5. Problema Remanescente: A remoção de duplicatas exatas pode ter apagado compras legítimas de itens idênticos no mesmo pedido; recomenda-se adicionar uma coluna explícita de 'Quantidade' por linha."
    )

    console.print(Panel(texto, title="[bold white]M1S07 - Análise Exploratória e Resumo Executivo[/]", expand=False))

    try:
        console.save_svg("resumo_terminal.svg", title="Resumo Executivo Varejo - M1S07")
    except Exception:
        pass

if __name__ == "__main__":
    df = importar_dados()
    mostrar_resumo(df)