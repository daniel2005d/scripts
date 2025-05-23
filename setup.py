from setuptools import setup
from glob import glob
import os

modules = glob("./*.py")
module_names = [
    os.path.splitext(os.path.basename(f))[0]
    for f in modules
    if os.path.basename(f) != "setup.py"
]

print(module_names)


setup(
    author="Daniel Vargas",
    platforms=["Unix","Windows"],
    name="run-scripts",
    version="1.4",
    py_modules=module_names,
    
    install_requires=["colored==2.3.0","rich==14.0.0","clipboard==0.0.4","beautifulsoup4==4.9.3",
                    "pwn==1.0","Requests==2.31.0","selenium==4.10.0",
                    "selenium_wire==5.1.0","termcolor==2.3.0","blinker==1.4",
                    "PyExifTool==0.5.6",
                    "lxml==5.3.1",
                    "PyPDF2==3.0.1"], 
    packages=["utils","crawler"],
    entry_points={
        "console_scripts": [
            "run-mergeuserpass=merge_userpass:main",
            "run-colortext=color_text:main",
            "run-parsenmap=parse_nmap:main",
            "run-pwdprocessor=pwdprocessor:main",
            "run-nxc=nxc:main",
            "run-dumpsql=dumpsqldb:main",
            "run-nmapp=parse_nmap:main",
            "run-snapshot=dsnapshot:main",
            "run-metadata=crawler.doc_crawler:main",

        ],
    }
)
