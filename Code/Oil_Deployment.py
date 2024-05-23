# import necessary libraries
import tsl2591
from machine import Pin, I2C
from neopixel import NeoPixel as np
import urtc
from time import sleep
from stats import mean, standard_deviation, coefficient_of_variation

# create LED pin
led = Pin(14, Pin.OUT)

# assign pins for the clock and the light sensor
i2c = I2C(scl=Pin(5), sda=Pin(4))
rtc = urtc.DS3231(i2c)
sensor = tsl2591.TSL2591(i2c)
led = np(Pin(15), 1)


# neopixel info
#np = neopixel.NeoPixel(Pin(1),  1)

threshold = 0.0

def read_sample(z):
    
    # open a data file
    datafile = open("test_light.csv","a")
    
    # turn on the LED
    led[0] = (255, 255, 255)
    led.write()
    sleep(1)
    
    # create empty list of data
    data = []
    
    # take a series of measurements
    for i in range(5):
        
        # get the current time and save it
        d = rtc.datetime()
        date = str(d.year) + "/" + str(d.month) + "/" + str(d.day) + " " + str(d.hour) + ":" + str(d.minute) + ":" + str(d.second)
        
        # take a light reading
        lux = sensor.read()
        data.append(lux)
        
        raw_BB, raw_IR = sensor.get_full_luminosity()
        #print(date, lux, raw_BB, raw_IR)
        
        # write to the data file
        datafile.write(str(str(z) + ',' + str(str(date) + ',' + str(lux) + ',' + str(raw_BB) + ',' + str(raw_IR) + '\n')))
        #sleep(3)
        
    # print the full data array
    print(data)
    
    # calculate stats
    average = mean(data)
    print("mean:", average)
    
    sd_base = standard_deviation(data)
    print("standard deviation:", sd_base)

    # close the data file
    datafile.close()
    
    # turn off the LED
    led[0] = (0,0,0)
    led.write()


