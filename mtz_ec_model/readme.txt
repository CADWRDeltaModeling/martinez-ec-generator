Martinez EC generator
*********************************************
by Yu Zhou 2017/8
generate EC at Martinez, modified from G-model (Denton)
originally part of CALSIM-DSM2 preprocess script at ${DSM2}\scripts\planning_ec_mtz.py, etc
*********************************************
path and files
dsm2-vista is required; version along with DSM2 v812, git commit 996783b2275e5281683de3027ed2789d60fd4a81; its bin (vscript) set up in environment variables
mtz_ec_model.bat to run the python script
Python scripts mtz_ec_model.py, ec_boundary.py, conserve.py, config.py, planning_time_window.py
parameters: param_so37196.dat
*********************************************
input: (could be modified in mtz_ec_model.py)
*NDO (Net Delta Outflow)
*stage (astro-planning at Martinez, NGVD)
The above 2 are stored in mtz_ec_input.dss
*time: twstr

output
mtz_ec_output.dss