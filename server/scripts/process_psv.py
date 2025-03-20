import pandas as pd
from openpyxl import load_workbook
from datetime import datetime

def exportar_fd_psv(file_path):
    caminho_template = r"server/excel/templates/PSV.xlsm"
    caminho_tags = r"server/excel/tags_filtradas.xlsx"

    wb_template = load_workbook(caminho_template, keep_vba=True)
    sheet_folhas = wb_template["Folhas"]
    df_tags = pd.read_excel(caminho_tags)

    mapeamento = {
        "G7": "Nº Instrumento", "B8": "Fluxograma", "B10": "Tipo",
        "B12": "Diâmetro", "N25": "Fluído", "N27": "Pressão Oper.",
        "N29": "Viscosidade", "N31": "Vazão max", "N32": "Vazão min",
        "N34": "Temperatura oper. max", "N36": "Densidade", "A43": "Nota",
    }

    data_atual = datetime.today().strftime("%d-%m-%Y")  # Pega a data de hoje no formato desejado

    for _, row in df_tags.iterrows():
        new_sheet = wb_template.copy_worksheet(sheet_folhas)  
        nome_aba = str(row["Nº Instrumento"])  
        new_sheet.title = nome_aba

        for cell, coluna in mapeamento.items():
            if coluna in row and pd.notna(row[coluna]):
                new_sheet[cell] = str(row[coluna])

        notas = str(row.get("Nota", "")).split("Nota")
        for i, nota in enumerate(notas):
            new_sheet[f"A{43 + i}"] = nota.strip()

    # Pegando apenas a parte inicial da tag (as letras antes de números)
    tag = str(row["Nº Instrumento"])
    tag_abreviada = "".join([char for char in tag if char.isalpha()])  # Mantém apenas letras

    # Criando o nome do arquivo no formato desejado
    caminho_saida = f"server/excel/tag_{tag_abreviada}_fd_preenchido_{data_atual}.xlsm"

    # Salvar o arquivo preenchido uma única vez
    wb_template.save(caminho_saida)
    print(f"Arquivo {caminho_saida} gerado com sucesso!")

