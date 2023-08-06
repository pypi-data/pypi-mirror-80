def generateKeys(keyByte):
    key = [0] * 56
    keys = [0] * 16
    for i in range(7):
        for j in range(8):
            key[i * 8 + j] = keyByte[8 * (7 - j) + i]
    for i in range(16):
        for j in range([1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1][i]):
            key = key[1:28] + key[0:1] + key[29:56] + key[28:29]
        keys[i] = [key[x] for x in [
            13, 16, 10, 23,  0,  4,  2, 27,
            14,  5, 20,  9, 22, 18, 11,  3,
            25,  7, 15,  6, 26, 19, 12,  1,
            40, 51, 30, 36, 46, 54, 29, 39,
            50, 44, 32, 47, 43, 48, 38, 55,
            33, 52, 45, 41, 49, 35, 28, 31
        ]]
    return keys


def initPermute(originalData):
    ipByte = [0] * 64
    for i in range(4):
        for k in range(8):
            ipByte[i * 8 + k] = originalData[(7 - k) * 8 + (2 * i + 1)]
            ipByte[i * 8 + k + 32] = originalData[(7 - k) * 8 + 2 * i]
    return ipByte


def expandPermute(rightData):
    epByte = [0] * 48
    for i in range(8):
        epByte[i * 6] = rightData[31 if i == 0 else i * 4 - 1]
        for k in range(4):
            epByte[i * 6 + k + 1] = rightData[i * 4 + k]
        epByte[i * 6 + 5] = rightData[0 if i == 7 else i * 4 + 4]
    return epByte


def xor(byteOne, byteTwo):
    return [x[0] ^ x[1] for x in zip(byteOne, byteTwo)]


def sBoxPermute(expandByte):
    sBoxByte = [0] * 32
    binary = ''
    s = \
        [
            [
                [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
            ],
            [
                [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
            ],
            [
                [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
            ],
            [
                [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
            ],
            [
                [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
            ],
            [
                [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
            ],
            [
                [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
            ],
            [
                [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
            ]
        ]
    for m in range(8):
        i = expandByte[m * 6] * 2 + expandByte[m * 6 + 5]
        j = expandByte[m * 6 + 1] * 2 * 2 * 2 +\
            expandByte[m * 6 + 2] * 2 * 2 +\
            expandByte[m * 6 + 3] * 2 +\
            expandByte[m * 6 + 4]
        binary = '{:04b}'.format(s[m][i][j])
        for k in range(4):
            sBoxByte[m * 4 + k] = int(binary[k])
    return sBoxByte


def pPermute(sBoxByte):
    return [sBoxByte[x] for x in [
        15, 6, 19, 20, 28, 11, 27, 16,
        0, 14, 22, 25, 4, 17, 30, 9,
        1, 7, 23, 13, 31, 26, 2, 8,
        18, 12, 29, 5, 21, 10, 3, 24
    ]]


def finallyPermute(endByte):
    return [endByte[x] for x in [
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25,
        32, 0, 40, 8, 48, 16, 56, 24
    ]]


def crypt(dataByte, keyByte, mode):
    keys = generateKeys(keyByte)
    ipByte = initPermute(dataByte)
    ipLeft, ipRight = ipByte[0:32], ipByte[32:64]
    for i in range(16)[::mode]:
        tempLeft = ipLeft
        ipLeft = ipRight
        ipRight = xor(pPermute(sBoxPermute(
            xor(expandPermute(ipRight), keys[i]))), tempLeft)
    return finallyPermute(ipRight + ipLeft)


def enc(dataByte, keyByte):
    return crypt(dataByte, keyByte, 1)


def dec(dataByte, keyByte):
    return crypt(dataByte, keyByte, -1)


def strToBt(s):
    r = len(s) % 4
    s += (4 - r if r else 0) * chr(0)
    bs = ''.join(['{:016b}'.format(ord(x)) for x in s])
    return [int(x) for x in bs]


def getKeyBytes(key):
    return [strToBt(key[i:i+4]) for i in range(0, len(key), 4)]


def bt64ToHex(byteData):
    return hex(int(''.join([str(x) for x in byteData]), 2))[2:].upper()


def strEnc(data, *keys):
    """Encrypt a string with keys to string made up of hex.

    return the encrypted string.
    """
    r = len(data) % 4
    data += (4 - r if r else 0) * chr(0)
    encData = ""
    for i in range(len(data) // 4):
        tempBt = strToBt(data[i * 4: i * 4 + 4])
        for key in keys:
            for b in getKeyBytes(key):
                tempBt = enc(tempBt, b)
        encData += bt64ToHex(tempBt)
    return encData


def byteToString(byteData):
    s = ""
    for b in [byteData[i: i + 16] for i in range(0, len(byteData), 16)]:
        s += chr(int(''.join([str(x) for x in b]), 2))
    return s


def strDec(data, *keys):
    """Decrypt the encrypted string to the original string.

    return the original string.
    """
    decStr = ""
    for s in [data[i: i+16] for i in range(0, len(data), 16)]:
        intByte = [int(x) for x in '{:064b}'.format(int(s, 16))]
        for key in keys[::-1]:
            for b in getKeyBytes(key)[::-1]:
                intByte = dec(intByte, b)
        decStr += byteToString(intByte)
    return decStr
