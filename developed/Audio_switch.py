import subprocess as sb
import os
import keyboard
import time
import sys
import pickle
from enum import Enum
import shutil

# -------------------------------------------------------------------
# pythonw.exe your_script.py     to run without any window
#  - DONE - vymazat vyskakující okno u engine.py . Je to kv;li shebangu # !/usr/bin/env python
#  - DONE - spustit pws skript nenápadněji ? vyskočí modré okno
#  - DONE - nefunguje opětovné spustění souboru startHookem
#  - DONE - přeprasat Audio_switch do OOP
#  - 80% přetavit do exe souboru a ten se bude spouštět podprahově. TEST jak funguje a jaký má vliv na CPU
#  - 70% winStart - Chci mít v engine nebo zde ? dát uživateli možnost nastavení přes settings.pkl? C:\Users\Exa\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
#  - vyřešit přejmenování id a tím nefunkčnost pws skriptu a nutnost jeho nového generování
#  - může pomoci ukládání do dict key: bedny123 value: id se bude dynamicky prohledávat
#  - bude fungovat automaticky. pokud selze prepnutí tak se spustí smyčka s kodem která jej obnoví. Muze být v Engine.py
#  -
# -------------------------------------------------------------------


class HotkeyType(Enum):
    TRIGGER = 1
    START_HOOK = 2
    END_HOOK = 3


class AudioSwitch:
    def __init__(self, hook_active=True, swapper="swapper.ps1", inform=True, last_alt_time=0) -> None:
        self.hook_active = hook_active
        self.swapper = swapper
        self.inform = inform
        self.last_alt_time = last_alt_time
        self.trigger_key = None
        self.start_key = None
        self.end_key = None
        self.current_dir = None
        self.check_startup()
        self.get_current_dir()
        self.get_hotkeys()
        keyboard.add_hotkey(self.start_key, self.start_listener)
        keyboard.add_hotkey(self.end_key, self.stop_listener)
        self.initialize_listener()

    def check_startup(self):
        startup_folder = os.path.join(
            os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        thisFilePath = os.path.basename(sys.argv[0])

        shortcut_path = os.path.join(startup_folder, thisFilePath)
        if not os.path.exists(shortcut_path):
            try:
                shutil.copy(sys.argv[0], startup_folder)
                print("Skript byl úspěšně přidán do složky Startup.")
            except Exception as e:
                print(f"Chyba při přidávání do složky Startup: {e}")

    def get_hotkeys(self):
        try:
            with open(os.path.join(self.current_dir, 'settings.pkl'), 'rb') as f:
                hotkey_bounds = pickle.load(f)
                self.trigger_key = hotkey_bounds.get(HotkeyType.TRIGGER)
                self.start_key = hotkey_bounds.get(HotkeyType.START_HOOK)
                self.end_key = hotkey_bounds.get(HotkeyType.END_HOOK)
            print(
                f"Trigger:{self.trigger_key}\nStart hook:{self.start_key}\nEnd hook:{self.end_key}")

        except Exception as error:
            print(error)

    def get_current_dir(self):
        self.current_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

    def initialize_listener(self):
        keyboard.on_press_key(self.trigger_key, self.on_key_event)
        print("Listener initialized")

    def start_listener(self):
        self.hook_active = True
        self.initialize_listener()
        print("Listening for key triggering")
        keyboard.add_hotkey(self.end_key, self.stop_listener)

    def stop_listener(self):
        self.hook_active = False
        print("Listener stopped")
        keyboard.unhook_all()
        keyboard.add_hotkey(self.start_key, self.start_listener)

    def on_key_event(self, event):
        if self.hook_active:
            if self.inform:
                print(f"Pressed key: {event.name}")
            if event.name == self.trigger_key:
                print(
                    f"{self.trigger_key} was pressed, executing powershell script...")
                try:
                    swapper_path = self.locate_file(
                        self.swapper, self.current_dir)
                    if swapper_path is None:
                        print("Exe not found")
                    else:
                        print(f"PWS Swapper found on this path {swapper_path}")
                        sb.run(["powershell", "-File", swapper_path,
                               "-WindowStyle", "Hidden"])
                except Exception as e:
                    print(f"An error occurred: {str(e)}")

    def locate_file(self, file, current_directory):
        for root, directory, files in os.walk(current_directory):
            if file in files:
                return os.path.join(root, file)
        return None


# Vytvoření instance třídy AudioSwitch
audio_switch = AudioSwitch()
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
