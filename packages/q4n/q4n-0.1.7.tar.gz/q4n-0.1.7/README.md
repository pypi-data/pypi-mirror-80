# mypwn

自己用的pwntools

暂时只在python2上测试

roputils: `https://github.com/inaz2/roputils`
can use to solve ret2dlresolve

## install

```bash
sudo pip install q4n
```

## PWN

这个class只是单独的对pwntools进行了简化。。 这样在编写exp的时候不需要编写那么多lambda函数

```python
from q4n import *
r=PWN("./pwn","./libc","./ld",aslr=False, timeout=2)
# r=BlindPWN(ip, port)

r.proc()
# r.remote(ip, port)

r.sla("hello","bb")
r.ru("xx") # drop==True

r.sl("zai?")
r.sd("kkp")

r.ia()
```

## AWD 相关

#### IPLIST

```python
IPLIST("192.168.1-100-2.1").result
# 返回一个list
```

#### FXXK...

这个是打全场的passwd的=.=

#### PostPWN

假如程序中没有加入alarm或者是timeout的时候，pwn是可以权限维持的。

这个类需要提供一个`submit flag`的function才能正常提交flag

传入的参数是一个`remote`的List

perhaps you can exec challenge program for test

#### SUBMMIT

提交flag的类

#### parse_tcp_stream

tcpstream流量分析（py3脚本，单独放在py3/下）

## payload

#### Fmt(Fmt_v2)

generate fmt payload automatically


