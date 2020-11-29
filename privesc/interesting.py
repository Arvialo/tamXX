#!/usr/bin/env python3

import os,sys
import pwd, grp

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

def zeroRights(nbr,perm,permission):
    if permission == "7":
        perm+= "rwx"
    elif permission== "6":
        perm+= "rw-"
    elif permission == "5":
        perm+= "r-x"
    elif permission == "4":
        perm+="r--"
    elif permission == "3":
        perm+= "-wx"
    elif permission == "2":
        perm+="-w-"
    elif permission == "1":
        perm+="--x  "
    elif permission == "0":
        perm+='---'
    return perm


def main():
    paths = ('/var','/tmp','/home','/opt','/etc','/usr','/root')
    exts = ('.txt','.py','.html','.php','.php5','.phtml','php4','.xml','.js')
    names = ["database","DataBase","DATABASE","UserName","Username","username","User","user","Name","name","pass","password","data","db","dbpass","dbPass","flag","Flag","FLAG","passwd",
    "shadow","Passwd","DB","ssh","id_rsa","id_rsa.pub",'linpeas','privesc','getUser']

    filename(paths,exts,names)
    content()

def filename(paths,exts,files):
    """
    COLOR
    """
    blue = "\033[0;94m"
    red = "\033[0;91m"
    green = "\033[0;35m"

    print("INTERESTING FILENAMES ...")
    for path in paths:
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                for file in files:
                    nb=0
                    perm=""
                    if file == filename:
                        name = dirpath+'/'+filename


                        st =     os.stat(name)
                        ownername = pwd.getpwuid(st.st_uid).pw_name
                        groupname = grp.getgrgid(st.st_gid)[0]


                        try:
                            permission = oct(os.stat(name).st_mode)[-4:]
                        except:
                            pass
                        firstPerm,permission = permission[0],permission[1:]
                        name = dirpath+"/"+red+filename
                        if firstPerm == "4":
                            for p in permission:
                                nb+=1
                                perm=fourRights(nb,perm,p)
                                permi=perm
                            print(blue+perm+'\t\t'+green+ownername+" "+groupname+'\t\t'+name)
                        elif firstPerm == "6":
                            for p in permission:
                                nb+=1
                                perm=sixRights(nb,perm,p)
                                permi=perm
                            print(blue+perm+'\t\t'+green+ownername+" "+roupname+'\t\t'+name)
                        elif firstPerm == "0":
                            for p in permission:
                                nb+=1
                                perm=zeroRights(nb,perm,p)
                                permi=perm
                            print(blue+perm+'\t\t'+green+ownername+' '+groupname+'\t\t'+name)
                for file in files:
                    perm=""
                    nb=0
                    for ext in exts:
                        f = file+ext
                        if f == filename:
                            name = dirpath+"/"+filename
                            try:
                                permission = oct(os.stat(name).st_mode)[-4:]
                            except:
                                pass
                            firstPerm,permission = permission[0],permission[1:]
                            name = dirpath+"/"+red+filename
                            if firstPerm == "4":
                                for p in permission:
                                    nb+=1
                                    perm=fourRights(nb,perm,p)
                                    permi=perm
                                print(blue+perm+'\t\t'+green+ownername+' '+groupname+'\t\t'+name)
                            elif firstPerm == "6":
                                for p in permission:
                                    nb+=1
                                    perm=sixRights(nb,perm,p)
                                    permi=perm
                                print(blue+perm+'\t\t'+green+ownername+' '+groupname+'\t\t'+name)
                            elif firstPerm == "0":
                                for p in permission:
                                    nb+=1
                                    perm=zeroRights(nb,perm,p)
                                    permi=perm
                                print(blue+perm+'\t\t'+green+ownername+' '+groupname+'\t\t'+name)


def content():
    paths = ('/var','/home')
    names = ['database','password','username']
    print("\n\nINTERESTING CONTENT ...\n")
    """
    COLOR
    """
    blue = "\033[0;94m"
    red = "\033[0;91m"
    green = "\033[0;35m"
    colorOff= "\033[0m"
    for path in paths:
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                absPath = os.path.join(dirpath,filename)
                try:
                    f=open(absPath,"r")
                    content=f.readline()
                    content = content.split(' ')
                    for name in names:
                        if name in content:
                            nb = content.index(name)
                            before = nb-1
                            after = nb+3
                            content = content[before:after]
                            content = " ".join(content)
                            content = content.replace(name,red+name+colorOff)
                            print(blue+absPath+colorOff+"\t\t\t"+content)
                except PermissionError:
                    pass
                except:
                    pass

if __name__ == "__main__":
    main()
