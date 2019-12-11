import time
import network
from ubinascii import hexlify
from umqtt.simple import MQTTClient
from machine import Pin

########### global variables ##############################

unique_ID = hexlify(network.WLAN().config('mac'))

def config  = {
    'mqtt_broker': '192.168.0.12',  # central server for our mqtt network
    'mqtt_client': unique_ID, # this device client ID
    'led_pin': 0,
    'button_pin': 13,
}

mq = MQTTClient(config.mqtt_client, config.mqtt_broker)
led = Pin(config.led_pin, Pin.OUT)
button = Pin(config.button_pin, Pin.IN, Pin.PULL_UP) 

######### turn LED on and off based on msg ##########################

def handle_msg(topic,msg):
	# for debugging
	print("topic: ", topic, " msg: ", msg)

    if msg == b'on':
        led.on()
    elif msg == b'off':
        led.off()


######## MQTT Client: starting and connecting ##########

# start the MQTT client for this microcontroller
mq.set_callback(handle_msg)
mq.connect()
mq.subscribe(b'led/#')

########## publishing an MQTT message ###############

# code for momentary switch behavior, toggle behavior is below
# Since this is in the top-level while True loop, it's the default behavior
last_button_value = True # not pressed

while True:
	button_value = button.value()

	if last_button_value == button_value:
		continue

	last_button_value = button_value

	if not button_value:
		print("pressed!!!!!")
		mq.publish(topic="led", msg="on")
	else:
		print("not pressed")
		mq.publish(topic="led", msg="off")

	time.sleep(0.1)

# below is the code for toggle behavior
# to use run mqtt.toggle() in the webrepl
def toggle():
	last_button_value = True # not pressed
	led_on = False # is the LED on?

	while True:
		button_value = button.value()
	
		if last_button_value == button_value:
			continue

		last_button_value = button_value
		
		if button_value:
			# button was released/unpressed
			print("button was released")
			continue
	
		led_on = not led_on
		print("pressed!!!!!")
		if led_on:
			mq.publish(topic="led", msg="on")
		else:
			mq.publish(topic="led", msg="off")
	
		time.sleep(0.1)
