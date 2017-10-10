@echo off
echo ------------------------------
echo --mtz ec from mtz stage, ndo--
echo ------------------------------

REM set SCRIPT_HOME=%DSM2_HOME%/scripts
call vscript mtz_ec_model.py
goto fin

:fin