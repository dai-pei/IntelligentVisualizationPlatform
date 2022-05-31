# import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
 
HOST = "test.ranye-iot.net"
PORT = 1883

if __name__ == '__main__':
    client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    # client = mqtt.Client(client_id)    # ClientId不能重复，所以使用当前时间
    # client.username_pw_set("admin", "123456")  # 必须设置，否则会返回「Connected with result code 4」
    # client.on_connect = on_connect
    # client.on_message = on_message
    # client.connect(HOST, PORT, 60)
    # client.publish("test", "你好 MQTT", qos=0, retain=False)  # 发布消息
 
    publish.single("test", "msg", qos = 1,hostname=HOST,port=PORT, client_id=client_id)