# Python script to setup the parameters
import time
import numpy as np
import matplotlib.pyplot as plt
from epics import caget, caput

# set parameters
prefix = 'SGE-BLC-JOBSIM:'

caput(prefix + 'SET-N-DEMOD',  240)
caput(prefix + 'SET-LOOP-PHA', 46.25)
caput(prefix + 'SET-KP',       80.0)
caput(prefix + 'SET-KI',       0.0)

caput(prefix + 'ENA-NOTCH-H1', 0)
caput(prefix + 'ENA-NOTCH-H2', 0)
caput(prefix + 'ENA-NOTCH-H3', 0)
caput(prefix + 'ENA-NOTCH-H4', 0)
caput(prefix + 'ENA-NOTCH-H5', 0)
caput(prefix + 'ENA-NOTCH-H6', 0)
caput(prefix + 'ENA-NOTCH-H7', 0)
caput(prefix + 'ENA-NOTCH-H8', 0)
caput(prefix + 'ENA-NOTCH-H9', 0)
caput(prefix + 'ENA-NOTCH-H10', 0)

caput(prefix + 'SET-NOTCH-G1', 100)
caput(prefix + 'SET-NOTCH-G2', 100)
caput(prefix + 'SET-NOTCH-G3', 100)
caput(prefix + 'SET-NOTCH-G4', 100)
caput(prefix + 'SET-NOTCH-G5', 100)
caput(prefix + 'SET-NOTCH-G6', 100)
caput(prefix + 'SET-NOTCH-G7', 100)
caput(prefix + 'SET-NOTCH-G8', 100)
caput(prefix + 'SET-NOTCH-G9', 100)
caput(prefix + 'SET-NOTCH-G10', 100)

caput(prefix + 'SET-NOTCH-HBW1', 2000)
caput(prefix + 'SET-NOTCH-HBW2', 2000)
caput(prefix + 'SET-NOTCH-HBW3', 2000)
caput(prefix + 'SET-NOTCH-HBW4', 2000)
caput(prefix + 'SET-NOTCH-HBW5', 2000)
caput(prefix + 'SET-NOTCH-HBW6', 2000)
caput(prefix + 'SET-NOTCH-HBW7', 2000)
caput(prefix + 'SET-NOTCH-HBW8', 2000)
caput(prefix + 'SET-NOTCH-HBW9', 2000)
caput(prefix + 'SET-NOTCH-HBW10', 2000)

step = 20
caput(prefix + 'SET-NOTCH-LP1', step * 1)
caput(prefix + 'SET-NOTCH-LP2', step * 2)
caput(prefix + 'SET-NOTCH-LP3', step * 3)
caput(prefix + 'SET-NOTCH-LP4', step * 4)
caput(prefix + 'SET-NOTCH-LP5', step * 5)
caput(prefix + 'SET-NOTCH-LP6', step * 6)
caput(prefix + 'SET-NOTCH-LP7', step * 7)
caput(prefix + 'SET-NOTCH-LP8', step * 8)
caput(prefix + 'SET-NOTCH-LP9', step * 9)
caput(prefix + 'SET-NOTCH-LP10', step * 10)

caput(prefix + 'ENA-NCO-H1', 0)
caput(prefix + 'ENA-NCO-H2', 0)
caput(prefix + 'ENA-NCO-H3', 0)
caput(prefix + 'ENA-NCO-H4', 0)
caput(prefix + 'ENA-NCO-H5', 0)
caput(prefix + 'ENA-NCO-H6', 0)
caput(prefix + 'ENA-NCO-H7', 0)
caput(prefix + 'ENA-NCO-H8', 0)
caput(prefix + 'ENA-NCO-H9', 0)
caput(prefix + 'ENA-NCO-H10', 0)

caput(prefix + 'SET-NCO-AMP1', 20000)
caput(prefix + 'SET-NCO-AMP2', 20000)
caput(prefix + 'SET-NCO-AMP3', 20000)
caput(prefix + 'SET-NCO-AMP4', 20000)
caput(prefix + 'SET-NCO-AMP5', 20000)
caput(prefix + 'SET-NCO-AMP6', 20000)
caput(prefix + 'SET-NCO-AMP7', 20000)
caput(prefix + 'SET-NCO-AMP8', 20000)
caput(prefix + 'SET-NCO-AMP9', 20000)
caput(prefix + 'SET-NCO-AMP10', 20000)

caput(prefix + 'SET-NCO-PHAP1', 90)
caput(prefix + 'SET-NCO-PHAP2', 90)
caput(prefix + 'SET-NCO-PHAP3', 90)
caput(prefix + 'SET-NCO-PHAP4', 90)
caput(prefix + 'SET-NCO-PHAP5', 90)
caput(prefix + 'SET-NCO-PHAP6', 90)
caput(prefix + 'SET-NCO-PHAP7', 90)
caput(prefix + 'SET-NCO-PHAP8', 90)
caput(prefix + 'SET-NCO-PHAP9', 90)
caput(prefix + 'SET-NCO-PHAP10', 90)

caput(prefix + 'SET-NCO-PHAN1', 90)
caput(prefix + 'SET-NCO-PHAN2', 90)
caput(prefix + 'SET-NCO-PHAN3', 90)
caput(prefix + 'SET-NCO-PHAN4', 90)
caput(prefix + 'SET-NCO-PHAN5', 90)
caput(prefix + 'SET-NCO-PHAN6', 90)
caput(prefix + 'SET-NCO-PHAN7', 90)
caput(prefix + 'SET-NCO-PHAN8', 90)
caput(prefix + 'SET-NCO-PHAN9', 90)
caput(prefix + 'SET-NCO-PHAN10', 90)

# commands
caput(prefix + 'CMD-SET-PARAM', 1)
time.sleep(0.5)
caput(prefix + 'CMD-SET-PARAM', 0)

caput(prefix + 'CMD-RESET', 1)
time.sleep(0.5)
caput(prefix + 'CMD-RESET', 0)




