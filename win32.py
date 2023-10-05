import win32con
import win32gui

# Definice konstant pro klávesy F10 a F11
F10 = 0x79
F11 = 0x7A

# Funkce pro obsluhu klávesových zkratek


def handle_hotkeys(hwnd, msg, wparam, lparam):
    if wparam == F10:
        print("F10 was pressed!")
    elif wparam == F11:
        print("F11 was pressed!")


# Registrace klávesových zkratek
id1 = 1
id2 = 2
win32gui.RegisterHotKey(None, id1, win32con.MOD_NOREPEAT, F10)
win32gui.RegisterHotKey(None, id2, win32con.MOD_NOREPEAT, F11)

# Spuštění smyčky zpráv pro obsluhu klávesových zkratek
try:
    msg = win32gui.PumpMessages()
except KeyboardInterrupt:
    win32gui.UnregisterHotKey(None, id1)
    win32gui.UnregisterHotKey(None, id2)
    # win32api.PostQuitMessage()
