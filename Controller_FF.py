"""
feedforward controller

Created by Zheqiao Geng on 2024.12.17
"""
import numpy as np

from NCO import *

# =================================================
# define the class
# =================================================
class Controller_FF():
    # -------------------------------------------
    # construction
    # -------------------------------------------
    def __init__(self):
        # init variables
        self.initialized = False    # indicate if initialized or not

        # contains an NCO
        self.nco = NCO()
    
    # -------------------------------------------
    # set parameters
    # Input: fs   - sampling frequency, Hz
    #        fnco - NCO frequency, Hz
    #        A    - ampltiude calibration
    #        P    - phase calibration, deg
    # -------------------------------------------
    def set_param(self, fs = 10.0e6, fnco = 0.0, A = 1.0, P = 0.0):
        # check the input (to be done ...)
        
        # store the results
        self.fs   = fs
        self.fnco = fnco
        self.A    = A
        self.P    = P * np.pi / 180.0

        # init the NCO
        self.nco.set_param(fs = fs, fnco = fnco)

        # declare initialized
        self.initialized = True

    # -------------------------------------------
    # reset
    # -------------------------------------------
    def reset(self):
        self.nco.reset()

    # -------------------------------------------
    # simulate a step    
    # -------------------------------------------
    def sim_step(self):
        # check if initialized
        if not self.initialized:
            return 0.0

        # calculate the output
        return self.nco.sim_step() * self.A * np.exp(1j * self.P)



    
