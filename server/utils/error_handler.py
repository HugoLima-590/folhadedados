import traceback

def handle_error(error):
    """Captura erros, registra no log e retorna uma resposta JSON."""
    error_message = str(error)
    error_traceback = traceback.format_exc()

    print(f"❌ Erro ocorrido: {error_message}\n{error_traceback}")  # Log no console

    # Retorna apenas a mensagem de erro, sem incluir o traceback na resposta
    return {"error": error_message}, 500
