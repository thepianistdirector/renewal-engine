"""Install the adjacent self-contained CLI without package downloads. AGPL-3.0."""

import argparse
import hashlib
from pathlib import Path
import sys


def main():
    parser=argparse.ArgumentParser(description='Install Renewal Engine into an explicit prefix; never overwrite an existing command.')
    parser.add_argument('--prefix',type=Path,required=True)
    args=parser.parse_args()
    if sys.version_info < (3,11):parser.error('Python 3.11 or newer is required')
    archive=Path(__file__).resolve().parent/'renewal-engine.pyz'
    data=archive.read_bytes()
    destination=args.prefix/'bin/renewal-engine'
    destination.parent.mkdir(parents=True,exist_ok=True)
    with destination.open('xb') as stream:stream.write(data)
    destination.chmod(0o755)
    print('Installed bin/renewal-engine under the selected prefix.')
    print('SHA-256: '+hashlib.sha256(data).hexdigest())
    print('No PATH or shell configuration was changed.')


if __name__=='__main__':main()
