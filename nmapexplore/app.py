from flask import Flask, render_template, redirect, session
from flask_session import Session
import argparse
from nmapexplore.db import DataBase
import uuid
import sys
import nmapexplore.definition as definition

app = Flask(__name__)
ports = None
hosts = None



class HttpServer:
    app = None
    def __init__(self, app, db, appname):
        
        @app.route('/', methods=['GET'])
        def index():
            session["ports"] = db.get_ports(appname)
            session["hosts"] = db.get_hostnames()
            assets = db.get_upassets()
            return render_template('index.html', title=appname, menu=session["ports"], hosts=session["hosts"],assets=assets)

        @app.route('/ports/<int:port>', methods=['GET'])
        def ports(port:int, hash:str=None):
            if "hosts" not in session or "ports" not in session:
                return redirect('/')
            
            items = db.get_byports(port, appname, hash)
            ports = {}
            for p in items:
                info = f"{p.serviceversion}{p.productname}{p.servicename}"
                if info not in ports:
                    extrainfo = []
                    for e in definition.getinfo(p.servicename):
                        if e != "":
                            extrainfo.append(e)
                    for e in definition.getinfo(p.productname):
                        if e != "":
                            extrainfo.append(e)


                    ports[info]={"hosts":[],"hash":p.hash, "servicename":p.servicename, "productname":p.productname, 
                                "version":p.serviceversion, "port":p.port, "extrainfo": extrainfo, "review": p.review, "id":p.id}
                
                ports[info]["hosts"].append({"address":p.address, "name":p.hostname})

            return render_template('ports.html', title=appname, menu=session["ports"], 
                                hosts=session["hosts"], ports=ports)

        @app.route('/ports/<string:hash>', methods=['GET'])
        def portsbyhash(hash:str):
            
            if "hosts" not in session or "ports" not in session:
                return redirect('/')
            else:
                return ports(None, hash)

        @app.route('/host/<string:host>', methods=['GET'])
        def host(host:str):
            
            if "hosts" not in session or "ports" not in session:
                return redirect('/')
            else:
                items = db.getbyhost(host, appname)
                return render_template('hosts.html', menu=session["ports"] , hosts=session["hosts"] , host=items)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w","--workspace",help="Name of Workspace", type=str, required=True)
    parser.add_argument("input",help="The XML file to be import",default=None, nargs="?")
    parser.add_argument("--clean",help="Clean Database", action='store_true')
    args = parser.parse_args()
    appname = args.workspace
    db = DataBase(appname)
    
    if args.clean:
        print("[!] Cleaning Database")
        db.clean()
    if args.input:
        from nmapexplore.beautynmap import BeautyNmap
        ws = db.get_workspace(args.workspace)
        if ws is None:
            bnmap = BeautyNmap()
            bnmap.importfile(filename=args.input, workspace=args.workspace)
        else:
            print("The file has already been imported.")
            sys.exit(0)

    app.config["SECRET_KEY"]= str(uuid.uuid1())
    app.config["SESSION_TYPE"]="filesystem"
    Session(app)
    http = HttpServer(app, db, appname)
    app.run(host="0.0.0.0",port=5200, debug=True, use_reloader=False)

if __name__ == '__main__':
    main()
