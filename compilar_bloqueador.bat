@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel%==0 (
    py -m pip install --upgrade pyinstaller
    py -m PyInstaller --onefile --name BloqueadorEscolar bloqueador_escola.py
) else (
    python -m pip install --upgrade pyinstaller
    python -m PyInstaller --onefile --name BloqueadorEscolar bloqueador_escola.py
)
echo.
echo ==========================================
echo EXE criado em: dist\BloqueadorEscolar.exe
echo ==========================================
pause
