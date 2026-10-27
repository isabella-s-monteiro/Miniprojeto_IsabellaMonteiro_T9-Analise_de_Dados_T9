### Mini-Projeto M1S07: Análise Exploratória e Higienização de Dados de Varejo

**Curso:** Análise de Dados (Senai/SC - SCTEC) | **Turma:** Analise_de_Dados_T9  
**Aluna:** Isabella Monteiro  

### 1. Apresentação e problema de negócio

Neste projeto trabalhei com uma base de vendas de varejo do Kaggle, com 830.000 registros de transações. O objetivo foi montar um pipeline em Python, modular e reproduzível, para limpar os dados e responder a quatro perguntas:

- Qual é o volume real de vendas válidas depois de remover inconsistências e duplicatas?
- Qual é o perfil dos clientes (estado civil, gênero e quantidade de filhos)?
- Quais categorias de produtos e SKUs mais vendem?
- Como o comportamento de compra se divide entre gêneros e classes sociais?

### 2. Tecnologias e estrutura do código

**Ferramentas:**

- **Pandas:** leitura do CSV, conversão de tipos, imputação de nulos e agrupamentos.
- **NumPy:** tratamento de valores ausentes (`np.nan`).
- **Rich:** painel de resultados no terminal, com exportação da saída em SVG.
- **Git e GitHub:** versionamento e documentação.

**Arquivos do repositório:**

| Arquivo | O que faz |
|---|---|
| `pipeline_dados_varejo.py` | Leitura do CSV, com caminho do arquivo resolvido dinamicamente (`os.path`) |
| `limpeza_dados.py` | Classe `LimpezaDados`: remove colunas vazias, padroniza texto, converte datas e remove duplicatas |
| `formatacao.py` | Exibição no terminal e formatação de números no padrão brasileiro |
| `resumo.py` | Script principal: estatística descritiva, agrupamentos e relatório final |
| `requirements.txt` | Dependências do ambiente |

### 3. Limpeza e tratamento dos dados

No diagnóstico encontrei dois problemas principais: quatro colunas totalmente vazias (`Unnamed: 10` a `Unnamed: 13`), causadas por excesso de ponto e vírgula no fim de cada linha do CSV, e muitas linhas duplicadas.

O que fiz:

1. **Colunas inúteis:** removi as quatro colunas `Unnamed`.
2. **Tipos de dados:** converti `DATA` de texto para `datetime` (dd/mm/aaaa) e os identificadores `CO_ID`, `CL_ID` e `PR_ID` para inteiros.
3. **Valores nulos:** em dados de clientes, preenchi com a moda do próprio cliente nos outros registros. Em dados de produtos, usei a moda do SKU.
4. **Duplicatas:** removi 96.553 linhas idênticas. A base passou de 830.000 para 733.447 registros, e o arquivo de 47,9 MB para 40,2 MB.

### 4. Resultado no terminal

### Painel executivo

![Painel executivo no terminal](resumo_terminal.svg)

### 5. Estatística descritiva de filhos (`CL_FHL`)

Para o perfil familiar não ser distorcido por clientes que compram várias vezes, usei só o registro mais recente de cada um dos 1.000 clientes.

| Medida | Valor |
|---|---|
| Clientes | 1.000 |
| Média | 1,14 |
| Mediana | 0,0 |
| Desvio padrão | 1,41 |
| Moda | 0 |
| Mínimo / Máximo | 0 / 4 |
| 1º Quartil (Q1 - 25%) | 0,0 |
| 3º Quartil (Q3 - 75%) | 2,0 |

### 6. Análises com `groupby`

- **Por gênero:** a divisão é equilibrada. Foram 9.615 compras do público feminino (382.427 itens) e 8.856 do masculino (351.020 itens), com leve vantagem feminina em compras e volume de itens.
- **Por categoria:** ALIMENTOS é a categoria com maior volume de itens vendidos (384.197 itens).
- **Produto mais vendido:** o SKU 51 (Papinha Infantil), com 3.322 unidades.
- **Por classe social:** a Classe B lidera em pedidos (11.843 compras), seguida pela Classe C (5.136 compras) e Classe A (1.492 compras).

### 7. Interpretação e limitações

**O que os dados mostram:**

- **Perfil dos clientes:** mediana e moda em 0 indicam que a maior parte do público não tem filhos cadastrados. Porém, a média de 1,14 e a presença de clientes com até 4 filhos apontam para um nicho familiar relevante. Isso orienta a loja a atender tanto a conveniência de pessoas sem filhos quanto o abastecimento de famílias maiores.
- **Sortimento:** o destaque de alimentos e de itens infantis, como as papinhas, sugere uma loja de abastecimento básico e conveniência.
- **Qualidade da base:** a limpeza deixou os dados consistentes e a base mais leve.

Limitações: 
Removi apenas duplicatas exatas (linhas 100% idênticas). No varejo, uma linha repetida pode ser a compra legítima de duas unidades do mesmo produto no mesmo carrinho. Como a base não tem uma coluna de quantidade por item, existe o risco de ter subestimado o volume real de vendas. Para versões futuras, o ideal é o sistema de origem registrar a quantidade vendida em cada linha.

### 8. Como executar

1. Clone este repositório.
2. Ative o ambiente virtual e instale as dependências:
   ```bash
   pip install -r requirements.txt

   
### 9. Melhorias futuras

Banco de dados (PostgreSQL): migrar o armazenamento para PostgreSQL utilizando SQLAlchemy e consultas SQL otimizadas.   
Modelo relacional (Star Schema): estruturar tabelas dimensão (clientes, produtos) e tabela fato (compras) para reduzir redundâncias.   Dashboard interativo: conectar os dados higienizados ao Power BI ou Looker Studio para análise visual de vendas por período e segmento.   
Automação de ETL: agendar o fluxo de ingestão, tratamento e emissão do relatório.
