# -*- coding: utf-8 -*-

"""
strdes En/Decrypt Library
~~~~~~~~~~~~~~~~~~~~~~

strdes is an En/Decrypt library, written in Python.
Basic Encrypt usage:

   >>> import strdes
   >>> strdes.strEnc('abcd', 'a', 'b', 'c')
   '238A77E95631FDAA'
   >>> strdes.strDec('238A77E95631FDAA', 'a', 'b', 'c')
   'abcd'

:copyright: (c) 2020 by tootal.
"""

from .des import strEnc, strDec