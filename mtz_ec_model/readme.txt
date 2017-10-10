Martinez EC generator
*********************************************
by Yu Zhou 2017/8
generate EC at Martinez, modified from G-model (Denton)
originally part of DSM2 preprocess script from CALSIM at ${DSM2}\scripts\planning_ec_mtz.py, etc
*********************************************
path+files
mtz_ec_model.bat to run the python script
dsm2-vista is required; its bin (vscript) set up in environment variables
Python scripts mtz_ec_model.py, ec_boundary.py, conserve.py
parameters: param_so37196.dat
*********************************************
input: (could be modified in mtz_ec_model.py)
*NDO (Net Delta Outflow)
*stage (astro-planning at Martinez, NGVD)
The above 2 are stored in mtz_ec_input.dss
*time: twstr

output
mtz_ec_output.dss