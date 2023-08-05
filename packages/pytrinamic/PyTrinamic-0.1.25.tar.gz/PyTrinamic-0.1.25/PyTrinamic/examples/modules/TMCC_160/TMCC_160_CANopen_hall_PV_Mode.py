'''
Move a motor back and forth in PV_Mode with CANopen using the TMCC160 ic

Created on 07.05.2020

@author: JM
'''

if __name__ == '__main__':
    pass

import time
from PyTrinamic.connections.ConnectionManager import ConnectionManager
from PyTrinamic.modules.TMCC160.TMCC_160 import TMCC_160

"""
    choose the right bustype before starting the script
"""
connectionManager = ConnectionManager(" --interface kvaser_CANopen", connectionType = "CANopen")
network = connectionManager.connect()

" use EDS file "
node = network.addDs402Node(TMCC_160.edsFile(), 1)
module = node

" this function initializes the DS402 state machine "
node.setup_402_state_machine()

" communication area objects "
objManufacturerDeviceName       = module.sdo[0x1008]
objManufacturerHardwareVersion  = module.sdo[0x1009]

" manufacturer specific objects "
objMaximumCurrent               = module.sdo[0x2020][1]
objSwitchParameter              = module.sdo[0x2005]
objMotorPolePairs               = module.sdo[0x2010]
objCommutationMode              = module.sdo[0x2055]
objHallDirection                = module.sdo[0x2070][2]
objHallInterpolation            = module.sdo[0x2070][3]
objHallPHI_E_offset             = module.sdo[0x2070][4]

" profile specific objects "
objControlWord                  = module.sdo[0x6040]
objModeOfOperation              = module.sdo[0x6060]
objAcceleration                 = module.sdo[0x6083]
objActualVelocity               = module.sdo[0x606C]
objTargetVelocity               = module.sdo[0x60FF]

print("\nModule name:    %s" % objManufacturerDeviceName.raw)
print("Hardware version: %s" % objManufacturerHardwareVersion.raw)

"""
    Configure motor settings. The configuration is based on our standard BLDC motor (QBL4208-61-04-013-1024-AT).
    If you use a different motor be sure you have the right configuration setup otherwise the script may not working.
"""
objMotorPolePairs.raw              = 4
objMaximumCurrent.raw              = 1500
objCommutationMode.raw             = 6
objHallDirection.raw               = 0
objHallPHI_E_offset.raw            = 0
objAcceleration.raw                = 500

print("MotorPoles:               %d" % objMotorPolePairs.raw)
print("MaxCurrent:               %d" % objMaximumCurrent.raw)
print("CommutationMode:          %d" % objCommutationMode.raw)
print("HallDirection:            %d" % objHallDirection.raw)
print("HallPHI_E_offset:         %d" % objHallPHI_E_offset.raw)
print("Acceleration:             %d" % objAcceleration.raw)

if node.is_faulted():
    print("\nResetting fault\n")
    node.reset_from_fault() # Reset node from fault and set it to Operation Enable state 

def startPV():

    print("Node state before switch parameter write:" + node.state)
    objSwitchParameter.raw = 3

    timeout = time.time() + 15
    node.state = 'READY TO SWITCH ON'
    while node.state != 'READY TO SWITCH ON':
        if time.time() > timeout:
            raise Exception('Timeout when trying to change state')
        time.sleep(0.001)

    print(node.state)

    timeout = time.time() + 15
    node.state = 'SWITCHED ON'
    while node.state != 'SWITCHED ON':
        if time.time() > timeout:
            raise Exception('Timeout when trying to change state')
        time.sleep(0.001)

    print(node.state)

    if objModeOfOperation.raw != 3:
        objModeOfOperation.raw = 3
    print("MODE OF OPERATION SET TO: %d" % objModeOfOperation.raw)

    timeout = time.time() + 15
    node.state = 'OPERATION ENABLED'
    while node.state != 'OPERATION ENABLED':
        if time.time() > timeout:
            raise Exception('Timeout when trying to change state')
        time.sleep(0.001)

    print(node.state)

    return

def velocityReached():
    return abs(objActualVelocity.raw - objTargetVelocity.raw) < 10

" switch to PV mode"
startPV()

" set a target velocity "
objTargetVelocity.raw = 1000

while not velocityReached():
    print("TargetVelocity: " + str(objTargetVelocity.raw) + " ActualVelocity: " + str(objActualVelocity.raw))
    time.sleep(0.1)

time.sleep(1)

" set target velocity to zero"
objTargetVelocity.raw = 0

while not velocityReached():
    print("TargetVelocity: " + str(objTargetVelocity.raw) + " ActualVelocity: " + str(objActualVelocity.raw))
    time.sleep(0.1)

network.close()
print("Ready.")
