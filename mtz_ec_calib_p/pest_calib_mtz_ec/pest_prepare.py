''' PEST preparation scripts
    out: hist EC
    in:  parameter
'''
import os
from vista.set import DataReference
from vtimeseries import *
from vdss import opendss,findpath,writeascii
    
def escape_regex(path):
    return path.replace("+","\+")
def write_output(file,model_output_file,model_output_path,twstr):
    print "Write measuremnt file for %s"%twstr
    output_data=DataReference.create(findpath(opendss(model_output_file),escape_regex(model_output_path))[0],timewindow(twstr)).getData()   
    writeascii(file,output_data)
    
def create_instruction_file(file,nlines):
    print "Write instruction file from measuremnt.dat"
    wr=open(file,"w")
    wr.write("pif @\n")
    wr.write("l12\n")
    for i in range(1,nlines-12):
        wr.write("l1 [m%d]17:25\n"%i)
    wr.close()

def write_pst(pst_f):
    ''' write model section to pst
    '''
    print "Add model in contrl pst"
    tmplt = 'pst_template'
    if os.path.exists(tmplt):os.remove(tmplt)
    os.rename(pst_f,tmplt)
    fr=open(tmplt,"r")
    fw=open('pest_mtz_ec.pst',"w")
    for line in fr:
      if line=='* model command line\n':
        fw.write(line)
        fr.readline()
        scriptpath = (os.getcwd()+r'\..\model\vista\bin\vscript')
        fw.write(scriptpath + ' mtz_ec_model.py\n')
      elif line=='model.tpl  model.inp\n':
        fw.write('pest_input.tpl  input.dat\n')
      elif line=='model.ins  model.out\n':
        fw.write('pest_output.ins  output.dat\n')
      else:
        fw.write(line)

    fr.close()
    fw.close()
    os.remove(tmplt)
    
if __name__=='__main__':
    file="mtz_ec_input.dss"
    path="/FILL+CHAN/RSAC054/EC//15MIN/HIST8914OM/"                         # 1990-2014
    #******** MAKE SURE THAT twstr matches mtz_ec.py <2yr10mon ***********
    twstr="01JAN1991 0000 - 01OCT1993 0000"
    # twstr="01APR2012 0000 - 01JAN2015 0000"
    os.system("tempchek pest_input.tpl pest_input.par")
    
    write_output("measurement.dat",file,path,twstr)
    fh=open("measurement.dat")
    nlines=len(fh.readlines())
    fh.close()
    create_instruction_file("pest_output.ins",nlines)    
    os.system("inschek pest_output.ins measurement.dat")
    os.system("copy pest_output.obf pest_measurement.obf")
    
    os.system("pestchek pest_mtz_ec")
    os.system("pestgen pest_mtz_ec pest_input.par pest_measurement.obf")
    write_pst("pest_mtz_ec.pst")
    
    exit()