import subprocess as sb
import os
import keyboard
from Engine import SetupStuff


e = SetupStuff()

monitored_key = e.get_hotKey_swap()
current_directory = os.path.dirname(__file__)
hook_active = True
swapper = "Audio_switch.exe"


def toggle_hook():
    global hook_active
    hook_active = not hook_active


def locate_file(swapper, current_directory):
    for root, directory, files in os.walk(current_directory):
        if swapper in files:
            return os.path.join(root, swapper)
    return None


def on_key_event(keyboard_event):
    global hook_active
    if hook_active:
        if keyboard_event.name == monitored_key:
            print(f"{monitored_key} was pressed, executing powershell script...")
            try:
                exe_path = locate_file(swapper, current_directory)
                if exe_path is None:
                    print("Exe not found")
                else:
                    print(f"Exe found on this path {exe_path}")
                    sb.run([exe_path], shell=True)
                # script_path = f"{current_directory}\\swapper.ps1"
                # subprocess.run(["powershell", "-File", script_path])
            except Exception as e:
                print(f"An error occurred: {str(e)}")


# Nastavení posluchače na zachycení kláves
keyboard.on_press(on_key_event)

# Pokud chcete zachytávat události klávesnice i mimo hlavní smyčku, můžete použít keyboard.wait()
keyboard.wait()
