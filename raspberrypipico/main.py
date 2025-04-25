import machine
import secrets
import network
import time
import ussl
from umqtt.simple import MQTTClient

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
led = machine.Pin("LED", machine.Pin.OUT)
led.on()
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print("Wifi connecting...")
wlan.connect(secrets.SSID, secrets.PASSWORD)
max_wait = 10
while max_wait > 0:
 if wlan.status() < 0 or wlan.status() >= 3:
  break
  max_wait -= 1
  print('waiting for connection...')
  time.sleep(1)
print(wlan.ifconfig())

with open("client2.key", 'rb') as f:
    key = f.read()
with open("client2.crt", 'rb') as f:
    cert = f.read()
ssl_params = dict()
#ssl_params["cert"] = cert
#ssl_params["key"] = key
#ssl_params["cert_reqs"] = ussl.CERT_OPTIONAL
#ssl_params["server_hostname"] = "192.168.1.198"
CLIENTID_DEVICEID = "device02"
led.off()
#MQTTSERVER = "192.168.174.56"
MQTTSERVER = "192.168.1.189"
USERNAME = ""
PASSWORD = ""
#c = MQTTClient(CLIENTID_DEVICEID,MQTTSERVER,user=USERNAME,password=PASSWORD,ssl=True,ssl_params=ssl_params)
print("MQTT connecting...")
led.on()
c = MQTTClient(CLIENTID_DEVICEID,MQTTSERVER,user=USERNAME,password=PASSWORD,port=8883,ssl=False,keepalive=90)

c.connect()
led.on()

counter = 0
while True:
    led.on()
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = 27 - (reading - 0.706)/0.001721
    c.publish(b"device02", f"{{\"temperature\": {temperature} }}".encode())
    counter+=1
    print(f"{counter} - {temperature}")
    led.off()
    time.sleep(2)
    
c.disconnect()


