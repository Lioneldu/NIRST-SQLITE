import sqlite3
import pymysql
import binascii
import numpy as np




def converse(data: str):  # 转换浮点型部分
    data = data.replace(" ", "")  # 消除空格
    start = 1  # 起始第一位0，将其跳过
    result = []
    for i in range(1, len(data)-27, 10):
        firstResult = hexTofloat(data[i:i+5])
        secondResult = hexTofloat(data[i+5:i+10])/2
        result.append(firstResult)
        result.append(secondResult)

    return result

def hexTofloat(data: str):
    firstInt = data[0:3]
    firstDec = data[3:4]
    firstResult = 0
    if int(firstInt, 16) & 0x800:  # 判断是否为负数
        firstInt = int(firstInt, 16) - 0x001
        firstInt = firstInt ^ 0xfff
        firstResult = firstInt
        firstDec = int(firstDec, 16)
        for i in range(4, 0, -1):
            firstResult -= (1 / (2 ** i)) * (firstDec & 0x001)
            firstDec = firstDec >> 1
        firstResult = -firstResult
    else:
        firstInt = int(firstInt, 16)
        firstDec = int(firstDec, 16)
        firstResult = firstInt
        for i in range(4, 0, -1):
            firstResult += (1 / (2 ** i)) * (firstDec & 0x001)
            firstDec = firstDec >> 1

    return firstResult

def hexToint(data, width=16):  # 转换整形部分,最后电量与加速度数据部分
    dec_data = int(data, 16)
    if dec_data > 2 ** (width - 1) - 1:
        dec_data = 2 ** width - dec_data
    dec_data = 0 - dec_data
    return dec_data

def tableConverse(result):
    fulltable = []
    for everyResult in result:
        temp = converse(everyResult[2])
        temp.insert(0, everyResult[1])
        temp.insert(0, everyResult[0])
        fulltable.append(temp)
    return np.array(fulltable)

if __name__ == '__main__':
    sqlName = sqlite3.connect(r"D:\work\文档\戒毒数据\nirsit_export.db")
    cursor = sqlName.cursor()
    cursor.execute("select * from test_000008")
    result = cursor.fetchall()
    fulltable = tableConverse(result)
    # cursor.execute("""select name from sqlite_master where type='table' order by name""")
    # result = cursor.fetchall()
    # print(binascii.a2b_hex(result[0][2][-9:-1]))
    print(sqlName)