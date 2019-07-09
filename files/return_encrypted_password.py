#!/usr/bin/env python

import argparse;
from passlib.hash import sha512_crypt;


def main():
    # begin: argument parsing
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--password', required=True,
                        help='password to encrypt')

    args = parser.parse_args()
    # end: argument parsing

    hashed = sha512_crypt.using(rounds=5000).hash(args.password)

    print(hashed)

if __name__ == "__main__": main()
