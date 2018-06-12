from yeelight import discover_bulbs
from yeelight import Bulb
from machine import Pin, time_pulse_us, ADC
import time
import random

class Ultrasonic:

    trig = Pin(15, Pin.OUT)
    echo = Pin(13, Pin.IN)

    def __init__(self):

        print("Class initialised")

    def measure(self):
        self.trig.off()
        time.sleep_us(2)
        self.trig.on()
        time.sleep_us(10)
        self.trig.off()
        while self.echo.value() == 0:
            pass
        t1 = time.ticks_us()
        while self.echo.value() == 1:
            pass
        t2 = time.ticks_us()
        cm = (t2 - t1) / 58.0
        print(cm)
        time.sleep(0.5)
        return cm

class YeelightController:

    bulbs_list = []
    ultrasonic = Ultrasonic()
    # Makes the list containing filtered dictionaries
    def __init__(self):
        filtered_list = self.discover()
        for ip in filtered_list:
            self.bulbs_list.append({'bulb_object': Bulb(ip['ip']), 'name': ip['name'], 'id':ip['id']})
            self.check_duplicatename()

    # Discovers bulbs on the network and filters unnecessary info away
    def discover(self):
        filtered_list = []
        for bulb in discover_bulbs(4):
            filtered_list.append({'ip': bulb['ip'], 'name': bulb['capabilities']['name'], 'id': bulb['capabilities']['id']})
        print('Bulbs found: ', filtered_list)
        return filtered_list

    # Checks for empty or duplicate names
    def check_duplicatename(self):
        previousName = 'ihatesand'
        for bulb in self.bulbs_list:
            if bulb['name'] == '':
                temp_name = str(random.randint(0, 10))
                bulb['name'] = temp_name
                bulb['bulb_object'].set_name(temp_name)
                return True
            elif bulb['name'] == previousName:
                return True
            previousName = bulb['name']
        return False

    # Changes name of bulb and checks if it isn't already in use
    def change_name(self, old_name, new_name):
        for bulb in self.bulbs_list:
            if bulb['name'] == old_name:
                bulb['name'] = new_name
                if self.check_duplicatename():
                    print('Name ', new_name, ' is already in use.')
                    bulb['name'] = old_name
                    return
                else:
                    bulb['bulb_object'].set_name(new_name)
                    print('Name succesfully changed to ', new_name)

    # Returns info used for GUI
    def get_info(self):
        return self.bulbs_list

    # Turns on all available bulbs
    def turnonallbulbs(self):
        print('Turning on all bulbs')
        for bulb in self.bulbs_list:
            bulb['bulb_object'].turn_on()

    # Turns off all available bulbs
    def turnoffallbulbs(self):
        print('Turning off all bulbs')
        for bulbs in self.bulbs_list:
            bulbs['bulb_object'].turn_off()

    # Toggle all available bulbs:
    def toggleallbulbs(self):
        print('toggling all bulbs')
        for bulbs in self.bulbs_list:
            bulbs['bulb_object'].toggle()

    # Changes all bulbs to a specific color
    def change_all_rgb(self, r, g, b):
        print('Parsing values', r, ' ', g, ' ', b)
        for bulbs in self.bulbs_list:
            bulbs['bulb_object'].set_rgb(r, g, b)

    # Changes all bulbs' color temperatures
    def change_all_temp(self, temp):
        print('Temperature: ', temp, ' K')
        for bulbs in self.bulbs_list:
            bulbs['bulb_object'].set_color_temp(temp)

    # Changes brightness in relation to distance from object
    def changeBrightnessDistance(self):
        brightness = self.ultrasonic.measure() / 255
        for bulbs in self.bulbs_list:
            bulbs['bulb_object'].set_brightness(brightness)

    # Toggles light witht button connect to ESP32
    def toggleLightsWithButton(self):
        button = Pin(15, Pin.IN)
        if button.value == 1:
            self.toggleallbulbs()
            time.sleep_us(300)

    # ESP demo
    def runESPdemo(self):
        while True:
            self.toggleLightsWithButton()
            self.changeBrightnessDistance()

YeelightController = YeelightController()
YeelightController.runESPdemo()
