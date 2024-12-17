"""
Cavity model for beam loading study
 * The cavity receives IF input and generate IF output
 * Beam loading is added for each bunch
 * Noise is added in the output to emulate meas noise

Created by Zheqiao Geng on 2024.12.14
"""
import numpy as np
from scipy import signal

from llrflibs.rf_noise import *

# =================================================
# define the class
# =================================================
class Cavity():
    # -------------------------------------------
    # construction
    # -------------------------------------------
    def __init__(self):
        # init variables
        self.vc_last     = 0.0              # temp var for solving cavity equ, V
        self.cnt         = 0                # counter of sim steps (with arbitrary init time)
        self.noise       = np.zeros(2048)   # noise series
        self.initialized = False            # indicate if initialized or not

    # -------------------------------------------
    # set parameters
    # Input: frf       - RF operation frequency, Hz
    #        RoQ       - R/Q (circular machine convenient), Ohm
    #        QL        - loaded quality factor
    #        detuning  - detuning of the cavity, Hz
    #        charge    - bunch charge, C
    #        fb        - bunch rep freq, Hz
    #        phib      - beam accelerating phase, deg
    #        fs        - sampling frequency, Hz
    #        fif       - IF frequency, Hz
    #        npsd      - noise PSD, dB/Hz
    # -------------------------------------------        
    def set_param(self, frf       = 650.0e6, 
                        RoQ       = 106.5, 
                        QL        = 1.5e5, 
                        detuning  = 0.0,
                        charge    = 2.234e-8,
                        fb        = 1.0e6,
                        phib      = 0.0,
                        fs        = 10.0e6,
                        fif       = 1.0e6,
                        npsd      = -135.0):
        # check the input (to be done ...)
        
        # store the results
        self.frf    = frf
        self.RoQ    = RoQ
        self.QL     = QL
        self.Qb     = charge
        self.fb     = fb
        self.phib   = phib * np.pi / 180.0
        self.fs     = fs
        self.fif    = fif
        self.npsd   = npsd
        
        # derived cavity parameters
        self.wrf    = 2.0 * np.pi * frf                     # RF angular freq, rad/s
        self.wc     = self.wrf                              # carrier frequency, rad/s
        self.dw     = 2.0 * np.pi * detuning                # detuning, rad/s
        self.w0     = self.wc + self.dw                     # cavity resonance frequency, rad/s        
        self.wh     = self.w0 / (2.0 * QL)                  # half bandwidth, rad/s
        self.RL     = RoQ * QL                              # loaded resistance (circular machine), Ohm
        self.Ts     = 1.0 / fs                              # sampling time, s
        self.Tb_clk = int(fs / fb)                          # determine when to add beam loading of a bunch
       
        # parameters for beam induced signal calculation
        self.w0p    = np.sqrt(self.w0**2 - self.wh**2)
        self.gl     = 1.0 + 1j * self.wh / self.w0p
        self.dwl    = self.w0p - self.wc        

        # declare initialized
        self.initialized = True

    # -------------------------------------------
    # reset
    # -------------------------------------------
    def reset(self):
        self.vc_last = 0.0
        self.cnt     = 0

    # -------------------------------------------
    # simulate a step
    # Input: vf_if  - IF signal of the cavity drive
    # -------------------------------------------
    def sim_step(self, vf_if):
        # check if initialized
        if not self.initialized:
            return (0.0,)*4
        
        # update noise series if needed
        if self.cnt % 2048 == 0:
            self._gen_noise()
        
        # get the cavity drive phasor
        # Note: 1. here we do not make the filtering, because the 2*fif term will
        #       be filtered by the cavity dyanmic automatically (i.e., the cavity 
        #       bandwidth is much smaller than fif)
        #       2. the factor 2.0 is needed to keep the amplitude of the response        
        vf = 2.0 * vf_if * np.exp(-1j * 2.0 * np.pi * self.fif * \
                                  self.cnt * self.Ts)
        
        # do a step of cavity simulation
        vc = (1.0 - self.Ts * (self.wh - 1j*self.dwl)) * self.vc_last + \
             self.wh * self.Ts * vf
        
        # add the beam loading
        if self.cnt % self.Tb_clk == 0:
            vc += 2.0 * self.wh * self.RL * self.Qb * self.gl * \
                  np.exp(1j * (np.pi - self.phib))
        
        # get the IF signal with noise
        vc_if = np.real(vc * np.exp(1j * 2.0 * np.pi * self.fif * \
                                    self.cnt * self.Ts)) * \
                     (1.0 + self.noise[self.cnt % 2048])
        
        # get the reflection 
        vr_if = vc_if - vf_if
        
        # update the variable for next step
        self.vc_last = vc
        self.cnt += 1
            
        # return the result
        return vc, vc_if, vf_if, vr_if

    # -------------------------------------------
    # private functions    
    # -------------------------------------------
    def _gen_noise(self):
        _, self.noise, _, _ = gen_noise_from_psd(np.array([10.0, 100.0]), 
                                                 np.array([self.npsd, self.npsd]), 
                                                 self.fs, 
                                                 2048)        

       






