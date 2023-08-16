import time
from mouse import move, get_position
import ctypes
import sys


start_x, start_y = get_position()
# Definice parametrů pohybu myši
square_size = 200  # Velikost čtverce
duration = 1  # Doba trvání jednoho pohybu


def mousemove():
    move(start_x + square_size, start_y, duration=duration)
    move(start_x + square_size, start_y + square_size, duration=duration)
    move(start_x, start_y + square_size, duration=duration)
    move(start_x, start_y, duration=duration)


def block_input():
    # Získání handle okna
    # Blokování vstupu pomocí funkce BlockInput
    print("mouse & keyboard blocked")
    ctypes.windll.user32.BlockInput(True)
    mousemove()

    time.sleep(1)
    print("spal jsem")

    mousemove()
    print("mouse & keyboard unblocked")
    time.sleep(0.5)
    # Obnovení vstupu pomocí funkce BlockInput
    ctypes.windll.user32.BlockInput(False)


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


# Zkontrolovat, zda je skript spuštěn jako správce
if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    # Skript není spuštěn jako správce, spustit jako správce
    run_as_admin()
else:
    # Skript je spuštěn jako správce, pokračovat s kódem
    block_input()
