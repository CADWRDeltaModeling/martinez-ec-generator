''' Nicky Sandhu, Yu Zhou Sept 22, 2014. Modifying script to use for PEST calibration
    PEST writes template input file with parameters
    so, sb, beta, npow1, npow2, adel
    Eli Ateljevich July 12, 2001
    Purpose: This script estimates EC for a multi-year planning run.
'''
# model Input:
#     ndo
#     astro: bandlimited estimate of astronomical stage, 15min
# model Output:
#     EC: 15min

from vdss import opendss,findpath,writedss,writeascii
from vtimeseries import timewindow,timeinterval   # for monthly add ,interpolate
from vista.time import TimeFactory
from vmath import godin
from vista.set import DataReference
import interpolate   # daily only
import os,sys,string
import ec_boundary
import conserve
from vtimeseries import interpolate
from planning_time_window import grow_window

def obtain_lock_or_keep_trying(fname):
    ''' only allow 1 slave-process visit the program at 1 time
    '''
    import os
    if not os.path.exists(fname):
        fh = open(fname,'w')
        fh.write("A file that should be locked on by slave processe to avoid zcat errors \n because simulataneous processes are cataloging a dss file at the same time.\n")
        fh.close()
    from java.io import RandomAccessFile
    import time
    file = RandomAccessFile(fname,"rw")
    fc = file.getChannel()
    while(True):
        fl = fc.tryLock()
        if fl==None:
            print "Waiting and trying again..."
            time.sleep(2)
        else:
            break
    return fl
    
def planning_ec_mtz(so,sb,beta,npow1,npow2,adel,c,outputfile,outputpath,twstr): # MTZ = RSAC054 BC for the qual
    ndofile = opendss("mtz_ec_input.dss")
    ndopath = "/DELTA/NDO/FLOW//1DAY/BDO/"                    # DICU 90-14

    astrofile=ndofile
    astropath="/DELTA/RSAC054/STAGE//15MIN/DWR-DMS-ASTRO/"          # astr plan 1967-2019
        
    g0=5000.                                          # initial value of g (antecedent outflow) for the beginning
                                                      # of the first year. This is pretty arbitrary and makes little difference
    TWIND=timewindow(twstr)                       # Actual period to be estimated
    TWINDBUF=grow_window(TWIND,"1MON","1MON")     # Conservative buffered period for retrieval
                                                  # so that after prelimiary operations (e.g. time average)
                                                  # time series will still span at least TWIND
    lock = obtain_lock_or_keep_trying(os.path.expanduser("~")+"zcat_dss_lock.txt")
    ndo=DataReference.create(findpath(ndofile,ndopath)[0],TWIND).getData()
    lock.release()
    
    # conserveSpline will attempt to preserve flow positivity, but we know that
    # in deep dark historical times NDO was negative, so we are going to add
    # an arbitrary amount, interpolate the time series, and subtract the same amount
    # back. The operation is still conservative
    ndo15=conserve.conserveSpline(ndo+14000.,"15MIN") - 14000.
    lock = obtain_lock_or_keep_trying(os.path.expanduser("~")+"zcat_dss_lock.txt")
    mtzastro=DataReference.create(findpath(astrofile,astropath)[0],TWINDBUF).getData()
    lock.release()
    
    astrorms=godin((mtzastro*mtzastro)**0.5)           # RMS energy of tide (used to predict filling and draining)
    dastrorms=(  (astrorms-(astrorms>>1))*96. ).createSlice(TWIND)    
    fifteenflo2=ndo15 - adel*(dastrorms)
    # call ec estimator
    [mtzecest, g1]=ec_boundary.ECEst(mtzastro,fifteenflo2,so,sb,beta,npow1,npow2,g0=g0,zrms=astrorms,c=c)
    writedss(outputfile,outputpath,mtzecest)
    g0=g1
    return mtzecest
    
def read_input_params(file):
    ''' Read input params from PEST file
        ignores the first two lines, reads parameters (one per line), returns the tuple
    '''
    fh = open(file)
    lines=fh.readlines()
    params=map(lambda x: float(x), tuple(lines[2:16]))
    fh.close()
    return params

if __name__ == "__main__":
    DEBUG=False
    #Read parameters from input
    so,sb,beta,npow1,adel,c0,c1,c2,c3,c4,c5,c6,c7=read_input_params("input.dat")
    c=[c0,c1,c2,c3,c4,c5,c6,c7]
    npow2=1.0     #npow2 not used
    if DEBUG: print "\nRunning model with params: ",so,sb,beta,npow1,adel, c0,c1,c2,c3,c4,c5,c6,c7
    DEFAULTS=False

    outputfile="mtz_ec_output.dss"
    outputpath="/FILL+CHAN/RSAC054/EC//15MIN/CALIB9193/"
    twstr="01JAN1991 0000 - 01OCT1993 0000"
    
    tw = timewindow(twstr)
    st = tw.getStartTime()
    stbuf = st - timeinterval("2MON")
    et = tw.getEndTime()
    TWINDBUF = TimeFactory.getInstance().createTimeWindow(stbuf,et) # 2mon + 1yr
    twbufstr = str(TWINDBUF)
    # model run
    mtzecest=planning_ec_mtz(so,sb,beta,npow1,npow2,adel,c,outputfile,outputpath,twbufstr)    
    #Write output file for PEST read
    writeascii("output.dat",mtzecest.createSlice(timewindow(twstr)))
    
    exit()
