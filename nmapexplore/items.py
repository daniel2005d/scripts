import hashlib
import datetime

class Item:

    def __init__(self, **kwargs) -> None:
        self.hostname = ''
        for key, value in kwargs.items():
            setattr(self, key, value)

    id:int=0
    address: str
    addresstype: str
    addressstatus: str
    port: str
    hostname: str
    portstatus: str
    portname: str
    servicename: str
    serviceversion: str
    protocol: str
    tunnel: str
    workspace: str
    hash: str = ""
    review:bool=False

class Workspace:
    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        sha256 = hashlib.sha256()
        sha256.update(self.filename.encode('utf-8'))
        self.hash = sha256.hexdigest()
        self.date = datetime.date.today()

    name: str
    filename: str
    hash: str
    date:None
