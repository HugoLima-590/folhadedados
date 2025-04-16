import pandas as pd
from openpyxl import load_workbook
from datetime import datetime
import re


def exportar_fd_chave_baixa(file_path):
    caminho_template = r"server/excel/templates/Chave de Vazão Baixa.xlsx"
    caminho_tags = r"server/excel/tags_filtradas.xlsx"

    wb_template = load_workbook(caminho_template, keep_vba=True)
    sheet_folhas = wb_template["Folhas"]
    df_tags = pd.read_excel(caminho_tags)

    mapeamento = {
        "D6": "Tag do Instrumento",
        "D12": "Fluído",
        "D15": "Diâmetro",
        "D25": "Diâmetro",
        "J32": "Fluído",
        "J33": "Densidade",
        "J34": "Viscosidade",
        "J36": "Pressão Oper.",
        "D38": "Vazão min",
        "P38": "Vazão max",
        "D40": "Nota",
    }

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

        notas = str(row.get("Nota", "")).split("Nota")
        for i, nota in enumerate(notas):
            new_sheet[f"A{43 + i}"] = nota.strip()

    # Pegando apenas a parte inicial da tag (as letras antes de números)
    tag = str(row["Tag do Instrumento"])
    tag_abreviada = "".join(re.findall(r"[A-Za-z]", tag))[:3]  # Mantém apenas letras

    # Criando o nome do arquivo no formato desejado
    caminho_saida = (
        f"server/excel/tag_{tag_abreviada}_fd_preenchido_{data_atual}.xlsm".lower()
    )

    # Salvar o arquivo preenchido uma única vez
    wb_template.save(caminho_saida)
    print(f"Arquivo {caminho_saida} gerado com sucesso!")
