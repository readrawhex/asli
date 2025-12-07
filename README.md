# aslicer

*automatic audio slicing through transient detection*

---

I've been using a DAW to do this manually for a while, thought I would save 
myself some time. This script should be able to process whatever filetypes `ffmpeg` 
supports, according to `pydub` documentation.

Install can be done by running `pipx install .`.

```bash
usage: aslicer [-h] [-t THRESHOLD] [-i] [-o OUTPUT] [-d] [-f FORMAT] files [files ...]

audio slicer tool

positional arguments:
  files                 audio files to slice

options:
  -h, --help            show this help message and exit
  -t THRESHOLD, --threshold THRESHOLD
                        set threshold for transient detection
  -i, --keep-intro      treat beginning of file as transient
  -o OUTPUT, --output OUTPUT
                        write audio slices to directory (implies -d)
  -d, --to-dir          write audio slices to directory named after file
  -f FORMAT, --format FORMAT
                        format of sliced audio clips
```

```bash
$ # slice multiple audio files to separate named directories
$ python3 aslicer.py -d audio1.wav audio2.mp3 audio3.flac
file: audio1.wav                    transients: 73
file: audio2.mp3                    transients: 73
file: audio3.flac                   transients: 73

$ # slice audio, detecting transients with a >5.0 change-in-rms ratio
$ python3 aslicer.py -t 5.0 audio.wav
file: audio.wav                     transients: 41

$ # slice audio to specific directory
$ python3 aslicer.py -o some/directory/path audio.wav
file: audio.wav                     transients: 73
```
