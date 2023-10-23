import requests
import os
from urllib.parse import urlparse
import re

regexendpoint = r'\/\w+(?:\/\w+)*(?:\/\w+\?[^ ]*)?'

def get_file(url):
    urlformat = urlparse(url)
    filename = os.path.basename(urlformat.path)
    content = ""
    if not os.path.exists(filename):
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text
            file = open(filename, 'wb')
            file.write(response.content)
    else:
        content = open(filename, 'r').read()
    
    return content

def getendpoints(text):
    match = re.match(regexendpoint, text)
    print(match)


content = get_file('https://www.turnosmovistar.com.mx/assets/mask/default/application-afb679f9026a52f7a735ce075e783f50.js')
getendpoints(content)
