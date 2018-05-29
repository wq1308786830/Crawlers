import base64
import hashlib
import json

import os
import scrapy
from Crypto.Cipher import AES


class NeteaseSpider(scrapy.Spider):
    name = "Netease"
    modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68a' \
              'ce615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341' \
              'f56135fccf695280104e0312ecbda92557c93870114af6c9d05c' \
              '4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82' \
              '047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    nonce = '0CoJUm6Qyw8W8jud'
    pubKey = '010001'

    def start_requests(self):
        urls = [
            'https://music.163.com/'
        ]

        md5 = hashlib.md5()
        md5.update('92QWWQ0828MM'.encode())
        psw = md5.hexdigest()
        text = {
            'username': '18357006605',
            'password': psw,
            'rememberLogin': 'true'
        }
        text = json.dumps(text)
        secKey = self.createSecretKey(16)
        encText = self.aesEncrypt(self.aesEncrypt(text, self.nonce), secKey)
        encSecKey = self.rsaEncrypt(secKey, self.pubKey, self.modulus)
        data = {
            'params': encText,
            'encSecKey': encSecKey
        }

        for url in urls:
            print('secKey: %s, encText: %s, encSecKey: %s', secKey, encText, encSecKey)
            yield scrapy.Request(url=url, method='POST', body=data, callback=self.parse)

    def parse(self, response):
        print('\n\n\nLogin Success!')

    def aesEncrypt(self, text, secKey):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(secKey, 2, '0102030405060708')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext

    def rsaEncrypt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = int(text.encode('hex'), 16) ** int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def createSecretKey(self, size):
        return (''.join(map(lambda xx: (hex(ord(xx))[2:]), list(os.urandom(size)))))[0:16]
