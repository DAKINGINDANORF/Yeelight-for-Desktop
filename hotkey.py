from yeelightcontroller import YeelightController
import keyboard
import time


class Hotkey_handler:

    yeelightcontroller = YeelightController()
    yeelightcontroller.discover()

    def __init__(self):
        print('Input handler initialised')

    def waitForInput(self):
        while True:
            if keyboard.is_pressed('ctrl+pageup'):
                self.yeelightcontroller.toggleallbulbs()
                time.sleep(0.5)


hot = Hotkey_handler()
hot.waitForInput()
