import requests
import json

# 读取文件内容
file_path = 'file/example.pdf'
with open(file_path, 'rb') as fp:
    image = fp.read()

# 初始化TextinOcr
app_id = '#####c07db002663f3b085#####'
app_secret = '######1b1b11a9f9bcd7cc7b######'
host = 'https://api.textin.com'

# 设置请求参数
options = {
    'page_start': 0,
    'page_count': 1000,
    'table_flavor': 'md',
    'parse_mode': 'scan',
    'page_details': 0,
    'markdown_details': 1,
    'apply_document_tree': 1,
    'dpi': 144
}

# 发送请求
url = f"{host}/ai/service/v1/pdf_to_markdown"
headers = {
    'x-ti-app-id': app_id,
    'x-ti-secret-code': app_secret
}
resp = requests.post(url, data=image, headers=headers, params=options)

# 打印请求时间
print("request time:", resp.elapsed.total_seconds())

# 保存结果
result = resp.json()
with open('result.json', 'w', encoding='utf-8') as fw:
    json.dump(result, fw, indent=4, ensure_ascii=False)
