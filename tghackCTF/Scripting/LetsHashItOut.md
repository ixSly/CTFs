``Remember the spells from Echo Chamber? Well, they're back! You will have to answer 100 questions before you get the flag.
nc hash.tghack.no 2001``

```python

import socket
import subprocess
import re
import struct
import binascii as bs

import hashlib

s = socket.socket()
s.connect(('hash.tghack.no', 2001))

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def sh512(str):
    hash_object = hashlib.sha512(str)
    return hash_object.hexdigest()




def md(str):
    hash_object = hashlib.md5(str)
    return hash_object.hexdigest()


while True:

    cmd = s.recv(1024)
    print (cmd)
    method = re.search("Hash me using (.*),",cmd).group(1).lower()
    str = re.search(": (.*)",cmd).group(1)

    if method == "md5":
        answer = md(str)
        bs.hexlify(answer)
        print answer
        s.sendall(answer + "\n")

    if method == "sha256":




        s.sendall(encrypt_string(str) + "\n")

    if method == "sha512":
        answer = sh512(str)
        bs.hexlify(answer)
        print answer
        s.sendall(answer + "\n")

#TG19{one_order_of_sha256_hashbrowns_please}       

```
