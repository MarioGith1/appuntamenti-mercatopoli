@echo off
title 🚀 AVVIO APPUNTAMENTI MERCATOPOLI
color 0E

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                   🚀 APPUNTAMENTI MERCATOPOLI                ║
echo ║                Sistema Completo di Prenotazioni               ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔄 Avvio dell'applicazione...
echo.

REM Controlla se Python è installato
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Errore: Python non è installato!
    echo 💡 Installa Python da https://python.org
    echo.
    pause
    exit /b 1
)

echo ✅ Python trovato
echo.

REM Controlla se esistono i file necessari
if not exist "app.py" (
    echo ❌ Errore: File app.py non trovato!
    pause
    exit /b 1
)

if not exist "credentials.json" (
    echo ❌ Errore: File credentials.json non trovato!
    echo 💡 Scarica il file dalle Google Cloud Console
    pause
    exit /b 1
)

echo ✅ File del progetto trovati
echo.

REM Installa dipendenze
echo 📦 Installazione dipendenze...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Alcune dipendenze potrebbero non essere state installate correttamente
) else (
    echo ✅ Dipendenze installate correttamente
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                     📱 AVVIO APPLICAZIONE                      ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 Avvio dell'applicazione...
echo.

REM Avvia l'applicazione
streamlit run app.py --server.port 8501 --server.address 127.0.0.1

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  App: http://localhost:8501                                   ║
echo ║                                                              ║
echo ║  Per fermare: premi CTRL+C                                   ║
echo ╚══════════════════════════════════════════════════════════════╝

pause
