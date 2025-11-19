@echo off
REM === Backup automático MySQL ===

REM Obtener fecha REAL sin errores (YYYY-MM-DD)
for /f %%i in ('powershell -NoLogo -Command "(Get-Date).ToString(\"yyyy-MM-dd\")"') do set FECHA=%%i

REM Carpeta donde se guardarán los respaldos
set BACKUP_DIR="C:\Users\esmer\OneDrive\Documentos\BUAP\7mo Semestre\Mantenimiento de equipos y redes de computadoras\SGMCL\respaldosBD"

REM Generar archivo con nombre automático
set DESTINO=%BACKUP_DIR%\backup_sgmcl_%FECHA%.sql

REM Ejecutar respaldo
"C:\Program Files\MySQL\MySQL Workbench 8.0\mysqldump.exe" -u root -pchangocome sgmcl > %DESTINO%

echo.
echo =====================================================
echo   Respaldo generado correctamente en:
echo   %DESTINO%
echo =====================================================
echo.

pause
