from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from urllib.parse import urlparse
import os
import argparse
import base64
import uuid
from time import sleep
from utils.colors import Color
from utils.folder import Folder

class Browser:

    def __init__(self, visible=True):
        
        
        self._chromepath = Folder.get_chromedriver_path()
        self._headers = {}
        chrome_options = Options()
        #chrome_options.add_argument('--proxy-server=http://localhost:8080')
        chrome_options.add_argument("--start-maximized")
        if not visible:
            chrome_options.add_argument("--headless")
        

        service = Service(self._chromepath)
        self._driver = webdriver.Chrome(service=service, options=chrome_options)
         
    
    def _request_handler(self, request): 
        for h in self._headers:
            request.headers[h]=self._headers[h]

    def add_header(self, header):
        h = header.split(":")
        self._headers[h[0]]=h[1]
        
    
    def navigate(self, url:str):
        self._driver.request_interceptor  = self._request_handler
        self._driver.get(url)
    
    def get_snapshot(self):
        return self._driver.get_screenshot_as_base64()
    
    def get_response(self, url):
        for request in self._driver.requests:
            if request.url == url:
                return request.response
    
    def close(self):
        self._driver.quit()


class Main:
    def __init__(self, args):
        self._sleep = args.sleep
        self._browser = Browser(args.hidden)
        self._filelist = args.domains
        self._saved_images={}
        self._headers = None
        if args.H:
            self._headers = args.H
 
    def _create_folder(self, url):
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        output_folder = os.path.join( Folder.get_current_folder(),domain)
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        return output_folder
    
    
    def _get_imagename(self):
      tmpimagename = str(uuid.uuid4())+".png"
      imagename = os.path.join(self._folder, tmpimagename)
      return imagename, tmpimagename
    
    def _save_image(self, b64image):
        imagename, tmpimagename = self._get_imagename()
        image = open(imagename, 'wb')
        image.write(base64.b64decode(b64image))
        image.close()
        return tmpimagename

    def _create_html(self):
        output_file = os.path.join(self._folder, "index.html") 
        index = open(output_file,'w')
        html="<div class='row'>"
        for d in self._saved_images:
            html+=f"<div class='row'><div class='col-md-12'><img style='width: 20%;' src='{self._saved_images[d]}'></div><div class='col-md-12'>{d}</div></div>"
        html+="<div class='row'>"
        index.write(html)
        Color.print(f"[green]File saved on [bold]{output_file}[reset]")
    
    def scan(self):
        domains = open(self._filelist, 'r').readlines()
        
        if self._headers:
            for h in self._headers:
              self._browser.add_header(h)
        for index, d in enumerate(domains):
          Color.print(f"\r[yellow]Taking Snapshot [bold]{index}/{len(domains)-1}[reset]", end='')
          domain = d.strip()
          self._folder = self._create_folder(domain)
          self._browser.navigate(domain)
          #response = self._browser.get_response(domain)
          sleep(self._sleep)
          b64 = self._browser.get_snapshot()
          image_name = self._save_image(b64)
          self._saved_images[domain]=image_name
        print("")
          
        self._create_html()
        self._browser.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l","--domains", required=True, help="File with urls list")
    parser.add_argument("-s","--sleep", required=False, help="Time to sleep between each request. Default 2", default=2, type=int)
    parser.add_argument("-H", action="append", help="Additional headers")
    parser.add_argument("--hidden", action="store_false", help="Hide Browser.")
    args = parser.parse_args()
    m = Main(args)
    m.scan()


if __name__ == '__main__':
    main()
    
    
