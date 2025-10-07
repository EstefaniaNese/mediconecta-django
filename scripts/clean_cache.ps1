# Script para limpiar archivos de caché de Python
# Uso: .\scripts\clean_cache.ps1

Write-Host "🧹 Limpiando archivos de caché de Python..." -ForegroundColor Green

# Eliminar directorios __pycache__
$pycacheDirs = Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__"
if ($pycacheDirs) {
    Write-Host "📂 Eliminando directorios __pycache__:" -ForegroundColor Yellow
    foreach ($dir in $pycacheDirs) {
        Write-Host "   - $($dir.FullName)" -ForegroundColor Gray
        Remove-Item $dir.FullName -Recurse -Force
    }
} else {
    Write-Host "✅ No se encontraron directorios __pycache__" -ForegroundColor Green
}

# Eliminar archivos .pyc y .pyo
$pycFiles = Get-ChildItem -Path . -Recurse -Filter "*.pyc"
$pyoFiles = Get-ChildItem -Path . -Recurse -Filter "*.pyo"
$allFiles = $pycFiles + $pyoFiles

if ($allFiles) {
    Write-Host "📄 Eliminando archivos .pyc/.pyo:" -ForegroundColor Yellow
    foreach ($file in $allFiles) {
        Write-Host "   - $($file.FullName)" -ForegroundColor Gray
        Remove-Item $file.FullName -Force
    }
} else {
    Write-Host "✅ No se encontraron archivos .pyc/.pyo" -ForegroundColor Green
}

# Remover del índice de Git si están trackeados
Write-Host "🔄 Actualizando índice de Git..." -ForegroundColor Yellow
git rm -r --cached **/__pycache__ 2>$null
git rm --cached **/*.pyc 2>$null
git rm --cached **/*.pyo 2>$null

Write-Host "✨ ¡Limpieza completada!" -ForegroundColor Green
Write-Host "💡 Recuerda hacer commit si hay cambios en el índice de Git" -ForegroundColor Cyan
