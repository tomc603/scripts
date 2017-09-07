#!/usr/bin/env python3

import random

choices = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
size=14
result=''

for i in range(0, size-1):
    result+=random.choice(choices)

print(result)

