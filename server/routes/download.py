from flask import Blueprint, send_file, jsonify
import os
import time
import threading
from server.config import UPLOAD_FOLDER
from server.utils.error_handler import handle_error

download_blueprint = Blueprint('download', __name__)

@download_blueprint.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        caminho_saida = os.path.join(UPLOAD_FOLDER, filename)

        if os.path.exists(caminho_saida):
            def delete_file_later():
                time.sleep(10)
                try:
                    os.remove(caminho_saida)
                    print(f"Arquivo {filename} deletado.")
                except Exception as e:
                    print(f"Erro ao deletar o arquivo: {str(e)}")

            threading.Thread(target=delete_file_later).start()
            return send_file(caminho_saida, as_attachment=True)

        # Arquivo não encontrado → erro tratado
        return jsonify({
            "error": "Arquivo não encontrado. Verifique se ele foi gerado corretamente.",
            "code": "ERR404"
        }), 404

    except Exception as e:
        return handle_error(e, code="ERR500")
