import win32com.client
import sys
import ctypes
import sounddevice as sd


possible_response = ["y","yes","yap","yeah",","]

def switch_audio(to_headphones):
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

def run_as_admin():
    if sys.platform.startswith('win'):
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, __file__, None, 1)
        except ctypes.WinError:
            # Uživatel zrušil spuštění jako správce nebo se nepodařilo získat potřebná oprávnění
            print(
                "User declined to start as Administrator or he/she lacks necessery permissions")
            pass
    else:
        # Skript není spuštěn na platformě Windows
        print("Script is not designed to run on other OS then Windows")
        pass




def main():
    inp = input("Do you want to switch audio system? y/n: ")

    if inp in possible_response:
        to_headphones = True
        run_as_admin()
        switch_audio(to_headphones)
    else:
        to_headphones = False




run_as_admin()
print(sd.query_devices())
print(sd.default.device)
inp = input("1 - sluchátka, 0 - bedny: ")

if inp == 1:
    sd.default.device = [-1,1]
else:
    sd.default.device = [-1,3]
    
print(sd.query_devices())
print("\n\n\n")
print(sd.default.device)