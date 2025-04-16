import pandas as pd
from openpyxl import load_workbook
from datetime import datetime

def exportar_fd_chave_alto(caminho_saida):
    # Caminho para o template e as tags filtradas
    caminho_template = r"server/excel/templates/Chave de Nível Alto.xlsx"
    caminho_tags = r"server/excel/tags_filtradas.xlsx"

    # Carregar o template do Excel com VBA
    wb_template = load_workbook(caminho_template, keep_vba=True)
    sheet_folhas = wb_template["Folhas"]
    df_tags = pd.read_excel(caminho_tags)

    # Mapeamento de células para as colunas de dados
    mapeamento = {
        "D6": "Tag do Instrumento",
        "D32": "Diâmetro",
        "D33": "Temperatura oper. max",
        "D35": "Viscosidade",
        "D34": "Densidade",
        "A37": "Nota",
    }

    # Valores padrão a serem usados quando algum campo estiver vazio
    valores_padrao = {
        "Vazão max": "Vazão",
        "Vazão min": "Vazão",
        "Temperatura oper. max": "Temperatura Oper.",
    }

    # Data atual para inclusão no nome do arquivo
    data_atual = datetime.today().strftime("%d-%m-%Y")

    # Preencher o template com os dados das tags
    for _, row in df_tags.iterrows():
        new_sheet = wb_template.copy_worksheet(sheet_folhas)
        nome_aba = str(row["Tag do Instrumento"])
        new_sheet.title = nome_aba

        # Preencher células de acordo com o mapeamento
        for cell, coluna in mapeamento.items():
            valor = row.get(coluna)

            # Se o valor estiver vazio e houver um valor padrão, usar o valor padrão
            if pd.isna(valor) and coluna in valores_padrao:
                valor = row.get(valores_padrao[coluna])

            # Atribuir o valor à célula se for válido
            if pd.notna(valor):
                new_sheet[cell] = str(valor)

        # Preencher a "Nota" caso haja múltiplos valores
        notas = str(row.get("Nota", "")).split("Nota")
        for i, nota in enumerate(notas):
            new_sheet[f"A{37 + i}"] = nota.strip()

    # Processa a Tag do Instrumento para gerar um nome de arquivo
    tag = str(row["Tag do Instrumento"])
    tag_abreviada = "".join([char for char in tag if char.isalpha()])  # Mantém apenas as letras

    # Criar o caminho do arquivo de saída com a data
    caminho_saida = f"server/excel/tag_{tag_abreviada}_fd_preenchido_{data_atual}.xlsm".lower()

    # Salva o arquivo preenchido
    wb_template.save(caminho_saida)
    print(f"Arquivo {caminho_saida} gerado com sucesso!")
