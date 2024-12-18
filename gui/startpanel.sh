#!/bin/bash
#####################################################################
#  Copyright (c) 2023 by Paul Scherrer Institute, Switzerland
#  All rights reserved.
#  Authors: Zheqiao Geng
#####################################################################
ModuleName=SGE-BLC

echo "Start panels for RFSysSim example"
declare -x EPICS_CA_ADDR_LIST="$EPICS_CA_ADDR_LIST localhost"

caqtdm -noMsg -macro "MODULE_NAME=$ModuleName" GUI_SimBLC.ui &


