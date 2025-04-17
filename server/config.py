import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "excel")
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'xlsm', 'csv'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ERROR_CODES = {
    "ERR001": "Extensão de arquivo inválida. Envie um arquivo .xlsm, .xlsx ou .xls.",
    "ERR002": "Tag não encontrada na planilha.",
    "ERR003": "Estrutura da planilha inválida.",
    "ERR004": "Erro na leitura do arquivo.",
    "ERR005": "Erro ao gerar documento final.",
    "ERR006": "Erro ao processar a planilha: número de colunas não corresponde ao esperado. Verifique se a estrutura da planilha segue o modelo padrão.",
    "ERR007": "Caminho do modelo ou planilha não encontrado.",
    "ERR008": "Permissão negada para acessar ou salvar arquivos.",
}

ERROR_MESSAGES = {
    # Leitura e estrutura de planilha
    "Columns must be same length as key": "ERR006",
    "No columns to parse from file": "ERR004",
    "Worksheet is empty": "ERR004",
    "unsupported file format": "ERR001",
    "Expected x columns": "ERR006",
    "Header is missing": "ERR003",
    "Tag": "ERR002",

    # Caminhos e arquivos
    "No such file or directory": "ERR007",
    "FileNotFoundError": "ERR007",
    "OSError": "ERR007",

    # Permissão
    "Permission denied": "ERR008",
    "Access is denied": "ERR008",

    # Pandas / Excel
    "pandas.errors.ParserError": "ERR004",
    "ValueError": "ERR006",
    "openpyxl": "ERR004",

    # Genérico
    "invalid file": "ERR001",
    "Erro ao gerar": "ERR005",
}

