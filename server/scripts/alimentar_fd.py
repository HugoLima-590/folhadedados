import os
import pandas as pd
from openpyxl import load_workbook

def exportar_fd(): 

    # Construir caminhos corretos independentemente do sistema operacional
    caminho_template = os.path.join("server", "excel", "Válvulas On-Off copia.xlsm")
    caminho_tags = os.path.join("server", "excel", "tags_filtradas.xlsx")
    caminho_saida = os.path.join("server", "excel", "FD_Preenchido.xlsm")

    # Carregar o arquivo template
    wb_template = load_workbook(caminho_template, keep_vba=True)

    # Carregar a aba 'Folhas'
    sheet_folhas = wb_template["Folhas"]
    df_tags = pd.read_excel(caminho_tags)

    mapeamento = {
        "B6": "Nº Instrumento","B8": "Fluxograma","B10": "Tipo",
        "B12": "Diâmetro","N25": "Fluído","N27": "Pressão Oper.",
        "N29": "Viscosidade","N31": "Vazão max","N32": "Vazão min",
        "N34": "Temperatura oper. max","N36": "Densidade","A43": "Nota",
    }

    for _, row in df_tags.iterrows():  # Preencher o arquivo template com os dados
        new_sheet = wb_template.copy_worksheet(sheet_folhas)
        nome_aba = str(row["Nº Instrumento"])
        new_sheet.title = nome_aba

        for cell, coluna in mapeamento.items():
            if coluna in row and pd.notna(row[coluna]):
                new_sheet[cell] = str(row[coluna])  

        notas = str(row.get("Nota", "")).split("Nota")
        for i, nota in enumerate(notas):
            new_sheet[f"A{43 + i}"] = nota.strip()

    # Salvar o novo arquivo preenchido
    wb_template.save(caminho_saida)
    print("Arquivo FD_Preenchido.xlsm gerado com sucesso!")
