#%%

import subprocess as sb
import re
import ctypes
import sys
from dataclasses import dataclass, field
import time
import os
import pickle
import keyboard
from enum import Enum



class HotkeyType(Enum):
    TRIGGER = 1
    START_HOOK = 2
    END_HOOK = 3



@dataclass
class SetupStuff:
    result: str = None
    confirm_list: set = ("y", "yes", "yeah", "ok", ".")
    device_data: list = field(default_factory=list)
    device_dict: dict = field(default_factory=dict)
    selected_list: list = field(default_factory=list)
    check: bool = None

    hotkey_bounds = {
        HotkeyType.TRIGGER: 'Insert',  
        HotkeyType.START_HOOK: 'Scroll lock',  
        HotkeyType.END_HOOK: 'Pause'  
    }

    def show_hotkeys(self):
        for key, value in self.hotkey_bounds.items():
            print(f"{key}: {value}")
    
    def set_hotKey(self, hotkey_type):
        print(f"Press the key you wish to save for {hotkey_type}: ")
        inp_key_str = keyboard.read_key()
        print(f"Your key is: {inp_key_str}")
        with open(f"{os.path.dirname(__file__)}\\settingsTEST.pkl", 'wb') as f:
            self.hotkey_bounds[hotkey_type] = inp_key_str
            pickle.dump(self.hotkey_bounds, f)
            print(f"{inp_key_str} exported and saved as type: {hotkey_type}")

    def get_hotKey(self, hotkey_type, path=os.path.dirname(__file__)):
        try:
            with open(f"{path}\\settingsTEST.pkl", 'rb') as f:
                self.hotkey_bounds = pickle.load(f)
                inp_key_str = self.hotkey_bounds.get(hotkey_type)
                if inp_key_str:
                    print(f"Loaded key for {hotkey_type} is: {inp_key_str}")
                return inp_key_str
        except Exception as error:
            print(error)
            
           
 
         
e = SetupStuff()            