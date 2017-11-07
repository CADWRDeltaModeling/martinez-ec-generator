''' Martinez EC Estimate Model
    so, sb, beta, npow1, adel, c
    modified from CALSIM-DSM2 preprocess scripts 2001
    by Nicky Sandhu, Yu Zhou 2014/11
'''
# model requirement: dsm2-vista
# model Input:
#     ndo: Net Delta Outflow, daily
#     astro: bandlimited estimate of astronomical stage (NGVD), 15min
#     params: coeff input
# model Output:
#     EC: 15min

import os,sys,string
import ec_boundary, conserve
from vmath import godin
from vista.set import DataReference
# import interpolate   # daily only
from vtimeseries import timewindow,timeinterval#,interpolate  # for monthly add
from planning_time_window import grow_window
from vdss import opendss,findpath,writedss,writeascii
from vista.time import TimeFactory

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
    ndo=DataReference.create(findpath(ndofile,ndopath)[0],TWIND).getData()
    
    # conserveSpline will attempt to preserve flow positivity, but we know that
    # in deep dark historical times NDO was negative, so we are going to add
    # an arbitrary amount, interpolate the time series, and subtract the same amount
    # back. The operation is still conservative
    ndo15=conserve.conserveSpline(ndo,"15MIN")
    mtzastro=DataReference.create(findpath(astrofile,astropath)[0],TWINDBUF).getData()

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
