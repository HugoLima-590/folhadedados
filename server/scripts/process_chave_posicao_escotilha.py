import pandas as pd
from openpyxl import load_workbook
from datetime import datetime

def exportar_fd_chave_escotilha(file_path):
    caminho_template = r"server/excel/templates/Chave Posição Escotilha.xlsx"
    caminho_tags = r"server/excel/tags_filtradas.xlsx"

    wb_template = load_workbook(caminho_template, keep_vba=True)
    sheet_folhas = wb_template["Folhas"]
    df_tags = pd.read_excel(caminho_tags)

    mapeamento = {
        "D6": "Tag do Instrumento"
    }

    data_atual = datetime.today().strftime("%d-%m-%Y")  # Pega a data de hoje no formato desejado

    for _, row in df_tags.iterrows():
        new_sheet = wb_template.copy_worksheet(sheet_folhas)  
        nome_aba = str(row["Tag do Instrumento"])  
        new_sheet.title = nome_aba

        for cell, coluna in mapeamento.items():
            if coluna in row and pd.notna(row[coluna]):
                new_sheet[cell] = str(row[coluna])

    # Pegando apenas a parte inicial da tag (as letras antes de números)
    tag = str(row["Tag do Instrumento"])
    tag_abreviada = "".join([char for char in tag if char.isalpha()])  # Mantém apenas letras

    # Criando o nome do arquivo no formato desejado
    caminho_saida = f"server/excel/tag_{tag_abreviada}_fd_preenchido_{data_atual}.xlsm".lower()

    # Salvar o arquivo preenchido uma única vez
    wb_template.save(caminho_saida)
    print(f"Arquivo {caminho_saida} gerado com sucesso!")

