 <h4>  Found File  </h4> 

``` We found the following file on a machine, we know it contains a secret but we don&#039;t know what this file is can you help us obtain the code?  ```



```
$ strings foundfile 
SYNT{SBERAFVPF_101}
HelloWorld
java/lang/Object
java/lang/String
length
charAt
....

Decoded " SYNT{SBERAFVPF_101} " with Caesar Cipher with the key 13 and I got this : flag{forensics_101}  

```

<h4> Help Ann </h4>

``` Ann scanned a QR code of an item, she tried to open the image but it seems it was corrupted, can you identify what is Ann lost item? ```

``` 
$ file help_ann_please
help_ann_please: data 

$ xxd help_ann_please | head
00000000: 0050 4e47 0d0a 1a0a 0000 000d 4948 4452  .PNG........IHDR

PNG file signature is 89 50 4E 47 0D 0A 1A 0A , lets edit this using iHex .

$ $ xxd help_ann_please | head
00000000: 8950 4e47 0d0a 1a0a 0000 000d 4948 4452  .PNG........IHDR
 And using zbar I decoded and got the flag .. 
 
$ $ zbarimg help_ann_please
QR-Code:Flag{Aw3s0m3-Y0u-G0t-th1s}

```


<h4> Just Smile </h4>


```
Can you find the flag hidden in the image.
```

``` 
$ file smile.png 
smile.png: PNG image data, 480 x 480, 8-bit/color RGBA, non-interlaced


$ binwalk smile.png 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 480 x 480, 8-bit/color RGBA, non-interlaced
154           0x9A            Zlib compressed data, best compression
79757         0x1378D         ELF, 64-bit LSB shared object, AMD x86-64, version 1 (SYSV)
87117         0x1544D         LZMA compressed data, properties: 0x89, dictionary size: 16777216 bytes, uncompressed size: 100663296 bytes
87309         0x1550D         LZMA compressed data, properties: 0xA3, dictionary size: 16777216 bytes, uncompressed size: 100663296 bytes
87501         0x155CD         LZMA compressed data, properties: 0xBF, dictionary size: 16777216 bytes, uncompressed size: 33554432 bytes

$ binwalk -e smile.png 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 480 x 480, 8-bit/color RGBA, non-interlaced
154           0x9A            Zlib compressed data, best compression
79757         0x1378D         ELF, 64-bit LSB shared object, AMD x86-64, version 1 (SYSV)
87117         0x1544D         LZMA compressed data, properties: 0x89, dictionary size: 16777216 bytes, uncompressed size: 100663296 bytes
87309         0x1550D         LZMA compressed data, properties: 0xA3, dictionary size: 16777216 bytes, uncompressed size: 100663296 bytes
87501         0x155CD         LZMA compressed data, properties: 0xBF, dictionary size: 16777216 bytes, uncompressed size: 33554432 bytes

$ cd _smile.png-0.extracted/ ; ls -la
total 248
drwxr-xr-x  11 xsly  staff    352 Jan  1 19:59 .
drwx------@ 53 xsly  staff   1696 Jan  1 19:59 ..
-rw-r--r--   1 xsly  staff   8448 Jan  1 19:59 1378D.elf
-rw-r--r--   1 xsly  staff      6 Jan  1 19:59 1544D
-rw-r--r--   1 xsly  staff   1096 Jan  1 19:59 1544D.7z
-rw-r--r--   1 xsly  staff     26 Jan  1 19:59 1550D
-rw-r--r--   1 xsly  staff    904 Jan  1 19:59 1550D.7z
-rw-r--r--   1 xsly  staff      6 Jan  1 19:59 155CD
-rw-r--r--   1 xsly  staff    712 Jan  1 19:59 155CD.7z
-rw-r--r--   1 xsly  staff      0 Jan  1 19:59 9A
-rw-r--r--   1 xsly  staff  88051 Jan  1 19:59 9A.zlib


$ chmod +x 1378D.elf 
$ ./1378D.elf 
Say the password:

$ strings 1378D.elf 
ABCDEFGHH
IJKLMNOPH
QRSTUVWXH
YZ{}f
This_Is_H
Not_the_H
Flag_butH
_Useful
dH3

I used  "This_Is_Not_the_Flag_but_Useful" as the password and it worked . 

$ python -c "print 'This_Is_Not_the_Flag_but_Useful' " |  ./1378D.elf 
Say the password:FLAG{APPENEDING_FILES_REALLY!!}

```
<h4> Light </h4>

```
Just get the flag
```
```
$ file Light 
Light: PNG image data, 381 x 393, 8-bit/color RGBA, non-interlaced

$ strings Light | tail
0}&1
of#1
M?kRh
KCbbe
pfWdy
yxGA
N5W3}
}o7V
IEND
01000110 01101100 01100001 01100111 01111011 01010011 01101111 00101101 01001100 00100001 01100111 01001000 01110100 01111101


Conver Binary to String , 

And I got this 
Flag{So-L!gHt} 

```


<h4> Phone Call </h4>

```
I use phone calls to hunt my victims .what kind of attack i am ?

A : Vishing 
```


<h1> Request Gate </h1> 

```
The flag is in the page , go and see it.
```


```

GET /request-gate/ HTTP/1.1
Host: 35.197.254.240
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9,ar;q=0.8
Cookie: userCookie=Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJOYW1lIjtzOjk6ImFub255bW91cyI7czo3OiJpc0FkbWluIjtiOjA7fQ%3D%3D


HTTP/1.1 405 This page is only accessible via PUT method
Server: nginx/1.10.3 (Ubuntu)
Date: Tue, 01 Jan 2019 16:29:40 GMT
Content-Type: text/html; charset=UTF-8
Transfer-Encoding: chunked
Proxy-Connection: Keep-alive



PUT /request-gate/index.php HTTP/1.1
Host: 35.197.254.240
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9,ar;q=0.8
Cookie: userCookie=Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJOYW1lIjtzOjk6ImFub255bW91cyI7czo3OiJpc0FkbWluIjtiOjA7fQ%3D%3D



HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Tue, 01 Jan 2019 16:32:13 GMT
Content-Type: text/html; charset=UTF-8
Transfer-Encoding: chunked
Proxy-Connection: Keep-alive

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Request Gate</title>

    <!-- Bootstrap -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>

      Here is your flag : M3th0ds!sN0t0nlyG3T0rP0ST

      <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
      <!-- Include all compiled plugins (below), or include individual files as needed -->
      <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
      <script>

      </script>
    </body>
  </html>



The Flag is : M3th0ds!sN0t0nlyG3T0rP0ST



```


<h4> Wanna some Biscuits </h4>

```
We believe we made a good job protecting our website, can you bypass our controls.
```

```
GET /wantbiscuits/ HTTP/1.1
Host: 35.197.254.240
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9,ar;q=0.8
Cookie: userCookie=Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJOYW1lIjtzOjk6ImFub255bW91cyI7czo3OiJpc0FkbWluIjtiOjA7fQ%3D%3D


HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Tue, 01 Jan 2019 16:36:15 GMT
Content-Type: text/html; charset=UTF-8
Set-Cookie: userCookie=Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJOYW1lIjtzOjk6ImFub255bW91cyI7czo3OiJpc0FkbWluIjtiOjA7fQ%3D%3D; expires=Thu, 31-Jan-2019 16:36:15 GMT; Max-Age=2592000; path=/
Content-Encoding: gzip
Transfer-Encoding: chunked
Proxy-Connection: Keep-alive

Hello anonymous</br>



$ echo Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJOYW1lIjtzOjk6ImFub255bW91cyI7czo3OiJpc0FkbWluIjtiOjA7fQ== | base64 -D
O:4:"User":2:{s:8:"userName";s:9:"anonymous";s:7:"isAdmin";b:0;}

Its Serelized using PHP Serialize Function . 

the "s" means a String
the number after means the length of the String
the "b" is a bool and 0 equals to false and 1 equals true

New Payalod 

O:4:"User":2:{s:8:"userName";s:5:"admin";s:7:"isAdmin";b:1;}

and base64 encode it ..

$ curl -H 'Host: 35.197.254.240' -H 'Cookie: userCookie=Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJOYW1lIjtzOjU6ImFkbWluIjtzOjc6ImlzQWRtaW4iO2I6MTt9' 'http://35.197.254.240/wantbiscuits/'
Hello admin</br>You got me, here's the flag: FLAG{REALLY!!_IN_COOKIES}


The Flag : FLAG{REALLY!!_IN_COOKIES}


```

<h4> Yellow Duck </h4>


```
he ducks swim in the river side by side and never left one behind, Have a look!. Note: Flag format flag{XXXXXXXXXX}
```

```
$ curl https://s3-eu-west-1.amazonaws.com/hubchallenges/Forensics/Yellow_duck.png > Yellow_Duck.png

$ strings Yellow_Duck.png  | head
uWB+dz06KjowMDA9eXh0YjAwMcQwMDHEODYwMDD75u+6MDAwOUB4aUMwMD70MDA+9DGlGz4rMDAQ
MHl0cWRIrNyNSYxdZ2XXyy1D3U3q6++rq44RFBE5IHI4kTsgAZKOMnsc9BqUGK49WhlipsKkgkhy
waSCGHWufZmQZWqY1Rv1YoGAegoTIjJ5OA0UEU2v66xL3wnXroPHqkOMD9YoQ55DcaogouyryctM
XkPGbktFS6/Nq9MHTlM8YWUqKioqKioqvl60t8s0KioqKioqKo5OBHJfWFhYWFgINuA4jZGRkZGR
0ShwE8S2tra2trZTML3gKyoqKioqvjEEcl9YWFhYWAg24DiNkZGRkZHRKHATxLa2tra2tlMwveAr
KioqKiq+MQRyX1hYWFhYCDbgOI2RkZGRkdEocBPEtra2tra2UzCTt8s0Kiq+9Po3Hw+3SMcpEbz+
eEHVDJULuUhIJxoLYjrrpOEs/BzzWDkJUS/tOceVgNMWZc3ImKuNdSf+i07b9Z9oToifk5GRkdGR
tIRZWz2/NCzOyxeusC7MDwS1JyE/bhTZwHl5PxM5orJ2GC9l/U/0zmXZuNxw8kYorUqgwSmHAEPy
F1RE0otFUePLhg3Zb+zDAG5qc3Nz83Oydtg9PxvmDkDGAwUsynHhpddbagl5kxJUgn55MHgZoKJm
MncROclpdWUD2TvwEhGstLz+tOGZlOHyDQoKzjO06c+MzeKvzO8/50UGBAQETJPhOI3REffU3y+L

$ strings Yellow_Duck.png | base64 -D | head -n 5 | xxd
00000000: b960 7e77 3d3a 2a3a 3030 303d 7978 7462  .`~w=:*:000=yxtb
00000010: 3030 31c4 3030 31c4 3836 3030 30fb e6ef  001.001.86000...
00000020: ba30 3030 3940 7869 4330 303e f430 303e  .0009@xiC00>.00>
00000030: f431 a51b 3e2b 3030 1030 7974 7164 48ac  .1..>+00.0ytqdH.
00000040: dc8d 498c 5d67 65d7 cb2d 43dd 4dea ebef  ..I.]ge..-C.M...
00000050: abab 8e11 1411 3920 7238 913b 2001 928e  ......9 r8.; ...


It seems to be encrypted in some way , I tried to Brute Force it using XOR Keys .. 


$ strings Yellow_Duck2.png | base64 -D > Yellow_Duck2.png

$ python xor.py Yellow_Duck.png > flag.txt 

$ strings flags.txt | grep png
[0X10]
©png-*:*   -ihdr  !‘  !‘(&   Îˆˇ™   )PhyS  .‰  .‰!µ

So the key is 0x10 . 

```

```python 
x = bytearray(open('Yellow_Duck.png','rb').read())

for i in range(len(x)):
    x[i] ^ = 0x10
open('Dec.png','wb').write(x)
```

```
$ strings Dec.png  | tail -n 3
    iend
FLAG[y
cATCHiT

```


```python 
import pwn

with open('Yellow_Duck2.png', 'r') as myfile:
    data = myfile.read()
    myKey = "\x10"
    print pwn.xor(data,myKey)
    
    for i in range(256):
        message = pwn.xor(pwn.xor(data,myKey),i)
        print message
        

```

```

$ python sly.py > flag.txt


$ strings flag.txt | grep flag
flag{Y0u_CatchIt_0100110120100}


```


<h4> Say my Name </h4>

```
can you find my name?
```





```
$ file a.out 
a.out: ELF 32-bit LSB pie executable Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=58c879e3608583ac3cd08b919a06e9891cd1bd01, not stripped


And the Flow .. 


```




<a href="url"><img src="https://i.imgur.com/K5QEIGm.png" align="left" height="1000" width="1000" ></a> <br>



```
I edited the binary so it will jump always give the flag . 

The edited Flow , it looke like this .

```




<a href="url"><img src="https://i.imgur.com/NYse8Dj.png" align="left" height="1000" width="1000" ></a> <br>





```
$  ./s0x.out 
Please enter your first name:
fewkfew
Please enter your last name:
fewkfkew
Hello Boss, Here's your flag:
CQLCk!OZPLJI-XJO^y
 
 
And then I tried to run it using ltrace.. 


$ ltrace -ff -s 1000 ./s0x.out 
[pid 1515] __libc_start_main(0x5655f68d, 1, 0xfff4fab4, 0x5655f8a0 <unfinished ...>
[pid 1515] puts("Please enter your first name:"Please enter your first name:
) = 30
[pid 1515] memset(0xfff4f9d3, '\0', 7)           = 0xfff4f9d3
[pid 1515] __isoc99_scanf(0x5655f95e, 0xfff4f9d3, 7, 0x5655f6a4fewkfew
) = 1
[pid 1515] puts("Please enter your last name:"Please enter your last name:
)  = 29
[pid 1515] memset(0xfff4f9da, '\0', 7)           = 0xfff4f9da
[pid 1515] __isoc99_scanf(0x5655f95e, 0xfff4f9da, 7, 0x5655f6a4fewfkefew
) = 1
[pid 1515] memset(0xfff4f9e1, '\0', 7)           = 0xfff4f9e1
[pid 1515] strcmp("fewkfew\274\372\364\377\353\370UV\001", "\005\035\r\004\020r") = 1
[pid 1515] puts("Hello Boss, Here's your flag:"Hello Boss, Here's your flag:
) = 30
[pid 1515] strlen("CQLCk!OZPLJI-XJO^y")          = 18
[pid 1515] strlen("CQLCk!OZPLJI-XJO^y")          = 18
[pid 1515] strlen("CQLCk!OZPLJI-XJO^y")          = 18
[pid 1515] strlen("CQLCk!OZPLJI-XJO^y")          = 18
[pid 1515] strlen("CQLCk!OZPLJI-XJO^y")          = 18
[pid 1515] strlen("CQLCk!OZPLJI-XJO^y")          = 18
[pid 1515] strlen("CQLCk!OZPLJI-XJO^y")          = 18
[pid 1515] strlen("CQLCk!OZPLJI-XJO^y")          = 18
[pid 1515] strlen("CQLCk!OZPLJI-XJO^y")          = 18
[pid 1515] strlen("CQLCk!OZPLJI-XJO^y")          = 18
[pid 1515] strlen("CQLCk!OZPLJI-XJO^y")          = 18
[pid 1515] strlen("CQLCk!OZPLJI-XJO^y")          = 18
[pid 1515] strlen("CQLCk!OZPLJI-XJO^y")          = 18
[pid 1515] strlen("CQLCk!OZPLJI-XJO^y")          = 18
[pid 1515] strlen("CQLCk!OZPLJI-XJO^y")          = 18
[pid 1515] strlen("CQLCk!OZPLJI-XJO^y")          = 18
[pid 1515] strlen("CQLCk!OZPLJI-XJO^y")          = 18
[pid 1515] strlen("CQLCk!OZPLJI-XJO^y")          = 18
[pid 1515] strlen("CQLCk!OZPLJI-XJO^y")          = 18
[pid 1515] puts("CQLCk!OZPLJI-XJO^y"CQLCk!OZPLJI-XJO^y
)            = 19
[pid 1515] +++ exited (status 0) +++



So from here , I knew that is XORING with some thing .. 

and if you notice the strcmp("fewkfew\274\372\364\377\353\370UV\001", "\005\035\r\004\020r") = 1

Its comparing my input with weird bytes .. 

I created a python script to XOR "CQLCk!OZPLJI-XJO^y" with this bytes "\005\035\r\004\020r"



```

```python
import pwn


mystring = "CQLCk!OZPLJI-XJO^y"
myKey = "\005\035\r\004\020r"

print pwn.xor(mystring,myKey)

```

```
$ python sly.py 
FLAG{SJG]HZ;(EGKN\x0b

It gave me a part of the flag , and in the end , weird byte "\x0b" So I Added it to the key .

```

```python

import pwn


mystring = "CQLCk!OZPLJI-XJO^y"
myKey = "\005\035\r\004\020r\x0b"

print pwn.xor(mystring,myKey)

```

```

$ python sly.py 

FLAG{SD_MANY_SORS}

The Flag : FLAG{SO_MANY_XORS}

```


