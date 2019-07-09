import argparse
import requests

READ_COMMAND = 'read'
WRITE_COMMAND = 'write'


def parse_args():
    parser = argparse.ArgumentParser(
        description='Client needed to read/write information about sold cars'
    )

    parser.add_argument(
        'command', help='Read or write command',
        choices=[READ_COMMAND, WRITE_COMMAND]
    )
    parser.add_argument(
        '--json-path',
        help='Path to json file with information about sold car'
    )
    parser.add_argument(
        '--serial-number',
        help='Serial number of car'
    )
    parser.add_argument('--host', help='Host:port of server')

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    if not args.host:
        print('HOST is not set!')
        return

    if args.command == READ_COMMAND:
        if not args.serial_number:
            print('Serial number is not set!')
            return

        req = requests.get(f'{args.host}/car/{args.serial_number}')
        if req.status_code == 200:
            print(f'Car info: {req.json()}')
        else:
            print('Server is unavailable.')

    # WRITE COMMAND
    else:
        if not args.json_path:
            print('JSON-PATH is not set!')
            return

        body = open(args.json_path).read()
        req = requests.post(f'{args.host}/car', data=body)
        if req.status_code == 200:
            print(f'Car info: {req.json()}')
        elif req.status_code == 400:
            print(f'Error: {req.json()}')
        else:
            print('Server is unavailable.')


if __name__ == '__main__':
    main()
