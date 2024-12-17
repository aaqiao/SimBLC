#####################################################################
#  Copyright (c) 2024 by Zheqiao Geng
#  All rights reserved.
#####################################################################
#################################################################
# Install a soft ioc
#################################################################
import os
import sys

from Softioc_Top import *

# define the soft IOC name
softIOCName = "SGE-CPCL-BLC"

# create object of the soft IOC
sIOC = Softioc_Top("SGE-BLC")    # "module name": 1st part of local PV names (name space)
sIOC.genRunScript(softIOCName)

# generate the soft IOC
Application.generateSoftIOC(softIOCName,
                            py_cmd = '/opt/gfa/python-3.10/latest/bin/python')

# copy the code to cfg folder, the execution home folder
os.system("cp *.py cfg/")           # copy all Python code to cfg/


