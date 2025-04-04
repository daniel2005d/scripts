import sys
import subprocess
import os

def main():
    if not os.path.isdir("nxc"):
        os.makedirs("nxc")

    if len(sys.argv) < 3:
        print("You need set target")
    else:
        file_name = f'nxc/{sys.argv[2].replace("/","_")}.log'
        subprocess.run(["nxc"]+sys.argv[1:]+["--log", file_name])