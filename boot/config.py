#
# This will configure the wifi and webrepl on an otherwise
# clean ESP8266 board.  It is run via ampy:
# ampy --port /dev/ttyUSB0 run config.py
#
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(essid,password)
wlan_ap = network.WLAN(network.AP_IF)
wlan_ap.active(False)

f = open("webrepl_cfg.py", "w")
f.write("PASS='abcd'")
f.close()
