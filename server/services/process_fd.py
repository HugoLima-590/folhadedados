from datetime import datetime
import os
import time
from server.config import UPLOAD_FOLDER
from server.scripts.gerar_listas_de_tag import processar_excel
from server.scripts.error_handler import handle_error

# Importando todas as funções de processamento
from server.scripts.process_chave_de_nivel_alto import exportar_fd_chave_alto
from server.scripts.process_chave_de_vazao_baixa import exportar_fd_chave_baixa
from server.scripts.process_chave_posicao_escotilha import exportar_fd_chave_escotilha
from server.scripts.process_transmissor_de_nivel import exportar_fd_transmissor_nivel
from server.scripts.process_transmissor_de_pressao import exportar_fd_transmissor_pressao
from server.scripts.process_transmissor_de_temperatura import exportar_fd_transmissor_temperatura
from server.scripts.process_valvulas_on_off import exportar_fd_valvulas
from server.scripts.process_vapv_psv import exportar_fd_vapv_psv

# Mapeando funções pelo prefixo da TAG
tag_functions = {
    "xv": exportar_fd_valvulas, "xzv": exportar_fd_valvulas,
    "zs": exportar_fd_chave_escotilha, "zsc": exportar_fd_chave_escotilha,
    "fsl": exportar_fd_chave_baixa, "tit": exportar_fd_transmissor_temperatura,
    "tt": exportar_fd_transmissor_temperatura, "lsh": exportar_fd_chave_alto,
    "ls": exportar_fd_chave_alto, "lzshh": exportar_fd_chave_alto,
    "lit": exportar_fd_transmissor_nivel, "lt": exportar_fd_transmissor_nivel,
    "pzit": exportar_fd_transmissor_pressao, "pit": exportar_fd_transmissor_pressao,
    "pt": exportar_fd_transmissor_pressao, "vapv": exportar_fd_vapv_psv,
    "psv": exportar_fd_vapv_psv
}

def process_fd(file_path, tag_instrumento):
    """Processa o arquivo e gera um novo FD preenchido."""
    try:
        processar_excel(file_path, tag_instrumento)
        
        # Nome do arquivo de saída
        data_atual = datetime.today().strftime("%d-%m-%Y")
        output_filename = f"tag_{tag_instrumento}_fd_preenchido_{data_atual}.xlsm"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)

        time.sleep(5)  # Simulando processamento

        # Remove arquivo de entrada
        if os.path.exists(file_path):
            os.remove(file_path)

        # Verifica se há uma função para essa TAG
        if tag_instrumento in tag_functions:
            tag_functions[tag_instrumento](output_path)
            return output_filename, 200
        else:
            return {"error": "Tag de instrumento não reconhecida"}, 400

    except Exception as e:
        return handle_error(e)
