
# VirtualBox to Proxmox  

A simple python script that migrate your VirtualBox VM to your Proxmox hypervisor




## Authors

- [@scorpix06](https://www.github.com/scorpix06)


## Installation on Linux

To deploy this project run this :

```bash
  git clone https://github.com/scorpix06/Virtualbox_to_Proxmox.git
  cd Virtualbox_to_Proxmox
  pip3 install -r requirements.txt
```

## Installation on Windows

To deploy this project make sure python 3 and  pip is installed on your computer then download the source code here :
https://github.com/scorpix06/Virtualbox_to_Proxmox/archive/refs/heads/main.zip
open the projet in cmd an run

```bash
  py -m pip install -r requirements.txt

```


## How to use

After your installation done, change the variables in settings.py file  with your own informations.

The informations needed by the script is

- ova file path on your computer
- Proxmox hypervisor IP
- Proxmox SSH port (default is 22)
- An account on proxmox with right to create VM's (The settings.py contain only username, the pass is asked when you run the script)
- A VM id not used on the Proxmox

## Roadmap 

- Automatic VM id detection
- windows executable version
- Automatic storage detection
