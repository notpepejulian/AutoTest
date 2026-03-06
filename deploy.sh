#!/bin/bash

# Creado por: Nacho Sanchez 
# @Github Repo: AutoTest
# Script para reconstruir el frontend 
# Descripción: Detiene los contenedores, reconstruye el frontend sin cache y levanta los servicios en segundo plano (util en staging y dev) ---- Mergear a PRO solo con cambios aplicativos

set -e  # Detener el script si ocurre algún error (usar -euo para depurar variables vacias)

# COlor morado
PURPLE='\033[0;35m'
SC='\033[0m' # sin color

echo -e "${PURPLE} Deteniendo contenedores...${SC}"
docker compose down

echo -e "${PURPLE} Reconstruyendo backend y frontend (sin cache)...${SC}"
docker compose build backend frontend --no-cache

echo -e "${PURPLE} Iniciando servicios en segundo plano...${SC}"
docker compose up -d

echo -e "${PURPLE} Proceso completado!${SC}"
echo -e "${PURPLE} Verificando estado de los contenedores...${SC}"
docker compose ps

echo -e "${PURPLE} Para ver los logs en tiempo real:${SC}"
echo -e "${PURPLE}   docker compose logs -f frontend${SC}"
echo -e "${PURPLE}   docker compose logs -f backend${SC}"
