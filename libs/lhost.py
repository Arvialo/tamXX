#!/usr/bin/env python3

import sys
import socket
import readline
import subprocess

class Lhost:

    def binding(target,port):
        if not len(target):
           target = "0.0.0.0"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((target,port))
        except OSError:
            print("Ce port est déjà/encore en cours d'utilisation ! ")
            sys.exit( )
        s.listen(1)
        print("Listening : [%s]:[%s]"%(target,port))
        conn, addr = s.accept()
        return conn,addr

    def args(args):
        listArgs = " ".join(args[1:]).split('-')
        while ("" in listArgs):
            listArgs.remove("")
        newListArgs = []
        for arg in listArgs:
            arg = arg.replace(' ','%')
            newListArgs.append(arg)
        return newListArgs

    def getDir():
        getDir = "ls"
        out = subprocess.getoutput(getDir)
        list = out.split('\n')

        def completer(text, state):
            options = [cmd for cmd in list if cmd.startswith(text)]
            if state < len(options):
                return options[state]
            else:
                return None

        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer)

    def init():
        home = subprocess.getoutput('pwd')
        user = subprocess.getoutput('whoami')
        if user != 'root':
            tag = "$"
        else:
            tag = "#"
        return home,user,tag
