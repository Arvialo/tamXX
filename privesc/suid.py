#!/usr/bin/env python3

import os, sys
import pwd,grp

def fourRights(nbr,perm,permission):
    if permission == "7":
        if nbr == 1:
            perm+= "rws"
        else:
            perm+= "rwx"
    elif permission== "6":
        perm+= "rw-"
    elif permission == "5":
        if nbr == 1:
            perm+= "r-s"
        else:
            perm+= "r-x"
    elif permission == "4":
        perm+="r--"
    elif permission == "3":
        if nbr == 1:
            perm+= "-ws"
        else:
            perm+= "-wx"
    elif permission == "2":
        perm+="-w-"
    elif permission == "1":
        if nbr == 1:
            perm+="--s"
        else:
            perm+= "--x"
    elif permission == "0":
        perm+='---'
    return perm
def sixRights(nbr,perm,permission):
    if permission == "7":
        if nbr == 1 or nbr == 2:
            perm+= "rws"
        else:
            perm+= "rwx"
    elif permission== "6":
        perm+= "rw-"
    elif permission == "5":
        if nbr == 1 or nbr == 2:
            perm+= "r-s"
        else:
            perm+= "r-x"
    elif permission == "4":
        perm+="r--"
    elif permission == "3":
        if nbr == 1 or nbr == 2:
            perm+= "-ws"
        else:
            perm+= "-wx"
    elif permission == "2":
        perm+="-w-"
    elif permission == "1":
        if nbr == 1 or nbr == 2:
            perm+="--s"
        else:
            perm+="--x  "
    elif permission == "0":
        perm+='---'
    return perm

def gtfobins(path):
    gtResult = ""
    vulnPaths="apt-get,apt,aria2c,arp,ash,awk,base32,base64,bash,bpftrace,bundler,busctl,busybox,byebug,cancel,capsh,cat,chmod,chown,chroot,cobc,composer,cowsay,cowthink,cp,cpan,cpulimit,crash,crontab,csh,curl,cut,dash,date,dd,dialog,diff,dmesg,dmsetup,dnf,docker,dpkg,easy_install,eb,ed,emacs,env,eqn,expand,expect,facter,file,find,finger,flock,fmt,fold,ftp,gawk,gcc,gdb,gem,genisoimage,ghc,ghci,gimp,git,grep,gtesterhd,head,hexdump,highlight,iconv,iftop,ionice,ip,irb,js,journalctl,jq,runscript,ksh,ksshell,ld.so,ldconfig,less,logsave,look,>ltrace,lua,lwp-download,lwp-request,mail,make,man,mawk,more,mount,mtr,mv,mysql,nano,nawk,nc,nice,nl,nmap,node,nohup,nroff,nsenter,od,openssl,pdb,perl,pg,php,pic,pico,pip,pkexec,pry,puppet,python,rake,readelf,red,redcarpet,restic,rlogin,rlwrap,rpm,rpmquery,rsync,ruby,run-mailcap,run-parts,rview,rvim,scp,screen,script,sed,service,setarch,sftp,shuf,slsh,smbclient,socat,soelim,sort,sqlite3,ssh,start-stop-daemon,stdbuf,strace,strings,su,sysctl,systemctl,tac,tail,tar,taskset,tclsh,tcpdump,tee,telnet,tftp,time,timeout,tmux,top,ul,unexpand,uniq,unshare,update-alternatives,uudecode,uuencode,valgrind,vi,view,vim,watch,wget,whois,wish,xargs,xxd,xz,yelp,yum,zip,zsh,zsoelim,zypper"
    vulnPaths=vulnPaths.split(',')
    for vulnPath in vulnPaths:
        if path == vulnPath:
            gtResult = "\033[33m {0}\x1b[0m\n".format(path)
    return gtResult

def main():
    print("ok")
    binaryPaths = ('/')
    print("""\033[32mColor Code :\x1b[0m
        \033[0;94m Blue Color : setuid + setgid
        \033[0;91m Red Color : setuid
    """)
    print("\033[0;35m Finding/Listing all SUID Binaries ..")
    for binaryPath  in binaryPaths:
        gtResult = ""
        for rootDir,subDirs,subFiles in os.walk(binaryPath):
            for subFile in subFiles:
                perm=""
                nb=0
                absPath = os.path.join(rootDir,subFile)
                try:
                    permission = oct(os.stat(absPath).st_mode)[-4:]
                    specialPermission = permission[0]
                except:
                    pass
                try:
                    if int(specialPermission) >= 4:

                        st = os.stat(absPath)
                        ownername = pwd.getpwuid(st.st_uid).pw_name
                        groupname = grp.getgrgid(st.st_gid)[0]

                        if subFile not in gtResult:
                            gtResult+=gtfobins(subFile)
                        firstPerm,permission = permission[0],permission[1:]
                        if firstPerm == "4":
                            for p in permission:
                                nb+=1
                                perm=fourRights(nb,perm,p)
                                permi=perm
                            print("\033[0;91m"+perm+"\t\t"+ownername+" "+groupname+"\t\t"+absPath)
                        elif firstPerm == "6":
                            for p in permission:
                                nb+=1
                                perm=sixRights(nb,perm,p)
                                permi=perm
                            print("\033[0;94m"+perm+"\t\t"+ownername+" "+groupname+"\t\t"+absPath)

                except:
                    pass
    print("\n\n\n\033[32mPOTENTIAL PRIVILEGE ESCALATION (based on gtfobins' binaries) :\x1b[0m\n{0}".format(gtResult))
if __name__ == "__main__":
    main()
