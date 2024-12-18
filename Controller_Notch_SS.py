#####################################################################
#  Copyright (c) 2024 by Zheqiao Geng
#  All rights reserved.
#####################################################################
#################################################################
# Notch feedback controller in state-space format
#################################################################
import numpy as np
from scipy import signal

from llrflibs.rf_control import *

# =================================================
# define the class
# =================================================
class Controller_Notch_SS():
    # -------------------------------------------
    # construction
    # -------------------------------------------
    def __init__(self):
        # init variables
        self.initialized = False    # indicate if initialized or not

    # -------------------------------------------
    # set parameters
    # Input: fs   - sampling frequency, Hz
    #        fh   - half-bandwidth of notch filter, Hz
    #        fn   - notch frequency offset from carrier, Hz
    #        gain - notch control gain
    # -------------------------------------------        
    def set_param(self, fs   = 10.0e6,
                        fh   = 10.0,
                        fn   = 0.0,
                        gain = 1.0):
        # check the input (to be done ...)
        
        # store the results
        self.fs   = fs
        self.wh   = 2.0 * np.pi * fh
        self.wn   = 2.0 * np.pi * fn
        self.gain = gain
                   
        # derived parameters
        self.Ts   = 1.0 / fs
        
        # construct the state-space controller
        Ac, Bc, Cc, Dc = signal.tf2ss([self.gain * self.wh], 
                                      [1.0, self.wh - 1j * self.wn])
        _, self.A, self.B, self.C, self.D, _ = ss_discrete(Ac, Bc, Cc, Dc, 
                                                           self.Ts, 
                                                           method = 'bilinear',
                                                           plot = False,
                                                           plot_pno = 100000)
        
        self.state_k = None         # state of the controller  
        
        # declare initialized
        self.initialized = True

    # -------------------------------------------
    # reset
    # -------------------------------------------
    def reset(self):
        # check if initialized
        if not self.initialized:
            return
        
        # clear the buffer and vars
        self.state_k = None

    # -------------------------------------------
    # simulate a step
    # Input: vi - instant input
    # -------------------------------------------
    def sim_step(self, vi):
        # check if initialized
        if not self.initialized:
            return 0.0

        # feedback for a step
        # - init the state of the controller
        if ((self.state_k is None) and (self.B is not None)):
            self.state_k = np.matrix(np.zeros(self.B.shape), dtype = complex)
            
        # - execute one step feedback
        vo = 0.0
        if self.state_k is not None:        
            _, vo, _, self.state_k = control_step(self.A, self.B, self.C, self.D,
                                                  vi, self.state_k)
            vo = vo[0, 0]
                    
        # return the result
        return vo

    
