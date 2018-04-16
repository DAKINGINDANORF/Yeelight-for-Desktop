from yeelight import discover_bulbs
from yeelight import Bulb
import random


class YeelightController:

    bulbs_list = []

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

    # Toggles specific light
    def toggle_specific_bulb(self, id):
        for bulb in self.bulbs_list:
            if bulb['id'] == id:
                bulb['bulb_object'].toggle()
                print('Bulb ', bulb['id'], ' toggled')
                return
        print('No bulb "', id, '" found')

    # Changes specific bulb
    def change_specific_rgb(self, id, r, g, b):
        for bulb in self.bulbs_list:
            if bulb['id'] == id:
                bulb['bulb_object'].set_rgb(r, g, b)
                print('Bulb ', bulb['name'], ' changed color')
                return
        print('No bulb "', id, '" found')