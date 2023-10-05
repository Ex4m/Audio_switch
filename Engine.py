
#%%

import subprocess as sb
import re
import ctypes
import sys
from  dataclasses import dataclass, field
import time
import os
import pickle
from pynput.keyboard import Key

@dataclass
class SetupStuff:
    result: str = None
    confirm_list: set = ("y", "yes", "yeah", "ok", ".")
    device_data: list = field(default_factory=list) 
    device_dict: dict = field(default_factory=dict)
    selected_list: list = field(default_factory=list)
    check: bool = None
   
    
    def _confirm(self, value):
        if value.lower() in self.confirm_list:
            return True
        
    def get_list(self, display_output = True):
        self.result = sb.run(["powershell", "Get-AudioDevice -list"], capture_output=True, text=True)
        if self.result.returncode == 0:
            self.result = str(self.result.stdout.strip())
            if display_output:
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
        self.get_list(False)
        self.convert_list()
        for i in index:
            device_info = self.get_device_key("ID", i)
            if len(self.selected_list) < 2:
                self.selected_list.append(device_info)
            else:
                raise ValueError(f"{self.get_device_key('Name',i)} cannot be added. Your list of selected items is full")
        return self.selected_list
        
        
    def remove_device(self, position):
        """Remove device from the selected_list. 0,1 choose position to delete or 2 to delete all

        Args:
            position (int): position of the item in a list you want to remove starting from 0

        Returns:
            list: list of selected items choosen for export to pws
        """
        if position == 2:
            self.selected_list.clear()
        else:
            del self.selected_list[position]
        return self.selected_list
        
    
    def set_hotKey_swap(self):
        inp_key = input("Your Key: ")
        if isinstance(inp_key, Key):
            with open('settings.pkl', 'wb') as f:
                pickle.dump(inp_key, f)
                print("Exported and saved")
        else:
            raise TypeError(f"Your key '{inp_key}' was not recogniyed")   
        
    def get_hotKey_swap(self):
        #toto by mohla využívat podclassa v tom lightweight souboru aby si natáhla co je potřeba
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
            print("Audio Module is installed")
        else:
            self.check = False
            print("Audio Module is not Installed")
    
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
                print("Installing ... 35%")
                command = ["powershell", "Install-Module ps2exe -Force -Scope CurrentUser"]
                self.pws_command( command)
                print("Installing ... 48%")
                self.get_list(False)
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
        if self._confirm(inp):
            try:
                command = ["powershell", "Uninstall-Module -Name AudioDeviceCmdlets -Force"]
                self.pws_command( command)
                command = ["powershell", "Uninstall-Module ps2exe -Force"]
                self.pws_command( command)
            except Exception as error:
                print(error)
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
            
            self._convert_to_exe()
        else:
            raise ValueError(f"{self.selected_list} does not contain 2 items")

    def _convert_to_exe(self):
        """Converts ps1 script to executable

        Raises:
            NameError: Module ps2exe is not installed and is required to proceed
        """
        command = ["powershell", "Get-InstalledModule"]
        result = self.pws_command(command)
        if len(re.findall('ps2exe', result.stdout)) < 0:
            raise NameError("ps2exe module is not installed, run install_preq")
        current_directory = os.getcwd() 
        print(current_directory)
        try:
            command = ["powershell", f"Invoke-PS2EXE '{current_directory}\swapper.ps1' '{current_directory}\SuperSwapper.exe'"]  
            self.pws_command(command)
        except Exception as error:
            print(error)
        else:
            print("File was converted to .exe sucessfully")
        
            
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
        

# e = SetupStuff()
# e.get_list()
# e.convert_list()
# e.install_preq()
# e.uninstall_preq()
# e.is_module_installed()
print("konec")


# if __name__ == "__main__":
#     audio_manager = SetupStuff()
#     audio_manager.run_as_admin()

#     while True:
#         print("\nAudio Device Manager Menu:")
#         print("1. Get Audio Device List")
#         print("2. Add Audio Device to Selected List")
#         print("3. Remove Audio Device from Selected List")
#         print("4. Generate PowerShell Script")
#         print("5. Install PowerShell Module")
#         print("6. Uninstall PowerShell Module")
#         print("7. Exit")

#         choice = input("Enter your choice: ")

#         match choice:
#             case "1":
#                 audio_manager.get_list()
#                 audio_manager.convert_list()
#                 print("Audio Device List retrieved.")
#             case "2":
#                 indices = input("Enter the indices of the audio devices to add (comma-separated): ").split(",")
#                 audio_manager.add_device(*map(int, indices))
#             case "3":
#                 position = int(input("Enter the position of the audio device to remove (0 for first, 1 for second, 2 for all): "))
#                 audio_manager.remove_device(position)
#             case "4":
#                 audio_manager.generate_pws_script()
#             case "5":
#                 audio_manager.install_module()
#             case "6":
#                 audio_manager.uninstall_module()
#             case "7":
#                 print("Exiting...")
#                 break
#             case _:
#                 print("Invalid choice. Please select a valid option.")
