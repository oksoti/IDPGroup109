from machine import Pin, ADC

class ResistanceMeasurer:
    def __init__(self, pin_number):
        self.adc = ADC(Pin(pin_number))

    def measure_resistance(self):
        adc_value = self.adc.read_u16()
        print(adc_value)
        #assuming 3.3 V is max adc output of 65535
        if adc_value < 6000:
            #true value is 1365
            return 1
        elif adc_value < 25000:
            #true value is 11497
            return 2
        elif adc_value < 45000:
            #true value is 44582
            return 3
        else:
            #true value is 62593
            return 4
