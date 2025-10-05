#!/bin/bash

echo "🚀 Desplegando Proyecto de Estadística..."
echo "⏳ Construyendo contenedores..."

docker-compose down
docker-compose up --build -d

echo "✅ Proyecto desplegado!"
echo "🌐 Abre: http://localhost"
echo "📊 La aplicación está corriendo..."
echo ""
echo "🛑 Para detener: docker-compose down"