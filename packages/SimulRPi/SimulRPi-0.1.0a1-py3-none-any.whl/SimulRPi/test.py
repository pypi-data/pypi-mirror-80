import sys


# combine_simulrpi.rst
def combine_simulrpi():
    import sys
    import time

    if len(sys.argv) > 1 and '-s' in sys.argv:
        import SimulRPi.GPIO as GPIO
        msg1 = "\nPress key 'cmd_r' to blink a LED"
        msg2 = "Key 'cmd_r' pressed!"
    else:
        import RPi.GPIO as GPIO
        msg1 = "\nPress button to blink a LED"
        msg2 = "Button pressed!"

    led_channel = 10
    button_channel = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led_channel, GPIO.OUT)
    GPIO.setup(button_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print(msg1)
    while True:
        try:
            if not GPIO.input(button_channel):
                print(msg2)
                start = time.time()
                while (time.time() - start) < 3:
                    GPIO.output(led_channel, GPIO.HIGH)
                    time.sleep(0.5)
                    GPIO.output(led_channel, GPIO.LOW)
                    time.sleep(0.5)
                break
        except KeyboardInterrupt:
            break
    GPIO.cleanup()


# display_problems.rst
def display_problems():
    import SimulRPi.GPIO as GPIO

    GPIO.setdefaultsymbols(
        {
            'ON': '\033[91m(0)\033[0m',
            'OFF': '(0)'
        }
    )
    led_channel = 11
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led_channel, GPIO.OUT)
    GPIO.output(led_channel, GPIO.HIGH)
    GPIO.cleanup()


# readme.rst
def readme(example):
    if example == 1:
        import SimulRPi.GPIO as GPIO

        led_channel = 10
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led_channel, GPIO.OUT)
        GPIO.output(led_channel, GPIO.HIGH)
        GPIO.cleanup()
    elif example == 2:
        import SimulRPi.GPIO as GPIO

        led_channels = [9, 10, 11]
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led_channels, GPIO.OUT)
        GPIO.output(led_channels, GPIO.HIGH)
        GPIO.cleanup()
    elif example == 3:
        import SimulRPi.GPIO as GPIO

        channel = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print("Press key 'cmd_r' to exit\n")
        while True:
            if not GPIO.input(channel):
                print("Key pressed!")
                break
        GPIO.cleanup()
    elif example == 4:
        import time
        import SimulRPi.GPIO as GPIO

        channel = 22
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.OUT)
        start = time.time()
        print("Ex 4: blink a LED for 4.0 seconds\n")
        while (time.time() - start) < 4:
            try:
                GPIO.output(channel, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(channel, GPIO.LOW)
                time.sleep(0.5)
            except KeyboardInterrupt:
                break
        GPIO.cleanup()
    elif example == 5:
        import time
        import SimulRPi.GPIO as GPIO

        led_channel = 10
        key_channel = 27
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led_channel, GPIO.OUT)
        GPIO.setup(key_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print("Press the key 'shift_r' to turn on light ...\n")
        while True:
            try:
                if not GPIO.input(key_channel):
                    print("The key 'shift_r' was pressed!")
                    start = time.time()
                    while (time.time() - start) < 3:
                        GPIO.output(led_channel, GPIO.HIGH)
                        time.sleep(0.5)
                        GPIO.output(led_channel, GPIO.LOW)
                        time.sleep(0.5)
                    break
            except KeyboardInterrupt:
                break
        GPIO.cleanup()
    else:
        raise Warning("Unknown example: {}".format(example))


# useful_functions.rst
def useful_functions(section):
    # print("Running {}\n".format(section))
    if section == "GPIO.cleanup":
        import SimulRPi.GPIO as GPIO

        led_channel = 11
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led_channel, GPIO.OUT)
        GPIO.output(led_channel, GPIO.HIGH)
        GPIO.cleanup()
    elif section == "GPIO.setchannelnames":
        import SimulRPi.GPIO as GPIO

        GPIO.setchannelnames({
            10: "led 10",
            11: "led 11"
        })
        GPIO.setmode(GPIO.BCM)
        for ch in [10, 11]:
            GPIO.setup(ch, GPIO.OUT)
            GPIO.output(ch, GPIO.HIGH)
        GPIO.cleanup()
    elif section == "GPIO.setchannels":
        import time
        import SimulRPi.GPIO as GPIO

        key_channel = 23
        led_channel = 10
        gpio_channels = [
            {
                "channel_id": "button",
                "channel_name": "The button",
                "channel_number": key_channel,
                "key": "cmd_r"
            },
            {
                "channel_id": "led",
                "channel_name": "The LED",
                "channel_number": led_channel,
                "led_symbols": {
                    "ON": "🔵",
                    "OFF": "⚪ "
                }
            }
        ]
        GPIO.setchannels(gpio_channels)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(key_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(led_channel, GPIO.OUT)
        print("\nPress key 'cmd_r' to blink a LED")
        while True:
            try:
                if not GPIO.input(key_channel):
                    print("Key 'cmd_r' pressed!")
                    start = time.time()
                    while (time.time() - start) < 3:
                        GPIO.output(led_channel, GPIO.HIGH)
                        time.sleep(0.5)
                        GPIO.output(led_channel, GPIO.LOW)
                        time.sleep(0.5)
                    break
            except KeyboardInterrupt:
                break
        GPIO.cleanup()
    elif section == "GPIO.setdefaultsymbols":
        import time
        import SimulRPi.GPIO as GPIO

        GPIO.setdefaultsymbols(
            {
                'ON': '🔵',
                'OFF': '⚪ '
            }
        )
        led_channel = 11
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led_channel, GPIO.OUT)
        GPIO.output(led_channel, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(led_channel, GPIO.LOW)
        time.sleep(0.5)
        GPIO.cleanup()
    elif section == "GPIO.setkeymap":
        import SimulRPi.GPIO as GPIO

        channel = 17
        GPIO.setkeymap({
            'ctrl_r': channel
        })
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print("\nPress key 'ctrl_r' to exit")
        while True:
            if not GPIO.input(channel):
                print("Key 'ctrl_r' pressed!")
                break
        GPIO.cleanup()
    elif section == "GPIO.setprinting":
        import SimulRPi.GPIO as GPIO

        GPIO.setprinting(False)
        led_channel = 11
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led_channel, GPIO.OUT)
        GPIO.output(led_channel, GPIO.HIGH)
        GPIO.cleanup()
    elif section == "GPIO.setsymbols":
        import time
        import SimulRPi.GPIO as GPIO

        GPIO.setsymbols({
            11: {
                'ON': '🔵',
                'OFF': '⚪ '
            }
        })
        led_channel = 11
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led_channel, GPIO.OUT)
        GPIO.output(led_channel, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(led_channel, GPIO.LOW)
        time.sleep(0.5)
        GPIO.cleanup()
    elif section == "GPIO.wait":
        import time
        import SimulRPi.GPIO as GPIO

        try:
            led_channel = 11
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(led_channel, GPIO.OUT)
            GPIO.output(led_channel, GPIO.HIGH)
            GPIO.wait(3)
        except Exception as e:
            # Could be an exception raised in a thread's target function from
            # ``SimulRPi.GPIO``
            print(e)
        finally:
            GPIO.cleanup()
    else:
        raise Warning("Unknown section: {}".format(section))


if __name__ == '__main__':
    which_doc = sys.argv[1]
    if which_doc == 'combine':
        combine_simulrpi()
    elif which_doc == 'display':
        display_problems()
    elif which_doc == 'readme':
        which_example = int(sys.argv[2])
        readme(which_example)
    elif which_doc == 'useful':
        which_section = sys.argv[2]
        useful_functions(which_section)
    else:
        raise Warning("Unknown document: {}".format(which_doc))
