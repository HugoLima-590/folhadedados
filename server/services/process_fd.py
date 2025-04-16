from datetime import datetime
from flask import jsonify
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
    "fv": exportar_fd_valvulas,
    "lv": exportar_fd_valvulas,
    "pv": exportar_fd_valvulas,
    "tv": exportar_fd_valvulas,
    "xv": exportar_fd_valvulas,
    "pcv": exportar_fd_valvulas,
    "xzv": exportar_fd_valvulas,
    
    "zs": exportar_fd_chave_escotilha,
    "zsc": exportar_fd_chave_escotilha,
    
    "fsl": exportar_fd_chave_baixa,
    
    "ait": exportar_fd_transmissor_temperatura,
    "tit": exportar_fd_transmissor_temperatura,
    "tt": exportar_fd_transmissor_temperatura,
    
    "ls": exportar_fd_chave_alto,
    "lsh": exportar_fd_chave_alto,
    "lzshh": exportar_fd_chave_alto,
    
    "li": exportar_fd_transmissor_nivel,
    "lt": exportar_fd_transmissor_nivel,
    "lit": exportar_fd_transmissor_nivel,
    
    "pi": exportar_fd_transmissor_pressao,
    "pt": exportar_fd_transmissor_pressao,
    "fit": exportar_fd_transmissor_pressao,
    "pit": exportar_fd_transmissor_pressao,
    "phit": exportar_fd_transmissor_pressao,
    "pzit": exportar_fd_transmissor_pressao,
    
    "psv": exportar_fd_vapv_psv,
    "vapv": exportar_fd_vapv_psv,
}


def process_fd(file_path, tag_instrumento):
    """Processa o arquivo e gera um novo FD preenchido."""
    try:
        # Processa o arquivo Excel
        processar_excel(file_path, tag_instrumento)

        # Nome do arquivo de saída
        data_atual = datetime.today().strftime("%d-%m-%Y")
        output_filename = f"tag_{tag_instrumento}_fd_preenchido_{data_atual}.xlsm"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)

        time.sleep(5)  # Simulando o processamento do arquivo

        # Remove arquivo de entrada
        if os.path.exists(file_path):
            os.remove(file_path)

        # Verifica se a tag está no mapeamento de funções
        if tag_instrumento in tag_functions:
            # Chama a função apropriada para a TAG
            tag_functions[tag_instrumento](output_path)
            return jsonify(
                {"filename": output_filename}
            ), 200  # Retorna um dicionário com o filename e o código de status
        else:
            # Caso a TAG não seja reconhecida
            return jsonify({"error": "Tag de instrumento não reconhecida"}), 400

    except Exception as e:
        # Em caso de erro, chama o handler para formatar o erro de maneira consistente
        error_message, status_code = handle_error(e)
        return {"error": error_message}, status_code
