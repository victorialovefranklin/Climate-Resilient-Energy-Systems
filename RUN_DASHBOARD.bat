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
