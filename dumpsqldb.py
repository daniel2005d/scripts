#!/bin/python

#--------------------------
# Allow dump all sql databases
# -----------------------------

from impacket import tds
import argparse
from pwn import log

class SQLDumper:
    def __init__(self, address, port, db, username, password, domain, table):
        self.log = log.progress("Dumping")
        self.sql = None
        self.address = address 
        self.port = port
        self.db= db 
        self.table = table
        self.username = username
        self.password = password
        self.domain = domain

        self.hashes=None
    
    def __write2file(self, tablename):
        records = 0
        output = open(self.db+"__"+tablename+".csv","w")
        columns = list()
        result = self.sql.sql_query("Select * from "+tablename)
        for col in result[0]:
            columns.append(col)
            output.write(col+"|")
        output.write("\r")
            
        for row in result:
            records+=1
            for col in columns:
                output.write(str(row[col]).replace("\r"," ").replace("\n"," ")+"|")
            output.write("\r")
        output.close()
        return records
    
    def __gettables(self):
        tables = self.sql.sql_query("Select name from sys.tables")
        return tables
   

    def dump(self):
        totalrecords = 0
        self.__connect()
        tables = list()
        if self.table is None:
            tables = self.__gettables()
        else:
            tables.append({"name":self.table} )

        for t in tables:
            tablename = t["name"]
            self.log.status(tablename)
            totalrecords+=self.__write2file(tablename)
        log.info("Total Tables: " + str(len(tables)))
        log.info("Total Records: " + str(totalrecords))
        
        self.log.success("Finished")

    def __connect(self):
        ms_sql = tds.MSSQL(self.address, int(self.port))
        ms_sql.connect()
        ms_sql.login(self.db, self.username, self.password, self.domain, self.hashes, False)
        self.sql = ms_sql
        ms_sql.printReplies()

def banner():
    log.info('Dump all Database Infor\r\n')
    log.ingo('Version: 1.0')

parser = argparse.ArgumentParser()
parser.add_argument('--db', required=True)
parser.add_argument('--username', required=True)
parser.add_argument('--password', required=True)
parser.add_argument('--ip', required=True)
parser.add_argument('--domain')
parser.add_argument('--table')
parser.add_argument('--port', default=1433)
args = parser.parse_args()

if __name__ == '__main__':
    banner()
    table = None
    if args.table != '':
        table = args.table

    dump = SQLDumper(args.ip,args.port,args.db,args.username,args.password,args.domain,table) 
    dump.dump()
