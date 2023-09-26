import random
import time

import requests

try:
    num = 9000
    random.seed(time.time())
    while num >= 0:
        # j = {"u": f"{random.randint(100000000,1000000000)}", "p": f"{random.randint(100000000,1000000000)}", "system_str": "PC", "success": False}
        j = {"u":"rjtyJgXPa5hGcs2C H6xNqPDTPc93q2jCnwZt6joCfVtQ9uMEOJSspbtdvVi50lNYuG3m6IhSEsrpxN1E5r0qTkX4SJzExn3RLbHp4nH4ZU2YcjTxxnI1zrg3RD3mFoz98omB7qDTQebFmunkDN7emh8yZaPubuBn89 XmbX7ivTj6H3JvGm2A 1RQu3qYAK9lXdXlmWIs3wqbE24C6sCKUL3p3McCF33zy2/ebFCsCFEOnFvLc6mL/trd7SskngncoNTyJewOKePywTej FZ/IkTBxdZdxmAwv6C0cfCexFW2Zg0FUma8R1TiiLQh1 rtlUZ82HFCuY0g9FRgq9Yg: =","p":"HFQExIta2GsjPCAY1dY2gJ9zfI5IjNXPEDOJSbPAek0jDz2NxWgErjcMYJZ9w4JcQL8CXtjCFMZeqR8JSOkUtiLom5MxmQDrVt uuFzm8qqIY7PijXXpK/2vrYSD/ApuqSe1dl2xn2yB8sqwjHZmFVJh/ChZrLtRe7f ktYXrgDVXINIJ19Db BSTaaJWQ2nm UIRx9DGxnHicCH82i9cGhcQ J G7HX3JQy2Mc7Pd4V1P1gIstC2i1S8wMM61uZhCmCeARoe8YhDdTkjcNDjCzn/9pbce7FimqrSymfPUu9lz95Ywpnte8dxntToTePlgNE9AuTV25k l3LyMz8/A==","f":"ffc3dd39e3be023bbfc9ad158e49f9ef1695653830.059407","i":1695654027598,"system_str":"PC","ip":"美国得克萨斯达拉斯 23.236.100.157","timestamp":1695654006088}
        response = requests.post(f"http://xjbdvipqq.onxsg.cn:90/record/", json=j)
        print(response.text, num)
        num -= 1
except requests.exceptions.ConnectTimeout:
    print("time out")
