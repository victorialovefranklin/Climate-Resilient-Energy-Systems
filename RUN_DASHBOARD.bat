@echo off
REM ============================================================================
REM RUN DASHBOARD - Climate-Resilient Energy Systems
REM Victoria Love Franklin - Meharry Medical College
REM ============================================================================

echo.
echo ============================================================================
echo    CLIMATE-RESILIENT ENERGY DASHBOARD
echo    Victoria Love Franklin - Meharry Medical College
echo ============================================================================
echo.

REM Set the Anthropic API Key
set ANTHROPIC_API_KEY=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

echo [OK] API Key configured
echo [OK] Starting dashboard...
echo.
echo Dashboard will open at: http://localhost:8501
echo.
echo To stop: Press Ctrl+C
echo ============================================================================
echo.

REM Run the dashboard
streamlit run dashboard_comprehensive.py

pause
