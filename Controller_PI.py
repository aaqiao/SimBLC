#####################################################################
#  Copyright (c) 2024 by Zheqiao Geng
#  All rights reserved.
#####################################################################
#################################################################
# PI feedback controller
#################################################################
import numpy as np

# =================================================
# define the class
# =================================================
class Controller_PI():
    # -------------------------------------------
    # construction
    # -------------------------------------------
    def __init__(self):
        # init variables
        self.integrator  = 0.0      # integrator for I control
        self.initialized = False    # indicate if initialized or not

    # -------------------------------------------
    # set parameters
    # Input: fs - sampling frequency, Hz
    #        Kp - proportional feedback gain
    #        Ki - integral feedback gain
    # -------------------------------------------
    def set_param(self, fs = 10.0e6, Kp = 10.0, Ki = 0.0):
        # check the input (to be done ...)
        
        # store the results
        self.Kp = Kp
        self.Ki = Ki

        # derived parameters
        self.Ts = 1.0 / fs

        # declare initialized
        self.initialized = True

    # -------------------------------------------
    # reset
    # -------------------------------------------
    def reset(self):
        self.integrator = 0.0        

    # -------------------------------------------
    # simulate a step
    # Input: vi - instant input
    # -------------------------------------------
    def sim_step(self, vi):
        # check if initialized
        if not self.initialized:
            return 0.0

        # update the integrator
        self.integrator += self.Ki * self.Ts * vi
        
        # generate output
        return self.Kp * vi + self.integrator



    
