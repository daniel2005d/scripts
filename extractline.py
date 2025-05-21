import re
import argparse


PATTERNS = {"email":r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"}


def find_text(pattern:str, line:str) -> bool:
    match = re.findall(PATTERNS[pattern], line)
    return len(match)>0



parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input', required=True)
parser.add_argument('-p','--pattern', choices=['email'], required=True)
parser.add_argument('-o','--output', required=True)
args = parser.parse_args()

file_name = args.input
with open(args.output, 'w') as w:
    with(open(file_name, 'r')) as fb:
        for index, line in enumerate(fb.readlines()):
            if find_text(args.pattern,line.strip()):
                print(f"Line {index}")
                w.write(f'{line.strip()}\n')