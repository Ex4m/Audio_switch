
#%%

import subprocess as sb
import re
import ctypes
import sys
from  dataclasses import dataclass
# Run powershell get list comm to get info of audiodevices and then parse it back to list

@dataclass
class Engine:
    result: str = None
    device_data: str = None
    device_dict: str = None
        
    def get_list(self):
        self.result = sb.run(["powershell", "Get-AudioDevice -list"], capture_output=True, text=True)
        # Zkontrolujte návratový kód
        if self.result.returncode == 0:
            # Získání výstupu jako řetězce
            self.result = str(self.result.stdout.strip())
            print(self.result)
        return self.result
        
       
       
    def convert_list(self):   
        # Použijeme regulární výraz k rozparsování vstupu
        self.device_data = re.findall(r'Index\s+: (\w+)\n?Default\s+: (\w+)\n?DefaultCommunication\s+: (\w+)\n?Type\s+: (.+)\n?Name\s+: (.+)\n?ID\s+: ({.+})\n?Device\s+: (.+)\n?', self.result)
        
        for item in self.device_data:
            index, default, default_communication, device_type, name, device_id, device = item
            self.device_dict[int(index)] = {
                'Default': default,
                'DefaultCommunication': default_communication,
                'Type': device_type.strip(),
                'Name': name.strip(),
                'ID': device_id.strip(),
                'Device': device.strip()
            }
            
        # Výpis výsledného slovníku
        for index, device_info in self.device_dict.items():
            print(f"Index: {index}")
            print(f"Default: {device_info['Default']}")
            print(f"DefaultCommunication: {device_info['DefaultCommunication']}")
            print(f"Type: {device_info['Type']}")
            print(f"Name: {device_info['Name']}")
            print(f"ID: {device_info['ID']}")
            print(f"Device: {device_info['Device']}")
            
            
    def get_device_id(self, index):
        # Zkontrolujte, zda existuje slovník
        if self.device_dict is None:
            return None

        # Získání ID pro daný index
        device_info = self.device_dict.get(index)
        if device_info is not None:
            return device_info['ID']
        else:
            return None
            
            
    # def run_as_admin(self):
    #     if sys.platform.startswith('win'):
    #         try:
    #             ctypes.windll.shell32.ShellExecuteW(
    #                 None, "runas", sys.executable, __file__, None, 1)
    #         except ctypes.WinError:
    #             # Uživatel zrušil spuštění jako správce nebo se nepodařilo získat potřebná oprávnění
    #             print(
    #                 "User declined to start as Administrator or he/she lacks necessery permissions")
    #             pass
    #     else:
    #         # Skript není spuštěn na platformě Windows
    #         print("Script is not designed to run on other OS then Windows")
    #         pass
        

e = Engine()
e.get_list()
e.convert_list()
print("konec")