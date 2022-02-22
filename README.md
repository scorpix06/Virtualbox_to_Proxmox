
# VirtualBox to Proxmox  

A simple python script that migrate your VirtualBox VM to your Proxmox hypervisor




## Authors

- [@scorpix06](https://www.github.com/scorpix06)


## Installation on Linux

To deploy this project run

```bash
  git clone https://github.com/scorpix06/Virtualbox_to_Proxmox.git
  cd Virtualbox_to_Proxmox
  pip3 install -r requirements.txt
```

## Installation on Windows

To deploy this project make sure python and  pip is installed on your computer then download the source code here :
https://github.com/scorpix06/Virtualbox_to_Proxmox/archive/refs/heads/main.zip

## Documentation

[Documentation](https://linktodocumentation)


## How to use

After your installation done change the variables in settings.py file  with your own informations.

The informations needed by the script is

- Proxmox hypervisor IP
- Proxmox SSH port (default is 22)
- An account on proxmox with right to create VM's (The settings.py contain only username, the pass is asked when you run the script)
- A VM id not used on the Proxmox
