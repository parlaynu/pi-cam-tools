#!/usr/bin/env python3
import hqlib


def main():

    pipe = hqlib.camera(preview=True)
    for i in pipe:
        pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

