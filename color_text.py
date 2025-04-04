from colored import Style, fore, Fore
import argparse
import random
import os
import glob
import clipboard

def get_random_color():
    color = random.choice(list(range(1,256)))
    return f'{fore(color)}'

def get_colors(words):
    word_list = {}
    for w in words:
        word_list[w]=get_random_color()
    
    return word_list

def get_words(text, words):
    return [word for word in words if word.lower() in text.lower()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input")
    parser.add_argument("--text",action="append")
    parser.add_argument("-u","--unique",action="store_true")
    parser.add_argument("-o","--output")
    parser.add_argument("-c","--color", help="Set output color")
    parser.add_argument("--copy", help="Set position to copy to clipboard", type=int)
    parser.add_argument("--pause", help="Pause when exists match", action='store_true')

    args = parser.parse_args()

    colors = {}
    if args.color is None:
        colors = get_colors(args.text)
    else:
        for w in args.text:
            colors[w]=fore(args.color)


    folder = args.input
    files = []
    if os.path.isfile(folder):
        files.append(folder)
    elif os.path.isdir(folder):
        for path in glob.glob(f'{folder}/*.*'):
            files.append(path)

    output = None
    toclipboard = ""
    pause_count=0

    if args.output:
        output = open(args.output, 'w')
    
    for file in files:
        with open(file, 'r') as fb:
            try:
                for line in fb.readlines():
                    text = line.strip()
                    match = get_words(text, args.text)
                    if len(match)>0:
                        pause_count+=1
                        print(f'{Style.bold}{colors[match[0]]}{text}{Style.reset}')
                        if output:
                            output.write(text+'\n')
                        if args.copy:
                            fragments = text.split(' ')
                            toclipboard+=fragments[args.copy]+"\n"
                        if args.pause:
                            if pause_count >=3:
                                input()
                                pause_count = 0
                    elif not args.unique:
                        print(text)
            except Exception as e:
                print(f"[-]{Fore.red}{Style.bold}{path}{Style.reset}")

    if output:
        output.close()
    
    if args.copy:
        clipboard.copy(toclipboard)

if __name__ == '__main__':
    main()