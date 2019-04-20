`Can you answer 1000 math questions? nc math.tghack.no 10000`

```python
import socket
import subprocess
import re
import struct
import hashlib

s = socket.socket()
s.connect(('math.tghack.no', 10000))

while True:

    cmd = s.recv(1024)
    print (cmd)

    stNum = re.search(" (.*) ",cmd).group(1)
    numbers = re.findall('[0-9]+', cmd)

    q = numbers[2] + stNum + numbers[3]

    x = int(eval(q))

    s.sendall(str(x) + "\n")
#TG19{calculate_all_the_things}
```
