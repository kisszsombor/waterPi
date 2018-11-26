def getSoilMoisture():
    from ReadSnsr import readSensor
    
    # Parameters
    # Sensor values
    #    Air 22646
    #    Hand 13900
    #    Dry Soil tbd
    #    In Water 11886
    valSoilFullDry_P = 22646
    valSoilFullWet_P = 11886
    valAdc = readSensor()
    
    if valAdc >= valSoilFullDry_P:
        pctSoilMoisture = 0
    elif valAdc <= valSoilFullWet_P:
        pctSoilMoisture = 100
    else:
        # Soil is somewhat wet, calculate percentage
        # Calculate range where the percentage value is calculated
        valAnalogRange = valSoilFullDry_P- valSoilFullWet_P
        # Transpond interval to start with zero and calculate percentage
        valADCAdj = valAdc - valSoilFullWet_P
        # Calculate percentage with inverting it because high ADC value means dry, which is low percentage)
        pctSoilMoisture = 100 - ((valADCAdj * 100) / valAnalogRange)
    
    #print ('{0}: Sensor ADC raw value: {1}'.format(getSoilMoisture.__name__, valAdc))
    return pctSoilMoisture