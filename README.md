# Lista de Itens para Folha de dados

### Projeto fullstack com **Backend em Python (Flask)** e **Frontend em React (Vite)**, preparado para execução local ou via **Docker**.
### Um case técnico para resolver automações de preenchimento de documentos de engenharia, onde as listas de itens precisavam passar para uma folha de dados convertendo e filtrando para cada tipo de item.

## 📃 Documentação
<a href="https://doc.clickup.com/9011561075/d/h/8cj30kk-1211/66973d8914121a3" target="_blank" rel="noopener noreferrer">
📄 Gerador de Folha de Dados
</a>



## 📋 Pré-requisitos

### Para rodar com Docker (recomendado)
- **Docker Desktop** instalado e em execução

### Para rodar sem Docker
- **Python 3.9+**
- **pip**
- **Node.js LTS** (inclui `node` e `npm`)
- **Git** (opcional)

Verifique no terminal:
```bash
python --version
pip --version
node -v
npm -v
```

🐳 Rodando com Docker (recomendado)

Na raiz do projeto (onde está o docker-compose.yml):

▶️ Subir os containers
```bash
docker-compose up --build
```

2️⃣ Frontend (React + Vite)

Entre na pasta do frontend:
```bash
cd automacao_fd_ld
npm install
npm run dev
```

Frontend disponível em:
👉 http://localhost:5173


📁 Estrutura do projeto
```
folhadedados/
│
├── main.py                  # Backend Flask
├── requirements.txt         # Dependências Python
├── Dockerfile               # Imagem do backend
├── docker-compose.yml       # Orquestra frontend + backend
│
├── automacao_fd_ld/         # Frontend React (Vite)
│   ├── package.json
│   ├── vite.config.js
│   └── src/

```

👤 Autor

Projeto mantido por HugoLima-590

