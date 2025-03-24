import pandas as pd
from openpyxl import load_workbook
from datetime import datetime

def exportar_fd_transmissor_nivel(file_path):
    caminho_template = r"server/excel/templates/Transmissor de Nível.xlsx"
    caminho_tags = r"server/excel/tags_filtradas.xlsx"

    wb_template = load_workbook(caminho_template, keep_vba=True)
    sheet_folhas = wb_template["Folhas"]
    df_tags = pd.read_excel(caminho_tags)

    mapeamento = {
        "D6": "Nº Instrumento","J32": "Fluído", "J33": "Densidade", 
        "J34": "Viscosidade", "D35": "Temperatura oper. min", "P35": "Temperatura oper. max",
        "J36": "Pressão Oper.", "D38": "Vazão min", "P38": "Vazão max", "D40": "Nota"
    }

    data_atual = datetime.today().strftime("%d-%m-%Y")  # Pega a data de hoje no formato desejado

    for _, row in df_tags.iterrows():
        new_sheet = wb_template.copy_worksheet(sheet_folhas)  
        nome_aba = str(row["Nº Instrumento"])  
        new_sheet.title = nome_aba

        for cell, coluna in mapeamento.items():
            if coluna in row and pd.notna(row[coluna]):
                new_sheet[cell] = str(row[coluna])

        fluidos = str(row.get("Fluído", "")).split("Fluído")
        for i, fluido in enumerate(fluidos):
            new_sheet[f"B{40 + i}"] = fluido.strip()
            
        notas = str(row.get("Nota", "")).split("Nota")
        for i, nota in enumerate(notas):
            new_sheet[f"D{40 + i}"] = nota[10:].strip()

    # Pegando apenas a parte inicial da tag (as letras antes de números)
    tag = str(row["Nº Instrumento"])
    tag_abreviada = "".join([char for char in tag if char.isalpha()])  # Mantém apenas letras

    # Criando o nome do arquivo no formato desejado
    caminho_saida = f"server/excel/tag_{tag_abreviada}_fd_preenchido_{data_atual}.xlsm".lower()

    # Salvar o arquivo preenchido uma única vez
    wb_template.save(caminho_saida)
    print(f"Arquivo {caminho_saida} gerado com sucesso!")

