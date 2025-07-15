#!/bin/bash

# Variables
BACKEND_URL="https://backend-4vzk.onrender.com"
SECRET="mi_clave_secreta_segura"  # reemplazá por tu INIT_SECRET real

echo "Creando tablas..."
curl -X POST "$BACKEND_URL/admin/init-db" -H "x-init-secret: $SECRET"
echo -e "\n"

echo "Importando datos desde Google Sheets..."
curl -X POST "$BACKEND_URL/admin/importar-recetas" -H "x-init-secret: $SECRET"
echo -e "\n"

echo "Realizando backup..."
curl -X POST "$BACKEND_URL/admin/backup-recetas" -H "x-init-secret: $SECRET"
curl -X POST "$BACKEND_URL/admin/backup-mensajes" -H "x-init-secret: $SECRET"
curl -X POST "$BACKEND_URL/admin/backup-planes" -H "x-init-secret: $SECRET"
echo -e "\n"

echo "✅ Reseteo completo"
