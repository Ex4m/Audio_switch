
#%%

import subprocess as sb
import re
import ctypes
import sys
from  dataclasses import dataclass, field
import time


@dataclass
class SetupStuff:
    result: str = None
    confirm_list: set = ("y", "yes", "yeah", "ok", ".")
    device_data: list = field(default_factory=list) 
    device_dict: dict = field(default_factory=dict)
    selected_list: list = field(default_factory=list)
    check: bool = None
   
    
    def confirm(self, value):
        if value.lower() in self.confirm_list:
            return True
        
    def get_list(self):
        self.result = sb.run(["powershell", "Get-AudioDevice -list"], capture_output=True, text=True)
        if self.result.returncode == 0:
            self.result = str(self.result.stdout.strip())
            print(self.result)
        return self.result
        
       
       
    def convert_list(self):   
        """Converts powershell script to python readable format
        """
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
        """From parsed list returns values based on index of the item

        Args:
            value (str): Key for value. i.e. Name, ID
            index (str): Index of the item, i.e. 1, 2, 5 

        Raises:
            TypeError: Prerequisites missing

        Returns:
            str: value of selected key and index of the parsed list
        """
        if self.device_dict is None:
            raise TypeError("origin dictionary is not created, try use .get_list ->.convert_list first")

        device_info = self.device_dict.get(index)
        if device_info is not None:
            return device_info[value]
        else:
            return None
        
    
    def add_device(self, *index):
        """Add devices to selected_list for export to powershell execution file

        Raises:
            ValueError: list can contain only 2 items at time

        Returns:
            list: list of selected items choosen for export to pws
        """
        for i in index:
            device_info = self.get_device_key("ID", i)
            if len(self.selected_list) < 2:
                self.selected_list.append(device_info)
            else:
                raise ValueError(f"{self.get_device_key('Name',i)} cannot be added. Your list of selected items is full")
        return self.selected_list
        
        
    def remove_device(self, position):
        """Remove device from the selected_list

        Args:
            position (int): position of the item in a list you want to remove starting from 0

        Returns:
            list: list of selected items choosen for export to pws
        """
        del self.selected_list[position]
        return self.selected_list
        
    
    def hot_key_swap(self):
        pass
    
    def is_module_installed(self):
        """Check whenever the AudioDevice Module is already installed or not
        
        Returns:
        Bool : False -> Not installed, run install_preq
        True -> Installed, you can proceed to get list and stuff
        """
        output = sb.run(["powershell", "Get-InstalledModule"], capture_output=True, text=True)
        print(output.stdout)
        if len(re.findall('AudioDeviceCmdlets', output.stdout)) > 0:
            self.check = True
            print("Module is installed")
        else:
            self.check = False
            print("Module is not Installed")
    
    def pws_command(self, command, admin = False):
        if admin == True:
            result = sb.run(["runas", "/user:Administrator"] + command, capture_output=True, text=True)
        else:
            result = sb.run(command, capture_output=True, text=True)
        print(result)
        return result
        
    
    def get_script_policy(self):
        command = ["powershell","Get-ExecutionPolicy"]
        self.pws_command(command)
        options ="""
Restricted: Skripty nejsou povoleny a lze spouštět pouze příkazy.
AllSigned: Skripty mohou být spuštěny pouze tehdy, pokud jsou podepsány důvěryhodným vydavatelem.
RemoteSigned: Lokální skripty mohou být spuštěny bez podpisu, ale skripty stažené z internetu musí být podepsány důvěryhodným vydavatelem.
Unrestricted: Všechny skripty mohou být spuštěny bez omezení."""
        print(options)
        
    def set_script_policy(self):
        options = input("What type of script policy you would like to choose")
        match options:
            case "Restricted":
                print("Restricted policy selected")
            case "AllSigned":
                print("AllSigned policy selected")
            case "RemoteSigned":
                print("Remote Signed policy selected")
            case "Unrestricted":
                print("Unrestricted  policy selected")    
            case _:
                print("Please select one of the policies")
                
        command = ["powershell",f"Set-ExecutionPolicy {options} -Scope CurrentUser -Force"]

        result = self.pws_command(command)
        if (result.stderr or result.stdout) is (None or ""):
            print(f"Policy changed to '{options}'") 
        else:
            print(f"Something has broke {result.stderr},{result.stdout}")
        
    def install_preq(self):
        """Install the powershell module AudioDeviceCmdlets which allows manipulation with audiodevices.
        Install Module -> Set Script Policy to RemoteSigned -> Converts list to Python readable format

        Raises:
            ValueError: _description_
        """
        self.is_module_installed()
        if self.check is None:
            raise ValueError("First you need to check if the module is installed or not, run 'is_module_installed'")
        elif self.check == False:
            try:
                print("Installing ...")
                command = ["powershell", "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"]
                self.pws_command( command)
                print("Installing ... 17%")
                command = ["powershell", "Install-Module -Name AudioDeviceCmdlets -Force -Scope CurrentUser"]
                self.pws_command( command)
                print("Installing ... 42%")
                self.get_list()
                print("Installing ... 68%")
                self.convert_list()
                print("Installing ... 100%") 
            except Exception as error:
                print(error)
            finally:
                self.is_module_installed()
        else:
            print("Module is already installed you can proceed to other operations")
    
    
    def uninstall_preq(self):
        inp = input("Do you want to uninstall Powershell AudioDevice Module (y/n): ")
        if self.confirm(inp) == True:
            command = ["powershell", "Uninstall-Module -Name AudioDeviceCmdlets -Force"]
            result = sb.run(command, capture_output=True, text=True)
            print(result)
        self.is_module_installed()
        if self.check == False:
            print("Module was sucesfully uninstalled")
        
    
    def generate_pws(self):
        """ Generate a pws file which is execution script for device swap
        """
        if len(self.selected_list) == 2:
            output_file = "swapper.ps1"
            headset = self.selected_list[0]
            speakers = self.selected_list[1]

            # Vytvořte text skriptu
            script_text = f"""\
            ###### Swapper.Core #######
            $headset = '{headset}'
            $speakers = '{speakers}'

            $headset_id = Get-AudioDevice -id $headset

            if ($headset_id.default) {{
                Set-AudioDevice -id $speakers
                Write-Output 'Speakers Active'
            }} else {{
                Set-AudioDevice -id $headset
                Write-Output 'Headset Active'
            }}
            """

            with open(output_file, "w") as file:
                file.write(script_text)

            print(f"Soubor {output_file} byl vytvořen.")
        else:
            raise ValueError(f"{self.selected_list} does not contain 2 items")

        
            
    def run_as_admin(self):
        """Run a function as an admin
        """
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
        

e = SetupStuff()
# e.get_list()
# e.convert_list()
# e.install_preq()
# e.is_module_installed()
print("konec")