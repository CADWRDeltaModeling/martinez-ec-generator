''' set up slave templates
'''
import shutil


#-- MAIN for single run--#
if __name__=='__main__':
  #set up master from template and start up.
  master_dir = 'pest_calib_mtz_ec'
  TEMPLATE_DIR="pest_slave_template"
  print 'Copy pst, tpl, ins to template dir: %s'%TEMPLATE_DIR
  shutil.copy(master_dir+"/pest_mtz_ec.pst", TEMPLATE_DIR)
  shutil.copy(master_dir+"/pest_input.tpl",TEMPLATE_DIR)
  shutil.copy(master_dir+"/pest_output.ins",TEMPLATE_DIR)
  
  print 'Copy model to template dir'
  shutil.copy(master_dir+'/mtz_ec_model.py',TEMPLATE_DIR)
  shutil.copy(master_dir+'/mtz_ec_input.dss',TEMPLATE_DIR)

  exit()
