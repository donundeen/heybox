import network 
from machine import Pin
from mqtt import MQTTClient 
import machine 
import time 
import ubinascii

ssid = "Hot Fuzz"
wifipw = "nanobot706"

mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()

print ("mac is " + mac)

# 60:01:94:1f:1b:f4 Black
# 60:01:94:25:8f:a9 Red

pin = Pin(16, Pin.OUT)
button = Pin(2, Pin.IN)
pin.value(1)
time.sleep(1)
pin.value(0)
time.sleep(1)
pin.value(1)
time.sleep(1)
pin.value(0)

prevvalue = 1
lizfeed = "heybox-toliz"
donfeed = "heybox-todon"

pubfeed = ""
subfeed = ""

if(mac == "60:01:94:1f:1b:f4"):
  #black button, don's
  pubfeed = "heybox-toliz"
  subfeed = "heybox-todon"
  devid = "dons"

if(mac == "60:01:94:25:8f:a9"):
  #red button, liz's 
  pubfeed = "heybox-todon"
  subfeed = "heybox-toliz"
  devid = "lizs"




def sub_cb(topic, msg): 
   print("got message")
   print(topic) 
   print(msg)
   if(msg == b"ON"):
      pin.value(1)
   if(msg == b"OFF"):
      pin.value(0) 
 
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid,wifipw)

while not station.isconnected():  
    print("not connected")
    print(wifipw)
    print(ssid)
    time.sleep(1)
    machine.idle() 

print("Connected to Wifi\n") 

pin.value(1)
time.sleep(1)
pin.value(0)
time.sleep(1)
pin.value(1)
time.sleep(1)
pin.value(0)


 
client = MQTTClient("heybox_donASDFQWER134l"+devid, "io.adafruit.com",user="donundeen", password="b20aea6d2bdc41beba537705083e094b", port=1883) 
client.set_callback(sub_cb) 
client.connect()
client.subscribe(topic="donundeen/feeds/"+subfeed) 
client.publish(topic="donundeen/feeds/" +pubfeed, msg="OFF")
pin.value(0) 

i = 0

while True: 
    i = i + 1
    if(i % 500 == 0):
       client.ping()
       i = 1
    client.check_msg() 
    buttonval = button.value()
    if(prevvalue != buttonval and buttonval == 0):
       print("on")
       client.publish(topic="donundeen/feeds/"+pubfeed, msg="ON")
    if(prevvalue != buttonval and buttonval == 1):
       client.publish(topic="donundeen/feeds/"+pubfeed, msg="OFF")
       print("off")
    prevvalue = buttonval

    if not station.isconnected():
       station.connect(ssid,wifipw)
       while not station.isconnected():  
          print("not connected")
          time.sleep(1)
          machine.idle()        
    machine.idle()

