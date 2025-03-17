from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import time
import threading
from datetime import datetime
from server.scripts.gerar_listas_de_tag_otimizada import processar_excel
from server.scripts.alimentar_fd_valvulas_on_off import exportar_fd

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "server", "excel")
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'xlsm', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['POST'])
def processar():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado."}), 400

    file = request.files['file']
    tag_instrumento = request.form.get("tag_instrumento", "").strip()

    if not tag_instrumento:
        return jsonify({"error": "Tag de instrumento não especificada."}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        print(f"✅ Arquivo salvo no servidor: {file_path}")  # Debug

        try:
            # Processa o Excel e gera o FD preenchido
            processar_excel(file_path, tag_instrumento)
            
            # Gera o nome do arquivo de saída dinâmico
            data_atual = datetime.today().strftime("%d-%m-%Y")
            output_filename = f"tag_{tag_instrumento}_fd_preenchido_{data_atual}.xlsm"
            output_path = os.path.join(UPLOAD_FOLDER, output_filename)

            time.sleep(5)

            # Deletar arquivo de entrada depois de processar
            if os.path.exists(file_path):
                os.remove(file_path)

            output_path = os.path.join(BASE_DIR, "server", "excel")  
            exportar_fd(output_path)

            return jsonify({"filename": output_filename}), 200  # Retorna o nome do arquivo gerado
        except Exception as e:
            print(f"❌ Erro ao processar o arquivo: {e}")  # Debug para erros
            return jsonify({"error": str(e)}), 500  # Retorna HTTP 500 se falhar
    else:
        return jsonify({"error": "Arquivo inválido. Apenas xlsm, xlsx, xls ou csv são permitidos."}), 400

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    caminho_saida = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(caminho_saida):
        
        # Função para deletar o arquivo em um thread separado
        def delete_file_later():
            time.sleep(3)
            try:
                os.remove(caminho_saida)  # Exclui o arquivo depois que ele for enviado
                print(f"Arquivo {filename} deletado com sucesso.")
            except Exception as e:
                print(f"❌ Erro ao excluir o arquivo: {e}")

        # Cria uma thread para excluir o arquivo após o envio
        threading.Thread(target=delete_file_later).start()

        return send_file(caminho_saida, as_attachment=True)
    else:
        return jsonify({"error": "Arquivo não encontrado."}), 404

if __name__ == '__main__':
    app.run(debug=True)
