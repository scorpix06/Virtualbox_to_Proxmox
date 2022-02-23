
from re import S
from paramiko import SSHClient, ssh_exception 
from scp import SCPClient
from pathlib import Path
import settings
import sys
import os
import time
import getpass

class vboxToProxmox():

    def __init__(self, ovaPath, pveIP, pvePort, pveLogin, pvePass, storage, vmId=0):
        #self.vboxPath = "C:\\Program Files\\Oracle\VirtualBox"
        self.ovaPath = Path(ovaPath)
        self.ovaName = os.path.basename(self.ovaPath)
        self.pveIp = pveIP
        self.pveLogin = pveLogin
        self.pvePass = pvePass
        self.vmId = int(vmId)
        self.storageDisk = storage

        self.run()

    def run(self):
        self.connection()
        self.checkVmId()
        #self.sendOva()
        #self.unzipOva()
        #self.createVM()
        #self.deleteFiles()

    def connection(self):
        print("[$] Connecting to the Proxmox Hypervisor")

        try:
            self.ssh = SSHClient()
            self.ssh.load_system_host_keys()
            self.ssh.connect(self.pveIp, 22, self.pveLogin, self.pvePass, timeout=10)

        except ssh_exception.AuthenticationException:
            print("Authentification error, make sur your username and password is right and allowed to connect in SSH")

        except Exception:
            print("Impossible to connect to the Proxmox hypervisor, make sur the SSH port and IP is right")

    def sendOva(self):

        def progress(filename, size, sent):
            sys.stdout.write("%s's progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )
       
        print("[$] Uploading OVA")
        scp = SCPClient(self.ssh.get_transport(), progress=progress)
        self.ssh.exec_command("mkdir ovascript")
        scp.put(self.ovaPath, "./ovascript/{}".format(self.ovaName))
        print("\n [$] OVA uploaded")

        
    def unzipOva(self):
        print("[$] Unzipping the ova")
        command = "cd ./ovascript && tar -xvf {}".format(self.ovaName)
        stdin, stdout, stderr = self.ssh.exec_command(command)
        print("[$] OVA Unzipped")
        print(stdout.readlines())

    def createVM(self):
        print("[$] Creating the VM")
        importOvfCommand = "cd ~/ovascript && qm importovf {} *.ovf {}".format(self.vmId, self.storageDisk)
        importDiskCommand = "cd ~/ovascript && qm importdisk {} *.vmdk {}".format(self.vmId, self.storageDisk)

        print("[$] Importing ovf file")
        stdin, stdout, stderr = self.ssh.exec_command(importOvfCommand)
        time.sleep(5)
        print("[$] Importing VM disk")
        stdin, stdout, stderr = self.ssh.exec_command(importDiskCommand, get_pty=True)

        # For stream of the ssh output
        for line in iter(stdout.readline, ""):
            print(line, end="")

    def deleteFiles(self):
        command = "rm -R ~/ovafile"
        stdin, stdout, stderr = self.ssh.exec_command(command, get_pty=True)

    def checkVmId(self):
        """ Check if VM id given by user is available and if user do not give vm id find availaible Vm id """

        vmList = []
        command = "cat /etc/pve/.vmlist"
        stdin, stdout, stderr = self.ssh.exec_command(command)
        out = stdout.readlines()

        for vm in out:
            begin = vm.find('"')
            end = vm.find('"', 2)
            vmId = vm[begin + 1:end]
            try: 
                vmId = int(vmId)
                vmList.append(int(vmId))
            except:
                pass
        
        if self.vmId == 0:
            self.vmId = max(vmList) + 1
        elif isinstance(self.vmId, int) == False:
            print("[$] The VM ID you choose is not a number, the VM id will be choose automaticly")
            self.vmId = max(vmList) + 1
        elif int(self.vmId) in vmList:
            while self.vmId in vmList:
                newId = input("The VM ID you choose is already taken, please enter an available ID :")
                if newId not in vmList:
                    try:
                        self.vmId = int(newId)
                    except:
                        print("Please enter a valid VM ID")
                elif newId == "":
                    self.vmId = max(vmList) + 1

if __name__ == "__main__":


    ovaPath = settings.ovaPath
    proxmoxIp = settings.ipProxmox
    sshPort = settings.sshPort
    username = settings.loginProxmox
    password = getpass.getpass(prompt='Password of {} user : '.format(username))
    vmId = input("Choose a VM id : ")
    if vmId == "":
        vmId = 0
    storageDisk = settings.diskStorage      
    
    vboxToProxmox(
        ovaPath,
        proxmoxIp,
        sshPort,
        username,
        password,
        storageDisk,
        vmId=vmId,
        )