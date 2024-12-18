#####################################################################
#  Copyright (c) 2024 by Zheqiao Geng
#  All rights reserved.
#####################################################################
#################################################################
# NCO model
#################################################################
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
        self.cnt = 0                # counter of sim steps
        self.initialized = False    # indicate if initialized or not

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
        self.cnt = 0

    # -------------------------------------------
    # simulate a step
    # -------------------------------------------
    def sim_step(self):
        # check if initialized
        if not self.initialized:
            return 0.0

        # update the output (2 for both sideband)
        vo = 2.0 * np.cos(self.cnt * self.dpha)

        # update the counter
        self.cnt += 1

        # generate output 
        return vo



    
