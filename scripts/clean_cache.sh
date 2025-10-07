#!/bin/bash
# Script para limpiar archivos de caché de Python
# Uso: ./scripts/clean_cache.sh

echo "🧹 Limpiando archivos de caché de Python..."

# Eliminar directorios __pycache__
echo "📂 Eliminando directorios __pycache__..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Eliminar archivos .pyc y .pyo
echo "📄 Eliminando archivos .pyc/.pyo..."
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true

# Remover del índice de Git si están trackeados
echo "🔄 Actualizando índice de Git..."
git rm -r --cached . --ignore-unmatch 2>/dev/null || true
git add . 2>/dev/null || true

echo "✨ ¡Limpieza completada!"
echo "💡 Recuerda hacer commit si hay cambios en el índice de Git"
