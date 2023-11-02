
# import Engine


# e = Engine.SetupStuff()


# hotkey = e.get_hotKey_swap()

# print("BOL SOM TU")


import keyboard
import time

last_alt_time = 0


def on_key_event(e):
    global last_alt_time
    if e.name == 'alt':
        last_alt_time = time.time()
    elif e.name == 'shift' and time.time() - last_alt_time < 0.5:
        print("Combo 'left alt + left shift' pressed")


keyboard.on_press(on_key_event)
keyboard.wait()
