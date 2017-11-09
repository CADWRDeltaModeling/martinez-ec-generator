''' runs model w required years
    parallel process w slaves
'''
import os,shutil,subprocess
nslaves=5 # number of slaves
p=subprocess.Popen(r'python scripts\run_mtz_ec_param.py '+str(nslaves), shell=True)
p.wait()
exit()