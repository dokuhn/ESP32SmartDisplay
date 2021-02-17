import network
import webrepl

import network_cfg


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(network_cfg.SSID, network_cfg.PASS)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


do_connect()

webrepl.start()