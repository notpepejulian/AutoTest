# Usar Node.js para SSR en runtime
FROM node:18-alpine

WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias de producción
RUN npm install --omit=dev

# Copiar código fuente
COPY . .

# Construir proyecto Astro (genera /dist con servidor SSR)
RUN npm run build

# Exponer puerto 80 para AWS Target Group
EXPOSE 80

# Variables de entorno
ENV HOST=0.0.0.0
ENV PORT=80

# Ejecutar el servidor Astro standalone
CMD ["node", "./dist/server/entry.mjs"]
