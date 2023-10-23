import xml.etree.ElementTree as ET
from colored import Fore, Style, Back
import argparse


def print_beauty(color, message):
    print(message)


parser = argparse.ArgumentParser()
parser.add_argument("input",help="FIle Name", type=str)
parser.add_argument("--port", help="Filter by PORT", type=int)
parser.add_argument("--host", help="Filter by HOST", type=str)
arguments = parser.parse_args()

file = arguments.input

discovered=[]

tree = ET.parse(file)
root = tree.getroot()

args = root.attrib.get("args")
print(f"[!] {Fore.blue} {args} {Style.reset}")
hosts = root.findall(".//host")
assets = []
for h in hosts:
    if arguments.port:
        ports = h.findall(f".//ports/port[@portid='{arguments.port}']")
    else:
        ports = h.findall(".//ports/port")
    
    if len(ports)>0:
        status = h.findall(".//status")[0].attrib.get("state")
        address = h.findall(".//address")[0].attrib.get("addr")
        ipv = h.findall(".//address")[0].attrib.get("addrtype")
        hostnames = h.findall(".//hostnames/hostname")
        
        color:str = ""
        if status == "up":
            color = Fore.yellow
        else:
            color = Fore.red+Back.yellow

        print(f"{color}[*] IP {address} {ipv} {status}{Style.reset}")
        ## HOSTS
        print(f"\t{Fore.spring_green_4}Hosts: {len(hostnames)}{Style.reset}")
            
        for hst in hostnames:
            host = hst.attrib.get("name")
            print(f"\t\t{Fore.green_3b}{host}{Style.reset}")
            
        print(f"\t{Fore.light_gray}Ports: {len(ports)}{Style.reset}")
        # PORTS
        for p in ports:
            statecolor:str = Fore.magenta

            protocol = p.attrib.get("protocol")
            port  = p.attrib.get("portid")
            state = p.findall(".//state")[0].attrib.get("state")

            service = p.findall(".//service")[0]
            servicename = service.attrib.get("name")
            tunnel  = service.attrib.get("tunnel")
            #p.findall(".//service")[0].attrib.get("tunnel")
            if state == 'open':
                statecolor = Fore.green
            elif state == 'closed':
                statecolor = Fore.red
            
            print(f"\t\t{statecolor}{port}:{state} {servicename}{'/'+tunnel if tunnel else ''}")

