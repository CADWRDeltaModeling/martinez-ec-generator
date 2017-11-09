REM set PATH=%PATH%;C:\condor\samples\mtz_ec_model\vista\bin
@echo off

set nslaves=5

for /l %%x in (1, 1, %nslaves%) do (
echo "copy %%x"
if not exist %%x (
mkdir %%x
)
xcopy /y pest.slave  %%x
)

for /l %%x in (1, 1, %nslaves%) do (
echo run slave %%x
cd %%x

if %%x==%nslaves% (start /wait start_pest_slave.bat
) else (start start_pest_slave.bat)
cd..
)


exit
