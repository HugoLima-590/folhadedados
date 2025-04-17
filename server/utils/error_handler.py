from flask import jsonify
from server.config import ERROR_CODES, ERROR_MESSAGES
import traceback 

def build_error_from_code(code, status=400):
    """Retorna um JSON padronizado com código e mensagem, baseado no dicionário de erros."""
    message = ERROR_CODES.get(code, "Erro desconhecido.")
    return jsonify({"error": message, "code": code}), status

def handle_error(error, code="ERR500"):
    error_message = str(error)
    error_traceback = traceback.format_exc()

    print("🔍 Erro bruto:", repr(error_message))  # Adicione essa linha para ver exatamente o que está vindo

    # Mapeia dinamicamente com base no conteúdo da mensagem
    for msg, cod in ERROR_MESSAGES.items():
        if msg.lower() in error_message.lower():
            code = cod
            break

    translated_msg = ERROR_CODES.get(code, "Erro desconhecido.")

    print(f"❌ Erro tratado: {translated_msg}\n{error_traceback}")

    return jsonify({
        "error": translated_msg,
        "code": code
    }), 500
    


