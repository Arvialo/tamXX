#!/usr/bin/env python3
import sys
class Help:
    def usageOff():
        print("""
        tamXX Tool :\n
        [OPTIONS] :
        \t\t-l , --listen\t\t\t-     listen on [host]:[port] for incoming connections
        \t\t--target [IP]\t\t\t-     target
        \t\t-p , --port [PORT]\t\t\t-     port
        \t\t--prompt\t\t\t-     initialize prompt
        \t\t-h , --help\t\t\t-     get some help ;)
        """)
        sys.exit()
    def usageOn():
        print("""
            WE ARE ON ! WHAT CAN I DO ?
            [OPTIONS] :
            \t\tFirst, you can execute almost same commands like real shell!
            \t\thelp\t\tget some help ;)
            \t\tsuid\t\tget all suid binaries !
            \t\tlinpeas\t\tupload linpeas.sh on machine
            \t\tshell\t\tget full interactive shell
            """)
        
