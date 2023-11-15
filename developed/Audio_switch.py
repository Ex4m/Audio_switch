import subprocess as sb
import os
import keyboard
from Engine import SetupStuff, HotkeyType
import time
import sys

e = SetupStuff()

# -------------------------------------------------------------------
# pythonw.exe your_script.py     to run without any window
# Start Hook zatím nefunguje
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
swapper = "swapper.ps1"  # "Audio_switch.exe"
last_alt_time = 0
inform = True


def toggle_hook():
    global hook_active
    hook_active = not hook_active
    print(f"Hook {'enabled' if hook_active else 'disabled'}")

def locate_file(file, current_directory):
    for root, directory, files in os.walk(current_directory):
        if file in files:
            return os.path.join(root, file)
    return None


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


        

nt_path = 'C:\\Program Files\\WindowsApps\\30881xwl.NiceTaskbar_1.0.6.0_x86__9ammpd0196578\\NiceTaskbar.exe'



def on_key_event(keyboard_event):
    global hook_active
    global last_alt_time
    if hook_active:
        if inform:
            print(f"Pressed key:" + keyboard_event.name)
        if keyboard_event.name == trigger_key:
            print(f"{trigger_key} was pressed, executing powershell script...")
            try:
                # exe_path = locate_file(swapper, current_directory)
                swapper_path = locate_file(swapper, current_directory)
                if swapper_path is None:
                    print("Exe not found")
                else:
                    print(f"PWS Swapper found on this path {swapper_path}")
                    # sb.run([exe_path], shell=True)
                    # script_path = f"{current_directory}\\swapper.ps1"
                    sb.run(["powershell", "-File", swapper_path])
                    # sb.run(exe_path)
            except Exception as e:
                print(f"An error occurred: {str(e)}")

        elif keyboard_event.name == start_key:
            print(f"{start_key} was pressed, starting hook...")
            hook_active = True

        elif keyboard_event.name == end_key:
            print(f"{end_key} was pressed, stopping hook...")
            hook_active = False
            
        if keyboard_event.name == 'alt':
            last_alt_time = time.time()
        elif keyboard_event.name == 'shift' and time.time() - last_alt_time < 0.5:
            print("Combo 'left alt + left shift' pressed")

            
            sb.run(nt_path)


# Nastavení posluchače na zachycení kláves
keyboard.on_press(on_key_event)

# Pokud chcete zachytávat události klávesnice i mimo hlavní smyčku, můžete použít keyboard.wait()
# keyboard.wait()
print("Listening for key triggering")
while True:
    time.sleep(1)
