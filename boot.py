import network
import webrepl

import network_cfg


def do_connect():
    sta_if = network.WLAN(network.STA_IF)                       # create station interface
    if not sta_if.isconnected():                                # check if the station is connected to an AP
        print('connecting to network...')
        sta_if.active(True)                                     # activate the interface
        sta_if.connect(network_cfg.SSID, network_cfg.PASS)      # connect to an AP
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())                 # get the interface's IP/netmask/gw/DNS addresses and print them to the console



do_connect()

webrepl.start()
