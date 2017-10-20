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
from vdss import opendss,findpath,writedss
from vista.time import TimeFactory

def planning_ec_mtz(so,sb,beta,npow1,npow2,adel,c,outputfile,outputpath,twstr): # MTZ = RSAC054 BC for the qual
    ndofile = opendss("mtz_ec_input.dss")
    ndopath = "/CALSIM/NDO/FLOW-NDO//1MON/2005A01A/"                   # planning study from Calsim
    
    astrofile=ndofile
    astropath="/FILL\+CHAN/RSAC054/STAGE//15MIN/ASTRO-PLANNING-2/"     # astr plan ngvd
    
    st=timewindow(twstr).startTime
    et=timewindow(twstr).endTime
    span_year = et.date.year-st.date.year
    
    if span_year>60:
      blocks=[]
      st_i=st
      for i in range(0,span_year/60):
        et_i = st_i+timeinterval('60year')
        blocks.append(TimeFactory.getInstance().createTimeWindow(st_i,et_i).__str__())
        st_i=et_i
      blocks.append(TimeFactory.getInstance().createTimeWindow(st_i,et).__str__())
    else:blocks=[twstr]
    print blocks
    
    g0=5000.                                          # initial value of g (antecedent outflow) for the beginning
                                                      # of the first year. This is pretty arbitrary and makes little difference
    for twstr in blocks:
    
      TWIND=timewindow(twstr)
      TWINDBUF=grow_window(TWIND,"1MON","1MON")     # Conservative buffered period for retrieval
                                                    # so that after prelimiary operations (e.g. time average)
                                                    # time series will still span at least TWIND
      ndo=DataReference.create(findpath(ndofile,ndopath)[0],TWIND).getData()
      ndo15=conserve.conserveSpline(ndo,"15MIN")
      mtzastro=DataReference.create(findpath(astrofile,astropath)[0],TWINDBUF).getData()
      
      astrorms=godin((mtzastro*mtzastro)**0.5)           # RMS energy of tide (used to predict filling and draining)
      dastrorms=(  (astrorms-(astrorms>>1))*96. ).createSlice(TWIND)    
      fifteenflo2=ndo15 - adel*(dastrorms)
      # call to ec estimator. all parameters are included
      [mtzecest, g1]=ec_boundary.ECEst(mtzastro,fifteenflo2,so,sb,beta,npow1,npow2,g0=g0,zrms=astrorms,c=c)
      writedss(outputfile,outputpath,mtzecest)
      
      g0=g1
    return 0
    
def read_input_params(file):
    """
    Read input params from file, ignores the first two lines and then reads parameters (one per line) and returns the tuple
    """
    fh = open(file)
    lines=fh.readlines()
    params=map(lambda x: float(x), tuple(lines[2:16]))
    fh.close()
    return params

    
if __name__ == "__main__":
    DEBUG=False
    suffix = 'so37196'  # calibrated from 91/1-93/9 astr stage & dicu, hist EC
    
    #Read param from input
    so,sb,beta,npow1,adel,c0,c1,c2,c3,c4,c5,c6,c7=read_input_params("param_"+suffix+".dat")
    c=[c0,c1,c2,c3,c4,c5,c6,c7]
    npow2=1.0    #npow2 fixed
    if DEBUG: 
      print "\nRunning model with params so,sb,beta,npow1,adel,c0-7: "
      print so,sb,beta,npow1,adel, c0, c1, c2, c3, c4, c5, c6, c7
    
    #Run model with input param
    outputfile="mtz_ec_output.dss"
    outputpath="/FILL+CHAN/RSAC054/EC//15MIN/PLAN/"
    twstr="01OCT1921 0000 - 01OCT2003 0000"
    
    planning_ec_mtz(so,sb,beta,npow1,npow2,adel,c,outputfile,outputpath,twstr)    
    
    exit()
