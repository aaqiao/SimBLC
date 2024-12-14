"""
Controller for beam loading compensation/control

Created by Zheqiao Geng on 2024.12.14
"""
import numpy as np
from scipy import signal

# =================================================
# define the class
# =================================================
class Controller():
    # -------------------------------------------
    # construction
    # -------------------------------------------
    def __init__(self):
        # init variables
        self.cnt         = 0                # counter of sim steps
        self.initialized = False            # indicate if initialized or not

    # -------------------------------------------
    # set parameters
    # Input: fb     - bunch rep freq, Hz
    #        fs     - sampling frequency, Hz
    #        fif    - IF frequency, Hz
    #        ndemod - demodulation avg num
    # -------------------------------------------        
    def set_param(self, fb     = 1.0e6,
                        fs     = 10.0e6,
                        fif    = 1.0e6,
                        ndemod = 4):
        # check the input (to be done ...)
        
        # store the results
        self.fb     = fb
        self.fs     = fs
        self.fif    = fif
        self.ndemod = ndemod

        # derived variables
        self.buf_demod = np.zeros(ndemod, dtype = 'complex')
        self.Ts     = 1.0 / fs                               # sampling time, s

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
        self.buf_demod[:] = 0.0
        self.cnt = 0

    # -------------------------------------------
    # simulate a step
    # Input: vc_if  - IF signal of the cavity voltage
    #        vc_sp  - setpoint phasor of cavity voltage
    # -------------------------------------------
    def sim_step(self, vc_if, vc_sp, pgain = 10.0):
        # check if initialized
        if not self.initialized:
            return 0.0
        
        # do demodulation
        vc = self._demod(vc_if)
        
        # feedback for a step
        vf = pgain * (vc_sp - vc)
        
        # get the IF signal of the actuation signal
        vf_if = np.real(vf * np.exp(1j * 2.0 * np.pi * self.fif * \
                                    self.cnt * self.Ts))
        
        # update the variable for next step
        self.cnt += 1
            
        # return the result
        return vc, vf_if

    # -------------------------------------------
    # private functions    
    # -------------------------------------------
    def _demod(self, vin_if):  
        self.buf_demod = np.roll(self.buf_demod, -1)
        self.buf_demod[-1] = 2.0 * vin_if * np.exp(-1j * 2.0 * np.pi * \
                                                   self.fif * self.cnt * self.Ts)
        return np.mean(self.buf_demod)






