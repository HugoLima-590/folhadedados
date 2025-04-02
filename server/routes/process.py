from flask import Blueprint, request, jsonify
from server.services.file_handler import save_upload_file
from server.services.process_fd import process_fd

process_blueprint = Blueprint('process', __name__)

@process_blueprint.route('/', methods=['POST'])
def processar():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado."}), 400

    file = request.files['file']
    tag_instrumento = request.form.get("tag_instrumento", "").strip()

    if not tag_instrumento:
        return jsonify({"error": "Tag de instrumento não especificada."}), 400

    file_path = save_upload_file(file)
    if not file_path:
        return jsonify({"error": "Formato de arquivo inválido."}), 400

    output_filename, status_code = process_fd(file_path, tag_instrumento)
    return jsonify({"filename": output_filename}), status_code
