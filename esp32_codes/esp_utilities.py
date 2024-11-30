from network import WLAN, STA_IF

def connect_wifi(ssid, password):
    wlan = WLAN(STA_IF)
    wlan.active(True)
    print('connecting to ' + ssid)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('.', end='')
        utime.sleep(1)
    print('IP address', wlan.ifconfig()[0])