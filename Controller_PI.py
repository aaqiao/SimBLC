"""
PI controller

Created by Zheqiao Geng on 2024.12.15
"""
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
        self.integrator  = 0.0              # integrator for I control
        self.initialized = False            # indicate if initialized or not

    # -------------------------------------------
    # set parameters
    # Input: Kp - proportional feedback gain
    #        Ki - integral feedback gain
    # -------------------------------------------
    def set_param(self, Kp = 10.0, Ki = 0.0):
        # check the input (to be done ...)
        
        # store the results
        self.Kp = Kp
        self.Ki = Ki

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
        self.integrator += self.Ki * vi
        
        # generate output
        return self.Kp * vi + self.integrator



    
