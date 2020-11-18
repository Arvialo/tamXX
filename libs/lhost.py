#!/usr/bin/env python3

import sys
import socket
import readline

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
