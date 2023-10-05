from pynput.keyboard import Key, Listener
import subprocess
import os


current_directory = os.getcwd() 
hook_active = True

monitored_key = Key.f10
# if -help written 

def change_monitored_key(desired_key):
    global monitored_key
    if isinstance(desired_key, Key):
        monitored_key = desired_key
        print(f"Monitored key changed to {desired_key}")
    else:
        print("Invalid key. Please choose a valid Key from pynput.keyboard.Key.")


def toggle_hook():
    global hook_active
    hook_active = not hook_active

def on_press(key):
    global hook_active
    if hook_active:
        if key == monitored_key:
            print("F10 was pressed, executing powershell script...")
            try:
                # Změňte cestu k vašemu PowerShell skriptu na správnou cestu.
                script_path = f"{current_directory}\swapper.ps1"
                subprocess.run(["powershell", "-File", script_path])
            except Exception as e:
                print(f"An error occurred: {str(e)}")

# Nastavení posluchače na zachycení kláves
with Listener(on_press=on_press) as listener:
    listener.join()

# https://github.com/frgnca/AudioDeviceCmdlets

# Install-Module -Name AudioDeviceCmdlets -> yes -> a / yes
# Set-ExecutionPolicy RemoteSigned -> yes