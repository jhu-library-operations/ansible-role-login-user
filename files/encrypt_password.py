#!/usr/bin/env python

import argparse;
from passlib.hash import sha512_crypt;


def main():
    # begin: argument parsing
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--password', required=True,
                        help='password to encrypt')

    parser.add_argument('-e', '--environment', required=True,
                        help='environment in which the password is to be used e.g. dev | stage | prod')

    args = parser.parse_args()
    # end: argument parsing

    hashed = sha512_crypt.using(rounds=5000).hash(args.password)

    print(
    '''
    Password encrypted. Add the following entry to your ini file:
    [{}]
    login_password={}
    '''.format(args.environment, hashed)
    )

if __name__ == "__main__": main()
