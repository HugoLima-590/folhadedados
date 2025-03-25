# Usa uma imagem leve do Python
FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia apenas o arquivo de dependências primeiro (boa prática para cache)
COPY ../requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Agora copia o restante dos arquivos do backend
COPY . .

# Expõe a porta onde a API será executada
EXPOSE 5000

# Comando para rodar a API
CMD ["python", "main.py"]
