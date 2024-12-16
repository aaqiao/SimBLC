"""
Simulate an NCO

Created by Zheqiao Geng on 2024.12.16
"""
import numpy as np

# =================================================
# define the class
# =================================================
class NCO():
    # -------------------------------------------
    # construction
    # -------------------------------------------
    def __init__(self):
        # init variables
        self.phase       = 0.0              # instant phase, rad
        self.initialized = False            # indicate if initialized or not

    # -------------------------------------------
    # set parameters
    # -------------------------------------------
    def set_param(self, fs = 1.0e6, fnco = 1.0e3):
        # check the input (to be done ...)
        
        # store the results
        self.fs   = fs
        self.fnco = fnco

        # derived parameters
        self.dpha = fnco / fs * 2.0 * np.pi

        # declare initialized
        self.initialized = True

    # -------------------------------------------
    # reset
    # -------------------------------------------
    def reset(self):
        self.phase = 0.0

    # -------------------------------------------
    # simulate a step
    # -------------------------------------------
    def sim_step(self):
        # check if initialized
        if not self.initialized:
            return 0.0, 0.0

        # update the phase
        self.phase += self.dpha

        # generate output
        return np.exp(1j * self.phase), np.exp(-1j * self.phase)



    
