import pandas as pd

def processar_excel(caminho_arquivo, tag_instrumento):
    
    #Lê o arquivo mas só as abas
    abas = pd.ExcelFile(caminho_arquivo, engine="openpyxl").sheet_names
    
    #retorna somente a primeira aba diferente de capa
    sheet_name = [aba for aba in abas if aba.lower() !="capa"][0]
    
    #aciona a aba para a leitura do arquivo
    df = pd.read_excel(caminho_arquivo, sheet_name= sheet_name, engine="openpyxl")

    #converte em string, substitui quebras de linha por espaço e remove espaços extras no inicio e fim
    df.columns = df.columns.astype(str).str.replace(r"\n", " ").str.strip()
    
    #Preenche os valores NaN com os valores de antes
    df = df.ffill()
    
    colunas_interesse = [
        df.columns[3], df.columns[37], df.columns[42], df.columns[50],
        df.columns[58], df.columns[66], df.columns[75], df.columns[79],
        df.columns[84], df.columns[88], df.columns[92], df.columns[96],
        df.columns[100], df.columns[104], df.columns[108], df.columns[111], df.columns[121]
    ]
    
    df_filtrado = df[df[df.columns[3]].fillna("").astype(str).str.lower().str.startswith(tag_instrumento.lower())]
    """
    Explicação da linha de código acima:
    Seleciona a 4° coluna,
    preenche NaN por espaços,
    converte todos os valores para string e minusculo,
    filtra as linhas onde o valor da coluna começa com o valor de tag_instrumento,
    mantém apenas as linhas que anteeram ao critério acima
    """
    #Filtra apenas as colunas listadas
    df_filtrado = df_filtrado[colunas_interesse]

    df_filtrado.columns = [
        "Nº Instrumento", "Diâmetro", "Fluído", "Fluxograma", "Desenho Nº",
        "Tipo", "Densidade", "Viscosidade", "Pressão Oper.", "Pressão Proj.",
        "Temperatura Oper.", "Temperatura Proj.", "Vazão", "Posição da Falha",
        "Motor", "Esquema Pintura Nº", "Nota"
    ]
    
    def split_vazao(vazao_value):
        if isinstance(vazao_value, str) and " - " in vazao_value:
            return vazao_value.split(" - ", 1)  
        else:
            return [None, None]  

    df_filtrado[["Vazão min", "Vazão max"]] = df_filtrado["Vazão"].apply(split_vazao).apply(pd.Series)

    df_filtrado[["Temperatura oper. min", "Temperatura oper. max"]] = df_filtrado["Temperatura Oper."].apply(split_vazao).apply(pd.Series)

    df_filtrado = df_filtrado.drop_duplicates(ignore_index=True).reset_index(drop=True)
    df_filtrado = df_filtrado.sort_values(by="Nº Instrumento", ascending=True)
    df_filtrado.to_excel(r"server/excel/tags_filtradas.xlsx", index=False, engine="openpyxl")
    
    return df.to_dict(orient="records")