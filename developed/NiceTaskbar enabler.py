import os

# # Nastavit cestu k aplikaci NiceTaskbar
# path = r'C:\\Program Files\\WindowsApps\\30881xwl.NiceTaskbar_1.0.6.0_x86__9ammpd0196578'

# # Spustit aplikaci
# # os.system(os.path.join(path, 'NiceTaskbar.exe'))

# # Vypnout aplikaci
# try:
#     os.system(os.path.join(path, 'NiceTaskbar.exe -exit'))
# except Exception as error:
#     print(error)


# import subprocess
# import os

# # Identifikátor balíčku aplikace z Microsoft Store
# package_name = '30881xwl.NiceTaskbar_1.0.6.0_x86__9ammpd0196578'

# app_path = f"C:\\\Program Files\\WindowsApps\\{package_name}"
# if os.path.exists(app_path):
#     powershell_script = f"Start-Process '{app_path}' -ExecutionPolicy Bypass"
#     subprocess.run(['powershell', '-Command', powershell_script], shell=True)
# else:
#     print(f"Specified path does not exist: {app_path}")


# # PowerShell skript pro spuštění aplikace
# powershell_script = f"Start-Process shell:appsFolder\\{package_name} -ExecutionPolicy Bypass"

# # Spuštění PowerShell skriptu
# subprocess.run(['powershell', '-Command', powershell_script], shell=True)


# ---------------------------------
#  Start-Process "shell:AppsFolder\30881xwl.NiceTaskbar_9ammpd0196578!App"
# ---------------------------------
from ctypes import windll, wintypes
import subprocess as sb
import time
import keyboard
# Enable
enable = 1

if enable == 0:
    # Spustit aplikaci NiceTaskbar
    sb.run(["powershell", "Start-Process -FilePath 'shell:AppsFolder\\30881xwl.NiceTaskbar_9ammpd0196578!App'"],
           capture_output=True, text=True)
    print("Spuštěno")

# Disable
else:

    # Zastavit aplikaci NiceTaskbar
    sb.run(["powershell", "Stop-Process -Name 'NiceTaskbar' -Force"],
           capture_output=True, text=True)
    # time.sleep(1)
    # definovat konstanty
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x001A

    # odeslat zprávu všem oknům o změně stavu taskbaru
    windll.user32.SendNotifyMessageW(
        HWND_BROADCAST, WM_SETTINGCHANGE, 0, wintypes.LPCWSTR("TraySettings"))
    keyboard.press_and_release('win')
    time.sleep(0.1)
    keyboard.press_and_release('esc')
    print("Vypnuto")
