#!/bin/bash

# Script para reconstruir el frontend con mensajes en morado
# Descripción: Detiene los contenedores, reconstruye el frontend sin cache y levanta los servicios en segundo plano

set -e  # Detener el script si ocurre algún error

# Definir color morado (púrpura)
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${PURPLE}🔻 Deteniendo contenedores...${NC}"
docker compose down

echo -e "${PURPLE}🔨 Reconstruyendo backend y frontend (sin cache)...${NC}"
docker compose build backend frontend --no-cache

echo -e "${PURPLE}🚀 Iniciando servicios en segundo plano...${NC}"
docker compose up -d

echo -e "${PURPLE}✅ Proceso completado!${NC}"
echo -e "${PURPLE}📊 Verificando estado de los contenedores...${NC}"
docker compose ps

echo -e "${PURPLE}📝 Para ver los logs en tiempo real:${NC}"
echo -e "${PURPLE}   docker compose logs -f frontend${NC}"
echo -e "${PURPLE}   docker compose logs -f backend${NC}"
