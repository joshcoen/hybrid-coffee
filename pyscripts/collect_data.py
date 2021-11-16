import grovepi
import math
# Connect the Grove Temperature & Humidity Sensor Pro to digital port D4
# This example uses the blue colored sensor.
# SIG,NC,VCC,GND
sensor = 4  # The Sensor goes on digital port 4.

# temp_humidity_sensor_type
# Grove Base Kit comes with the blue sensor.
blue = 0    # The Blue col

from influxdb import InfluxDBClient
client = InfluxDBClient(host='localhost')
line = 'coffee_info,sensorId="28-01204fee0355",sensorType="tempProbe" temperature=82.40'
client.write([line], {'db': 'hybrid-coffee'}, 204, 'line')
client.close

