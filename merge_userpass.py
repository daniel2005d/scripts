import argparse
from base64 import b64encode


def permute(users, passwords, output_type):
    output = []
    
    for user in users:
        for pwd in passwords:
            combine = f'{user}:{pwd}'
            if output_type == 'b64':
                output.append(b64encode(combine.encode()).decode())
            else:
                output.append(combine)
    
    return output

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--users', required=True)
    parser.add_argument('--passwords', required=True)
    parser.add_argument('--format', choices=['b64','raw'])
    parser.add_argument('--permute', action='store_false')
    parser.add_argument('--onebyone', action='store_true')
    parser.add_argument('--output', required=True)

    args = parser.parse_args()

    users = []
    passwords = []

    with open(args.users , 'r') as fb:
        for user in fb:
            users.append(user.strip())

    with open(args.passwords, 'r') as fb:
        for pwd in fb:
            passwords.append(pwd.strip())

    output = None
    if args.permute:
        output = permute(users, passwords, args.format)

    with open(args.output, 'w') as fb:
        for o in output:
            fb.write(f'{o}\r\n')

if __name__ == '__main__'   :
    main()
