from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import time
from server.scripts.gerar_listas_de_tag_otimizada import processar_excel
from server.scripts.alimentar_fd import exportar_fd

app = Flask(__name__)
CORS(app)  

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "server/excel")
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'xlsm', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print(f"Pasta de upload criada: {UPLOAD_FOLDER}")

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
            dados_processados = processar_excel(file_path, tag_instrumento)

            time.sleep(5)
            
            if os.path.exists(file_path):
                os.remove(file_path)
            
            exportar_fd()

            return jsonify(dados_processados), 200  # Retorna HTTP 200 se der certo
        except Exception as e:
            print(f"❌ Erro ao processar o arquivo: {e}")  # Debug para erros
            return jsonify({"error": str(e)}), 500  # Retorna HTTP 500 se falhar
    else:
        return jsonify({"error": "Arquivo inválido. Apenas xlsm, xlsx, xls ou csv são permitidos."}), 400
    
@app.route('/download', methods=['GET'])
def download_file():
    caminho_saida = os.path.join(BASE_DIR, "server/excel/FD_Preenchido.xlsm")

    if os.path.exists(caminho_saida):
        return send_file(caminho_saida, as_attachment=True)
    else:
        return jsonify({"error": "Arquivo não encontrado."}), 404

if __name__ == '__main__':
    app.run(debug=True)
