#####################################################################
#  Copyright (c) 2024 by Zheqiao Geng
#  All rights reserved.
#####################################################################
#################################################################
# This is a job to simulate the beam loading compensation
#################################################################
import time
import threading
import numpy as np

from ooepics.Job import *
from llrflibs.rf_noise import *

from Cavity import *
from Controller import *

# =================================
# define the class
# =================================
class Job_SimBLC(Job):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    # class variables
    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    DAQ_SIZE = 2**15            # buffer size for DAQ
    MAX_BH   = 10               # max number of beam harmonics
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    # create the object
    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, modName, jobName):
        # init the parent class
        Job.__init__(self, modName, jobName)

        # define local PVs, PV names will be built up as: $(module_name)-$(job_name):$(data_name)
        #   parameters:
        #       module name; 
        #       job name; 
        #       data name; 
        #       selection string list (for mbbi/mbbo); 
        #       number of element; 
        #       record type; 
        #       description

        self.lpv_setNDemod    = LocalPV(self.modName, self.jobName, "SET-N-DEMOD",  "",  "",    1, "longout", "n of noniq demod")
        self.lpv_setLoopPha   = LocalPV(self.modName, self.jobName, "SET-LOOP-PHA", "",  "deg", 1, "ao",      "loop phase corr")
        self.lpv_setKp        = LocalPV(self.modName, self.jobName, "SET-KP",       "",  "",    1, "ao",      "P gain")
        self.lpv_setKi        = LocalPV(self.modName, self.jobName, "SET-KI",       "",  "",    1, "ao",      "I gain")

        self.lpv_enaNotchH    = [LocalPV(self.modName, self.jobName, "ENA-NOTCH-H" + str(i+1),   "", "",   1, "bo", "notch harmonic") \
                                 for i in range(Job_SimBLC.MAX_BH)]
        self.lpv_setNotchG    = [LocalPV(self.modName, self.jobName, "SET-NOTCH-G" + str(i+1),   "", "",   1, "ao", "notch gain") \
                                 for i in range(Job_SimBLC.MAX_BH)]
        self.lpv_setNotchHbw  = [LocalPV(self.modName, self.jobName, "SET-NOTCH-HBW" + str(i+1), "", "Hz", 1, "ao", "notch half bandwidth") \
                                 for i in range(Job_SimBLC.MAX_BH)]

        self.lpv_enaNCOH      = [LocalPV(self.modName, self.jobName, "ENA-NCO-H" + str(i+1),   "", "",    1, "bo", "NCO harmonic") \
                                 for i in range(Job_SimBLC.MAX_BH)]
        self.lpv_setNCOA      = [LocalPV(self.modName, self.jobName, "SET-NCO-AMP" + str(i+1), "", "",    1, "ao", "NCO amplitude") \
                                 for i in range(Job_SimBLC.MAX_BH)]
        self.lpv_setNCOP      = [LocalPV(self.modName, self.jobName, "SET-NCO-PHA" + str(i+1), "", "deg", 1, "ao", "NCO phase") \
                                 for i in range(Job_SimBLC.MAX_BH)]

        self.lpv_monVcIF      = LocalPV(self.modName, self.jobName, "MON-VC-IF",  "",   "V", Job_SimBLC.DAQ_SIZE, "waveform", "VC IF")
        self.lpv_monVcA       = LocalPV(self.modName, self.jobName, "MON-VC-A",   "",   "V", Job_SimBLC.DAQ_SIZE, "waveform", "VC amplitude")
        self.lpv_monVcP       = LocalPV(self.modName, self.jobName, "MON-VC-P",   "", "deg", Job_SimBLC.DAQ_SIZE, "waveform", "VC phase")
        self.lpv_monTimeX     = LocalPV(self.modName, self.jobName, "MON-TIME-X", "",  "us", Job_SimBLC.DAQ_SIZE, "waveform", "time x axis")                
        self.lpv_monVcIFSpecF = LocalPV(self.modName, self.jobName, "MON-SPEC-F", "",  "Hz", Job_SimBLC.DAQ_SIZE, "waveform", "VC IF spec freq")
        self.lpv_monVcIFSpecA = LocalPV(self.modName, self.jobName, "MON-SPEC-A", "",  "dB", Job_SimBLC.DAQ_SIZE, "waveform", "VC IF spec amplitude")
                
        # parameters of the beam and cavity
        frf     = 650e6                     # RF operation frequency, Hz
        dw      = 0                         # cavity detuning, rad/s
        RoQ     = 106.5                     # R/Q (circular machine convence), Ohm
        QL      = 1.5e5                     # loaded quality factor
        Qb      = 1.6e-19 * 14e10           # bunch charge, C
        h       = 216820 / 10               # harmonic number
        phb     = -50 * np.pi / 180         # beam accelerating phase, rad

        self.vc_sp = 1e6                    # desired cavit voltage        
        self.fb    = frf / h                # bunch repititon rate, Hz              
        self.fs    = 4000 * self.fb         # sampling frequency, Hz
        self.fif   = 500 * self.fb          # IF frequency, Hz

        # define the cavity and controller object
        self.cav = Cavity()
        self.ctl = Controller()
        self.cav.set_param(frf       = frf, 
                           RoQ       = RoQ, 
                           QL        = QL, 
                           detuning  = dw / 2 / np.pi,
                           charge    = Qb,
                           fb        = self.fb,
                           phib      = phb * 180 / np.pi,
                           fs        = self.fs,
                           fif       = self.fif,
                           npsd      = -130.0)

        # mutex
        self.mutex = threading.Lock()
        
        # variables and buffers
        self.init_done = False
        self.daq_id    = 0
        self.sim_time  = 0.0
        self.vact      = 0.0

        self.sig_vcif = np.zeros(Job_SimBLC.DAQ_SIZE)
        self.sig_vca  = np.zeros(Job_SimBLC.DAQ_SIZE)
        self.sig_vcp  = np.zeros(Job_SimBLC.DAQ_SIZE)
        self.time_x   = np.zeros(Job_SimBLC.DAQ_SIZE)

        # define the local thread
        self.simThread = threading.Thread(target = self.sim_step,
                                          args   = (),
                                          daemon = True,
                                          name   = "TRD-JOB")       

        print("INFO: Job_SimBLC object created.")

    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    # start the thread
    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    def letGoing(self):
        print('INFO: Thread TRD-JOB started.')
        self.simThread.start()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    # execute the job  
    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    def execute(self, cmdId, dataBus):
        # response to command: SET-PARAM
        if cmdId == 0:
            # get the parameters from the PVs
            ndemod, _, _, _ = self.lpv_setNDemod.read()
            lp_pha, _, _, _ = self.lpv_setLoopPha.read()
            Kp,     _, _, _ = self.lpv_setKp.read()
            Ki,     _, _, _ = self.lpv_setKi.read()

            notch_fn  = []
            notch_g   = []
            notch_hbw = []
            nco_fn    = []
            nco_amp   = []
            nco_pha   = []

            for i in range(Job_SimBLC.MAX_BH):
                ft,  _, _, _ = self.lpv_enaNotchH[i].read()
                g,   _, _, _ = self.lpv_setNotchG[i].read()
                hbw, _, _, _ = self.lpv_setNotchHbw[i].read()
                fo,  _, _, _ = self.lpv_enaNCOH[i].read()
                amp, _, _, _ = self.lpv_setNCOA[i].read()
                pha, _, _, _ = self.lpv_setNCOP[i].read()
                
                notch_fn.append (ft)
                notch_g.append  (g)
                notch_hbw.append(hbw)
                nco_fn.append   (fo)
                nco_amp.append  (amp)
                nco_pha.append  (pha)

            # set the parameters for controller
            notch_harmnics = np.where(np.array(notch_fn) == 1)[0] + 1
            notch_harmnics = np.hstack((notch_harmnics, -notch_harmnics))
            nco_harmonics  = np.where(np.array(nco_fn) == 1)[0] + 1

            notches = {'freq_offs': notch_harmnics * self.fb,
                       'gain':      notch_g * 2,
                       'half_bw':   notch_hbw * 2}
            ffncos  = {'freq_offs': nco_harmonics * self.fb,
                       'amp_cal':   nco_amp,
                       'pha_cal':   nco_pha}

            self.mutex.acquire()
            self.ctl.set_param(fb      = self.fb,
                               fs      = self.fs,
                               fif     = self.fif,
                               ndemod  = int(ndemod),            # 240 = delay of 1 us
                               lp_pha  = lp_pha,
                               Kp      = Kp,
                               Ki      = Ki,
                               notches = notches,
                               ffncos  = ffncos)
            self.mutex.release()     
           
            # indicate the init is done
            self.init_done = True  

            # message and return          
            print("INFO: Set parameters.")   
            return dataBus, True

        # response to command: RESET
        elif cmdId == 1:
            # reset the model
            self.mutex.acquire()
            self.cav.reset()
            self.ctl.reset()
                        
            self.daq_id   = 0
            self.sim_time = 0.0

            self.lpv_monVcIF.write      (np.zeros(Job_SimBLC.DAQ_SIZE))
            self.lpv_monVcA.write       (np.zeros(Job_SimBLC.DAQ_SIZE))
            self.lpv_monVcP.write       (np.zeros(Job_SimBLC.DAQ_SIZE))
            self.lpv_monTimeX.write     (np.arange(Job_SimBLC.DAQ_SIZE) / self.fs * 1e6)
            self.lpv_monVcIFSpecF.write (np.zeros(Job_SimBLC.DAQ_SIZE))
            self.lpv_monVcIFSpecA.write (np.zeros(Job_SimBLC.DAQ_SIZE))
            self.mutex.release()
                        
            print("INFO: Reset simulation.")
            return dataBus, True

        # unkown commands
        else:
            print("ERROR: Command not known!")
            return dataBus, False

    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    # simulation for a step
    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    def sim_step(self):
        while True:
            # check the init
            if not self.init_done:
                time.sleep(0.1)
                continue
        
            # lock access to the model
            self.mutex.acquire()
        
            # do a step of simulation
            _, vc_if, vf_if, vr_if = self.cav.sim_step(self.vact)
            vc, self.vact = self.ctl.sim_step(vc_if, 
                                             self.vc_sp * np.exp(1j * np.pi / 6), 
                                             fb_enable = True,
                                             ff_enable = True)

            # update the simulation time
            self.sim_time = self.sim_time + 1.0 / self.fs

            # collect the results
            if self.daq_id < Job_SimBLC.DAQ_SIZE:
                self.sig_vcif[self.daq_id] = vc_if
                self.sig_vca[self.daq_id]  = np.abs(vc)
                self.sig_vcp[self.daq_id]  = np.angle(vc, deg = True)
                self.time_x[self.daq_id]   = self.sim_time

            # write the DAQ waveform and restart
            self.daq_id = self.daq_id + 1
            if self.daq_id == Job_SimBLC.DAQ_SIZE:
                self.lpv_monVcIF.write  (self.sig_vcif)
                self.lpv_monVcA.write   (self.sig_vca)
                self.lpv_monVcP.write   (self.sig_vcp)
                self.lpv_monTimeX.write (self.time_x)

                result = calc_psd_coherent(self.sig_vcif, fs = self.fs, n_noniq = 8)
                self.lpv_monVcIFSpecF.write(result['freq'])
                self.lpv_monVcIFSpecA.write(result['amp_resp'])

            if self.daq_id >= Job_SimBLC.DAQ_SIZE:
                self.daq_id = 0

            # end of usage of the model
            self.mutex.release()

            # wait
            time.sleep(0.00001)




