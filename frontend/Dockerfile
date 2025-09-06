# Etapa de construcción
FROM node:18-alpine AS builder

WORKDIR /app

# Crear usuario frontend
RUN groupadd -r frontend && useradd -r -g frontend frontend

# Copiar archivos de configuración
COPY package*.json ./
RUN npm ci

# Copiar código fuente y construir
COPY . .
RUN npm run build

# Etapa de producción
FROM nginx:alpine

# Copiar archivos construidos
COPY --from=builder /app/dist /usr/share/nginx/html

# Configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Cambiar al usuario frontend
USER frontend

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]