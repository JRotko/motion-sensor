print("RUN: boot.py")

from config import wifi_config

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(wifi_config['ssid'], wifi_config['password'])
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

do_connect()

# TODO: set correct time zone
def setTime():
    import ntptime
    try:
        ntptime.settime()
        print("NTP query succesfull")
    except:
        ("NTP query failed")

setTime()
