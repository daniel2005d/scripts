import argparse
import os
import requests
import exiftool
from concurrent.futures import ThreadPoolExecutor
import threading
from threading import Thread
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, DownloadColumn, BarColumn
from utils.colors import Color
from utils.folder import Folder
from crawler.data import DBData, Pages, Metadata, Files

class Crawler:
    def __init__(self, seed:str):
        self._seed = seed
        self._visited = set()
        parsed_url = urlparse(seed)
        domain = parsed_url.netloc.replace(f":{parsed_url.port}","")
        self._output = os.path.join(Folder.get_local_folder(), domain)
        self._files_folder = os.path.join(self._output,'files')
        self._summary = []
        self._results = []
        self._EXTENSIONS = [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"]
        self._ALLOWED_PAGES = [".aspx",".html",".htm",".jsp",".php",".php5",".asp"]
        self._table_name = "Pages"
        self._db = None
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._progress = Progress(SpinnerColumn(),
                        BarColumn(),
                        TextColumn("[bold blue]{task.description}:[/] {task.fields[url]}"),
                        DownloadColumn())
        self._task = self._progress.add_task("[green]Indexing...", url="...", total=None)
        self._downloaded_task = self._progress.add_task("[yellow]Downloading...", url="...", total=100, visible=False)
        self._threads = []
        self._init()
    
    def _init(self):
        Folder.create_folder(self._output)
        Folder.create_folder(self._files_folder)
        db_file = os.path.join(self._output,'data.db')
        self._db = DBData(db_file)
        
        self._print_summary()
        

    def _is_valid(self, url:str, extensions)->bool:
        return any(url.lower().endswith(ext) for ext in extensions)

    def _is_document_valid(self, url) -> bool:
        return self._is_valid(url, self._EXTENSIONS)
    
    def _is_url_valid(self, url:str) -> bool:
        isvalid = self._is_valid(url, self._ALLOWED_PAGES)
        if not isvalid:
            path = urlparse(url).path
            _,ext = os.path.splitext(path)
            isvalid = ext == ""
        
        return isvalid

   
    
    def _get_metadata(self, file_name:str) -> dict:
        
        metadata = None
        with exiftool.ExifTool() as et:
            metadata = et.execute_json(file_name)
            author = None
            creator = None
            producer = None

            for properties in metadata:
                if "PDF:Author" in properties:
                    author = properties["PDF:Author"]
                if "PDF:Creator" in properties:
                    creator = properties["PDF:Creator"]
                if "PDF:Producer" in properties:
                    producer = properties["PDF:Producer"]
                
                information = {
                    "author":author,
                    "producer":producer,
                    "creator":creator,
                    "filename":file_name
                }

                self._results.append(information)
        
        return metadata

    def _download_file(self, url:str):
        query = self._db.select_files(url)
        if len(query) == 0:
            file_name = os.path.basename(urlparse(url).path)
            self._progress.update(self._downloaded_task, url=file_name, advance=0,total=100, visible=True)
            target_path = os.path.join(self._files_folder,file_name)
            if not os.path.exists(target_path):
                resp = requests.get(url, stream=True)
                resp.raise_for_status()
                self._progress.update(self._downloaded_task, total=int(resp.headers.get('Content-Length', 0)))
                with open(target_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                        self._progress.update(self._downloaded_task, advance=len(chunk))

                # TODO: Change
            information = self._get_metadata(target_path)
            file_id = self._db.add(Files(url=url))
            
            list = []
            for info in information:
                for property in info:
                    list.append(Metadata(file_id=file_id, key=property, value=str(info[property])))
                
                self._db.add_all(list)
                self._progress.update(self._downloaded_task, visible=False)

    def _print_summary(self):
        summary = self._db.get_summary()
        if len(summary) > 0:
            authors = set()
            software = set()
            users_table = Table(title="Users")
            software_table = Table(title="Software")
            console = Console()
            users_table.add_column("User")
            software_table.add_column("Software", style="green")

            for item in summary:
                if item.key == "PDF:Author":
                    if item.value not in authors:
                        authors.add(item.value)
                    
                if item.key == "PDF:Creator":
                    if item.value not in software:
                        software.add(item.value)

            for user in authors:
                users_table.add_row(user)
            
            for s in software:
                software_table.add_row(s)

            console.print(users_table)
            console.print(software_table)

    def start(self, url:str=None):

        if url is None:
            url = self._seed
            
        if url in self._visited:
            return
        
        if not self._is_url_valid(url):
            return

        
        self._visited.add(url)
        page = self._db.select_page(url)
        if len(page) == 0:
            self._db.add(Pages(url=url))
        #Color.print_info(f'{url}', end='\r')
        #self._progress.print(f"[white][▼][bold]{url}[reset]")
        self._progress.update(self._task, url=url)
        
        try:
            self._summary.append(url)
            r = requests.get(url)
            r.raise_for_status()
            soup = BeautifulSoup(r.content, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link["href"]
                abs_url = urljoin(url, href)
                if self._is_document_valid(abs_url):
                    #self._executor.submit(self._download_file, abs_url)
                    self._download_file(abs_url)
                elif abs_url.startswith(self._seed):
                    self.start(abs_url)
                    # th = Thread(target=self.start, args=(abs_url,))
                    # self._threads.append(th)
                    # th.start()
                    

                    # if len(self._threads) > 3:
                    #     for t in self._threads:
                    #         if t is not threading.current_thread():
                    #             self._progress.update(self._task, description=f"Waiting for end {t.name}")
                    #             t.join()

                    #     self._threads.clear()
                    #self._executor.submit(self.start, abs_url)
                    #self.start(abs_url)
        except requests.exceptions.RequestException as e:
            self._progress.print(e)
        except Exception as e:
            self._progress.print(e)
       
    
    def crawler(self):
        try:
            with self._progress:
                self.start()
        except Exception as e:
            Color.print_error(e)
        finally:
            self._executor.shutdown(wait=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input", required=True, help="Single domain or file with list of URls")
    args = parser.parse_args()
    domains = set()
    if os.path.isfile(args.input):
        with open(args.input, 'r') as input:
            for line in input:
                if line not in domains:
                    domains.add(line.strip())
    else:
        domains.add(args.input)
    

    executor = ThreadPoolExecutor(max_workers=len(domains))

    for domain in domains:

        crawler = Crawler(domain)
        executor.submit(crawler.crawler)
        executor.shutdown(wait=True)
        #crawler.crawler()

if __name__ == '__main__':
    main()


