import network
import time
import machine
from umqtt import MQTTClient

pin1=machine.Pin(12) # D6
servo1=machine.PWM(pin1,freq=50)
pin2=machine.Pin(13) # D7
servo2=machine.PWM(pin2,freq=50)
pin3=machine.Pin(15) # D8
servo3=machine.PWM(pin3,freq=50)

sta = network.WLAN(network.STA_IF)
sta.active(False)

ssid="scut_303"
pwd="scutb8303"

mqttHost="broker.emqx.io"
subTopic=b'testtopic'

def connectWifi():    
    global ssid,pwd

    sta.active(True)
    if sta.isconnected():
        return None

    print('Connect to %s' % ssid)
    sta.connect(ssid, pwd)
    
    for retry in range(100):
        connected = sta.isconnected()
        if connected:
            break
        print('.', end='')
        time.sleep(0.1)
    if connected:
        print('\nConnected : ', sta.ifconfig())
    else:
        print('\nFailed. Not Connected to: ' + ssid)
        return

    connectMQTT()
    return 

def connectMQTT():
    global mqttHost,subTopic
    client=MQTTClient("1", mqttHost,0)
    client.set_callback(mqttCallback)
    print("set_callback")

    conn_ret_code = client.connect()
    if conn_ret_code != 0:
        return
                    
    print('conn_ret_code = {0}'.format(conn_ret_code))
    
    client.subscribe(subTopic)
    print("Connected to %s, subscribed to %s " % (mqttHost, subTopic))
  
    while True:
            client.wait_msg()
            # else:
            #     # Non-blocking wait for message
            #     c.check_msg()
            #     # Then need to sleep to avoid 100% CPU usage (in a real
            #     # app other useful actions would be performed instead)
            #     time.sleep(1)


def mqttCallback(topic,msg):
    print('topic: {}'.format(topic))
    print('msg: {}'.format(msg))
    if topic==subTopic:
        if msg='xx'
        if msg==b'tom':
            # print("duty 20")
            servo1.duty(20)
            time.sleep(1)
            # print("duty 20 to 120")
            for i in range(20,120,5):
                servo1.duty(i)
                time.sleep_ms(50)
        elif msg==b'close':
            servo2.duty(20)
            time.sleep(1)
            for i in range(20,120,5):
                servo2.duty(i)
                time.sleep_ms(50)
        elif msg==b'open':
            servo3.duty(20)
            time.sleep(1)
            for i in range(20,120,5):
                servo3.duty(i)
                time.sleep_ms(50)

if __name__ == '__main__':
    connectWifi()