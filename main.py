import time
import sys

from umqtt.simple import MQTTClient
from machine import Pin
from neopixel import NeoPixel
import ujson
import uio


rows = 10
cols = 10
n = (rows * cols)                # set the number of pixels in your strip

pin = Pin(0, Pin.OUT)            # set GPIO0 to output to drive NeoPixels
np = NeoPixel(pin, n)            # create NeoPixel driver on GPIO0 for n pixels

# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):

    try:

        if( msg is not None ):
            img = ujson.loads(msg)

            if (img is not None) and (img["height"] <= cols) and (img["width"] <= rows):
                for i in range(n):
                    pixel = [ (img["data"][i][0] >> 1), (img["data"][i][1] >> 1), (img["data"][i][2] >>  1) ]
                    np[i] = pixel

            np.write()

            print( topic + '\t' +  ujson.dumps(msg) )

    except ValueError as e:

        buf = uio.StringIO()
        sys.print_exception(e, buf)
        print("JSON string is not correctly formed")


def main(server="dompfaf"):

    c = MQTTClient("umqtt_client", server)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(b"image")

    while True:
        if True:
            # Blocking wait for message
            c.wait_msg()
        else:
            # Non-blocking wait for message
            c.check_msg()
            # Then need to sleep to avoid 100% CPU usage (in a real
            # app other useful actions would be performed instead)
            time.sleep(1)

    c.disconnect()


if __name__ == "__main__":
    main()
