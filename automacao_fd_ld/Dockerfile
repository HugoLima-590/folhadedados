# Usa uma imagem do Node.js para construir o frontend
FROM node:18-alpine AS build

WORKDIR /app

# Copia os arquivos do React
COPY . .

# Instala as dependências e constrói o React
RUN npm install && npm run build

# Usa um servidor Nginx para servir os arquivos do React
FROM nginx:stable-alpine

# Copia os arquivos buildados do React para o Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Expõe a porta 80 para servir o frontend
EXPOSE 80

# Inicia o Nginx
CMD ["nginx", "-g", "daemon off;"]
