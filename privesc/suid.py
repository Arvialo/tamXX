#!/usr/bin/env python3

import os
binaryPaths = ('/usr/bin' , '/usr/sbin' , '/bin', '/sbin')

for binaryPath  in binaryPaths:
    for rootDir,subDirs,subFiles in os.walk(binaryPath):
        for subFile in subFiles:
            absPath = os.path.join(rootDir,subFile)
            permission = oct(os.stat(absPath).st_mode)[-4:]
            specialPermission = permission[0]
            if int(specialPermission) >= 4:
                print(permission , absPath)
