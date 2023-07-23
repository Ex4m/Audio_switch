import win32com.client

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
