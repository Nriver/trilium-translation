import os
import base64
import sys
import requests
import json
from datetime import datetime

if not sys.argv[1] or not os.path.exists(sys.argv[1]):
    print('No file provided!')
    exit()

title = f"截图 {datetime.now()}"
secret = '你的密码'
# today or related
target = 'today'


def image_encode_to_base64(img_path):
    '''image data to base64'''
    with open(img_path, 'rb') as f:
        data = f.read()
        encoded_data = base64.b64encode(data)
        return encoded_data.decode()


image_path = sys.argv[1].replace('//', '/')


with open(image_path, 'r') as f:

    content = image_encode_to_base64(image_path)

    print('try to upload')
    TRILIUM_URL = "https://你的域名/custom/create-image-note"
    resp = requests.post(TRILIUM_URL,
                         json={
                             "secret": secret,
                             "title": title,
                             "content": content,
                             "type": "image",
                             "target": target,
                         },
                         )
    print(resp.text)
