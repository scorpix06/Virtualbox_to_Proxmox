
from paramiko import SSHClient
from scp import SCPClient
from pathlib import Path
import settings
import sys
import os

class vboxToProxmox():

    def __init__(self, ovaPath, pveIP, pvePort, pveLogin, pvePass):
        #self.vboxPath = "C:\\Program Files\\Oracle\VirtualBox"
        self.ovaPath = Path(ovaPath)
        self.ovaName = os.path.basename(self.ovaPath)
        self.pveIp = pveIP
        self.pveLogin = pveLogin
        self.pvePass = pvePass

        self.run()

    def run(self):
        self.connection()
        #self.sendOva()
        self.unzipOva()

    def connection(self):
        print("[*] Connecting to host")
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.connect(self.pveIp, 22, self.pveLogin, self.pvePass, timeout=20)

    def sendOva(self):

        def progress(filename, size, sent):
            sys.stdout.write("%s's progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )
       
        print("[*] Uploading OVA")
        scp = SCPClient(self.ssh.get_transport(), progress=progress)
        scp.put(self.ovaPath)
        print("\n [*] OVA uploaded")

        
    def unzipOva(self):
        print("[*] Unzipping the ova")
        command = "mkdir ovascript && mv {} ./ovascript && cd ovascript && tar -xvf {}".format(self.ovaName)
        stdin, stdout, stderr = self.ssh.exec_command(command)
        print("[*] OVA Unzipped")
        print(stderr)



if __name__ == "__main__":        
    vboxToProxmox(
        settings.ovaPath,
        settings.ipProxmox,
        settings.sshPort,
        settings.loginProxmox,
        settings.passProxmox,
        )