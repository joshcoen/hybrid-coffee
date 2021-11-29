import glob
import grovepi
import time
import math
import sys
from influxdb import InfluxDBClient
client = InfluxDBClient(host='54.186.121.136')

temp_sensor1 = '/sys/bus/w1/devices/28-01204fe74e92/w1_slave'
temp_sensor_id = 'tps02'
sensor = 4
blue = 0


def read_temp_raw():
    f = open(temp_sensor1, 'r')
    sensor1_lines = f.readlines()
    f.close()
    return sensor1_lines


def read_temp():
    sensor_type = 'temperature'
    lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        # return temp_sensor_id, temp_f
        temp = 'coffee_info,location_id=3445,sensor_type=%s,sensor_id=%s sensor_value=%s' % (sensor_type, temp_sensor_id, temp_f)
        # print(temp)
        client.write([temp], {'db': 'coffee_events'}, 204, 'line')


def get_ambient():
    try:
        sensor_id_amb = 'trs01'
        sensor_id_hum = 'hs04'
        [temp,humidity] = grovepi.dht(sensor,blue)
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            temp=temp*1.8+32
            ambient_temp = 'coffee_info,location_id=3445,sensor_type=temperature,sensor_id=%s sensor_value=%d' % (sensor_id_amb, temp)
            ambient_humidity = 'coffee_info,location_id=3445,sensor_type=humidity,sensor_id=%s sensor_value=%d' % (sensor_id_hum, humidity)
            client.write([ambient_temp], {'db': 'coffee_events'}, 204, 'line')
            client.write([ambient_humidity], {'db': 'coffee_events'}, 204, 'line')
    except IOError:
        print ("Error")


def set_tare():
    EMULATE_HX711 = False

    referenceUnit = 479.5

    if not EMULATE_HX711:
        import RPi.GPIO as GPIO
        from hx711py.hx711 import HX711
    else:
        from hx711py.emulated_hx711 import HX711

    hx = HX711(23, 24)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(referenceUnit)
    hx.reset()
    hx.tare()
    # print("Tare done! Add weight now...")


def get_weight():
    EMULATE_HX711 = False
    referenceUnit = 479.5
    if not EMULATE_HX711:
        import RPi.GPIO as GPIO
        from hx711py.hx711 import HX711
    else:
        from hx711py.emulated_hx711 import HX711
    hx = HX711(23, 24)
    hx.set_reading_format("MSB", "MSB")
    # hx.set_reference_unit(referenceUnit)
    # hx.reset()

    def cleanAndExit():
        print("Cleaning...")

        if not EMULATE_HX711:
            GPIO.cleanup()

        print("Bye!")
        sys.exit()

    try:
        sensor_type = 'weight'
        weight_sensor_id = 'ws03'
        weight_val = max(0, int(hx.get_weight(5)))
        weight = 'coffee_info,location_id=3445,sensor_type=%s,sensor_id=%s sensor_value=%s' % (sensor_type, weight_sensor_id, weight_val)
        # client.write([weight], {'db': 'hybrid-coffee'}, 204, 'line')
        print(weight)
        hx.power_down()
        hx.power_up()
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


print("starting tare")
set_tare()
while True:
    #read_temp()
    #get_ambient()
    get_weight()
    # time.sleep(1)
