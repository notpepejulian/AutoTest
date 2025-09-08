# Etapa de construcción
FROM node:18-alpine AS builder

WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar todas las dependencias definidas en package.json
RUN npm install

# Copiar código fuente
COPY . .

# Construir proyecto Astro (genera /dist)
RUN npm run build

# Etapa de producción
FROM nginx:alpine

WORKDIR /usr/share/nginx/html

# Copiar el build de la etapa anterior
COPY --from=builder /app/dist ./

# Configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
