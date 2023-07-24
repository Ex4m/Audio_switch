import win32com.client
import sys
import ctypes

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


inp = input("Do you want to switch audio system? y/n: ")

if inp in possible_response:
    to_headphones = True
    switch_audio(to_headphones)
else:
    to_headphones = False





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


