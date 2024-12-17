#####################################################################
#  Copyright (c) 2024 by Zheqiao Geng
#  All rights reserved.
#####################################################################
#################################################################
# The top structure for the soft IOC
#################################################################
from ooepics.Application import *

from Job_SimBLC import *

# =================================
# assemble the soft IOC
# =================================
class Softioc_Top:
    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    # create the object
    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, moduleName):
        # remember input
        self.moduleName = moduleName            # "moduleName" is the first part of the local PV names

        # --------
        # define an application - the run coordinator
        # --------
        #   parameters : 
        #       1st: application name, define the thread name by adding "TRD-" before it
        #       2ed: module name, used to define local PV names
        self.appTest = Application("BLC", self.moduleName)

        # --------
        # define the jobs
        # --------
        #   parameters:
        #       1st: module name, used to define local PV names
        #       2ed: job name, used to define local PV names
        #       3rd: object of service for run-time message log
        #       4,5th: objects of RF station services for two stations
        self.jobSimBLC = Job_SimBLC(self.moduleName, "JOBSIM")

        # --------
        # register jobs to the application
        # --------
        #   parameters:
        #       1st: the object of a job
        #       2ed: commands that the job needs to handle, the string will appear in the command PV name
        self.appTest.registJob(self.jobSimBLC, ["SET-PARAM", "RESET"])

    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    # run the soft IOC thread
    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    def run(self):
        self.appTest.letGoing()           # each application is driven by a thread
        self.jobSimBLC.letGoing()         # start the simulation thread

    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    # generate the run script
    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    def genRunScript(self, softIOCName):
        # remember
        self.softIOCName = softIOCName
        fullFileName     = softIOCName + "_run.py"

        # create the file
        try:
            ssFile = open(fullFileName, "wt")    
        except IOError:
            print("Failed to created file " + fullFileName)
            return
    
        ssFile.write("# -------------------------------------------\n")
        ssFile.write("# " + fullFileName + "\n")
        ssFile.write("# Auto created by Softioc_Top, do not modify\n")
        ssFile.write("# -------------------------------------------\n")
        ssFile.write("from Softioc_Top import *\n\n")

        ssFile.write("# configure the environment\n")
        ssFile.write('sIOC = Softioc_Top("' + self.moduleName + '")\n\n')

        ssFile.write("# connect to all PVs\n")
        ssFile.write("RemotePV.connect()\n\n")
        ssFile.write("# run the soft ioc\n")
        ssFile.write("sIOC.run()\n\n")





