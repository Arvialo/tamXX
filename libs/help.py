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
            \t\tlinpeas\t\tupload linpeas.sh on machine
            \t\tshell\t\tget full interactive shell
            \t\tupload\t\tupload file into machine
            \t\t\t\t(ex : upload <fileSource> <fileDestination>
            \t\t\t\t      files available : suid.py, suid2.py)
            """)
