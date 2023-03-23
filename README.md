# windows-php-switcher
PHP Switcher is a simple tool that allows you to switch between php versions by modifying the system environment variable "PATH" to tell windows where the disired php is.

- [Installation](#Installation)
- [Requirements](#Requirements)
- [Configration](#Configration)
- [Config Notes](#config-notes)
- [Usage](#Usage)


# Installation
-	clone the repo

		git clone https://github.com/maged909/windows-php-switcher.git

-	changes the current directory to windows-php-switcher

		cd windows-php-switcher
		
-	install python requirements

		pip install -r requirements.txt

# Requirements
	
	colorama==0.4.6
	tabulate==0.9.0

# Configration
Go to config.js and add the php versions you want with their absolute path
here's an example

	{
    "php7.3": {
        "selection": "1", 
        "path": "C:\\xampp\\php"
    },
    "php8.2.3": {
        "selection": "2",
        "path": "C:\\xampp\\php823"
    }
	}
	
here i have two php versions php7.3 and php8.2.3 each one with their selection that would show in menu and their path that would be used in the environment variable
i'm here using php in my xampp folder but you can point to wherever you have the php 

# Config Notes
- each php version must have selection and path
- selection must be unique for each php version
- path must be a valid absolute path to the php folder not file and cannot contain ";"
	
	
# Usage
to use it just run the phpSwitcher.py on a terminal that has an adminstrator permissions

	python phpSwitcher.py
	
keep in mind that the script would ask for primission that's just coz it needs that to modify the system environment variable "PATH"


![program picture](https://github.com/maged909/windows-php-switcher/blob/main/program%20screenshot.jpg)

