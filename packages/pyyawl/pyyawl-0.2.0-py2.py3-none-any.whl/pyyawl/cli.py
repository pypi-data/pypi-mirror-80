"""Console script for pyyawl."""
import argparse
import sys
from pathlib import Path
from pyyawl import pyyawl


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate', dest='generate', action='store_true')
    parser.add_argument('--f', type=Path)
    parser.add_argument('--verbose', dest='verbose', action='store_true')
    args = parser.parse_args()

    if args.generate:
        print(pyyawl.generate())
    else:
        sys.exit(pyyawl.execute(args.f, args.verbose))


if __name__ == "__main__":
    main()
