import requests
print('尝试调用api')

TRILIUM_URL = "https://你的域名/custom/create-note"
resp = requests.post(TRILIUM_URL,
    json={
        "secret": "你的密码",
        "title": "hello",
        "content": "world"
    }
)
print(resp.text)
