from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
import os
import argparse
import base64
import uuid
import requests
from time import sleep

class Browser:

    def __init__(self, visible=True):
        self._chromepath = "chromedriver"
        self._headers = {}
        chrome_options = Options()
        #chrome_options.add_argument('--proxy-server=http://localhost:8080')
        chrome_options.add_argument("--start-maximized")
        if not visible:
            chrome_options.add_argument("--headless")

        self._driver = webdriver.Chrome(options=chrome_options)
    
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
        self._browser = Browser(args.hidden)
        self._filelist = args.domains
        self._savedimages={}
        self._headers = None
        if args.H:
            self._headers = args.H
 
    def _create_folder(self, url):
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if not os.path.exists(domain):
            os.mkdir(domain)
        return domain
    
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
        index = open(os.path.join(self._folder, "index.html"),'w')
        html="<div class='row'>"
        for d in self._savedimages:
            html+=f"<div class='row'><div class='col-md-12'><img style='width: 20%;' src='{self._savedimages[d]}'></div><div class='col-md-12'>{d}</div></div>"
        html+="<div class='row'>"
        index.write(html)
    
    def scan(self):
        domains = open(self._filelist, 'r')
        count=1
        if self._headers:
            for h in self._headers:
              self._browser.add_header(h)
        for d in domains:
          print(f"\rTaking Snapshop {count}", end='')
          domain = d.strip()
          self._folder = self._create_folder(domain)
          self._browser.navigate(domain)
          response = self._browser.get_response(domain)

          contenttype = response.headers["Content-Type"]
        #   if "application/binary" in contenttype:
        #       binary=requests.get(domain)
        #       imagename, folderpath = self._get_imagename()
        #       img = open(imagename, 'wb')
        #       img.write(binary.body())
        #       img.close()

          sleep(2)
          b64 = self._browser.get_snapshot()
          imagename = self._save_image(b64)
          self._savedimages[domain]=imagename
          count+=1
        self._create_html()
        self._browser.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l","--domains", required=True)
    parser.add_argument("-H", action="append")
    parser.add_argument("--hidden", action="store_false")
    args = parser.parse_args()
    m = Main(args)
    m.scan()
