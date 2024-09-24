english | [中文](./README_zh.md)

# mp4-moov-optimize-GUI

make mp4 video play faster
(Move `moov` atom before `mdat`)

<img width="616" alt="Snipaste_2024-09-24_08-39-36" src="https://github.com/user-attachments/assets/661903f2-9414-4591-b860-f904ad68e6be">

# function
make a commend:
```bash
ffmpeg -y -i input_video.mp4 -movflags faststart -progress pipe:1 -nostats output_video.mp4
```
and run

# how to develop

1. install [pdm](https://github.com/pdm-project/pdm)
2. cd /path/to/code
3. pdm install
4. pdm run pythonw main.pyw

# how to release a exe

1. cd /path/to/code
2. pdm run pyinstaller main.pyw -F
3. copy exe file in ./dist
