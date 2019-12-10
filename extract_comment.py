#/usr/bin/python3

#from lxml import etree
import requests,sys
from bs4 import BeautifulSoup, Comment
from termcolor import colored, cprint
from colored import fg,attr

url = sys.argv[1]
s = requests.Session()
resp = s.get(url)

def scan_url(word):
    try:
        new_url = url+word.strip()
        f = s.get(new_url)
        if f.status_code == 200:
            print('{}[*]{}{} {} {}'.format(fg('blue'),attr('reset'),fg('green'), new_url, fg('green'),attr('reset') ))
        else:
            print('{}[*]{}{} {} {}'.format(fg('red'),attr('reset'),fg('green'), new_url,attr('reset') ))
    except:
        print('{}[*]{}{} {} {}'.format(fg('red'),attr('reset'),fg('green'), new_url,attr('reset') ))
    

if resp.status_code == 200:
    text = resp.content
    soup = BeautifulSoup(text, 'lxml')
    if soup:
        cprint('***************************** ','green')
        for x in soup.findAll(text=lambda text:isinstance(text, Comment)):
            scan_url(x)
            #cprint(x, 'yellow')
        cprint('***************************** ','green')
