import pandas as pd
from openpyxl import load_workbook
from datetime import datetime

def exportar_fd_transmissor_temperatura(caminho_saida):
    caminho_template = r"server/excel/templates/Transmissores de Temperatura.xlsm"
    caminho_tags = r"server/excel/tags_filtradas.xlsx"

    wb_template = load_workbook(caminho_template, keep_vba=True)
    sheet_folhas = wb_template["Folhas"]
    df_tags = pd.read_excel(caminho_tags)

    mapeamento = {
        "D6": "Tag do Instrumento",
        "D12": "Fluído",
        "J32": "Fluído",
        "J36": "Densidade",
        "J37": "Viscosidade",
        "D38": "Temperatura oper. min",
        "P38": "Temperatura oper. max",
        "J39": "Pressão Oper.",
        "D41": "Vazão min",
        "P41": "Vazão max",
        "D43": "Nota"
    }

    # Campos com fallback para valores alternativos
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

            # Verifica se o valor está vazio e se há um valor padrão
            if pd.isna(valor) or valor == "":
                coluna_padrao = valores_padrao.get(coluna)
                if coluna_padrao and pd.notna(row.get(coluna_padrao)):
                    valor = row.get(coluna_padrao)

            # Se o valor for válido, preenche a célula
            new_sheet[cell] = str(valor) if pd.notna(valor) else ""

        # Preenchendo o campo "Fluído", tratando múltiplos fluidos
        fluidos = str(row.get("Fluído", "")).split("Fluído")
        for i, fluido in enumerate(fluidos):
            new_sheet[f"B{43 + i}"] = fluido.strip()

        # Preenchendo as notas, se houver
        notas = str(row.get("Nota", "")).split("Nota")
        for i, nota in enumerate(notas):
            new_sheet[f"D{43 + i}"] = nota[10:].strip()

    tag = str(row["Tag do Instrumento"])
    tag_abreviada = "".join([char for char in tag if char.isalpha()])
    caminho_saida = f"server/excel/tag_{tag_abreviada}_fd_preenchido_{data_atual}.xlsm".lower()

    wb_template.save(caminho_saida)
    print(f"Arquivo {caminho_saida} gerado com sucesso!")
