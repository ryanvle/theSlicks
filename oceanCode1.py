import tsl2591 #import library for light sensor
from machine import Pin, I2C #import functions from machine library
import neopixel
import urtc
from time import sleep

# assign pins for the clock and the light sensor
i2c = I2C(scl=Pin(5), sda=Pin(4))
np = neopixel.NeoPixel(machine.Pin(1),  1)
rtc = urtc.DS3231(i2c)
sensor = tsl2591.TSL2591(i2c)

rtc.datetime() #prints the current date/time
led = Pin(14, Pin.OUT)

threshold = 0.0


def mean(data):
    return sum(data) / len(data)    

def variance(data):
    mu = mean(data)
    return sum((x - mu) ** 2 for x in data) / len(data)

def standard_deviation(data):
    return variance(data) ** 0.5   

def coefficient_of_variation(data):
    mu = mean(data)
    sigma = standard_deviation(data)
    if mu != 0:
        cv = (sigma / mu) * 100
    else:
        cv = 0
        return cv  

# create the function
def baseline(z):
    datafile = open("final_housingTest.csv","a")
    led.value(1)
    sleep(1)
    data = []
    
    for i in range(5):
        d = rtc.datetime()
        date = str(d.year) + "/" + str(d.month) + "/" + str(d.day) + " " + str(d.hour) + ":" + str(d.minute) + ":" + str(d.second)
        lux = sensor.read()
        data.append(lux)
        print(sensor.get_full_luminosity())
        print(date, z, lux)
        datafile.write(str("debugging pt2 " + str(date) + ', ' + str(z) + ', lux: ' + str(lux) + '\n'))
        sleep(3)
        #making sure it actually adds to the array
        print(data)
    
    average = mean(data)
    sd_base = standard_deviation(data)

    threshold = average + (2*sd_base)
    #cv = coefficient_of_variation(data)
    #print("Coefficient of Variation:", cv)


    #store in csv
    #datafile.write('Coefficient of Variation: ' + str(cv))

    datafile.close()
    led.value(0)


def experimental(z):
    datafile = open("final_housingTest.csv","a")
    led.value(1)
    sleep(1)
    counter = 0
    data = []
    
    for i in range(5):
        d = rtc.datetime()
        date = str(d.year) + "/" + str(d.month) + "/" + str(d.day) + " " + str(d.hour) + ":" + str(d.minute) + ":" + str(d.second)
        lux = sensor.read()
        data.append(lux)
        print(sensor.get_full_luminosity())
        print(date, z, lux)
        datafile.write(str("debugging pt2 " + str(date) + ', ' + str(z) + ', lux: ' + str(lux) + '\n'))
        sleep(3)
        #making sure it actually adds to the array
        print(data)
    
    average = mean(data)
    sd_experimental = standard_deviation(data)

    for i in enumerate(data):
        if data[i] > threshold:
            counter += 1
        

    #cv = coefficient_of_variation(data)
    #print("Coefficient of Variation:", cv)


    #store in csv
    #datafile.write('Coefficient of Variation: ' + str(cv))

    datafile.close()
    led.value(0)



