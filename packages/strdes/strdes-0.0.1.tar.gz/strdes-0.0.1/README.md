# StrDES
**strdes** is a easy to use string encrypt and decrypt library. 

Refactoring from [des.js](https://sso.scut.edu.cn/cas/comm/js/des.js), the original author is Guapo.

```py
>>> import strdes
>>> strdes.strEnc('abcd', 'a', 'b', 'c')
'238A77E95631FDAA'
>>> strdes.strDec('238A77E95631FDAA', 'a', 'b', 'c')
'abcd'
```

## Installing
strdes is available on PyPI, install via `pip install strdes`.