
import os

res = os.popen('connmanctl services').read()
res = res.replace('*AO Wired', '')  # remove word
res = " ".join(res.split())  # white space
print(res)
