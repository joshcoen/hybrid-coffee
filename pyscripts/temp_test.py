import glob
import time
from influxdb import InfluxDBClient
client = InfluxDBClient(host='192.168.100.157')

sensor1 = '/sys/bus/w1/devices/28-01204fe74e92/w1_slave'
sensor2 = '/sys/bus/w1/devices/28-01204fee0355/w1_slave'
sensor3 = '/sys/bus/w1/devices/28-012050011f8c/w1_slave'
sensor_ids = ['28-01204fe74e92', '28-01204fee0355', '28-012050011f8c']
# print(sensor_ids[0])
# print(sensor_ids[1])
# print(sensor_ids[2])

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
    sensordata = []
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
            sensordata += current_sensor, temp_f
    print(sensordata)
    return sensordata

while True:
    sensors = []
    sensors = read_temp()
    sensorType = 'temperatureProbe'
    pos = 0
    for sensor in sensors:
        print(sensor)
        # line = 'coffee_info,sensorId=%s,sensorType=%s temperature=%s' % (sensor[pos], sensorType, sensor[pos+1])
        # client.write([line], {'db': 'hybrid-coffee'}, 204, 'line')
        print(line)
        pos += 1
        # print(sensor)
        time.sleep(1)