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
        "D6": "Tag do Instrumento",
        "J32": "Fluído",
        "J33": "Densidade",
        "J34": "Viscosidade",
        "D35": "Temperatura oper. min",
        "P35": "Temperatura oper. max",
        "J36": "Pressão Oper.",
        "D38": "Vazão min",
        "P38": "Vazão max",
        "D40": "Nota"
    }

    valores_padrao = {
        "Vazão max": "Vazão",
        "Vazão min": "Vazão",
        "Temperatura oper. max": "Temperatura Oper.",
        "Temperatura oper. min": "Temperatura Oper."
    }

    data_atual = datetime.today().strftime("%d-%m-%Y")

    for _, row in df_tags.iterrows():
        new_sheet = wb_template.copy_worksheet(sheet_folhas)
        nome_aba = str(row["Tag do Instrumento"])
        new_sheet.title = nome_aba

        for cell, coluna in mapeamento.items():
            valor = row.get(coluna, "")

            if pd.isna(valor) or valor == "":
                coluna_padrao = valores_padrao.get(coluna)
                if coluna_padrao and pd.notna(row.get(coluna_padrao)):
                    valor = row.get(coluna_padrao)

            new_sheet[cell] = str(valor) if pd.notna(valor) else ""

        # Preenchendo o campo "Fluído"
        fluidos = str(row.get("Fluído", "")).split("Fluído")
        for i, fluido in enumerate(fluidos):
            new_sheet[f"B{40 + i}"] = fluido.strip()

        # Preenchendo as notas
        notas = str(row.get("Nota", "")).split("Nota")
        for i, nota in enumerate(notas):
            new_sheet[f"D{40 + i}"] = nota[10:].strip()

    # Define o nome do arquivo com base na última tag, de forma segura
    if not df_tags.empty:
        ultima_tag = str(df_tags.iloc[-1]["Tag do Instrumento"])
        tag_abreviada = "".join([char for char in ultima_tag if char.isalpha()])
    else:
        tag_abreviada = "sem_tag"

    caminho_saida = f"server/excel/tag_{tag_abreviada}_fd_preenchido_{data_atual}.xlsm".lower()

    wb_template.save(caminho_saida)
    print(f"Arquivo {caminho_saida} gerado com sucesso!")
