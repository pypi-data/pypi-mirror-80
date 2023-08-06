# Mediaspace Extractor

*Extract video links from Mediaspace*

UIUC uses [Mediaspace](https://mediaspace.illinois.edu/) to upload content like lecture videos for a lot of classes. To download these videos, one need to first extract the m3u8 stream URL. This can be done manually by inspecting the web requests in developer mode, but this becomes tedious over time and doesn't work inside scripts. This tool uses headless Selenium to automatically extract links from a list of mediaspace URLs.

## Usage

```
mediaspace-extractor [-h] [-j] [-t] [-q] [-m METADATA] username password [mediaspace_urls [mediaspace_urls ...]]

Mediaspace m3u8 extractor using Selenium

positional arguments:
  username              Illinois netid to use
  password              Corresponding password for netid
  mediaspace_urls       Mediaspace URLs to extract m3u8 from

optional arguments:
  -h, --help            show this help message and exit
  -j, --json            Output as json lines
  -t, --title           Output title of video
  -q, --quiet           Hide status output
  -m METADATA, --metadata METADATA
                        Extra json metadata to attach to each element
```

Example:

```bash
nano password.txt
mediaspace-extractor ajohnson7 "$(cat password.txt)" https://mediaspace.illinois.edu/media/t/abc123 | tee url.txt
ffmpeg -protocol_whitelist file,http,https,tcp,tls -i "$(cat url.txt)" -c copy -bsf:a aac_adtstoasc "video.mp4"
```

This tool also supports extracting all viewable URLs on a channel.

## Installation

This package requires `python3` and the downloaded [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/home) executable in your PATH. Make sure the version number corresponds to the version of Chrome you have installed.

Install via PyPI:

```
pip3 install --user mediaspace-extractor
```

