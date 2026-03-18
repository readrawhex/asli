# asli

*audio slicing through transient detection*

---

I've been using a DAW to do this manually for a while, thought I would save 
myself some time. This script should be able to process whatever filetypes `ffmpeg` 
supports, according to `pydub` documentation.

Install can be done by running `pipx install .`.

```bash
usage: asli [-h] [-t THRESHOLD] [-i] [-o OUTPUT] [-d] [-f FORMAT] [-e EVERY]
            [-m MAX_SLICES] [-c COOLDOWN] [--fadeo FADEO] [--fadei FADEI]
            [--fadeout-all] [--fadein-all] [--db DB] [--hpf HPF] [--lpf LPF]
            [--bpf BPF] [--trim-end TRIM_END] [--trim-start TRIM_START]
            files [files ...]

audio slicer tool

positional arguments:
  files                 audio files to slice

options:
  -h, --help            show this help message and exit
  -t THRESHOLD, --threshold THRESHOLD
                        set threshold for transient detection [def=3.0]
  -i, --keep-intro      treat beginning of file as transient
  -o OUTPUT, --output OUTPUT
                        write audio slices to directory (implies -d)
  -d, --to-dir          write audio slices to directory named after file
  -f FORMAT, --format FORMAT
                        format of sliced audio clips
  -e EVERY, --every EVERY
                        slice every EVERY seconds instead of at transients
  -m MAX_SLICES, --max-slices MAX_SLICES
                        maximum number of slices to write (will skip trailing
                        slices)
  -c COOLDOWN, --cooldown COOLDOWN
                        minimum seconds between transients [def=0.05]
  --fadeo FADEO         add fade out at last FADEO seconds of slice
  --fadei FADEI         add fade in at first FADEO seconds of slice
  --fadeout-all         fade out audio clips start to finish (or half with
                        fade in)
  --fadein-all          fade in audio clips start to finish (or half with fade
                        out)
  --db DB               minimum NEGATIVE db value to treat as transient
                        [def=20]
  --hpf HPF             find transients while applying highpass filter at freq
  --lpf LPF             find transients while applying lowpass filter at freq
  --bpf BPF             find transients while applying bandpass filter at freq
  --trim-end TRIM_END   number of seconds to trim off end of clips
  --trim-start TRIM_START
                        number of seconds to trim off beginning of clips
```

```bash
$ # slice multiple audio files to separate named directories
$ python3 asli.py -d audio1.wav audio2.mp3 audio3.flac
file: audio1.wav                    transients: 73
file: audio2.mp3                    transients: 73
file: audio3.flac                   transients: 73

$ # slice audio at transients with db > -6.0 db
$ python3 asli.py --db 6.0 audio1.wav
file: audio1.wav                    transients: 32

$ # slice audio, detecting transients with a >5.0 change-in-rms ratio
$ python3 asli.py -t 5.0 audio.wav
file: audio.wav                     transients: 41

$ # slice audio to specific directory
$ python3 asli.py -o some/directory/path audio.wav
file: audio.wav                     transients: 73

$ # slice audio that has been highpassed at 500hz
$ # the output is not highpassed! highpassing occurs during transient detection
$ python3 asli.py -o some/directory/path audio.wav
file: audio.wav                     transients: 80

$ # slice audio every 0.7 seconds instead of at transients
$ python3 asli.py -e 0.7 audio.wav
file: audio.wav                     divisions: 35
```
