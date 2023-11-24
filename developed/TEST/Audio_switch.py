import subprocess as sb
import os
import keyboard
from Engine import SetupStuff, HotkeyType
import sys
import pickle

e = SetupStuff()

# -------------------------------------------------------------------
# pythonw.exe your_script.py     to run without any window
#  - DONE - vymazat vyskakující okno u engine.py . Je to kv;li shebangu # !/usr/bin/env python
#  - DONE - spustit pws skript nenápadněji ? vyskočí modré okno
#  - DONE - nefunguje opětovné spustění souboru startHookem
#  - přetavit do exe souboru a ten se bude spouštět podprahově. TEST jak funguje a jaký má vliv na CPU
#  - vyřešit přejmenování id a tím nefunkčnost pws skriptu a nutnost jeho nového generování
#  - může pomoci ukládání do dict key: bedny123 value: id se bude dynamicky prohledávat
#  - bude fungovat automaticky. pokud selze prepnutí tak se spustí smyčka s kodem která jej obnoví. Muze být v Engine.py
#  -
#  -
# -------------------------------------------------------------------
if getattr(sys, 'frozen', False):
    current_directory = sys._MEIPASS
else:
    current_directory = os.path.dirname(os.path.realpath(__file__))

print(current_directory)
trigger_key = e.get_hotKey(HotkeyType.TRIGGER)
start_key = e.get_hotKey(HotkeyType.START_HOOK)
end_key = e.get_hotKey(HotkeyType.END_HOOK)
print(f"Trigger:{trigger_key}\nStart hook:{start_key}\nEnd hook:{end_key}")
hook_active = True
swapper = "swapper.ps1"
last_alt_time = 0
inform = True


def initialize_listener():
    keyboard.on_press(on_key_event)
    print("Listener initialized")


def start_listener():
    global hook_active
    hook_active = True
    initialize_listener()
    print("Listening for key triggering")
    keyboard.add_hotkey(end_key, stop_listener)


def stop_listener():
    global hook_active
    hook_active = False
    print("Listener stopped")
    keyboard.unhook_all()
    keyboard.add_hotkey(start_key, start_listener)


def locate_file(file, current_directory):
    for root, directory, files in os.walk(current_directory):
        if file in files:
            return os.path.join(root, file)
    return None


def on_key_event(keyboard_event):
    global hook_active
    global last_alt_time
    if hook_active:
        if inform:
            print(f"Pressed key:" + keyboard_event.name)
        if keyboard_event.name == trigger_key:
            print(f"{trigger_key} was pressed, executing powershell script...")
            try:
                swapper_path = locate_file(swapper, current_directory)
                if swapper_path is None:
                    print("Exe not found")
                else:
                    print(f"PWS Swapper found on this path {swapper_path}")
                    sb.run(["powershell", "-File", swapper_path,
                           "-WindowStyle", "Hidden"])
            except Exception as e:
                print(f"An error occurred: {str(e)}")


keyboard.add_hotkey(start_key, start_listener)
keyboard.add_hotkey(end_key, stop_listener)

print("Listening for key triggering")
keyboard.wait()


# WIP TASKBAR SWITCH SCHEME //////////////////////////
# class ThemeSwitcher:
#     def __init__(self):
#         self.switch = False
#         self.themeSwitcher_path = locate_file(
#             'ThemeSwitcher.exe', current_directory)
#         self.theme_path_EN = 'C:\\Users\\oz\\AppData\\Roaming\\Microsoft\\Windows\\Themes\\Custom_EN.theme'
#         self.theme_path_CZ = 'C:\\Users\\oz\\AppData\\Roaming\\Microsoft\\Windows\\Themes\\Custom_CZ.theme'

#     def switch_theme(self):
#         if self.switch:
#             self.switch = False
#             return self.theme_path_CZ
#         else:
#             self.switch = True
#             return self.theme_path_EN

# theme_switcher = ThemeSwitcher()

# PWS
# $proc = Get-Process | Where-Object { $_.Name -eq "NiceTaskbar" }
# $proc.Id
# $proc.Id
