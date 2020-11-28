import requests

# url = 'http://mlg.ucd.ie/files/datasets/bbc.zip'
# content = requests.get(url)
#
# # unzip the content
# from io import BytesIO
# from zipfile import ZipFile
#
# f = ZipFile(BytesIO(content.content))
#
# print(f.namelist())



# Pass in the following
# service
# version to install as selected by the user
# user
# dir



# sudo bash script.bash start -u=pi -dir=/home/pi/bacnet-flask -lib_dir=/home/pi/common-py-libs

import requests

r = requests.get('https://api.github.com/repos/NubeDev/bacnet-flask/releases')
status = r.status_code
r = r.json()

user_selected = "https://api.github.com/repos/NubeDev/bacnet-flask/zipball/v1.1.1"

if status == 200:
    for item in r:
        print(item)

from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

dir = "/home/aidan/code/test"

from pathlib import Path
import shutil

dirpath = Path(dir)
if dirpath.exists() and dirpath.is_dir():
    print(222)
    shutil.rmtree(dirpath)

zipurl = 'http://stash.compjour.org/data/1800ssa.zip'
with urlopen(zipurl) as zipresp:
    with ZipFile(BytesIO(zipresp.read())) as zfile:
        zfile.extractall(dir)
