import win32com.client
import sys
import ctypes
import sounddevice as sd
import time

def run_as_admin():
    if sys.platform.startswith('win'):
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, __file__, None, 1)
        except ctypes.WinError:
            # Uživatel zrušil spuštění jako správce nebo se nepodařilo získat potřebná oprávnění
            print("User declined to start as Administrator or lacks necessary permissions")
            sys.exit(1)
    else:
        # Skript není spuštěn na platformě Windows
        print("Script is not designed to run on other OS than Windows")
        sys.exit(1)






"""def switch_audio(to_headphones):
    # create a Win32 COM object for the Windows audio endpoint
    endpoint = win32com.client.Dispatch("AudioEndpointControl.CoreAudioEndpointControl")

    if to_headphones:
        # get the ID of the headphones device
        headphones_id = None
        for device in endpoint.GetAudioEndpoints():
            if device.FriendlyName == "Headphones":
                headphones_id = device.Id
                break

        # switch to the headphones device
        endpoint.SetDefaultEndpoint(headphones_id)
    else:
        # switch to the sound system device
        endpoint.SetDefaultEndpoint("")

# this should help to switch with admin righths
"""



def switch_audio_output(output_device_index):
    try:
        # Získání seznamu dostupných zařízení
        devices = sd.query_devices()
        
        # Získání aktuálního výchozího zařízení
        current_default_device = sd.default.device
        
        # Nastavení nového výchozího zařízení
        run_as_admin()
        sd.default.device = [-1,output_device_index]

        # Získání informací o novém výchozím zařízení
        new_default_device = devices[output_device_index]['name']
        print(current_default_device)
        print(f"Audio output switched to: {new_default_device}")
        

    except Exception as e:
        print(f"Error switching audio output: {e}")

def main():
    # Zobrazení dostupných zvukových zařízení
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        print(f"Device {i}: {device['name']}")

    # Výběr zařízení pro přepnutí (pomocí indexu)
    output_device_index = int(input("Enter the index of the device to switch to: "))

    # Přepnutí výstupního zařízení
    switch_audio_output(output_device_index)

if __name__ == "__main__":
    main()


print(sd.query_devices())
print("Konec")





