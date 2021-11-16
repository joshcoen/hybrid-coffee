import grovepi
import math
from influxdb import InfluxDBClient

# temp_humidity_sensor_type
sensorId = '74-2366894'
sensorType = "ambientProbe"
sensor = 4
blue = 0
client = InfluxDBClient(host='192.168.100.157')
while True:
    try:
        [temp,humidity] = grovepi.dht(sensor,blue)
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            temp=temp*1.8+32
            #print("temp = %.02f F humidity =%.02f%%"%(temp, humidity))
            line = 'coffee_info,sensorId=%s,sensorType=%s temperature=%d,humidity=%d'%(sensorId, sensorType, temp, humidity)
            client.write([line], {'db': 'hybrid-coffee'}, 204, 'line')
    except IOError:
        print ("Error")



line = 'coffee_info,sensorId=28-01204fee0355,sensorType=ambientProbe temperature=82.40,humidity=60'
client.write([line], {'db': 'hybrid-coffee'}, 204, 'line')
client.close

