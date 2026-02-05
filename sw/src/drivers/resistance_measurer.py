from machine import Pin, ADC
r1 = 100
resistor = 4700
r2 = 1000
r3 = 10000
r4 = 100000
adc = ADC(Pin(26))
def measure_resistance():
    adc_value = adc.read_u16()
    #assuming 3.3 V is max adc output of 65535
    if adc_value > 500 and adc_value < 2000:
        #true value is 1365
        resistance = r1
    elif adc_value > 7000 and adc_value < 15000:
        #true value is 11497
        resistance = r2
    elif adc_value > 35000 and adc_value < 50000:
        #true value is 44582
        resistance = r3
    elif adc_value > 57000 and adc_value < 65535:
        #true value is 62593
        resistance = r4
    else:
        resistance = 0 # no reel detected/ outside threshold values
    return resistance



