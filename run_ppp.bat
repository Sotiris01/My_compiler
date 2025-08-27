@echo off
setlocal ENABLEDELAYEDEXPANSION
REM Easy runner for P++ compiler_to_c using ANTLR4
REM Usage: run_ppp.bat [path\to\file.ppp]

set "ROOT=%~dp0"
set "PPPDIR=%ROOT%compiler_to_c"

if "%~1"=="" (
  set "INPUT=%PPPDIR%\examples\calculator.ppp"
) else (
  set "INPUT=%~f1"
)

if not exist "%INPUT%" (
  echo [run_ppp] Input file not found: "%INPUT%"
  pause
  exit /b 1
)

pushd "%PPPDIR%" >nul 2>&1
if errorlevel 1 (
  echo [run_ppp] Could not change directory to: "%PPPDIR%"
  pause
  exit /b 1
)

REM Generate ANTLR4 Python artifacts if missing
if not exist "PppLexer.py" (
  where antlr4 >nul 2>&1
  if "%ERRORLEVEL%"=="0" (
    call antlr4 -Dlanguage=Python3 -listener Ppp.g4
  ) else (
    echo [run_ppp] 'antlr4' not found on PATH. If you have the jar, set ANTLR_JAR to its full path.
    if defined ANTLR_JAR (
      call java -jar "%ANTLR_JAR%" -Dlanguage=Python3 -listener Ppp.g4
    ) else (
      echo [run_ppp] Set ANTLR_JAR environment variable to antlr-4.x-complete.jar and re-run.
      popd >nul 2>&1
  pause
      exit /b 1
    )
  )
)

python .\PppExecute.py "%INPUT%"
set "RC=%ERRORLEVEL%"

if not "%RC%"=="0" (
  echo [run_ppp] Generation failed with exit code %RC%
  popd >nul 2>&1
  pause
  exit /b %RC%
)

REM Try to build generated C (optional)
if exist "exe.c" (
  where gcc >nul 2>&1
  if "%ERRORLEVEL%"=="0" (
    gcc .\exe.c -o exe
    if "%ERRORLEVEL%"=="0" (
      echo [run_ppp] Built: exe
    ) else (
      echo [run_ppp] gcc failed to build exe.c (skipping)
    )
  ) else (
    echo [run_ppp] gcc not found; skipping build step
  )
)

popd >nul 2>&1

echo [run_ppp] Done. Outputs: tree.txt, exe.c, header.h (and optional exe)
pause
endlocal
