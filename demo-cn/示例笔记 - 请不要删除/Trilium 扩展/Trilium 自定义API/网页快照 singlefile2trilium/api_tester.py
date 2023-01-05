import requests
print('尝试调用api')
TRILIUM_URL = "https://你的域名/custom/singlefile2trilium"
resp = requests.post(TRILIUM_URL,
                    json={
                        "secret": "你的密码",
                        "title": 'Trilium Note 翻译',
                        "url": 'https://github.com/Nriver/trilium-translation',
                        "content": '芜湖，起飞~'
                    }
                    )


print(resp.text)
