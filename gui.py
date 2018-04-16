from tkinter import *
from yeelightcontroller import YeelightController
import random

class GUI:

    yeelightcontroller = YeelightController()
    gui_window = Tk()
    gui_window.title('Yeelight controls for PC and Mac')

    # Initialises the GUI with the selected
    def __init__(self):
        print('GUI initialised')

        self.bulbinfo_list = self.yeelightcontroller.get_info()
        self.singlebulbcontrol_list = []
        x = 0
        for bulbs in self.bulbinfo_list:
            self.singlebulbcontrol_list.append({'label' : Label(self.gui_window, text = bulbs['id']), 'buttonid' : x , 'button':  Button(self.gui_window, text= 'Toggle',
                                                    command =lambda: self.test_buttons())})
            x = x + 1
        rowheight = 0
        for bulb in self.singlebulbcontrol_list:
            bulb['label'].grid(row= rowheight + 1, column=0, sticky=NW)
            bulb['button'] = Button(self.gui_window, text= 'Toggle',
                                    command =lambda: self.test_buttons(bulb['buttonid']))
            bulb['button'].grid(row= rowheight + 1, column=1, sticky=NW)
            rowheight = rowheight + 1

        self.rvalue_slider = Scale(self.gui_window, from_=0, to=255)
        self.gvalue_slider = Scale(self.gui_window, from_=0, to=255)
        self.bvalue_slider = Scale(self.gui_window, from_=0, to=255)
        self.temp_slider = Scale(self.gui_window, from_=1700, to=6500)

        title_label = Label(self.gui_window,text='Xiaomi YeeLight for Desktop/Mac')
        toggleall_button = Button(self.gui_window, text='Toggle all lights', fg='red',
                                    command = self.yeelightcontroller.toggleallbulbs)
        turnon_button = Button(self.gui_window, text='Turn on all lights', fg='blue',
                                    command = self.yeelightcontroller.turnonallbulbs)
        turnoff_button = Button(self.gui_window, text='Turn off all lights', fg='green',
                                    command = self.yeelightcontroller.turnoffallbulbs)
        changergb_button = Button(self.gui_window, text='Parse rgb values',
                                    command = self.parsergb)
        changetemp_button = Button(self.gui_window, text='Change color temperature',
                                    command= lambda: self.yeelightcontroller.change_all_temp(self.temp_slider.get()))

        title_label.grid(row= 0, column =0, sticky=NW)

        toggleall_button.grid(row= 3, column=0, sticky=W)
        turnon_button.grid(row= 4, column=0, sticky=W)
        turnoff_button.grid(row= 5, column=0, sticky=W)
        changergb_button.grid(row=6,column=0,sticky=W)
        changetemp_button.grid(row=7,column=0,sticky=W)

        self.rvalue_slider.grid(row=0, column=7, rowspan=5, sticky=E)
        self.gvalue_slider.grid(row=0, column=8, rowspan=5, sticky=E)
        self.bvalue_slider.grid(row=0, column=9, rowspan=5, sticky=E)
        self.temp_slider.grid(row=0, column=10, rowspan=5, sticky=E)

    # Binds buttons to bulbID
    def test_buttons(self, x):
        print(x)

    # Lights up the bulbs in the given R G B colors
    def parsergb(self):
        r = self.rvalue_slider.get()
        g = self.gvalue_slider.get()
        b = self.bvalue_slider.get()
        if r == 0 and g == 0 and b == 0:
            self.yeelightcontroller.turnoffallbulbs()
        else:
            self.yeelightcontroller.turnonallbulbs()
            self.yeelightcontroller.change_all_rgb(r, g, b)

    def run(self):
        self.gui_window.mainloop()


gui = GUI()
gui.run()
