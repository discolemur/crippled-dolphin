#! /usr/bin/env python

def main(args) :
    seq = readFile(args.infile)
    result = action(seq)
    print(result)
    write(result, args.outfile)

if __name__ == '__main__' :
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('outfile')
    args = parser.parse_args()
    main(args)
