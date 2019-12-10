#!/usr/bin/python3

import requests,sys,time,argparse
from colored import fg,attr,bg

results = []
parser = argparse.ArgumentParser('Users enumeration based on response time')
parser.add_argument('-u','--url', required=True)
parser.add_argument('-w','--wordlist', required=True)

args = parser.parse_args()

URL = args.url
file = args.wordlist

#URL = 'http://127.0.0.1:5000/api/recover?email={}'
#file = '/usr/share/wordlists/rockyou.txt'

def banner():
    print("==========================================")
    print("{}Users enumeration based on response time{}".format(fg('spring_green_3a'), attr('reset')))
    print("{} Author: Daniel Vargas{}".format(fg('cyan'), attr('reset')))
    print("Version: 0.1")
    print("==========================================")

def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    return mins, sec

def p(message):
    print(message)
    sys.stdout.write("\033[F")  

def main():
    f = open(file, 'r', encoding='ISO-8859-1')
    for line in f.readlines():
        user = line.replace('\n','')
        try:
            p('{}{}Getting {}{}'.format(bg('1'), fg('white'), user, attr('reset')))
        #p('Getting... ' + user)
            now = time.time()
            resp = requests.get(URL.format(user))
            if resp.status_code != 404:
                end = time.time()
                elapsed_time = end - now
                time_convert(elapsed_time)
                min,sec = time_convert(elapsed_time)
                results.append({'user':user, 'time':sec})
            else:
                p('{} not found {}'.format(fg('red'), attr('reset')))
        except:
            p('{} {} not found                   {}'.format(fg('red'),user, attr('reset')))

        
    
    print_results()

def print_results():
    sort = sorted(results, key = lambda i:i['time'], reverse=True)
    for s in sort:
        print('{}{}{} seconds {}{}{}{}'.format(fg('yellow'),s['user'],attr('reset'),attr('bold'),
                fg('red'), s['time'], attr('reset')))

if __name__ == '__main__':
    banner()
    main()
