# mp4-moov-optimize-GUI

make mp4 video play fast
(Move `moov` atom before `mdat`)

# how to develop

1. install [pdm](https://github.com/pdm-project/pdm)
2. cd /path/to/code
3. pdm install
4. pdm run pythonw main.pyw

# how to release a exe

1. cd /path/to/code
2. pdm run pyinstaller main.pyw -F
3. copy exe file in ./dist