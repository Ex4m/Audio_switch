import subprocess as sb
import os
import keyboard
import time
from Engine import SetupStuff, HotkeyType

e = SetupStuff()


def start_main_script():
    # Změňte cestu k hlavnímu skriptu na odpovídající
    main_script_path = "C:\\cesta\\k\\vasemu\\hlavnimu_skriptu.py"
    sb.Popen(["pythonw", main_script_path])


start_key = HotkeyType.START_HOOK  # Nastavte klávesovou zkratku dle potřeby

keyboard.add_hotkey(start_key, start_main_script)

while True:
    time.sleep(1)
