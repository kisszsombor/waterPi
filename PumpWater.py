# -*- coding: utf-8 -*-
"""
DOCSTRING: WaterPi project: pump control
INPUT: no input
OUTPUT: no output
"""
def pumpWater():
    # imports
    import RPi.GPIO as GPIO
    import time, logging
    from waterpi import GV_TiDurPumpActv_P
    
    # set up logger
    moduleLogger = logging.getLogger('WaterPiApp.PumpWater')
    
    # set up GPIO using BCM numbering
    GPIO.setmode(GPIO.BCM)
    
    # set pump pin to output
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
     
    # activate the pump
    print('PmpWater: pump on')
    moduleLogger.info('Start pumping water')
    GPIO.output(17,False)
    GPIO.output(27,False)
    
    # keep pump active
    time.sleep(GV_TiDurPumpActv_P)
    
    # turn off the pump
    #print('PmpWater: pump off')
    GPIO.output(17,True)
    GPIO.output(27,True)
    
    #cleanup
    GPIO.cleanup()