# Easy_Upload 

Easy Upload was a web challenge in ROIS CTF, with PHP as the backend and Symfony as a Framework. 

It was clear from naming convention that it's a file upload challenge. The challenge had some built-in functions to restrict extension, contents, so it was clear that there were some PHP pitfalls involved. 

```php
<?php
...
{
    public function __construct()
    {
        mb_detect_order(["BASE64","ASCII","UTF-8"]);
        $this->ext_blacklist = [
            "php",
            "ini",
            "phtml",
            "htaccess",
        ];
        $this->content_blacklist = ["<?", "php", "handler"];
    }
    public function invalid($msg){
        return new Response("error occurs: $msg");
    }
    #[Route('/', name: 'upload')]
    public function index(Request $request)
    {
        $uploadHtml = <<<EOF
<html>
<form action="/" enctype="multipart/form-data" method="post">
  <input type="file" id="file" name="file">
  <input type="submit">
</form>
</html>
EOF;

        $file = @$_FILES["file"];
        if($file == null){
            return new Response(
                //'<p>Before start you should know that it\'s not a good challenge.You can\'t get anything from this challenge.If you hate this challenge, just skip plz. </p><p>这道题并不是一道好题，你不会从这道题上获得任何东西。如果你讨厌这道题就直接跳过吧。</p>'
                $uploadHtml
            );
        }else {

            $content = file_get_contents($file["tmp_name"]);
            $charset = mb_detect_encoding($content, null, true);
            if(false !== $charset){
                if($charset == "BASE64"){
                    $content = base64_decode($content);
                }
                foreach ($this->content_blacklist as $v) {
                    if(stristr($content, $v)!==false){
                        return $this->invalid("fucking $v .");
                    }
                }
            }else{
                return $this->invalid("fucking invalid format.");
            }
            $ext = Path::getExtension($file["name"], true);
            if(strstr($file["name"], "..")!==false){
                return $this->$this->invalid("fucking path travel");
            }
            foreach ($this->ext_blacklist as $v){
                if (strstr($ext, $v) !== false){
                    return $this->invalid("fucking $ext extension.");
                }
            }
            $dir = dirname($request->server->get('SCRIPT_FILENAME'));

            $result = move_uploaded_file($file["tmp_name"], "$dir/upload/".strtolower($file["name"]));
            if($result){
                return new Response("upload success");
            }else {
                return new Response("upload failed");
            }
        }
    }
}
```

At first glance it looked somewhat CTFey, though it had some built-in functions, which meant that there is something intresting with it. 

The logic was pretty simple, we CANT upload **php, ini, htaccess and phtml** files due to them existing in **ext_blacklist**. 

The 2nd issue was that even if we could upload a PHP file, we cant use php tags, and yes, this was there to make the challenge more annoying. 

**strstr** was being used to validate our file extension, playing with that locally, it appeared that uploading a file with a an upper case PHP extension (e.g file.PHP) passed the check. 

```php
> php -a
Interactive shell

php > echo strstr("file.php","php") == true;
1
php > echo strstr("file.PHP","php") == true;
php > 

```

This means that we can upload PHP files, here comes the struggling part where we can't execute the files due to the prevention of PHP tags in **content_blacklist**. 


The file contents were being passed through **mb_detect_encoding** which was another built-in function in PHP that detects the encoding. 

If we supply a base64 php webshell, it's going to decode & detect our file contents, so that was not the idea behind the challenge. After doing some research against **mb_detect_encoding**, a [Github issue](https://github.com/php/php-src/issues/9008) popped up. Reproducing the issue resulted in a getting RCE. 



# FileChecker Mini 

FileChecker-mini was a fairly straight forward web challenge in ROIS CTF, a mini Flask web app that has a functionality to upload files. 


```python
from flask import Flask, request, render_template, render_template_string
from waitress import serve
import os
import subprocess


app_dir = os.path.split(os.path.realpath(__file__))[0]
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = f'{app_dir}/upload/'

@app.route('/', methods=['GET','POST'])
def index():
    try:
        if request.method == 'GET':
            return render_template('index.html',result="ヽ(=^･ω･^=)丿 ヽ(=^･ω･^=)丿 ヽ(=^･ω･^=)丿")

        elif request.method == 'POST':
            f = request.files['file-upload']
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)

            if os.path.exists(filepath) and ".." in filepath:
                return render_template('index.html', result="Don't (^=◕ᴥ◕=^) (^=◕ᴥ◕=^) (^=◕ᴥ◕=^)")
            else:
                f.save(filepath)
                file_check_res = subprocess.check_output(
                    ["/bin/file", "-b", filepath], 
                    shell=False, 
                    encoding='utf-8',
                    timeout=1
                )
                os.remove(filepath)
                if "empty" in file_check_res or "cannot open" in file_check_res:
                    file_check_res="wafxixi ฅ•ω•ฅ ฅ•ω•ฅ ฅ•ω•ฅ"
                return render_template_string(file_check_res)

    except:
        return render_template('index.html', result='Error ฅ(๑*д*๑)ฅ ฅ(๑*д*๑)ฅ ฅ(๑*д*๑)ฅ')


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=3000, threads=1000, cleanup_interval=30)
```


Once the file is being uploaded, **/bin/file** gets executed with with **-b flag** to remove the filename from the output. Since ***file_check_res*** is being rendered with **render_template_string**, it was a matter of having /bin/file to output extra information that we control, **metadata** in this case, that way we can use a simple SSTI payload to get code execution.

injection the following code as a metadata resulted in RCE

```python
{{[].__class__.__mro__[1].__subclasses__()[127].__init__.__globals__['popen']('ls').read()}} 
```


# FileChecker Plus

FileChecker Plus was a revenge of the mini challenge, having the same code with a very minor modifications, where **render_template** won't render what we supply. 

```python
from flask import Flask, request, render_template, render_template_string
from waitress import serve
import os
import subprocess

app_dir = os.path.split(os.path.realpath(__file__))[0]
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = f'{app_dir}/upload/'

@app.route('/', methods=['GET','POST'])
def index():
    try:
        if request.method == 'GET':
            return render_template('index.html',result="ヽ(=^･ω･^=)丿 ヽ(=^･ω･^=)丿 ヽ(=^･ω･^=)丿")

        elif request.method == 'POST':
            f = request.files['file-upload']
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)

            if os.path.exists(filepath) and ".." in filepath:
                return render_template('index.html', result="Don't (^=◕ᴥ◕=^) (^=◕ᴥ◕=^) (^=◕ᴥ◕=^)")
            else:
                f.save(filepath)
                file_check_res = subprocess.check_output(
                    ["/bin/file", "-b", filepath], 
                    shell=False, 
                    encoding='utf-8',
                    timeout=1
                )
                os.remove(filepath)
                if "empty" in file_check_res or "cannot open" in file_check_res:
                    file_check_res="wafxixi ฅ•ω•ฅ ฅ•ω•ฅ ฅ•ω•ฅ"
                return render_template('index.html', result=file_check_res)

    except:
        return render_template('index.html', result='Error ฅ(๑*д*๑)ฅ ฅ(๑*д*๑)ฅ ฅ(๑*д*๑)ฅ')

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=3000, threads=1000, cleanup_interval=30) 
```

However, it was using **path.join** to save our filepath, where the path was the 2nd argument in path.join, it was no secret that there's room for file overwrite. 

In cases os.path.join is being used and the 2nd input is an input where the user can control, there's a trick to supply an absolute path (e.g /etc/passwd) as a 2nd argument, the return value will result in being the absoulute path that we control. 


```python
> python
Python 3.10.8 (main, Nov  4 2022, 09:21:25) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import os
>>> uploaddir = "/upload/"
>>> userinput = "/etc/passwd"
>>> filepath = os.path.join(uploaddir,userinput)
>>> filepath
'/etc/passwd'
```

This means that we can overwrite files on the system, the challenging part was to come up with ideas, one was to simply overwrite **/bin/file** and get code execution, testing that locally worked, not on the remote target sadly :(. 

HOWEVER, one suggested to overwrite **/app/templates/index.html** containing an SSTI payload, fighting with the remote target for a bit resulted in an RCE, so whoever was visiting the page during the time we've been fighting with the remote host got the flag as well. 

### GOTCHAS 

The same vulnerability existed on the mini challenge, because the user was set to **nobody**, this techqniue wouldn't work due insuffucient privileges. 


