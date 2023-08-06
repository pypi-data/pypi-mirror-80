#! /usr/bin/env python3
import argparse
import pathlib
import re
import sys

import yaml

from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE, SIG_DFL)


def grep(pattern, file):
    with file.open() as f:
        try:
            data = yaml.safe_load(f)
            try:
                hits = {k: v for k, v in data.items() if re.search(pattern, k)}
                if hits:
                    print('==>', file, '<==')
                    yaml.dump(hits, sys.stdout, default_flow_style=False)
                    print()
            except AttributeError:
                pass
        except yaml.scanner.ScannerError:
            print('Parse error:', file, file=sys.stderr)



def main():
    parser = argparse.ArgumentParser(description='searches and prints YAML (top-level) properties and their values')
    parser.add_argument(
        'pattern',
        action='store',
        help='regex to filter YAML properties on',
    )
    parser.add_argument(
        'files',
        nargs='*',
        help='Files to search, defaults to .yaml under the current directory (recursively).',
        default=[pathlib.Path('.')],
        type=pathlib.Path,
    )
    args = parser.parse_args()

    try:
        pattern = re.compile(args.pattern)
        for root in args.files or ['.']:
            if root.is_dir():
                for file in pathlib.Path(root).rglob('*.yaml'):
                    grep(pattern, file)
            elif root.is_file():
                grep(pattern, root)
            else:
                print('Not a file:', root, file=sys.stderr)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
