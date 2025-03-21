from flask import jsonify

def handle_error(error):
    error_message = str(error)
    
    if "Columns must be same length as key" in error_message:
        return jsonify({"error": "Tag não encontrada na Planilha"}), 400
    elif "No such file or directory" in error_message:
        return jsonify({"error": "Arquivo não encontrado."}), 404
    elif "Invalid file type" in error_message:
        return jsonify({"error": " Arquivo inválido. Apenas xlsm, xlsx, xls ou csv são permitidos."}), 400
    elif "Network Error" in error_message:
        return jsonify({"error": "Servidor não disponível, contate a equipe de TI"}), 500
    else:
        return jsonify({"error": " Erro desconhecido"}), 500
