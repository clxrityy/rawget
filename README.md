# rawget

<img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/clxrityy/rawget/ci.yml?style=flat-square&label=ci" />

<img alt="PyPI - Version" src="https://img.shields.io/pypi/v/rawget?style=flat-square&logo=pypi&label=%20" />

A lightweight CLI tool for downloading files from a URL.

## Features

- [x] No external dependencies.
- [x] Cross-platform default download directory detection.
- [x] Simple command-line interface.
- [x] Automatic file extension detection based on content.
- [x] Works on all major platforms (Linux, macOS, Windows)

> Note: Streaming platform downloads (e.g., YouTube) are not supported (yet). This tool is designed for direct file downloads.

### Installation

```bash
pip install rawget
```

#### Usage

```bash
rawget <URL> [output_file_name]
```
