
#%%

import subprocess as sb
import re
import ctypes
import sys
from  dataclasses import dataclass, field
# Run powershell get list comm to get info of audiodevices and then parse it back to list

@dataclass
class SetupStuff:
    result: str = None
    device_data: list = field(default_factory=list) 
    device_dict: dict = field(default_factory=dict)
    selected_list: list = field(default_factory=list)
        
    def get_list(self):
        self.result = sb.run(["powershell", "Get-AudioDevice -list"], capture_output=True, text=True)
        if self.result.returncode == 0:
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
        
            
    def get_device_key(self, value, index):
        if self.device_dict is None:
            raise TypeError("origin dictionary is not created, try use .get_list ->.convert_list first")

        device_info = self.device_dict.get(index)
        if device_info is not None:
            return device_info[value]
        else:
            return None
        
    
    def add_device(self, index):
        device_info = self.get_device_key("ID", index)
        if len(self.selected_list) < 2:
            self.selected_list.append(device_info)
            return self.selected_list
        else:
            raise ValueError(f"{self.get_device_key('Name',index)} cannot be added. Your list of selected items is full")
        
    def remove_device(self, position):
        del self.selected_list[position]
        return self.selected_list
        
    
    def hot_key_swap(self):
        pass
    
    def install_preq(self):
        pass
        #To DO
    
    def generate_pws(self):
        if self(self.selected_list) == 2:
            file_name = "swapper.ps1"

            # Otevřete soubor pro zápis
            with open(file_name, "w") as file:
                # Zde můžete provádět zápis do souboru
                file.write("# Toto je váš PowerShell skript.\n")
                file.write("$headset = ") + self.selected_list[0] + ("\n")
                file.write("$speakers = ") + self.selected_list[1] + ("\n")
                file.write("Write-Host $variable\n")
                # $headset_id = Get-AudioDevice -id $headset

                # if ($headset_id.default){
                #     Set-AudioDevice -id $speakers
                #     Write-Output 'Speakers Active'
                # }
                # else{
                #     Set-AudioDevice -id $headset
                #     Write-Output 'Headset Active'
                # }

            # Soubor je automaticky uzavřen po opuštění bloku 'with'

            print(f"Soubor {file_name} byl vytvořen/upraven a uložen.")
        else:
            raise ValueError(f"{self.selected_list} does not contain 2 items")

        
            
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
        

e = SetupStuff()
e.get_list()
e.convert_list()
print("konec")