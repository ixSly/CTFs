<b>Echo back what you receive 50 times! See the Python tutorial for more information</b>

<b>nc echo.tghack.no 5555</b>

```python

import socket
import subprocess

s = socket.socket()
s.connect(('echo.tghack.no', 5555))

while True:
    cmd = s.recv(1024)
    print cmd

  	
    s.sendall(cmd)

#TG19{behold_the_echo_chamber_of_secrets}    
```
