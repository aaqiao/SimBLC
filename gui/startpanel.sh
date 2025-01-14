#!/bin/bash
#####################################################################
#  Copyright (c) 2024 Zheqiao Geng
#  All rights reserved.
#####################################################################
ModuleName=SGE-BLC

echo "Start panels for RFSysSim example"
declare -x EPICS_CA_ADDR_LIST="$EPICS_CA_ADDR_LIST localhost"

caqtdm -noMsg -macro "MODULE_NAME=$ModuleName" GUI_SimBLC.ui &


