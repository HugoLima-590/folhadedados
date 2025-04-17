from flask import Blueprint, request
from server.services.file_handler import save_upload_file
from server.services.process_fd import process_fd
from server.utils.error_handler import build_error_from_code

process_blueprint = Blueprint('process', __name__)

@process_blueprint.route('/', methods=['POST'])
def processar():
    try:
        if 'file' not in request.files:
            return build_error_from_code("Nenhum arquivo enviado.", "ERR_NO_FILE", 400)

        file = request.files['file']
        tag_instrumento = request.form.get("tag_instrumento", "").strip()

        if not tag_instrumento:
            return build_error_from_code("Tag de instrumento não especificada.", "ERR_NO_TAG", 400)

        file_path = save_upload_file(file)
        if not file_path:
            return build_error_from_code("Formato de arquivo inválido.", "ERR_INVALID_FILE", 400)

        return process_fd(file_path, tag_instrumento)

    except Exception as e:
        # Usa o handler que você já criou com traceback
        from server.utils.error_handler import handle_error
        return handle_error(e)
