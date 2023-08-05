# coding=utf-8

"""
    @header encrpyt_decrpyt_sheet.py
    @abstract   
        加密设计思路：1， 需要自己做一个加密表，表的长度为29位（26个英文字母加3个特殊符号 +，/，=）main_sheet，
                       宽度是一个22位的辅助查询表sub_sheet，另加一个索引坐标定位表 number_sheet
                   2， 加密：
                          * 1> 使用base32先对要加密的字符串（大写）进行编码
                          * 2> 加密时是逐个字符进行加密的
                          * 3> 获取字符在number_sheet中的坐标索引x
                          * 4> 计算结果坐标索引y， mn = 28 - x
                          * 5> 分解mn，取n, 则结果坐标索引 y = 21 - n  注，28, 21分别为main_sheet, sub_sheet的索引最大值（索引从0开始）根据实际情况进行调整
                          * 6> 根据计算出的结果坐标索引 (x,y)，从main_sheet去查询 A = main_sheet[y][x]
                          * 7> 对y值作为索引查询 sub_sheet， B = sub_sheet[y]
                          * 8> 则加密结果为  AB
                          * 9> 例如 加密字符 S -> x=18 mn=28-18=10 n=0 y=21-n=21 A=main_sheet[21][18]=J B=[sub_sheet][21]=W  => JW
                          * 10> 对于数字字符a，直接计算B=21-int(a) 从sub_sheet中查询 A=sub_sheet[B]，获取A后再在前面补"-"， a => -A
                   3， 解密：
                          * 1> 解密时先将字符串两两一组进行分割
                          * 2> 根据两个字符再进行解密，例如 AB 先用于B从 sub_sheet获取索引值y
                          * 3> 根据索引值y，从main_sheet中找到相应的行
                          * 4> 根据行号y，找到的那行再获取A在该行的索引值x ，x=main_sheet[sub_sheet[B]].index(A)
                          * 5> 使用索引值x从number_sheet中获取解密的字符
                          * 6> 对于数字型字符， -A, 直接a = 21 - sub_sheet[A]即可
                          * 7> 最后将所有解密后的字符拼接，再进行base32解码即可

                   4， 随机辅助查询表， 新的功能中加入了随机更换辅助查询表的功能

    @MyBlog: http://www.kuture.com.cn
    @author  Created by Kuture on 2020/9/21
    @version 0.1.2 2020/9/21 Creation()
    
    @Copyright © 2020年 Mr.Li All rights reserved
"""
import pickle
from random import randint
from base64 import b32encode, b32decode


class SecrecSheet(object):

    def __init__(self):
        self._main_sheet = [
            ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
             'W',
             'X', 'Y', 'Z', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '=', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
             'k',
             'l', 'm', 'n', 'o', 'p', 'q', '+', '/', 'a'],
            ['Y', 'Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
             'U',
             'V', 'W', 'X', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '=', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
             'i',
             'j', 'k', 'l', 'm', 'n', 'o', '+', '/', 'a'],
            ['W', 'X', 'Y', 'Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
             'S',
             'T', 'U', 'V', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '=', 'b', 'c', 'd', 'e', 'f',
             'g',
             'h', 'i', 'j', 'k', 'l', 'm', '+', '/', 'a'],
            ['U', 'V', 'W', 'X', 'Y', 'Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
             'Q',
             'R', 'S', 'T', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '=', 'b', 'c', 'd',
             'e',
             'f', 'g', 'h', 'i', 'j', 'k', '+', '/', 'a'],
            ['S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
             'O',
             'P', 'Q', 'R', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
             '=',
             'b', 'c', 'd', 'e', 'f', 'g', '+', '/', 'a'],
            ['Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
             'M',
             'N', 'O', 'P', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '=', 'b',
             'c',
             'd', 'e', 'f', 'g', 'h', 'i', '+', '/', 'a'],
            ['O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
             'K',
             'L', 'M', 'N', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
             'y',
             'z', '=', 'b', 'c', 'd', 'e', '+', '/', 'a'],
            ['M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
             'I',
             'J', 'K', 'L', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
             'w',
             'x', 'y', 'z', '=', 'b', 'c', '+', '/', 'a'],
            ['K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'A', 'B', 'C', 'D', 'E', 'F',
             'G',
             'H', 'I', 'J', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
             'u',
             'v', 'w', 'x', 'y', 'z', '=', '+', '/', 'a'],
            ['I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'A', 'B', 'C', 'D',
             'E',
             'F', 'G', 'H', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
             'v',
             'w', 'x', 'y', 'z', '=', 'b', '+', '/', 'a'],
            ['G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'A', 'B',
             'C',
             'D', 'E', 'F', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
             'x',
             'y', 'z', '=', 'b', 'c', 'd', '+', '/', 'a'],
            ['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
             'A',
             'B', 'C', 'D', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
             'z',
             '=', 'b', 'c', 'd', 'e', 'f', '+', '/', 'a'],
            ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
             'Y',
             'Z', 'A', 'B', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '=',
             'b',
             'c', 'd', 'e', 'f', 'g', 'h', '+', '/', 'a'],
            ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
             'X',
             'Y', 'Z', 'A', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '=', 'b', 'c',
             'd',
             'e', 'f', 'g', 'h', 'i', 'j', '+', '/', 'a'],
            ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
             'Z',
             'A', 'B', 'C', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '=', 'b', 'c', 'd', 'e',
             'f',
             'g', 'h', 'i', 'j', 'k', 'l', '+', '/', 'a'],
            ['F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'A',
             'B',
             'C', 'D', 'E', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '=', 'b', 'c', 'd', 'e', 'f', 'g',
             'h',
             'i', 'j', 'k', 'l', 'm', 'n', '+', '/', 'a'],
            ['J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'A', 'B', 'C', 'D', 'E',
             'F',
             'G', 'H', 'I', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '=', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
             'j',
             'k', 'l', 'm', 'n', 'o', 'p', '+', '/', 'a'],
            ['H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'A', 'B', 'C',
             'D',
             'E', 'F', 'G', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '=', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
             'l',
             'm', 'n', 'o', 'p', 'q', 'r', '+', '/', 'a'],
            ['L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
             'H',
             'I', 'J', 'K', 'u', 'v', 'w', 'x', 'y', 'z', '=', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
             'n',
             'o', 'p', 'q', 'r', 's', 't', '+', '/', 'a'],
            ['N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
             'J',
             'K', 'L', 'M', 'w', 'x', 'y', 'z', '=', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
             'p',
             'q', 'r', 's', 't', 'u', 'v', '+', '/', 'a'],
            ['P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
             'L',
             'M', 'N', 'O', 'y', 'z', '=', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
             'r',
             's', 't', 'u', 'v', 'w', 'x', '+', '/', 'a'],
            ['R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
             'N',
             'O', 'P', 'Q', '=', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
             't',
             'u', 'v', 'w', 'x', 'y', 'z', '+', '/', 'a'],
            ['=', 'b', 'c', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
             'K',
             'L', 'M', 'N', 'O', 'P', 'Q', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
             't',
             'u', 'v', 'w', 'x', 'y', 'z', '+', '/', 'a'],
            ['h', 'i', 'j', 'k', 'l', 'N', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
             'H',
             'I', 'J', 'K', 'L', 'M', 'w', 'x', 'y', 'z', '=', 'b', 'c', 'd', 'e', 'f', 'O', 'P', 'Q', 'g', 'm', 'n', 'o',
             'p',
             'q', 'r', 's', 't', 'u', 'v', '+', '/', 'a'],

        ]

        self._sub_encrypt_sheet_list = [
            ['a', 'Y', '8', '7', '9', 'K', 'u', 'T', 'U', 'R', 'E', 'e', 'I', 'N', 'S', 't', '1', 'i', 'n', 'y', 'J', 'j',
             '0',
             'k'],
            ['A', 'y', '8', '7', '9', 'k', 'U', 't', 'u', 'r', 'e', 'E', 'i', 'n', 's', 'T', '1', 'I', 'N', 'Y', 'j', 'J',
             '0',
             'K'],
            ['a', 'b', '0', '1', 'c', '2', '3', 'd', '5', 'e', '6', 'f', '7', 'g', '8', 'h', 'i', 'j', 'o', 'l', '9', 'm',
             'n',
             'k'],
            ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'Y', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
             'X',
             'K']
        ]

        self._number_sheet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                        'U',
                        'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                        'p',
                        'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '+', '/', '=']

        self._rand_encrypt_dict = {'0': 'k', '1': 'u', '2': 't', '3': 'U'}
        self._rand_decrypt_dict = {'k': '0', 'u': '1', 't': '2', 'U': '3'}


class AKbase2233(SecrecSheet):
    ''' 加密与解密是分别是1对2，2对1的关系，同时在加密与解密过程中需要3个密码表参与查询与处理，故称为2233'''

    def encode(self, input_str, ak_rand=False):
        '''
        :param input_str: input encrypt string
        :param ak_rand:   is ak_rand is True, will be use random secret sheet, encrypt input string
        :return:          return encrypt string
        '''

        # check ak key, if ak rand is exist and use random sub sheet
        rand_str = ''
        if ak_rand:
            rand_num = randint(0, len(self._sub_encrypt_sheet_list) - 1)
            sub_encrypt_sheet = self._sub_encrypt_sheet_list[rand_num]
            rand_str = self._rand_encrypt_dict[str(rand_num)]
        else:
            sub_encrypt_sheet = self._sub_encrypt_sheet_list[0]

        # use base64 encode input str
        if isinstance(input_str, str):
            input_str = input_str.encode()
        base64_en_str = b32encode(input_str)
        base64_en_str = base64_en_str.decode()

        encrypt_list = []
        for encrypt_char in base64_en_str:

            # obtain char index number
            if encrypt_char.isdigit():
                encrypt_result = '-' + sub_encrypt_sheet[len(sub_encrypt_sheet) - 1 - int(encrypt_char)]
            else:
                encrypt_x = self._number_sheet.index(encrypt_char.upper())
                char_number_y = str(len(self._number_sheet) - 1 - encrypt_x)

                # calculator encrypt y index number
                if len(char_number_y) == 2:
                    encrypt_y = len(sub_encrypt_sheet) - 1 - int(char_number_y[1])
                else:
                    encrypt_y = len(sub_encrypt_sheet) - 1 - int(char_number_y)

                # search encrypt char
                main_encrypt_char = self._main_sheet[encrypt_y][encrypt_x]
                sub_encrypt_char = sub_encrypt_sheet[encrypt_y]

                # join main encrypt char and sub encrypt char
                encrypt_result = main_encrypt_char + sub_encrypt_char
            encrypt_list.append(encrypt_result)

        result_encrypt_str = ''.join(encrypt_list)
        if ak_rand: result_encrypt_str = result_encrypt_str + rand_str

        return result_encrypt_str

    def decode(self, input_str, res_decode=False, ak_rand=False):
        '''

        :param input_str:   input string
        :param res_decode:  decode output or not, default is False
        :param ak_rand:     if ak_rand is true, will be use random secrec sheet decrypt input string
        :return:
        '''
        # check ak key, if ak key is exist, use customer key
        if ak_rand:
            rand_str = input_str[-1]
            rand_num = self._rand_decrypt_dict[rand_str]
            sub_encrypt_sheet = self._sub_encrypt_sheet_list[int(rand_num)]
            input_str = input_str[:-1]
        else:
            sub_encrypt_sheet = self._sub_encrypt_sheet_list[0]

        input_str_length = int(len(input_str) / 2)
        input_str_list = [input_str[a * 2:(a + 1) * 2] for a in range(input_str_length)]

        decrypt_list = []
        for en_str in input_str_list:
            # decrypt number char
            if '-' in en_str:
                result_char = str(len(sub_encrypt_sheet) - 1 - sub_encrypt_sheet.index(en_str[1]))
            # decrypt string char
            else:
                tail_char = en_str[1]
                tail_char_index = sub_encrypt_sheet.index(tail_char)
                start_char_index = self._main_sheet[tail_char_index].index(en_str[0])
                result_char = self._number_sheet[start_char_index]
            decrypt_list.append(result_char)

        result_str = ''.join(decrypt_list)
        decrypt_result = b32decode(result_str.encode())
        if res_decode:
            decrypt_result = decrypt_result.decode()

        return decrypt_result


if __name__ == '__main__':

    ak2233 = AKbase2233()

    input_str = 'www.kuture.com.cn'
    print('{} Input: {}'.format(len(input_str), input_str))
    encrypt_result = ak2233.encode(input_str, ak_rand=True)
    print('{} Encrypt Result: {}'.format(len(encrypt_result), encrypt_result))

    decrypt_result = ak2233.decode(encrypt_result, res_decode=True, ak_rand=True)
    print('Decrypt Result: ', decrypt_result)










