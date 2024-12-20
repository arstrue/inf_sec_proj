#! /usr/bin/python
import numpy as np
from argparse import ArgumentParser
import sys

def KSA(key):
    keylength = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % keylength]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K
        
def RC4(key):
    S = KSA(key)
    return PRGA(S)

def encrypt(key, plaintext):
    keystream = RC4(key)
    res = []
    for c in plaintext:
        val = c ^ next(keystream)
        res.append(val)
    return bytes(res)


def main():

    key = b'\x73\x75\x70\x65\x72\x5f\x73\x65\x63\x72\x65\x74\x5f\x74\x65\x73\x74\x5f\x6b\x65\x79'

    parser = ArgumentParser()
    parser.add_argument("knownPlaintext")
    parser.add_argument("unknownPlaintext")
    args = parser.parse_args()

    knownPlaintext = args.knownPlaintext
    unknownPlaintext = args.unknownPlaintext

    knownchiphertext = encrypt(key, knownPlaintext.encode('utf-8'))
    unknownchiphertext = encrypt(key, unknownPlaintext.encode('utf-8'))

    print("knownPlaintext: ", knownPlaintext)
    print("knownCiphertext: ", knownchiphertext.hex())
    print("unknownPlaintext: ", unknownPlaintext)
    print("unknownCiphertext: ", unknownchiphertext.hex())

    with open ("knownplaintext.txt", "w") as outfile:
        outfile.write(knownPlaintext)
    with open ("unknownplaintext.txt", "w") as outfile:
        outfile.write(unknownPlaintext)
    with open ("known_ciphertext.rc4", "wb") as outfile:
        outfile.write(knownchiphertext)
    with open ("unknown_ciphertext.rc4", "wb") as outfile:
        outfile.write(unknownchiphertext)

if __name__=='__main__':
	main()
