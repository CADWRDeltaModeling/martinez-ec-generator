''' run model for specified year
    with slaves on Z drive
'''
import sys, os, shutil
import subprocess, time
import signal

# temporary dir where template will be copied and beopest run
master_dir = 'pest_calib_mtz_ec'
SLAVES_DIR="C:/temp/pest_slaves"
TEMPLATE_DIR="pest_slave_template"
slave_process=[]
master_process=None

def cleanup():
  for p in slave_process:
    p.terminate()
  if master_process:
    master_process.terminate()
    shutil.rmtree(SLAVES_DIR,ignore_errors=True)
def ctrl_break_signal_handler(signal, frame):
  print 'User pressed Ctrl-Break'
  cleanup()
def start_slaves(start_id, nslaves):
  print 'Starting %d slaves in %s'%(nslaves,SLAVES_DIR)
  slave_process=[]
  # shutil.copytree('model',SLAVES_DIR+"/model")
  for id in range(start_id,start_id+nslaves):
    slave_dir=SLAVES_DIR+"/"+"pest.slave.%d"%id
    shutil.copytree(TEMPLATE_DIR, slave_dir)
    print 'Starting slave %d'%id
    slave_process.append(subprocess.Popen('start_pest_slave.bat < Nul',cwd=slave_dir,shell=True, stdout=open(os.devnull, 'wb')))
  print 'Spawned %d slaves'%len(slave_process)
def check_on_slaves(slave_process):
  while True:
    try:
      all_terminated=True
      for p in slave_process:
        if p.poll() == None:
          all_terminated = False
          break
      if all_terminated:
        print 'All processes are terminated!'
        break
        time.sleep(10)
    except KeyboardInterrupt:
      print "Key board interrupt"
      cleanup()


def run_mtz_ec_param(nslaves):
  print 'Start master'
  master_process = subprocess.Popen('start_pest_master.bat < Nul',cwd=master_dir,shell=True)
  signal.signal(signal.SIGINT, ctrl_break_signal_handler)
  # clean up temp dir and start slaves
  shutil.rmtree(SLAVES_DIR,ignore_errors=True)
  
  start_slaves(1, nslaves)
  #check_on_slaves(slave_process)
  master_process.wait()
  print 'End'


#-- MAIN for single run--#
if __name__=='__main__':
  if len(sys.argv) < 2 :
    print 'Enter slave amount to run'
    exit(1)
  try:
    nslaves = int(sys.argv[1])
  except Exception:
    print 'slave amount not input'
    exit(1)

  run_mtz_ec_param(nslaves)
  exit(0)
