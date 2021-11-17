import glob
import time


sensor1 = '/sys/bus/w1/devices/28-01204fe74e92/w1_slave'
sensor2 = '/sys/bus/w1/devices/28-01204fee0355/w1_slave'
sensor3 = '/sys/bus/w1/devices/28-012050011f8c/w1_slave'
sensor_ids = ['28-01204fe74e92', '28-01204fee0355', '28-012050011f8c']
print(sensor_ids[0])
print(sensor_ids[1])
print(sensor_ids[2])

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
    lines = read_temp_raw()
    for line in lines:
        senseid = 0
        sensor = sensor_ids[senseid]
        print(sensor)
        senseid += 1
        print(senseid)
        equals_pos = line[1].find('t=')
        if equals_pos != -1:
            temp_string = line[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return sensor, temp_f

while True:
    print(read_temp())
    time.sleep(1)