import requests
import json

# Đọc dữ liệu từ tệp JSON
with open('data3.json', 'r') as file:
    data = json.load(file)
# URL của MeiliSearch API
url = "http://127.0.0.1:7700/indexes/ameo1/documents"

# Headers chứa MASTER_KEY
headers = {
    "Content-Type": "application/json",
    "X-Meili-API-Key": "Usx-rsHaXi6exm1WGm89pLspa7yMhkdUhxGbGuu7fNI"
}

# Gửi yêu cầu POST để thêm các tài liệu vào index
response = requests.post(url, headers=headers, json=data)

# Kiểm tra phản hồi từ MeiliSearch
if response.status_code == 202:  # 202: Accepted
    print("Dữ liệu đã được thêm vào index thành công!")
else:
    print(f"Lỗi: {response.json()}")