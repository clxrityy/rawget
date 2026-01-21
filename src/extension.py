from pathlib import Path

FILE_SIGNATURES = {
    # Images
    b"\x89PNG\r\n\x1a\n": ".png",
    b"\xff\xd8\xff": ".jpg",
    b"GIF87a": ".gif",
    b"GIF89a": ".gif",
    b"RIFF": ".wav",  # WAV & AVI start with RIFF; AVI handled below
    b"OggS": ".ogg",
    b"fLaC": ".flac",
    b"BM": ".bmp",
    b"RIFF": ".avi",  # AVI (overlaps WAV, check later)
    b"WEBP": ".webp",
    # Audio
    b"ID3": ".mp3",
    b"\xff\xfb": ".mp3",
    # Video
    b"\x00\x00\x00\x18ftyp": ".mp4",
    b"\x00\x00\x00\x14ftyp": ".mp4",
    b"ftyp": ".mp4",
    # Documents
    b"%PDF-": ".pdf",
}

def detect_file_extension(data: bytes, url: str, content_type: str) -> str:
    import mimetypes

    # 1. Try Content-Type header
    ext = mimetypes.guess_extension(content_type)

    if ext:
        return ext

    # 2. Try file signature (magic numbers)
    for sig, sig_ext in FILE_SIGNATURES.items():
        if data.startswith(sig):
            # Special case: RIFF can be WAV or AVI
            if sig == b"RIFF":
                if data[8:12] == b"WAVE":
                    return ".wav"
                elif data[8:12] == b"AVI ":
                    return ".avi"
            else:
                return sig_ext

    # 3. Try URL suffix
    path_ext = Path(url).suffix
    if path_ext:
        return path_ext

    # 4. Fallback
    return ".bin"
