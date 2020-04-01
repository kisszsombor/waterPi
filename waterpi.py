# -*- coding: utf-8 -*-
"""
DOCSTRING: This is the main file. of the WaterPi project
INPUT: no input
OUTPUT: no output
"""
# general imports
import time, datetime, logging

# Global Parameters
GV_TiMinBetwWaterings_Minutes_P = 640 # [min] Minimum elapsed time between 2 waterings
GV_TiMinBetwWaterings_P         = GV_TiMinBetwWaterings_Minutes_P * 60 \
                                     # [s] Minimum elapsed time between 2 waterings
GV_PctSoilMoistLoThd_P          = 75 # [%] Soil moisture lower threshold to start watering
GV_PctSoilMoistHiThd_P          = 85 # [%] Soil moisture upper threshold to finish watering
GV_TiIntrvlToWateringCheck_P    = 60 # Time interval [s] to check if watering is necessary
GV_TiDurPumpActv_P              = 15 # [s] Duration of activating the pump when watering
GV_NrAvgRng                     = 50 # Running average factor (number of samples)

# old params
#GV_StSumpWaterLevelMonitoringEnad_P   = 0   # [bool] Enable or diasble monitoring the water level in the pump sump
#GV_StPotWaterLevelMonitoringEnad_P    = 0   # [bool] Enable or diasble monitoring the water level in the flower pot

# Global variables
GV_PctSoilMoistureAvg = GV_PctSoilMoistLoThd_P
GV_PctSoilMoistureAvg_Y = [GV_PctSoilMoistLoThd_P]*GV_NrAvgRng

def main():
    # main code

    ################################################################################################
    # create logger for WateringPi application
    loggerWaterPiApp = logging.getLogger('WaterPiApp')
    loggerWaterPiApp.setLevel(logging.DEBUG) # log all escalated at and above DEBUG
    # add a file handler
    fh_loggerWaterPiApp = logging.FileHandler('/home/pi/project/waterpi/log/WaterPiMainLog.txt')
    fh_loggerWaterPiApp.setLevel(logging.DEBUG) # ensure all messages are logged to file
    # create a formatter and set the formatter for the handler.
    #formatter = logging.Formatter('%(asctime)s,%(name)s,%(levelname)s,%(message)s')
    formatter = logging.Formatter('%(asctime)s,%(name)s,%(levelname)s,%(message)s')
    fh_loggerWaterPiApp.setFormatter(formatter)
    # add the Handler to the logger
    loggerWaterPiApp.addHandler(fh_loggerWaterPiApp)
    ################################################################################################
    
    ################################################################################################
    # create logger for WateringPi data aquisition
    loggerWaterPiData = logging.getLogger('WaterPiData')
    loggerWaterPiData.setLevel(logging.INFO) # log all escalated at and above DEBUG
    # add a file handler
    from datetime import datetime
    #fh_loggerWaterPiData = logging.FileHandler('/home/pi/project/waterpi/log/WaterPiData_{:%Y-%m-%d}.log'.format(datetime.now()))
    fh_loggerWaterPiData = logging.FileHandler('/home/pi/project/waterpi/log/WaterPiDataLog.csv')
    fh_loggerWaterPiData.setLevel(logging.INFO) # ensure all messages are logged to file
    # create a formatter and set the formatter for the handler.
    formatter = logging.Formatter('%(asctime)s,%(name)s,%(levelname)s,%(message)s',\
                                  datefmt="%Y-%m-%d,%H:%M:%S")
    fh_loggerWaterPiData.setFormatter(formatter)
    # add the Handler to the logger
    loggerWaterPiData.addHandler(fh_loggerWaterPiData)
    ################################################################################################
    
    loggerWaterPiApp.info('WaterPi Application staring')
    
    # make sure the code starts with watering immediately 
    tiSinceLastWatering = GV_TiMinBetwWaterings_P - (GV_TiIntrvlToWateringCheck_P*2)
    stWateringInProgress = 0
    
    # main loop
    while True:
        
        # waiting until checking for watering need
        #print('main: sleep for {0} s'.format(GV_TiIntrvlToWateringCheck_P))
        time.sleep(GV_TiIntrvlToWateringCheck_P)
        
        # count up elapsed time
        tiSinceLastWatering += GV_TiIntrvlToWateringCheck_P
        #print('main: Time since last watering: {0}s/{1}s'.format(tiSinceLastWatering,GV_TiMinBetwWaterings_P))
        
        # checking need for watering
        from checkForWatering import checkForWatering
        stWateringReq, stWateringInProgressRet = checkForWatering(tiSinceLastWatering, stWateringInProgress)
        
        # update watering in progress flag
        stWateringInProgress = stWateringInProgressRet
        #print('main: stWateringInProgress: {0}'.format(stWateringInProgress))
        
        if stWateringReq:
               # start pumping
               from PumpWater import pumpWater
               pumpWater()
               
               # reset counter: time since last watering
               tiSinceLastWatering = 0

if __name__ == '__main__':
    main()