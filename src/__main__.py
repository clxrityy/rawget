#! /usr/bin/env python3

"""
Lightweight CLI tool for downloading files from a URL.
File type detection from raw content.
No external dependencies.
"""
import sys
import argparse

from .selection import classify
from .download import download_file
from .process import process_url

parser = argparse.ArgumentParser(description="Lightweight CLI tool for downloading files from a URL.", add_help=True)
parser.add_argument("url", help="URL of the file to download")
parser.add_argument("output", nargs="?", help="Optional output file name")
parser.add_argument("--list", action="store_true", help="List available files instead of downloading")
parser.add_argument("--pick", type=int, help="Pick a specific file from the list by index")
parser.add_argument("--type", choices=["video", "audio", "image", "other", "icon"], help="Choose the type of file to download")
parser.add_argument("--largest", action="store_true", help="Download the largest file available")
parser.add_argument("--smallest", action="store_true", help="Download the smallest file available")

def main():
    args = parser.parse_args()

    # Resolve URL -> list of candidates
    url = process_url(args.url)

    if not url:
        print("No downloadable media found.")
        sys.exit(1)

    urls = [url] if isinstance(url, str) else url
    final_url = None

    # --list: show options and exit
    if args.list:
        for i, u in enumerate(urls):
            print(f"[{i}] {u}")
        sys.exit(0)

    # --pick: user-selected index
    if args.pick is not None:
        try:
            final_url = urls[args.pick]
        except IndexError:
            print("Invalid index for --pick.")
            sys.exit(1)

    # --type: filter by file type
    if args.type:
        urls = [u for u in urls if classify(u) == args.type]

    # --largest / --smallest
    elif args.largest or args.smallest:
        from .selection import content_length

        key_fn = content_length
        final_url = (
            max(urls, key=key_fn)
            if args.largest
            else min(urls, key=key_fn)
        )

    # Default selection logic
    else:
        from .selection import select_default
        final_url = select_default([u for u in urls if classify(u) != "icon"])

    # Download
    if final_url:
        download_file(final_url, args.output)
    else:
        print("No suitable file found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
