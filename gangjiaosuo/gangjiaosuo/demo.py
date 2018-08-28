# -*- coding: utf-8 -*-
# -*- create by gt 18-8-1 -*-
import base64
import requests
# from cryptography.hazmat.backends.openssl import rsa
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA


# public_key = '''-----BEGIN PUBLIC KEY-----
# MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDC2FkFY3OwF45etT0RunPkREd0
# 6W6uvoolQgA0RDsLBduAib4QCLXzDtQQ892qI8n4sOlq5AUUxygwHEoUXi24hWoO
# j6x7OlZ1xTvIKX26gRHssqob4mQR9hCoGfsvwC0rvpAN78XF1cOQ+QHASV8XEAp8
# KrsKg23fYvG86pAY+QIDAQAB
# -----END PUBLIC KEY-----'''
#
# def rsa_encrypt(biz_content, public_key):
#     _p = RSA.importKey(public_key)
#     cipher = Cipher_pkcs1_v1_5.new(_p)
#     biz_content = biz_content.encode('utf-8')
#     cipher_text = base64.b64encode(cipher.encrypt(biz_content))
#     return cipher_text.decode()



# u_name = 'towl770901'
# passwd = 'gt770901'
# account = rsa_encrypt(u_name, public_key)
# print(account)
#
# passd = rsa_encrypt(passwd, public_key)
# print(passd)
# print(account)
# print('*'*100)
# print(passd)
# url = 'http://auth.10jqka.com.cn/verify2?reqtype=unified_login&account={}&passwd={}&rsa_version=default_2&imei=F1460DEE9D99320435B3DC129098A854'.format(account, passd)
# url = 'http://upass.10jqka.com.cn/docookie2.php?userid=458301760&sessionid=13cf130fee1ffc7394481467316cd2e7f&signvalid=2018092611&flag=1'
# url = 'http://s.thsi.cn/cb?js/ta_callback_https.20150328.js;js/m/common/zepto.js'

# url = 'https://basic.10jqka.com.cn/mobile/000001/companyn.html'

# headers= {
#     'User-Agent': 'GetSessionID',
#     # 'Cookie': 'searchGuide=sg; v=Au_-PuBS6AdInew7dHE4Bqz7fgj7lEO23ehHqgF8i95lUAT2CWTTBu241_sS; ClientInfo=eyJudW0iOjMsInJlY29yZCI6W3siY2xpZW50SUQiOjUsIklzTG9naW4iOmZhbHNlLCJJc0d1ZXN0IjpmYWxzZSwiQ2xpZW50S2V5IjoiIiwiVXNlcklEIjoiNDU2MTg3MDI4IiwiTWFjQWRkcmVzcyI6Ijg0LTNhLTRiLTFmLWI3LWRhOzNjLTk3LTBlLTYyLWRhLTM5OzAwLTUwLTU2LWMwLTAwLTAxOzAwLTUwLTU2LWMwLTAwLTA4OyIsIlVzZXJOYW1lIjoiZ3Q4MDk4MDI3NDciLCJOaWNrTmFtZSI6IiIsIkxvZ2luVGltZSI6IjIwMTgtMDctMzEgMTY6NDA6MzYiLCJMb2dvdXRUaW1lIjoiMjAxOC0wNy0zMSAxNjo0MTozMSJ9LHsiY2xpZW50SUQiOjYsIklzTG9naW4iOmZhbHNlLCJJc0d1ZXN0IjpmYWxzZSwiQ2xpZW50S2V5IjoiIiwiVXNlcklEIjoiNDU4MjkwODg2IiwiTWFjQWRkcmVzcyI6Ijg0LTNhLTRiLTFmLWI3LWRhOzNjLTk3LTBlLTYyLWRhLTM5OzAwLTUwLTU2LWMwLTAwLTAxOzAwLTUwLTU2LWMwLTAwLTA4OyIsIlVzZXJOYW1lIjoidG93bDc3MDkwMSIsIk5pY2tOYW1lIjoiIiwiTG9naW5UaW1lIjoiMjAxOC0wNy0zMSAxNjo0NToxNSIsIkxvZ291dFRpbWUiOiIyMDE4LTA3LTMxIDE2OjQ4OjI2In0seyJjbGllbnRJRCI6OSwiSXNMb2dpbiI6dHJ1ZSwiSXNHdWVzdCI6dHJ1ZSwiQ2xpZW50S2V5IjoibmM1NzkzYkowMmlIaGc3Zzc5aDhGRTIzQzY3RjY4ZjliTldQcnlvV0tJSEhxMGVhRWczVWZIaTJtNEJkajlkTm9XaVgzRUNjR1lLa1h6QW5lWWxJUGpudVY1ZGZZN2FDaUw5T0tTanRxMWhqRml5SFU0cmwwUW8lMkZsOUlndW1CZmR0ckt3REl0dkk2SHUyM1BDR0h0VUE0Q1hQT1ByZzkxc1JUTHBHdWNGTkFtMENaUiUyQlVJelpZJTJCbW85Q3BGcGcwaHBJJTJCem5iN1p1OCUzRCIsIlVzZXJJRCI6IjQ1ODMwMTc2MCIsIk1hY0FkZHJlc3MiOiI4NC0zYS00Yi0xZi1iNy1kYTszYy05Ny0wZS02Mi1kYS0zOTswMC01MC01Ni1jMC0wMC0wMTswMC01MC01Ni1jMC0wMC0wODsiLCJVc2VyTmFtZSI6InRoc2d1ZXN0X2w0OWxqb2d0IiwiTmlja05hbWUiOiIiLCJMb2dpblRpbWUiOiIyMDE4LTA4LTAxIDE4OjAzOjE5IiwiTG9nb3V0VGltZSI6IiJ9XX0=; @#!userid!#@=458301760; @#!sessionid!#@=13cf130fee1ffc7394481467316cd2e7f; @#!rsa_version!#@=default_2'
#
# }
# headers= {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
#     'Cookie': 'searchGuide=sg; v=Au_-PuBS6AdInew7dHE4Bqz7fgj7lEO23ehHqgF8i95lUAT2CWTTBu241_sS; ClientInfo=eyJudW0iOjMsInJlY29yZCI6W3siY2xpZW50SUQiOjUsIklzTG9naW4iOmZhbHNlLCJJc0d1ZXN0IjpmYWxzZSwiQ2xpZW50S2V5IjoiIiwiVXNlcklEIjoiNDU2MTg3MDI4IiwiTWFjQWRkcmVzcyI6Ijg0LTNhLTRiLTFmLWI3LWRhOzNjLTk3LTBlLTYyLWRhLTM5OzAwLTUwLTU2LWMwLTAwLTAxOzAwLTUwLTU2LWMwLTAwLTA4OyIsIlVzZXJOYW1lIjoiZ3Q4MDk4MDI3NDciLCJOaWNrTmFtZSI6IiIsIkxvZ2luVGltZSI6IjIwMTgtMDctMzEgMTY6NDA6MzYiLCJMb2dvdXRUaW1lIjoiMjAxOC0wNy0zMSAxNjo0MTozMSJ9LHsiY2xpZW50SUQiOjYsIklzTG9naW4iOmZhbHNlLCJJc0d1ZXN0IjpmYWxzZSwiQ2xpZW50S2V5IjoiIiwiVXNlcklEIjoiNDU4MjkwODg2IiwiTWFjQWRkcmVzcyI6Ijg0LTNhLTRiLTFmLWI3LWRhOzNjLTk3LTBlLTYyLWRhLTM5OzAwLTUwLTU2LWMwLTAwLTAxOzAwLTUwLTU2LWMwLTAwLTA4OyIsIlVzZXJOYW1lIjoidG93bDc3MDkwMSIsIk5pY2tOYW1lIjoiIiwiTG9naW5UaW1lIjoiMjAxOC0wNy0zMSAxNjo0NToxNSIsIkxvZ291dFRpbWUiOiIyMDE4LTA3LTMxIDE2OjQ4OjI2In0seyJjbGllbnRJRCI6OSwiSXNMb2dpbiI6dHJ1ZSwiSXNHdWVzdCI6dHJ1ZSwiQ2xpZW50S2V5IjoibmM1NzkzYkowMmlIaGc3Zzc5aDhGRTIzQzY3RjY4ZjliTldQcnlvV0tJSEhxMGVhRWczVWZIaTJtNEJkajlkTm9XaVgzRUNjR1lLa1h6QW5lWWxJUGpudVY1ZGZZN2FDaUw5T0tTanRxMWhqRml5SFU0cmwwUW8lMkZsOUlndW1CZmR0ckt3REl0dkk2SHUyM1BDR0h0VUE0Q1hQT1ByZzkxc1JUTHBHdWNGTkFtMENaUiUyQlVJelpZJTJCbW85Q3BGcGcwaHBJJTJCem5iN1p1OCUzRCIsIlVzZXJJRCI6IjQ1ODMwMTc2MCIsIk1hY0FkZHJlc3MiOiI4NC0zYS00Yi0xZi1iNy1kYTszYy05Ny0wZS02Mi1kYS0zOTswMC01MC01Ni1jMC0wMC0wMTswMC01MC01Ni1jMC0wMC0wODsiLCJVc2VyTmFtZSI6InRoc2d1ZXN0X2w0OWxqb2d0IiwiTmlja05hbWUiOiIiLCJMb2dpblRpbWUiOiIyMDE4LTA4LTAxIDE4OjAzOjE5IiwiTG9nb3V0VGltZSI6IiJ9XX0=; @#!userid!#@=458301760; @#!sessionid!#@=13cf130fee1ffc7394481467316cd2e7f; @#!rsa_version!#@=default_2'
#
# }
url = 'https://basic.10jqka.com.cn/mobile/ajax/finance/000001/maintablen/all'
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G950F Build/LMY48Z) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Safari/537.36 Hexin_Gphone/9.63.13 (Royal Flush) hxtheme/1 innerversion/G037.08.320.1.32 userid/-458478636',
     # 'Cookie':'v=Au_-PuBS6AdInew7dHE4Bqz7fgj7lEO23ehHqgF8i95lUAT2CWTTBu241_sS'
     # 'Cookie':'v=Au_-PuBS6AdInew7dHE4Bqz7fgj7lEO23ehHqgF8i95lUAT2CWTTBu241_sS'

    # 'Cookie': 'user=MDp0b3dsNzcwOTAxOjpOb25lOjUwMDo0NjgyOTA4ODY6NywxMTExMTExMTExMSw0MDs0NCwxMSw0MDs2LDEsNDA7NSwxLDQwOzEsMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOjo6OjQ1ODI5MDg4NjoxNTMzMDk5MTI1Ojo6MTUzMzAyNjY0MDoyNjc4NDAwOjA6MWM4NjI2ZjM4NWIwMzFmOWMwNWE0ZWM0ZTM4YzM5ZmIwOjow; v=AquNG149dJNpZKjHTSihio56M8SVwL9COdSD9h0oh-pBvMC-pZBPkkmkE0Uu'
}
response = requests.get(
    url=url,
    headers=headers
)
data = response.content.decode('gbk')
print(data)
# print(response.cookies)
# with open('1.js', 'w') as f:
#     f.write(data)
# import hashlib

#'Cookie': 'user=MDp0b3dsNzcwOTAxOjpOb25lOjUwMDo0NjgyOTA4ODY6NywxMTExMTExMTExMSw0MDs0NCwxMSw0MDs2LDEsNDA7NSwxLDQwOzEsMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOjo6OjQ1ODI5MDg4NjoxNTMzMDk5MTI1Ojo6MTUzMzAyNjY0MDoyNjc4NDAwOjA6MWM4NjI2ZjM4NWIwMzFmOWMwNWE0ZWM0ZTM4YzM5ZmIwOjow; userid=458290886; u_name=towl770901; escapename=towl770901; ticket=53cca22a97ba81912cc5dea34517ca5e; historystock=000001; hxmPid=free_stock_fincanaly_000001; v=AquNG149dJNpZKjHTSihio56M8SVwL9COdSD9h0oh-pBvMC-pZBPkkmkE0Uu'

# url = 'http://upass.10jqka.com.cn/docookie2.php?userid=458478636&sessionid=15ca4e31cb5b1dc85f19a8d26183b6fca&signvalid=2018082211&sid=1110110000000110000000'
