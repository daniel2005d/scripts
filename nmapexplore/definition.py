SERVICES = {
    'java-rmi':['https://book.hacktricks.xyz/network-services-pentesting/1099-pentesting-java-rmi',
                'https://github.com/qtc-de/remote-method-guesser#serial'],
    'rpcbind': ['https://book.hacktricks.xyz/network-services-pentesting/pentesting-rpcbind'],
    'Ajenti http control panel':['https://www.nagios.org/ncpa/help/2.2/api.html']
                                  

}

def getinfo(name:str):
    if name in SERVICES:
        return SERVICES[name]
    else:
        return [""]