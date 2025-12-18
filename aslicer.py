import argparse
import argcomplete
import sys
import os
from pathlib import Path
from pydub import AudioSegment


def main():
    parser = argparse.ArgumentParser(description="audio slicer tool")
    parser.add_argument("-t", "--threshold", type=float, default=3.0, help="set threshold for transient detection")
    parser.add_argument("-i", "--keep-intro", action="store_true", help="treat beginning of file as transient")
    parser.add_argument("-o", "--output", type=str, help="write audio slices to directory (implies -d)")
    parser.add_argument("-d", "--to-dir", action="store_true", help="write audio slices to directory named after file")
    parser.add_argument("-f", "--format", type=str, default="wav", help="format of sliced audio clips")
    parser.add_argument("files", nargs="+", help="audio files to slice")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    try:
        files = []
        for a in args.files:
            p = Path(a)
            if not p.exists():
                raise Exception(f"file '{a}' does not exist")
            files.append((a, a[0 : -len(p.suffix)], p.suffix.strip(".")))

        for f in files:
            audio = AudioSegment.from_file(f[0], f[2])
            transients = []

            if args.keep_intro:
                transients.append(0)

            baseline = audio[0].rms
            a = 0.95
            maxDeriv = 0.01
            cooldown = 10
            cool = 0

            for i in range(1, len(audio)):
                baseline = a * baseline + (1 - a) * audio[i].rms
                ratio = audio[i].rms / (baseline + 1e-9)
                deriv = audio[i].rms - audio[i - 1].rms
                if cool == 0:
                    if ratio > args.threshold and deriv > maxDeriv:
                        transients.append(i)
                        cool = cooldown
                        print(
                            f"file: {f[0]:<30}transients: {len(transients)}",
                            end="\r",
                            file=sys.stderr,
                        )
                else:
                    cool -= 1
            print("")

            if len(audio) - 1 not in transients:
                transients.append(len(audio) - 1)

            directory = f[1] if (args.to_dir and args.output is None) else args.output
            if directory and not os.path.exists(directory):
                os.mkdir(directory)

            for i in range(1, len(transients)):
                seg = audio[transients[i - 1] : transients[i]]
                seg.export(
                    "{}{}_{}.{}".format(
                        (directory + "/" if directory else ""),
                        f[1],
                        i,
                        args.format,
                    ),
                    args.format,
                )
    except Exception as e:
        print(f"failure: {e}", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
