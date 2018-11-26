def checkForWatering(tiSinceLastWatering, stWateringInProgress):
    """
    DOCSTRING: Function looks at elapsed time since last watering. If elapsed time is higher than \
    the threshold, it checks current soil moisture.
        If maximum moisture is not reached and the watering active flag is false, it returns true (situation after once reaching full moisture).
        If maximum moisture is not reached and the watering active flag is true, it returns true (situation, where watering until full moisture is reached).
        If measured moisture is below minimum moisture to start watering, it returns true.
    INPUT: GV_TiSinceLastWatering
    OUTPUT: reqWatering 
    """
    
    # imports
    import logging
    
    #import global variables
    from waterpi import GV_PctSoilMoistLoThd_P, GV_PctSoilMoistHiThd_P, GV_TiMinBetwWaterings_P
    
    #create logging instance
    dataLogger = logging.getLogger('WaterPiData.checkForWatering')
    
    #check for current soil moisture
    from GetSoilMoisture import getSoilMoisture
    pctSoilMoisture = getSoilMoisture()
    
    # calculate running average
    GV_PctSoilMoistureAvg = PctMoistAvg(pctSoilMoisture)
    
    print ('checkForWatering: Soil moisture avg GV: {0}%, thresholds: min {1}%, max {2}%'.format(GV_PctSoilMoistureAvg, \
        GV_PctSoilMoistLoThd_P, GV_PctSoilMoistHiThd_P))
        
    if GV_PctSoilMoistureAvg > GV_PctSoilMoistHiThd_P:
        # reset watering in progress flag when max moisture is reached
        stWateringInProgress = False
        
    if tiSinceLastWatering > GV_TiMinBetwWaterings_P:
        # enough time elapsed since last watering, decide if watering is necessary
        #print ('checkForWatering: Minimum elapsed time since last watering reached')
        
        if GV_PctSoilMoistureAvg < GV_PctSoilMoistLoThd_P:
            # Soil is dry as the desert
            
            # Set flag watering is in progress
            stWateringInProgress = True
            
            # Request watering
            reqWatering = True
            
        elif GV_PctSoilMoistureAvg < GV_PctSoilMoistHiThd_P and stWateringInProgress:
            # moisture did not reach max yet, watering is still in progress
            
            # continue watering until max moisture is reached
            reqWatering = True
            
        else:
            # no need for any watering
            
            # Reject watering due to sufficient soil moisture
            reqWatering = False
    else:
        # Reject watering because not enough time has elapsed
        reqWatering = False
        #print ('checkForWatering: Minimum elapsed time since last watering NOT reached')
    
    # Log data
    dataLogger.info('{0},{1},{2},{3},{4},{5}' \
                .format(tiSinceLastWatering, GV_TiMinBetwWaterings_P, stWateringInProgress, \
                GV_PctSoilMoistureAvg, GV_PctSoilMoistLoThd_P, GV_PctSoilMoistHiThd_P))
    
    return reqWatering, stWateringInProgress

def PctMoistAvg(pctSoilMoisture):
    """
    DOCSTRING: Rolling average calculation of the measured moisture
    INPUT: 
    OUTPUT: Rolling average of the measured moisture
    """
    # import global average
    from waterpi import GV_PctSoilMoistureAvg_Y, GV_PctSoilMoistureAvg
    
    # reset sum for average
    sumMoist = 0    

    # shift old values in the array
    for k in range(3,-1,-1):
        #print('k: {0}'.format(k))
        GV_PctSoilMoistureAvg_Y[k] = GV_PctSoilMoistureAvg_Y[k-1]

    # write latest value to the first position
    GV_PctSoilMoistureAvg_Y[0] = pctSoilMoisture
    #print('GV_PctSoilMoistureAvg_Y: {0}'.format(GV_PctSoilMoistureAvg_Y))
    
    # calculate average
    for k in range(4):
        sumMoist += GV_PctSoilMoistureAvg_Y[k-1]

    avgMoist = sumMoist / 4
    #print('avgMoist: {0}, sumMoist: {1}'.format(avgMoist,sumMoist))
    return avgMoist

    
    