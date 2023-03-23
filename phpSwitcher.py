import os,re,winreg,json,ctypes,sys
from tabulate import tabulate
from colorama import init, Fore,Back, Style
# Initialize colorama
init()

errorColoring = Fore.WHITE + Back.RED
docs = 'https://github.com/maged909/windows-php-switcher'
configGuideUrl = "https://github.com/maged909/windows-php-switcher/blob/main/README.md#config-notes"

# Define constants from the Windows API
ASADMIN = 'asadmin'
if sys.argv[-1] != ASADMIN:
    # Re-run the script with administrator permissions
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    sys.exit(0)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
def configGuide():
    print(errorColoring + f"Check Our Config Guide on the documentaions: {configGuideUrl} " + Style.RESET_ALL)
    

if not is_admin():
    print(errorColoring + "Error: Access Denied, make sure to run the program as an Adminstrator for it to be able to edit system environment variables" + Style.RESET_ALL)
    input('')
    sys.exit(0)
    

# Load the contents of the JSON file into a dictionary
with open('config.json', 'r') as file:
    php_versions = json.load(file)
    
validConfig=False
if os.path.exists('config.json'):
    validationFailed = False
    # Check that the dictionary has the expected structure
    expected_keys = {"selection", 'path'}
    for key in php_versions:
        if not isinstance(php_versions[key], dict) or set(php_versions[key].keys()) != expected_keys:
            print(errorColoring + "Config Error: 'config.json' has an invalid structure. key {} must have 'path' and 'selection' keys." + Style.RESET_ALL)
            configGuide()
            validationFailed = True
        if not validationFailed:
            if php_versions[key]['selection'] == 'ext':
                print(errorColoring + "Config Error: selection for {} equals 'ext' which is a reserved value and cannot be used for 'selection'.".format(key)+ Style.RESET_ALL)
                configGuide()
                validationFailed = True
            if not os.path.isabs(php_versions[key]['path']):
                print(errorColoring + "Config Error: 'path' value for '{}' is not a vaild absolute path.".format(key)+ Style.RESET_ALL)
                configGuide()
                validationFailed = True
            if re.search(r';', php_versions[key]['path']):
                print(errorColoring + "Config Error: 'path' value for '{}' contains ';' character.".format(key)+ Style.RESET_ALL)
                configGuide()
                validationFailed = True
    if not validationFailed:
        # Check that there are no duplicate values in any key or value
        flat_values = []
        for key, value in php_versions.items():
            flat_values.extend(list(value.values()) + [key])
        if len(set(flat_values)) != len(flat_values):
            print(errorColoring + "Error: 'config.json' contains duplicate values."+Style.RESET_ALL)
            configGuide()
        else:
            validConfig = True
else:
    print(errorColoring + "Error: MISSING 'config.json' - does not exist in the current directory."+Style.RESET_ALL)
    configGuide()

if validConfig:
    # Add a new key-value pair to the dictionary
    php_versions[""] = {"selection": "ext", "path": ""}

    # Convert the dictionary to a list of lists
    table_data = [[config["selection"], version, config["path"]] for version, config in php_versions.items()]


    # Get the current value of the PATH variable
    path_value = os.environ.get("PATH", "")

    # Get a list of available PHP versions
    version_numbers = [php_versions[key]["selection"] for key in php_versions]

    # Check if the current PHP version is in the PATH variable
    php_version = "unknown"
    for version, config in php_versions.items():
        if config["path"]+";" in path_value:
            php_version = version
            break

    # get banner
    with open('banner.txt', encoding='utf-8') as file:
        file_contents = file.read()

    while True:
        os.system('cls')
        print(Fore.BLUE +Style.BRIGHT + "Repo: " + docs + Style.RESET_ALL)
        print(file_contents)

        print(f" ----- PHP version: {Fore.GREEN +Style.BRIGHT + php_version + Style.RESET_ALL} -----")

        # Print the table
        print(tabulate(table_data, headers=["Selection", "Version", "Path"], tablefmt="heavy_grid"))

        # Set the path to the PHP version you want to switch to
        selection = input("\n select : ")

        if selection == 'ext':
            break
        elif selection in version_numbers:
            selected_version = [key for key in php_versions if php_versions[key]["selection"] == selection][0]
            new_path = php_versions[selected_version]["path"]
            php_version = selected_version
        else:
            continue

        # Get the environment variable registry key
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment", 0, winreg.KEY_ALL_ACCESS)

        # Get the current value of the PATH variable
        path_value = winreg.QueryValueEx(key, "PATH")[0]

        # Split the path value into a list of directories
        path_dirs = path_value.split(";")

        # Check if the new PHP path is already in the PATH variable
        if new_path not in path_dirs:
            # Replace the old PHP path with the new one
            path_dirs = [p for p in path_dirs if not p.startswith("C:\\xampp\\php")]
            path_dirs.insert(0, new_path)

            # Join the path directories back into a single string
            new_path_value = ";".join(path_dirs)

            # Update the PATH variable in the registry
            winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path_value)

            # Update the PATH variable in the current process environment
            os.environ["PATH"] = new_path_value

        # Close the registry key
        winreg.CloseKey(key)
input('')