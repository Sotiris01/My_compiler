@echo off
setlocal ENABLEDELAYEDEXPANSION
REM Easy runner for Starlet compiler (compiler_to_asemply)
REM Usage: run_starlet.bat [path\to\file.stl]

set "ROOT=%~dp0"
set "COMPILER_DIR=%ROOT%compiler_to_asemply\compiler"

if "%~1"=="" (
  set "INPUT=%ROOT%compiler_to_asemply\examples\test4.stl"
) else (
  set "INPUT=%~f1"
)

if not exist "%INPUT%" (
  echo [run_starlet] Input file not found: "%INPUT%"
  exit /b 1
)

pushd "%COMPILER_DIR%" >nul 2>&1
if errorlevel 1 (
  echo [run_starlet] Could not change directory to: "%COMPILER_DIR%"
  exit /b 1
)

python ".\starletc.py" -i "%INPUT%"
set "RC=%ERRORLEVEL%"

popd >nul 2>&1

if not "%RC%"=="0" (
  echo [run_starlet] Compilation failed with exit code %RC%
  exit /b %RC%
)

echo [run_starlet] Done. Generated .asm/.c/.int next to: "%INPUT%"
pause
endlocal
