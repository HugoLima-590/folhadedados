import pandas as pd

# Caminho do arquivo Excel
caminho_arquivo =  r"server\excel\PHS1-PR24-1702-Rev.04 LISTA DE INSTRUMENTOS.xlsx"
filtered_file_path = r"server\excel\tags_filtradas.xlsx"

df = pd.read_excel(caminho_arquivo, sheet_name="Projeto BIR", engine="openpyxl")

df.columns = (
    df.columns.astype(str).str.replace(r"\n", " ").str.strip()
)                                                                           # Limpar os nomes das colunas (remover espaços e quebras de linha)
df = df.ffill()                                                             # Preencher células mescladas (importante para garantir que todas as linhas tenham valores)
tag_instrumento = "zs"

coluna_instrumento = df.columns[3]
coluna_diametro = df.columns[37]
coluna_fluido = df.columns[42]
coluna_fluxograma = df.columns[50]
coluna_desenho_numero = df.columns[58]
coluna_tipo = df.columns[66]
coluna_densidade = df.columns[75]
coluna_viscosidade = df.columns[79]
coluna_pressao_oper = df.columns[84]
coluna_pressao_proj = df.columns[88]
coluna_temperatura_oper = df.columns[92]
coluna_temperatura_proj = df.columns[96]
coluna_vazao = df.columns[100]
coluna_posicao_da_falha = df.columns[104]
coluna_motor = df.columns[108]
coluna_num_esquema_pintura = df.columns[111]
coluna_nota = df.columns[121]


if not tag_instrumento or not isinstance(tag_instrumento, str):
        raise ValueError("O valor da TAG não pode ser nulo ou inválido.")

df_filtrado = df[
        df[coluna_instrumento].fillna("").astype(str).str.lower().str.startswith(tag_instrumento.lower())
    ]


df_filtrado = df_filtrado[
    [
        coluna_instrumento,
        coluna_diametro,
        coluna_fluido,
        coluna_fluxograma,
        coluna_desenho_numero,
        coluna_tipo,
        coluna_densidade,
        coluna_viscosidade,
        coluna_pressao_oper,
        coluna_pressao_proj,
        coluna_temperatura_oper,
        coluna_temperatura_proj,
        coluna_vazao,
        coluna_posicao_da_falha,
        coluna_motor,
        coluna_num_esquema_pintura,
        coluna_nota,
    ]
]

# Renomear as colunas para nomes mais claros
df_filtrado.columns = [
    "Nº Instrumento",
    "Diâmetro",
    "Fluído",
    "Fluxograma",
    "Desenho Nº",
    "Tipo",
    "Densidade",
    "Viscosidade",
    "Pressão Oper.",
    "Pressão Proj.",
    "Temperatura Oper.",
    "Temperatura Proj.",
    "Vazão",
    "Posição da Falha",
    "Motor",
    "Esquema Pintura Nº",
    "Nota",
]

df_filtrado[["Temperatura oper. min", "Temperatura oper. max"]] = df_filtrado[
    "Temperatura Oper."
].str.split(" - ", expand=True)
df_filtrado[["Vazão min", "Vazão max"]] = df_filtrado["Vazão"].str.split(
    " - ", expand=True
)

df_filtrado = df_filtrado.drop_duplicates(ignore_index=True).reset_index(drop=True)
df_filtrado = df_filtrado.sort_values(by="Nº Instrumento", ascending=True)

print(df_filtrado.head())

df_filtrado.to_excel(filtered_file_path, index=False, engine="openpyxl")
