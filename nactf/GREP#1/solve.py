```python
import re
flags = open('flag.txt').read().splitlines()
for flag in flags:
	regx = re.search("_[aeiou][aeiou][aeiou][aeiou][aeiou][aeiou][aeiou]}",flag)

	if regx:
		print flag
```
### nactf{r3gul4r_3xpr3ss10ns_ar3_m0r3_th4n_r3gul4r_euaiooa}
