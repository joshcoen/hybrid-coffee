import glob
import grovepi
import time
import math
from influxdb import InfluxDBClient
client = InfluxDBClient(host='192.168.100.154')

temp_sensor1 = '/sys/bus/w1/devices/28-01204fe74e92/w1_slave'
temp_sensor_id = '28-01204fe74e92'
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
        client.write([temp], {'db': 'hybrid-coffee'}, 204, 'line')


def get_ambient():
    try:
        sensor_id = '76-014897f0912f'
        [temp,humidity] = grovepi.dht(sensor,blue)
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            temp=temp*1.8+32
            ambient_temp = 'coffee_info,location_id=3445,sensor_type=ambient_temperature,sensor_id=%s sensor_value=%d' % (sensor_id, temp)
            ambient_humidity = 'coffee_info,location_id=3445,sensor_type=humidity,sensor_id=%s sensor_value=%d' % (sensor_id, humidity)
            client.write([ambient_temp], {'db': 'hybrid-coffee'}, 204, 'line')
            client.write([ambient_humidity], {'db': 'hybrid-coffee'}, 204, 'line')
    except IOError:
        print ("Error")

#def get_weight():


while True:
    read_temp()
    get_ambient()
    #get_weight()
    time.sleep(1)
