"""
Controller for beam loading compensation/control
 * PI feedback control
 * notch feedback controls
 * feedforward control
 
Created by Zheqiao Geng on 2024.12.14
"""
import numpy as np
from Controller_PI import * 
from Controller_Notch import * 

# =================================================
# define the class
# =================================================
class Controller():
    # -------------------------------------------
    # construction
    # -------------------------------------------
    def __init__(self):
        # init variables
        self.cnt = 0                    # counter of sim steps
        self.initialized = False        # indicate if initialized or not

    # -------------------------------------------
    # set parameters
    # Input: fb      - bunch rep freq, Hz
    #        fs      - sampling frequency, Hz
    #        fif     - IF frequency, Hz
    #        ndemod  - demodulation avg num
    #        lp_pha  - loop phase correction, deg
    #        Kp      - proportional feedback gain
    #        Ki      - integral feedback gain
    #        notches - data structure for notch controller
    # -------------------------------------------        
    def set_param(self, fb      = 1.0e6,
                        fs      = 10.0e6,
                        fif     = 1.0e6,
                        ndemod  = 4,
                        lp_pha  = 10,
                        Kp      = 10.0,
                        Ki      = 0.0,
                        notches = None):
        # check the input (to be done ...)
        
        # store the results
        self.fb      = fb
        self.fs      = fs
        self.fif     = fif
        self.ndemod  = ndemod
        self.lp_pha  = lp_pha * np.pi / 180.0
        self.Kp      = Kp
        self.Ki      = Ki
        self.notches = notches

        # derived variables
        self.buf_demod = np.zeros(ndemod, dtype = 'complex')
        self.Ts = 1.0 / fs                  # sampling time, s

        # construct the controller
        self.control = []
        
        # - define PI controller
        pictrl = Controller_PI()
        pictrl.set_param(Kp = Kp, Ki = Ki)
        self.control.append(pictrl)
        
        # - define notch controller
        if notches is not None:
            # get the notch parameters
            nt_fn = notches['freq_offs']     # notch frequency offset to carrier, Hz
            nt_fh = notches['half_bw']       # half BW of notch filter, Hz
            nt_g  = notches['gain']          # gain
            
            # construct the notch controller
            for i in range(len(nt_fn)):
                nctrl = Controller_Notch()
                nctrl.set_param(fs   = fs, 
                                fh   = nt_fh[i], 
                                fn   = nt_fn[i], 
                                gain = nt_g[i])
                self.control.append(nctrl)
            
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
        
        # reset notch controllers
        for ctl in self.notch_ctrl:
            ctl.reset()

    # -------------------------------------------
    # simulate a step
    # Input: vc_if      - IF signal of the cavity voltage, V
    #        vc_sp      - setpoint phasor of cavity voltage, V
    #        fb_enable  - True for enabling feedback
    # -------------------------------------------
    def sim_step(self, vc_if, vc_sp, 
                       fb_enable = False):
        # check if initialized
        if not self.initialized:
            return 0.0
        
        # demodulation/corr loop phase/calc error
        vc = self._demod(vc_if) * np.exp(1j * self.lp_pha)
        vc_err = vc_sp - vc
        
        # feedback for a step
        vf = 0.0
        for ctl in self.control:
            vf += ctl.sim_step(vc_err)

        # if feedback not enable
        if not fb_enable:
            vf = 0.0
        
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






