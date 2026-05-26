:: Run all unit tests for the AgenticNewsLetter project.
:: Discovers tests under newsletter\nodes\unittests and newsletter\utils\unittests
:: using the standard `unittest` library. Run this from the AgenticNewsLetter root.
@echo off
setlocal

set EXITCODE=0

echo ============================================================
echo Running newsletter/nodes unit tests ...
echo ============================================================
call uv run python -m unittest discover -s newsletter\nodes\unittests -t newsletter -p "test_*.py" -v
if errorlevel 1 set EXITCODE=1

echo.
echo ============================================================
echo Running newsletter/utils unit tests ...
echo ============================================================
call uv run python -m unittest discover -s newsletter\utils\unittests -t newsletter -p "test_*.py" -v
if errorlevel 1 set EXITCODE=1

echo.
if "%EXITCODE%"=="0" (
    echo All unit tests passed.
) else (
    echo One or more unit test suites failed.
)

endlocal & exit /b %EXITCODE%
