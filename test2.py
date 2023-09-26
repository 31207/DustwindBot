import random
import time

import requests

try:
    num = 8400
    random.seed(time.time())
    while num >= 0:
        response = requests.get(f"http://xjbdvipqq.onxsg.cn/api/update/delect/{num}")
        print(response.text, num)
        num -= 1
except requests.exceptions.ConnectTimeout:
    print("time out")
