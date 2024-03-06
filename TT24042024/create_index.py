import requests


# URL của MeiliSearch API
url = "http://127.0.0.1:7700/indexes"

# Tên của index bạn muốn tạo
index_name = "ameo1"

# Headers chứa MASTER_KEY
headers = {
    "Content-Type": "application/json",
    "X-Meili-API-Key": "Usx-rsHaXi6exm1WGm89pLspa7yMhkdUhxGbGuu7fNI"
}
# Dữ liệu JSON để tạo index
data = {
    "uid": index_name
}

# Gửi yêu cầu POST để tạo index
response = requests.post(url, headers=headers, json=data)

# Kiểm tra phản hồi từ MeiliSearch
if response.status_code == 202:  # 202: Accepted
    print(f"Index '{index_name}' đã được tạo thành công!")
else:
    print(f"Lỗi: {response.json()}")
