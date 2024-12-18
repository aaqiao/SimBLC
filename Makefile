#############################################################################
#  Copyright (c) 2024 by Zheqiao Geng
#  All rights reserved.
#############################################################################
# Make file for the SimBLC

default: help
help ::
	@echo "Makefile for SimBLC"
	@echo "======================================================"
	@echo "available targets:"
	@echo " -> make clean       clean the Python compilation"
	@echo " -> make install     install the soft IOC"
	@echo "======================================================"

# remove all compiled data
clean ::
	rm -rf __pycache__	
	rm -rf cfg
	rm -rf SGE-CPCL-*
		
# install soft IOC
install ::
	/opt/gfa/python-3.10/latest/bin/python Install_SoftIOC.py

