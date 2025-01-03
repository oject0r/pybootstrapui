import os
from pybootstrapui.desktop.build import start
import sys

print("=> PyBootstrapUI Builder =>")

while True:
    print(
        "PyBootstrapUI Builder is currently in BETA state.\nType [yes, no] if you want to continue."
    )
    c = input()

    if c.lower().startswith("n"):
        exit()
    elif c.lower().startswith("y"):
        break
    else:
        print("Please, type in YES or NO.")

args = list(sys.argv)
args.pop(0)

if len(args) < 2:
    print("Not enough arguments.")
    exit(-1)

script_file = args[0]
nwjs_folder = args[1]

args.pop(0)
args.pop(0)

start(script_file, nwjs_folder, args)
