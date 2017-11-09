sample to use PEST calibration (parallel version)
reverse-gmodel to calibrate parameters
auto prepare, model run
******************************************
by Nicky Sandhu, Yu Zhou 2015/6
******************************************
to use
******************************************
python installation
parallel run (master/slave.bat with PC name/port consistent)
DSM2-vista is included (*confirm vscript path in pst)
lock is needed for dss read parallel run (in scripts)
******************************************
steps
******************************************
1. cleanup & prepare (optional)
del all z:\temp\pest_slaves\
switch to pest_calib_mtz_ec\
vscript pest_prepare.py

2-1. multiple_slaves.bat (slaves on the same PC)
generate slave template and spawn slaves
run calib w slaves
slave amount and their running drives could be specified (z/c/d)

2-2. HTcondor (submit slaves on other PC)
place HTcondor files in the parent folder of PEST slave template + model
update pest.slave with what are updated in slave_template after pest_prepare; confirm DSM2-vista (in .pst) point to its relative path
start master first on submitter's machine, then use HTcondor to run slaves on execute machines

*******************************
to run manually (debug)
*******************************
do generate + pst_run_svd once, as steps
start 1 master
start 1 slave
(copy master folder to create slaves except master/slave.bat)

******************************************
folder structure
******************************************
\pest_calib_mtz_ec\
model and PEST files
*prepare
exe (inschek pestgen tempchek)
pest_prepare.py
pest_input.tpl, par

*model run
input.dat, hld
pst (generated from prepare)

beopest32.exe start_pest_master.bat

\pest_slave_template\
template for slaves
beopest.exe *slave.bat output.dat (empty)

\model\
model support scripts for calib (.py)
vista (supporting py module)

\scripts_samePC\
auto-process control PEST run
pst_run_p -> run_mtz_ec_param

