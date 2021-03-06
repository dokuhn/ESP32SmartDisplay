# @author Dominik Kuhn
# @mail dominik.kuhn90@googlemail.com
# @create date 2021-02-16 17:05:40
# @modify date 2021-05-11 10:55:23
# @desc [description]


import time
import sys

from umqtt.simple import MQTTClient
from machine import Pin
from neopixel import NeoPixel
import ujson
import uio


import libGFX


rows = 10
cols = 10
n = (rows * cols)                # set the number of pixels in your strip

pin = Pin(0, Pin.OUT)            # set GPIO0 to output to drive NeoPixels
np = NeoPixel(pin, n)            # create NeoPixel driver on pin for n pixels



def sub_cb(topic, msg):
    """Received messages from subscriptions will be delivered to this callback."""
    try:

        if(msg is not None):
            img = ujson.loads(msg)       # parse the given message stream, interpreting it as a JSON string and deserialising the data to a Python object

            if (img is not None) and (img["height"] <= cols) and (img["width"] <= rows):
                for i in range(n):
                    pixel = [(img["data"][i][0] >> 1), (img["data"][i][1] >> 1), (img["data"][i][2] >>  1)]
                    np[i] = pixel       # set every pixels to the colour of the imagepixels in the JSON object

            np.write()          # write data to all pixels

            print(topic + '\t' +  ujson.dumps(msg))

    except ValueError as e:

        buf = uio.StringIO()
        sys.print_exception(e, buf)
        print("JSON string is not correctly formed")


def main(server="dompfaf"):

    c = MQTTClient("umqtt_client", server)      # instantiate an MQTTClient object
    c.set_callback(sub_cb)                      # subscribed messages will be delivered to this callback
    c.connect()
    c.subscribe(b"image")
     
    x = libGFX.gfx(np, rows, cols)

    while(True):

        x.drawChar('A', (16, 0, 0))

        time.sleep(1)

        x.clearScreen()

        x.drawChar('i', (16, 0, 0))

        time.sleep(1)

        x.clearScreen()

        x.drawChar('l', (16, 0, 0))

        time.sleep(1)

        x.clearScreen()

        x.drawChar('e', (16, 0, 0))

        time.sleep(1)

        x.clearScreen()

        x.drawChar('e', (16, 0, 0))

        time.sleep(1)

        x.clearScreen()

        x.drawChar('n', (16, 0, 0))

        time.sleep(1)

        x.clearScreen()

        x.writeLine(1, 1, 8, 5, (16, 0, 0))

        time.sleep(2)

        x.clearScreen()

        x.writeRect(2, 3, 4, 5, (16, 0, 0))

        time.sleep(2)

        x.clearScreen()

        x.writeFillRect(2, 3, 4, 5, (16, 0, 0))

        time.sleep(2)

        x.clearScreen()


        x.writeCircle(4, 4, 3, (16, 0, 0))

        time.sleep(2)

        x.clearScreen()

        x.writeCircleHelper(4, 4, 3, 0x4, (16, 0, 0))

        time.sleep(2)

        x.clearScreen()

        x.writefillRoundRect(2, 3, 4, 5, 1, (16, 0, 0))

        time.sleep(2)

        x.clearScreen()


        x.writeTriangle(5, 0, 8, 8, 1, 8, (16, 0, 0))

        time.sleep(2)

        x.clearScreen()

        x.drawfillTriangle(4, 1, 7, 7, 1, 7, (16, 0, 0))

        np.write()

        time.sleep(2)

        x.clearScreen()



    while(True):
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
