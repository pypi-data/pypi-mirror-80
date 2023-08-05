#!/usr/bin/env python
import os, sys

def main():
    print("Cozinha --> Paçoquinha!")
    print("este programa está em contrução.")
if __name__ == "__main__":
    rc = 1
    try:
        main()
        rc=0
    except Execution as e:
        print('Error: %e', file=sys.stderr)
    sys.exit(rc)
