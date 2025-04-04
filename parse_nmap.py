import glob
import xml.etree.ElementTree as ET
import argparse
from colored import Style, Fore, Back
from rich.console import Console
from rich.table import Table


def repair_xml(file_path):
    f=open(file_path,'a+')                                                                                                                                                                                                        
    f.write('</nmaprun>')
    f.close()
    

def parse_nmap_xml(file_path):
    command = None
    results = {}
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Obtener el comando usado
        command = root.attrib.get("args", "No command found")

        for host in root.findall("host"):
            ip_address = host.find("address").attrib["addr"]  # Obtiene la IP del host
            ports_info = []
            ports = host.find("ports")
            if ports:
                for port in ports.findall("port"):
                    port_id = port.attrib["portid"]
                    protocol = port.attrib["protocol"]
                    state = port.find("state").attrib["state"]
                    service_elem = port.find("service")
                    service_name = service_elem.attrib["name"] if service_elem is not None else "Unknown"
                    
                    ports_info.append({
                        "port": port_id,
                        "protocol": protocol,
                        "service": service_name,
                        "state": state
                    })
                
            results[ip_address] = ports_info  
    except Exception as e:
        print(f"{Fore.red} File {file_path} error{Style.reset}")
        repair_xml(file_path)
        return parse_nmap_xml(file_path)

    return command, results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input', help='Directory with nmap xml')
    parser.add_argument('-s','--service', required=False)
    parser.add_argument('-p','--port', required=False)
    parser.add_argument('--host', required=False)
    parser.add_argument('--output', help='Save host IP to destination file.')

    args = parser.parse_args()

    output = open(args.output, 'w') if args.output else None
    filter = False

    console = Console()
    for scan in glob.glob(f'{args.input}/*.xml'):
        command, scan_results = parse_nmap_xml(scan)
        for ip, ports in scan_results.items():
            filter = False
            if (args.host and ip.startswith(args.host)) or not args.host:
                
                table = Table()
                table.add_column("Port")
                table.add_column("Service")
                table.add_column("Status")
                for port in ports:
                    service = port['service']

                    if args.service:
                        if args.service == service:
                            table.add_row(port['port'],service, port['state'])
                            filter = True
                    if args.port:
                        if args.port == port['port']:
                            table.add_row(port['port'],service, port['state'])
                            filter = True
                    if args.service is None and args.port is None:
                        table.add_row(port['port'],service, port['state'])
                
                if len(table.rows) > 0:
                    print(f'{Back.black}{Fore.green}{scan}{' '*10}{Style.reset}')
                    print(f'{Back.white}{Fore.black}{ip}{' '*10}{Style.reset}')
                    console.print(table)
                
                if filter and output:
                    output.write(ip+'\n')
    if output:
        output.close()

            
if __name__ == '__main__':
    main()
    