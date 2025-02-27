import paho.mqtt.client as mqtt
from random import choice, uniform
import time

client = mqtt.Client()
client.connect("192.168.0.2", 1883, 60)

test_objects = [
    ("tele/tasmota_6666666/STATE", f'{{"Time":"1970-01-26T16:15:45","Uptime":"25T16:15:13","UptimeSec":{int(uniform(2200000, 2250000))},"Heap":{int(uniform(0, 100))},"SleepMode":"Dynamic","Sleep":50,"LoadAvg":{int(uniform(0, 100))},"MqttCount":2,"POWER":"{choice(["OFF", "ON"])}","Dimmer":{int(uniform(0, 100))},"Color":{int(uniform(6000, 6500))},"Speed":1,"LedTable":"{choice(["OFF", "ON"])}","Wifi":{{"AP":1,"SSId":"Anonymous","Channel":6,"Mode":"11n","RSSI":{int(uniform(0, 100))},"Signal":{int(uniform(-100, 0))},"LinkCount":1,"Downtime":"0T00:00:07"}}}}'),
    ("tele/tasmota_3434334/STATE", f'{{"Time":"1970-01-01T05:40:09","Uptime":"0T05:40:11","UptimeSec":{int(uniform(22000, 22500))},"Vcc":{uniform(3, 5)},"Heap":{int(uniform(0, 100))},"SleepMode":"Dynamic","Sleep":10,"LoadAvg":{int(uniform(0, 100))},"MqttCount":1,"POWER":"{choice(["OFF", "ON"])}","Dimmer":{int(uniform(0, 100))},"Fade":"{choice(["OFF", "ON"])}","Speed":1,"LedTable":"{choice(["OFF", "ON"])}","Wifi":{{"AP":1,"SSId":"Anonymous","Channel":6,"Mode":"11n","RSSI":{int(uniform(0, 100))},"Signal":{int(uniform(-100, 0))},"LinkCount":1,"Downtime":"0T00:00:03"}}}}'),
    ("tele/tasmota_ABCDEFG/STATE", f'{{"Time":"1970-01-01T04:50:09","Uptime":"0T04:50:11","UptimeSec":17411,"Vcc":{uniform(3, 5)},"Heap":{int(uniform(0, 100))},"SleepMode":"Dynamic","Sleep":10,"LoadAvg":{int(uniform(0, 100))},"MqttCount":1,"POWER":"{choice(["OFF", "ON"])}","Dimmer":{int(uniform(0, 100))},"Color":"E5B4200000","HSBColor":"{int(uniform(0, 100))},{int(uniform(0, 100))},{int(uniform(0, 100))}","White":0,"CT":{int(uniform(100, 200))},"Channel":[{int(uniform(0, 100))},{int(uniform(0, 100))},{int(uniform(0, 100))},0,0],"Scheme":0,"Fade":"{choice(["OFF", "ON"])}","Speed":1,"LedTable":"{choice(["OFF", "ON"])}","Wifi":{{"AP":1,"SSId":"Anonymous","Channel":6,"Mode":"11n","RSSI":{int(uniform(0, 100))},"Signal":{int(uniform(-100, 0))},"LinkCount":1,"Downtime":"0T00:00:03"}}}}')
]

while True:
    # num = uniform(0, 100)
    # tp = choice([0, 1 , 2])
    # client.publish(f"test{tp}", str(num))
    # print("Posted " + str(num) + " to test" + str(tp))

    test_object = choice(test_objects)
    client.publish(test_object[0], test_object[1])
    print("Posted update to tele/tasmota_" + test_object[0])
    time.sleep(6)