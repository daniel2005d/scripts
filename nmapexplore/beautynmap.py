import xml.etree.ElementTree as ET
from colored import Fore, Style, Back
import argparse
from nmapexplore.db import DataBase
from nmapexplore.items import Item, Workspace
import hashlib
import os
from glob import glob

class BeautyNmap:
    def importfile(self, filename: str, workspace: str):
        files = []
        if not os.path.exists(filename):
            raise "This file doesn't exists"

        if os.path.isfile(filename):
            files.append(filename)
        elif os.path.isdir(filename):
            for file in glob(f'{filename}/*.xml'):
                files.append(file)
        
        
        db = DataBase(workspace)
        ws = Workspace(name=workspace, filename=filename)
        db.create_workspace(ws)
        for file in files:
            tree = ET.parse(file)
            root = tree.getroot()

            args = root.attrib.get("args")
            print(f"[!] {Fore.blue} {args} {Style.reset}")
            hosts = root.findall(".//host")
            
            for h in hosts:
                item: Item = Item(workspace=workspace, port="",
                            hostname="",portstatus="",portname="",servicename="",
                            serviceversion="",protocol="",tunnel="")

                ports = h.findall(".//ports/port")
                address = h.findall(".//address")[0].attrib.get("addr")
                status = h.findall(".//status")[0].attrib.get("state")
                ipv = h.findall(".//address")[0].attrib.get("addrtype")
                hostnames = h.findall(".//hostnames/hostname")
                item.address = address
                item.addressstatus = status
                item.addresstype = ipv
                

                ## HOSTS
                if len(hostnames) > 0:
                    for hst in hostnames:
                        host = hst.attrib.get("name")
                        item.hostname = host


                if len(ports) == 0:
                    db.insert(item)
                # PORTS
                for p in ports:
                    protocol = p.attrib.get("protocol")
                    port  = p.attrib.get("portid")
                    state = p.findall(".//state")[0].attrib.get("state")
                    services = p.findall(".//service")
                    service = ""
                    servicename = ""
                    tunnel  = ""
                    product = ""
                    version = ""
                    if len(services) > 0:
                        service = p.findall(".//service")[0]
                        servicename = service.attrib.get("name")
                        tunnel  = service.attrib.get("tunnel")
                        product = service.attrib.get("product")
                        version = service.attrib.get("version")

                    item.port = port
                    item.protocol = protocol
                    item.portstatus = state
                    item.servicename = servicename
                    item.portname = product
                    item.serviceversion = version
                    item.tunnel = tunnel
                    sha256 = hashlib.sha256()
                    sha256.update(f"{item.portstatus}{item.port}{item.servicename}{item.serviceversion}{item.portname}".encode('utf-8'))
                    item.hash = sha256.hexdigest()
                    db.insert(item)
                

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input",help="FIle Name", type=str)
    parser.add_argument("-w","--workspace",help="Name of Workspace", type=str, required=True)
    arguments = parser.parse_args()