#! /usr/bin/env python3
import argparse
import os
import pathlib
import re
import sys

import yaml

from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE, SIG_DFL)

debug = os.environ.get('DEBUG')
VERSION = '0.0.16'


def grep(pattern, file):
    with file.open() as f:
        try:
            data = yaml.safe_load_all(f)
            for doc in data:
                if isinstance(doc, dict):
                    hits = {k: v for k, v in doc.items() if re.search(pattern, k)}
                    if hits:
                        print('==>', file, '<==')
                        yaml.dump(hits, sys.stdout, default_flow_style=False)
                        print()
        except (yaml.YAMLError, UnicodeDecodeError) as e:
            if debug:
                print(e, file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description='searches and prints YAML (top-level) properties matching regex')
    parser.add_argument(
        'pattern',
        action='store',
        help='regex to filter YAML properties on',
    )
    parser.add_argument(
        'files',
        nargs='*',
        help='Files to search, defaults to all files under the current directory (recursively).',
        default=[pathlib.Path('.')],
        type=pathlib.Path,
    )
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s ' + VERSION),
    parser.epilog = '(Add DEBUG=1 to env for debug output.)'
    args = parser.parse_args()

    try:
        pattern = re.compile(args.pattern)
        for root in args.files or ['.']:
            if root.is_dir():
                for file in pathlib.Path(root).rglob('*'):
                    if file.is_file():
                        grep(pattern, file)
            elif root.is_file():
                grep(pattern, root)
            else:
                if debug:
                    print('Not a file:', root, file=sys.stderr)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
