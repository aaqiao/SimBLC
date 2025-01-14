#####################################################################
#  Copyright (c) 2024 by Zheqiao Geng
#  All rights reserved.
#####################################################################
# Python script to display the waveforms
import time
import numpy as np
import matplotlib.pyplot as plt
from epics import caget, caput

# get parameters
prefix = 'SGE-BLC-JOBSIM:'

vc_if  = caget(prefix + 'MON-VC-IF')
vc_a   = caget(prefix + 'MON-VC-A')
vc_p   = caget(prefix + 'MON-VC-P')
t_us   = caget(prefix + 'MON-TIME-X')
spec_f = caget(prefix + 'MON-SPEC-F')
spec_a = caget(prefix + 'MON-SPEC-A')

plt.figure()
plt.subplot(221)
plt.plot(t_us, vc_a)
plt.grid()
plt.xlabel('Time ($\mu$s)')
plt.ylabel('Amplitude (V)')
plt.subplot(222)
plt.plot(t_us, vc_p)
plt.grid()
plt.xlabel('Time ($\mu$s)')
plt.ylabel('Phase (deg)')
plt.subplot(223)
plt.plot(spec_f, spec_a)
plt.grid()
plt.xlabel('Freq (Hz)')
plt.ylabel('Mag (dB)')
plt.show()

