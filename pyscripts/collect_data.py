import glob
import grovepi
import time
import math
from influxdb import InfluxDBClient
client = InfluxDBClient(host='192.168.100.157')

sensor1 = '/sys/bus/w1/devices/28-01204fe74e92/w1_slave'
sensor2 = '/sys/bus/w1/devices/28-01204fee0355/w1_slave'
sensor3 = '/sys/bus/w1/devices/28-012050011f8c/w1_slave'
sensor_ids = ['28-01204fe74e92', '28-01204fee0355', '28-012050011f8c']
sensor = 4
blue = 0


def read_temp_raw():
    f = open(sensor1, 'r')
    sensor1_lines = f.readlines()
    f.close()

    f = open(sensor2, 'r')
    sensor2_lines = f.readlines()
    f.close()

    f = open(sensor3, 'r')
    sensor3_lines = f.readlines()
    f.close()
    return sensor1_lines, sensor2_lines, sensor3_lines


def read_temp():
    sensordata_list = []
    lines = read_temp_raw()
    senseid = 0
    for line in lines:
        current_sensor = sensor_ids[senseid]
        # print(current_sensor)
        senseid += 1
        # print(senseid)
        equals_pos = line[1].find('t=')
        if equals_pos != -1:
            temp_string = line[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            sensordata_list.append((current_sensor, temp_f))
    return sensordata_list


def get_ambient():
    try:
        sensortype = "ambientProbe"
        sensorid = '76-014897f0912f'
        [temp,humidity] = grovepi.dht(sensor,blue)
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            temp=temp*1.8+32
            ambient = 'coffee_info,sensor_id=%s,sensor_type=%s temperature=%d,humidity=%d' % (sensorid, sensortype, temp, humidity)
            client.write([ambient], {'db': 'hybrid-coffee'}, 204, 'line')
    except IOError:
        print ("Error")


while True:
    sensorType = 'temperatureProbe'
    for value, key in read_temp():
        temp = 'coffee_info,sensor_id=%s,sensor_type=%s temperature=%s' % (value, sensorType, key)
        client.write([temp], {'db': 'hybrid-coffee'}, 204, 'line')
        test = 'coffee_info1,sensor_id=%s,sensor_type=%s temperature=%s, time_precision=ms' % (value, sensorType, key)
        client.write_points([test])
        time.sleep(1)
    get_ambient()
