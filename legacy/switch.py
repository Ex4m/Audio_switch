
import psutil
import subprocess
import time
import pyautogui


# Otevření ovládacího panelu zvuku
subprocess.run(["control", "mmsys.cpl"])

# Čekání na otevření okna
time.sleep(0.5)

# Kliknutí na tlačítko "Playback" pomocí jeho názvu
headphones_location = pyautogui.locateOnScreen('headphones.png')
print(headphones_location)
if headphones_location:
    pyautogui.click(headphones_location)
else:
    print("headphones button not found")

# Čekání na akci
time.sleep(0.4)

# Kliknutí na tlačítko "Recording" pomocí jeho názvu
speakers_location = pyautogui.locateOnScreen('speakers.png')
print(speakers_location)
if speakers_location:
    pyautogui.click(speakers_location)
else:
    print("speakers button not found")

# Ukončení ovládacího panelu zvuku
for proc in psutil.process_iter():
    if "mmsys.cpl" in proc.name():
        proc.terminate()
        break
