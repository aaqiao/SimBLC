#####################################################################
#  Copyright (c) 2024 by Zheqiao Geng
#  All rights reserved.
#####################################################################
#################################################################
# Notch feedback controller
#################################################################
import numpy as np

# =================================================
# define the class
# =================================================
class Controller_Notch():
    # -------------------------------------------
    # construction
    # -------------------------------------------
    def __init__(self):
        # init variables
        self.vo_last     = 0.0      # temp var for solving diff equ                
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
        
        # declare initialized
        self.initialized = True

    # -------------------------------------------
    # reset
    # -------------------------------------------
    def reset(self):
        self.vo_last = 0.0        

    # -------------------------------------------
    # simulate a step
    # Input: vi - instant input
    # -------------------------------------------
    def sim_step(self, vi):
        # check if initialized
        if not self.initialized:
            return 0.0

        # simulate a step        
        vo = (1.0 - self.Ts * (self.wh - 1j*self.wn)) * self.vo_last + \
             self.gain * self.wh * self.Ts * vi        
        
        # update the variable for next step
        self.vo_last = vo        
                    
        # return the result
        return vo

    
