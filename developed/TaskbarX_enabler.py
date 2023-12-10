

import psutil
import subprocess as sb
import keyboard
import time
import ctypes
from ctypes import windll, wintypes

keyboard_dict = {
    "0x405": "cs-CZ",  # Čeština
    "0x409": "en-US",  # Angličtina (USA)
    "0x40C": "fr-FR",  # Francouzština
    "0x407": "de-DE",  # Němčina
    "0x410": "it-IT",  # Italština
    "0x40A": "es-ES",  # Španělština
    "0x411": "ja-JP",  # Japonština
    "0x412": "ko-KR",  # Korejština
    "0x804": "zh-CN",  # Čínština (zjednodušená)
    "0x404": "zh-TW",  # Čínština (tradiční)
    "0x419": "ru-RU",  # Ruština
    "0x416": "pt-BR",  # Portugalština (Brazílie)
    "0x41F": "tr-TR",  # Turečtina
    "0x41D": "sv-SE",  # Švédština
    "0x413": "nl-NL",  # Holandština
    "0x40D": "he-IL",  # Hebrejština
    "0x40E": "hu-HU",  # Maďarština
    "0x41E": "th-TH",  # Thajština
    "0x41B": "sk-SK",  # Slovenština
    "0x414": "nb-NO",  # Norština (Bokmål)
    "0x415": "pl-PL",  # Polština
    "0x418": "ro-RO",  # Rumunština
    "0x41A": "sr-Latn-RS",  # Srbština (latinka, Srbsko)
    "0x81A": "sr-Cyrl-RS",  # Srbština (cyrilice, Srbsko)
    "0x422": "uk-UA",  # Ukrajinština
    "0x420": "ur-PK",  # Urdština
    "0x42A": "vi-VN",  # Vietnamština
    "0x43E": "ms-MY",  # Malajština
    "0x440": "ky-KG",  # Kyrgyzština
    "0x442": "tn-ZA",  # Tswana
    "0x444": "xh-ZA",  # Xhosa
    "0x446": "zu-ZA",  # Zulu
    "0x448": "wo-SN",  # Wolof
    "0x44A": "pa-IN",  # Pandžábština
    "0x44E": "mr-IN",  # Maráthština
    "0x450": "mn-MN",  # Mongolština
    "0x454": "lo-LA",  # Laoština
    "0x456": "gl-ES",  # Galicijština
    "0x458": "kok-IN",  # Konkánština
    "0x45A": "syr-SY",  # Syrština
    "0x45C": "gsw-FR",  # Alsasština
    "0x460": "ti-ER",  # Tigriňština (Eritrea)
    "0x461": "rm-CH",  # Rétorománština
    "0x462": "nso-ZA",  # Sesotho sa Leboa
    "0x464": "quz-PE",  # Quechua (Peru)
    "0x465": "fil-PH",  # Filipínština
    "0x466": "haw-US",  # Havajština
    "0x467": "yo-NG",  # Yorubština
    "0x468": "quc-Latn-GT",  # K'iche'
    "0x46A": "moh-CA",  # Mohawk
    "0x46B": "br-FR",  # Bretonština
    "0x46C": "ug-CN",  # Ujgurština
    "0x46D": "mi-NZ",  # Maorština
    "0x46E": "oc-FR",  # Okcitánština
    "0x46F": "co-FR",  # Korsičtina
    "0x470": "gsw-LI",  # Švýcarská němčina (Lichtenštejnsko)
    "0x471": "ku-Arab-IQ",  # Kurdština (Irák)
    "0x472": "lb-LU",  # Lucemburština
    "0x473": "qut-GT",  # K'iche' (Guatemala)
    "0x474": "guz-KE",  # Gusii
    "0x475": "rw-RW",  # Kinyarwanda
    "0x476": "wo-SN",  # Wolof (Senegal)
    "0x477": "prs-AF",  # Darí
    "0x478": "gd-GB",  # Skotská gaelština
    "0x479": "ku-Arab-IQ",  # Kurdština (Irák)
    "0x47A": "ar-IQ",  # Arabština (Irák)
    "0x47C": "nso-ZA",  # Sesotho sa Leboa (Jihoafrická republika)
    "0x47E": "tn-ZA",  # Tswana (Jihoafrická republika)
    "0x480": "ii-CN",  # Sichuan Yi
    "0x481": "arn-CL",  # Mapudungun
    "0x482": "moh-CA",  # Mohawk (Kanada)
    "0x483": "br-FR",  # Bretonština (Francie)
    "0x484": "ug-CN",  # Ujgurština (Čína)
    "0x485": "mi-NZ",  # Maorština (Nový Zéland)
    "0x486": "oc-FR",  # Okcitánština (Francie)
    "0x487": "co-FR",  # Korsičtina (Francie)
    "0x488": "gsw-FR",  # Alsasština (Francie)
    "0x489": "sah-RU",  # Jakutština
    "0x48A": "qut-GT",  # K'iche' (Guatemala)
    "0x48B": "rw-RW",  # Kinyarwanda (Rwanda)
    "0x48C": "wo-SN",  # Wolof (Senegal)
    "0x48D": "prs-AF",  # Darí (Afghánistán)
    "0x48E": "plt-MG",  # Malgaština (Madagaskar)
    "0x48F": "zh-YUE",  # Kantonská čínština
    "0x490": "tdd-Tale-CN",  # Tai Nüa
    "0x491": "khb-Talu-CN",  # Tai Lü
    "0x492": "gd-GB",  # Skotská gaelština (Velká Británie)
    "0x493": "ku-Arab-IQ",  # Kurdština (Irák)
    "0x494": "quc-Latn-GT",  # K'iche' (Guatemala)
    "0x495": "qps-ploc",  # Pseudo Language
    "0x496": "qps-ploca",  # Pseudo Language
    "0x497": "qps-plocm",  # Pseudo Language
    "0x498": "ar-IQ",  # Arabština (Irák)
    "0x499": "qps-Latn-x-sh",  # Pseudo Language
    "0x49A": "qps-Latn-x-si",  # Pseudo Language
    "0x49B": "qps-Latn-x-ajami",  # Pseudo Language
    "0x49C": "qps-Latn-x-t-iq",  # Pseudo Language
}


def refresh_taskbar():
    # Odeslat zprávu o změně nastavení do taskbaru
    ctypes.windll.user32.SendNotifyMessageW(
        0xFFFF, 0x001A, 0, ctypes.create_unicode_buffer("TraySettings"))
    print("Něco jsem poslal messagem")
    time.sleep(4)
    # Simulujte stisk klávesy WIN
    ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)  # Stisk klávesy WIN
    ctypes.windll.user32.keybd_event(
        0x5B, 0, 0x0002, 0)  # Uvolnění klávesy WIN

    print("zmáčkl jsem WIN")
    # Počkejte krátkou dobu, než se otevře nabídka Start
    time.sleep(4)

    # Simulujte stisk klávesy ESC
    ctypes.windll.user32.keybd_event(0x1B, 0, 0, 0)  # Stisk klávesy ESC
    ctypes.windll.user32.keybd_event(
        0x1B, 0, 0x0002, 0)  # Uvolnění klávesy ESC
    print("zmáčkl jsem ESC")


# Aktualizovat taskbar
enable = True
lastId = ''
switchPrint = 1
while True:

    user32 = ctypes.WinDLL('user32', use_last_error=True)
    curr_window = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
    klid = user32.GetKeyboardLayout(thread_id)
    lid = klid & (2**16 - 1)
    lid_hex = hex(lid)
    # print(lid_hex)

    # if lid_hex in keyboard_dict:
    #     print(keyboard_dict[lid_hex])

    if keyboard_dict[lid_hex] == 'cs-CZ' and lastId != 'cs-CZ':
        # Spustit aplikaci NiceTaskbar
        if "TaskbarX" not in (p.name() for p in psutil.process_iter()):
            command = r"C:\Users\Exa\Desktop\TaskbarX\TaskbarX.exe -tbs=2 -color=165;44;48;50 -tpop=100 -tsop=100 -as=quinteaseinout -tbr=100 -tbsg=1 -obas=cubiceaseinout -asp=300 -ptbo=0 -stbo=0 -lr=400 -oblr=400 -sr=0 -sr2=0 -sr3=0 -cso=1 -ftotc=1 -rzbt=0 -dct=1 -console"
            sb.run(command, shell=False)
            print("Spuštěno") if switchPrint else ''

    # Disable
    elif keyboard_dict[lid_hex] == 'en-US' and lastId != 'en-US':

        # refresh_taskbar()

        # Zastavit aplikaci NiceTaskbar
        sb.run(["powershell", "Stop-Process -Name 'TaskbarX' -Force"],
               capture_output=True, text=True)
        # definovat konstanty
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A

        # odeslat zprávu všem oknům o změně stavu taskbaru
        windll.user32.SendNotifyMessageW(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0, wintypes.LPCWSTR("TraySettings"))

        # time.sleep(0.1)
        # keyboard.press_and_release('win')
        # time.sleep(0.2)
        # keyboard.press_and_release('esc')
        # time.sleep(0.2)
        # keyboard.press_and_release('esc')

        print("Vypnuto") if switchPrint else ''

    else:
        print("čekám") if switchPrint else ''
    enable = not enable
    lastId = keyboard_dict[lid_hex]
    print(f"last ID: {lastId}") if switchPrint else ''

    time.sleep(1)

# # ---------------------------------
# #  Start-Process "shell:AppsFolder\30881xwl.NiceTaskbar_9ammpd0196578!App"
# # ---------------------------------
