from warnings import catch_warnings
def getSoilMoisture():
    """
    DOCSTRING: reads current soil moisture from 2 analog moisture sensors Range: 0-100[%]
    INPUT: none
    OUTPUT: pctSoilMoistureAvg: average soil moisture [%]
            pctSoilMoistureSnsr1: measured soil moisture on sensor 1 [%]
            pctSoilMoistureSnsr2: measured soil moisture on sensor 2 [%]
    """
    from ReadSnsr import readSensor

    valAdc0, valAdc1, valAdc2 = readSensor()
    
    tSoil = convRaw2T(valAdc0)
    pctSoilMoistureSnsr1 = convRaw2Pct(valAdc1)
    pctSoilMoistureSnsr2 = convRaw2Pct(valAdc2)
    pctSoilMoistureAvg = (pctSoilMoistureSnsr1 + pctSoilMoistureSnsr2)/2
    
    #print ('{0}: Sensor ADC raw value: {1}, {2}'.format(getSoilMoisture.__name__, valAdc1,valAdc2))
    return pctSoilMoistureAvg, pctSoilMoistureSnsr1, pctSoilMoistureSnsr2, tSoil

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
    valSoilFullDry_P = 17000
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
    
def convRaw2T(rawAdcTemp):
    """
    DOCSTRING: convert raw 16 bit ADC value into soil temperature
    INPUT: rawAcdTemp: 16 bit ADC value
    OUTPUT: tSoil: soil temperature 
    """
    # numpy for the look.up interpolation
    import numpy as np
    
    # Parameters
    # Sensor values
    #    Air 22646
    #    Hand 13900
    #    Dry Soil tbd
    #    In Water 11886
    r10k = 10100.0 # [ohm] NTC sensor resistance
    ADCmax = 26353.0 # measured adc value at 3.3 V

    rTSnsr = (r10k)/((ADCmax/rawAdcTemp)-1)
    #rTSnsr = int(rTSnsr)
    
    # define R-T look-up table for NTC 10k
    #R2T_X = [677,    915,    1256,    1753,    2490,    2989,    3605,    4372,    5330,    6535,    8059,    8447,    8835,    9224,    9612,    10000,    10498,    10995,    11493,    11990,    12488,    13130,    13772,    14414,    15056,    15698,    16533,    17368,    18202,    19037,    19872,    25339,    32554,    55046,    96358] # NTC R values [ohm]
    #R2T_Y = [100,    90,    80,    70,    60,    55,    50,    45,    40,    35,    30,    29,    28,    27,    26,    25,    24,    23,    22,    21,    20,    19,    18,    17,    16,    15,    14,    13,    12,    11,    10,    5,    0,    -10,    -20] # Temperature values [oC]
    
    #tSoil = np.interp(rTSnsr, R2T_X, R2T_Y)
    
    # calculate temperature using Steinhardt-Hart equation simplified B parameter only
    
    #defining Beta from https://www.ametherm.com/thermistor/ntc-thermistor-beta
    # R1 = 10000 T1 = 25 theoretical
    # R2 = 53439 T2 = -10 C fridge, proved by lidl idojarasallomas
    # Beta1 = 3756.93 --> in icebath show x C and in boiling water shows 87.5 C
    #
    # R1 = 27000    T1 = 0.01 C icebath
    # R2 = 1025.0    T2 = 100.0 C boiling water
    # Beta2 = 3334.6
    
    rThermistorNominal = 10000.0
    tThermistorNominal = 25.0
    ValCoeffBeta = 3334.6
    
    import math
    
    tSoilSteinhart = rTSnsr / rThermistorNominal     # (R/Ro)
    tSoilSteinhart = math.log(tSoilSteinhart)                  # ln(R/Ro)
    tSoilSteinhart /= ValCoeffBeta                   # 1/B * ln(R/Ro)
    tSoilSteinhart += 1.0 / (tThermistorNominal + 273.15) # + (1/To)
    tSoilSteinhart = 1.0 / tSoilSteinhart                 # Invert
    tSoilSteinhart -= 273.15                         # convert to C

    
    #print("T_ADC_Raw: {0}, R_Thermistor: {1:.1f} ohm, T_Stein: {2:.2f} C".format(rawAdcTemp,rTSnsr,tSoilSteinhart))
    
    return tSoilSteinhart