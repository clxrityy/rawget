from yt_dlp import YoutubeDL

def youtube_resolve(url: str) -> list[str]:
    DL = YoutubeDL({
        'format': ('bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best').replace(' ', ''),
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'noplaylist': True,
    })

    info = DL.extract_info(url, download=False)

    urls = []

    if info is not None and 'formats' in info:
        for format in info['formats'] or []:
            if 'url' not in format:
                continue

            vcodec = format.get('vcodec')
            acodec = format.get('acodec')

            # Only include formats that have both video and audio
            if vcodec != 'none' and acodec != 'none':
                urls.append(format['url'])
            else:
                continue

    return urls
