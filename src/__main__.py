#! /usr/bin/env python3

"""
Lightweight CLI tool for downloading files from a URL.
File type detection from raw content.
No external dependencies.
"""
import sys
from .download import download_file

def main():
    if len(sys.argv) < 2:
        print(f"Usage: rawget <URL> [output_file_name]")
        sys.exit(1)

    url = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) >= 3 else None

    download_file(url, output)

if __name__ == "__main__":
    main()
