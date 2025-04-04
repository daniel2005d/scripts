import sqlite3
import os
from nmapexplore.items import Item, Workspace
from typing import List


class DataBase:
    def __init__(self, workspace:str) -> None:
        homedirectory = os.path.expanduser("~")
        databasedirectory = os.path.join(homedirectory,".config/nmapexplore")
        if not os.path.exists(databasedirectory):
            os.makedirs(databasedirectory)

        self._database = os.path.join(databasedirectory,f'{workspace}.db')
        self._createtable()
    
    def _createtable(self):
        scans_table = '''
                CREATE TABLE IF NOT EXISTS scans (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 address TEXT,addressstatus TEXT, port TEXT, hostname TEXT, addresstype TEXT,
                portstatus TEXT,productname TEXT, servicename TEXT, serviceversion TEXT, protocol TEXT,tunnel TEXT, hash TEXT,
                workspace TEXT, review boolean)
            '''
        workspaces_table = '''
                CREATE TABLE IF NOT EXISTS workspaces (filename TEXT, hash TEXT, date DATE,
                name TEXT)
        '''
        cur , conn= self._getcursor()
        cur.execute(workspaces_table)
        cur.execute(scans_table)
        conn.commit()
        conn.close()


    def _getcursor(self):
        conn = sqlite3.connect(self._database)
        cursor = conn.cursor()
        return cursor, conn

    
    def insert(self, item: Item):
        insert = """INSERT INTO scans (address,addressstatus,port,hostname, addresstype,
                portstatus,productname, servicename, serviceversion, protocol,tunnel, hash, workspace, review)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?, false)"""
        
        cur , conn= self._getcursor()
        cur.execute(insert, (item.address,item.addressstatus,item.port if item.port else "",
                             item.hostname if item.hostname else "", item.addresstype,
                item.portstatus if item.portstatus else "",
                item.portname  if item.portname else "", 
                item.servicename  if item.servicename else "",
                item.serviceversion  if item.serviceversion else "", 
                item.protocol  if item.protocol else "",
                item.tunnel  if item.tunnel else "", item.hash, item.workspace) )
        conn.commit()
        conn.close()
    
    def create_workspace(self, workspace: Workspace):
        cur , conn = self._getcursor()
        cur.execute("SELECT * FROM workspaces where name=?", (workspace.name,))
        rows = cur.fetchall()

        if len(rows) == 0:
            cur.execute("INSERT INTO workspaces (name, filename, hash, date) VALUES (?,?,?,?)", (workspace.name, 
                                                                                                    workspace.filename, 
                                                                                                    workspace.hash, 
                                                                                                    workspace.date))
            conn.commit()
        conn.close()
    
    
    def get_workspace(self, workspace: str) -> Workspace:
        ws:Workspace=None
        cur , conn = self._getcursor()
        cur.execute("SELECT * FROM workspaces where name=?", (workspace,))
        rows = cur.fetchall()
        for r in rows:
            ws = Workspace(filename=r[0],hash=r[1],date=r[2],name=r[3])

        conn.close()
        return ws
    
    def get_upassets(self):
        items = []
        sentence = """Select address,addressstatus,count(port) from scans
                    where port!=''
                    group by address,addressstatus
                """
        
        cur , conn = self._getcursor()
        cur.execute(sentence)
        rows = cur.fetchall()
        for r in rows:
            item = Item(address=r[0], addressstatus=r[1])
            items.append(item)
        
        conn.close()
        return items

    def get_ports(self, workspace) -> List[Item]:
        items = []
        cur,conn = self._getcursor()
        cur.execute("""SELECT DISTINCT port,portstatus,productname, servicename, serviceversion, protocol, hash 
                    from scans where workspace=?  order by port asc""", (workspace,))
        rows = cur.fetchall()
        for r in rows:
            item: Item=Item(port=r[0], portstatus=r[1],productname=r[2], servicename=r[3], serviceversion=r[4], protocol=r[5], hash=r[6])
            items.append(item)
        conn.close()
        return items
    
    def get_hostnames(self)-> List[Item]:
        items = []
        cur,conn = self._getcursor()
        cur.execute("SELECT DISTINCT address,hostname, addressstatus, review from scans")
        rows = cur.fetchall()
        for r in rows:
            item: Item=Item(address=r[0], hostname=r[1], addressstatus=r[2], review=r[3])
            items.append(item)
        conn.close()
        return items

    def get_byports(self, port: int, workspace:str, hash:str=None):
        items = []
        cur,conn = self._getcursor()
        cur.execute("""SELECT address, port,hostname, addresstype, 
                            productname, servicename, serviceversion, hash, review, id
                    from scans where port=IFNULL(?,port) and workspace=? and hash=IFNULL(?,hash)
                    order by port asc""", (port,workspace, hash))
        rows = cur.fetchall()
        for r in rows:
            item: Item=Item(address=r[0], port=r[1],hostname=r[2], addresstype=r[3], 
                            productname=r[4], servicename=r[5], serviceversion=r[6], hash=r[7], review=r[8], id=r[9])
            items.append(item)
        conn.close()
        return items
    
    def getbyhost(self, host, workspace:str):
        items = []
        cur,conn = self._getcursor()
        cur.execute("SELECT * from scans where address=? and workspace=?",(host, workspace))
        rows = cur.fetchall()
        for r in rows:
            item: Item=Item(id=r[0],address=r[1], addressstatus=r[2],port=r[3],
                            hostname=r[4], addresstype=r[5], portstatus=r[6],
                            productname=r[7], servicename=r[8], serviceversion=r[9],
                            protocol=r[10], tunnel=r[11], hash=r[12])
            items.append(item)
        conn.close()
        return items
    
    def clean(self):
        cur,conn = self._getcursor()
        cur.execute("delete from scans")
        cur.execute("delete from workspaces")
        conn.commit()
        conn.close()
    
if __name__ == '__main__':
    db = DataBase()
        


