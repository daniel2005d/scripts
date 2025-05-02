import sys
import subprocess
import os

def main():
    if not os.path.isdir("nxc"):
        os.makedirs("nxc")

    if len(sys.argv) < 2:
        print("You need set target")
        print("Usage:")
        print(f"{sys.argv[0]} 127.0.0.1")
    else:
        file_name = f'nxc/{sys.argv[1].replace("/","_")}.log'
        subprocess.run(["nxc"]+sys.argv[1:]+["--log", file_name])

if __name__ == '__main__':
    main()