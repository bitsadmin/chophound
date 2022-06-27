import mmap
import argparse

VERSION = 1.0

def main(args):
    file = args.file
    verbose = args.verbose
    crapbytes = []

    print('Locating non-ASCII characters in %s' % file)
    with open(file, 'r+b') as f:
        mem = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        offset = 0
        for byte in mem:
            obyte = ord(byte)
            if (obyte < 0x20 or obyte > 0x7e) and obyte not in (0x0a, 0x0d):
                crapbytes.append(offset)
                if verbose:
                    print("Found non-ASCII character at offset 0x%.8x" % offset)

            offset += 1

        mem.close()
    print('Found a total of %d non-ASCII characters' % len(crapbytes))

    print('Fixing non-ASCII characters in %s' % file)
    with open(file, 'r+b') as f:
        mem = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)

        # Navigate to offset and write question mark
        for offset in crapbytes:
            if verbose:
                print("Writing '?' to offset 0x%.8x" % offset)
            mem.seek(offset)
            mem.write_byte(0x3f)

        mem.close()
    print('Fixed a total of %d non-ASCII characters' % len(crapbytes))

def getargs():
    parser = argparse.ArgumentParser(
        description='In-place replacement of non-ASCII characters to question marks'
    )
    parser.add_argument('file', help='File to replace non-ASCII characters in')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Show verbose output')

    return parser.parse_args()

if __name__ == '__main__':
    print('ReplaceNonASCII v%.2f ( https://github.com/bitsadmin/chophound/ )' % VERSION)
    main(getargs())
