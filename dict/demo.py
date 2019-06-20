# 隐藏输入 转换加密

import getpass
import hashlib

# while True:
#     print("a")
#     cmd = input()
#     if cmd == "in":
#         while True:
#             print("b")
#             cmd = input()
#             if cmd == "out":
#                 break
#

# 输入隐藏
pwd = getpass.getpass()
print(pwd)


# hash 对象
hash = hashlib.md5('#$@a_'.encode())
hash.update(pwd.encode())   # 算法加密
pwd = hash.hexdigest()      # 提取加密后的密码
