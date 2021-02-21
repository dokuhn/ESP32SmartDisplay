# ESP32SmartDisplay

ESP32SmartDrsplay is a [MircoPython](https://github.com/micropython) based project to control WS2812 LEDs over MQTT (wifi). 

To control the LEDs, the [NeonPixel](https://docs.micropython.org/en/latest/esp32/quickref.html#neopixel-driver) driver built in MicroPython is used. Image data are sent unencoded in JSON format over MQTT to the ESP32, which reads the individual pixel values and sets the LED colour equally.

## Instal MicroPython on ESP32

See the [Quick reference for the ESP32](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html#esp32-intro)

Install the esptool.py tool to copy across the firmware. You can find this tool here: https://github.com/espressif/esptool/, or install it using pip:

`pip install esptool`

And then deploy the new firmware using:

`esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20180511-v1.9.4.bin`



