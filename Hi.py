import ctypes
import mouse
from mouse import move, get_position
import time
import sys

start_x, start_y = get_position()
# Definice parametrů pohybu myši
square_size = 200  # Velikost čtverce
duration = 1  # Doba trvání jednoho pohybu


ctypes.windll.shell32.ShellExecuteW(
    None, "runas", sys.executable, __file__, None, 1)
print("mouse & keyboard blocked")
ctypes.windll.user32.BlockInput(True)
move(start_x + square_size, start_y, duration=duration)
move(start_x + square_size, start_y + square_size, duration=duration)
move(start_x, start_y + square_size, duration=duration)
move(start_x, start_y, duration=duration)
ctypes.windll.user32.BlockInput(False)
print("mouse & keyboard unblocked")
time.sleep(0.5)
