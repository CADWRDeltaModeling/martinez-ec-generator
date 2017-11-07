sample to use PEST
calibrate gmodel parameters from EC
******************************************
Created by Nicky Sandhu 2014/11
Modified & noted by Yu Zhou 2015/6
******************************************
requirement
******************************************
python installation
DSM2-vista is included (vscript in path)
******************************************
to run
******************************************
1. prepare pest files (skip when ready)
vscript pest_prepare.py
*modify initial/range in .par
*modify time window for calibration period

2. pest calibrate
pest pest_mtz_ec.pst
*freeze/unfreeze (local) parameters in hld

3. collect optimized parameters in pest_mtz_ec.par
*inspect .rec for detailed running process

******************************************
folder structure
******************************************
*pest program
exe (pest, tempchek, inscheck, pestchek, pestgen)

*pest files
input.par .tpl 
.hld 

*model
py (mtz_ec_model, ec_boundary, conserve, config, planning_time_window)
mtz_ec_input.dss

*scripts to auto-process
pest_prepare.py


