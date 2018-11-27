def getSoilMoisture():
    """
    DOCSTRING: reads current soil moisture from 2 analog moisture sensors Range: 0-100[%]
    INPUT: none
    OUTPUT: pctSoilMoistureAvg: average soil moisture [%]
            pctSoilMoistureSnsr1: measured soil moisture on sensor 1 [%]
            pctSoilMoistureSnsr2: measured soil moisture on sensor 2 [%]
    """
    from ReadSnsr import readSensor

    valAdc1, valAdc2 = readSensor()
    
    pctSoilMoistureSnsr1 = convRaw2Pct(valAdc1)
    pctSoilMoistureSnsr2 = convRaw2Pct(valAdc2)
    pctSoilMoistureAvg = (pctSoilMoistureSnsr1 + pctSoilMoistureSnsr2)/2
    
    #print ('{0}: Sensor ADC raw value: {1}'.format(getSoilMoisture.__name__, valAdcAvg))
    return pctSoilMoistureAvg, pctSoilMoistureSnsr1, pctSoilMoistureSnsr2

def convRaw2Pct(rawAcdMoisture):
    """
    DOCSTRING: convert raw 16 bit ADC value into soil moisture percentage
    INPUT: rawAcdMoisture: 16 bit ADC value
    OUTPUT: pctSoilMoisture: soil moisture 0-100% 
    """
    # Parameters
    # Sensor values
    #    Air 22646
    #    Hand 13900
    #    Dry Soil tbd
    #    In Water 11886
    valSoilFullDry_P = 22646
    valSoilFullWet_P = 11886
    
    if rawAcdMoisture >= valSoilFullDry_P:
        pctSoilMoisture = 0
        
    elif rawAcdMoisture <= valSoilFullWet_P:
        pctSoilMoisture = 100
        
    else:
        # Soil is somewhat wet, calculate percentage
        # Calculate range where the percentage value is calculated
        valAnalogRange = valSoilFullDry_P- valSoilFullWet_P
        # Transpond interval to start with zero and calculate percentage
        valADCAdj = rawAcdMoisture - valSoilFullWet_P
        # Calculate percentage with inverting it because high ADC value means dry, which is low percentage)
        pctSoilMoisture = 100 - ((valADCAdj * 100) / valAnalogRange)
    
    return pctSoilMoisture
    