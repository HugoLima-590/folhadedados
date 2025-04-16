import os
import pandas as pd
from openpyxl import load_workbook
from datetime import datetime

def exportar_fd_valvulas(caminho_saida):
    caminho_template = r"server/excel/templates/Válvulas On-Off copia.xlsm"
    caminho_tags = r"server/excel/tags_filtradas.xlsx"

    try:
        wb_template = load_workbook(caminho_template, keep_vba=True)
        sheet_folhas = wb_template["Folhas"]

        df_tags = pd.read_excel(caminho_tags)

        mapeamento = {
            "B6": "Tag do Instrumento", "B8": "Fluxograma", "B10": "Tipo",
            "B12": "Diâmetro", "N25": "Fluído", "N27": "Pressão Oper.",
            "N29": "Viscosidade", "N31": "Vazão max", "N32": "Vazão min",
            "N34": "Temperatura oper. max", "N36": "Densidade", "A43": "Nota",
        }

        # Campos que devem usar um valor alternativo se estiverem vazios
        valores_padrao = {
            "Vazão max": "Vazão",
            "Vazão min": "Vazão",
            "Temperatura oper. max": "Temperatura Oper.",
        }

        data_atual = datetime.today().strftime("%d-%m-%Y")

        for _, row in df_tags.iterrows():
            new_sheet = wb_template.copy_worksheet(sheet_folhas)
            nome_aba = str(row["Tag do Instrumento"])  
            new_sheet.title = nome_aba

            for cell, coluna in mapeamento.items():
                valor = row.get(coluna)

                # Se estiver vazio e tiver valor padrão definido
                if pd.isna(valor) and coluna in valores_padrao:
                    valor = row.get(valores_padrao[coluna])

                if pd.notna(valor):
                    new_sheet[cell] = str(valor)

            # Notas em várias linhas
            notas = str(row.get("Nota", "")).split("Nota")
            for i, nota in enumerate(notas):
                new_sheet[f"A{43 + i}"] = nota.strip()

        tag = str(row["Tag do Instrumento"])
        tag_abreviada = "".join([char for char in tag if char.isalpha()])
        output_filename = f"tag_{tag_abreviada}_fd_preenchido_{data_atual}.xlsm".lower()
        output_path = os.path.join("server/excel", output_filename)

        wb_template.save(output_path)

        return output_filename

    except Exception as e:
        print(f"Erro ao exportar FD: {e}")
        raise
