import requests

# Tên của index bạn muốn xóa
index_name = "music"

# URL của MeiliSearch API
url = f"http://127.0.0.1:7700/indexes/{index_name}"

# Headers chứa API Key
headers = {
    "X-Meili-API-Key": "Z9gqb14VZf_zyYU616YKfhqYEuLOvk9iFJFbd_wk5Xw"  # Thay API_KEY bằng key của bạn
}

# Gửi yêu cầu DELETE để xóa index
response = requests.delete(url, headers=headers)

# Kiểm tra phản hồi từ MeiliSearch
if response.status_code == 204:  # 204: No Content
    print(f"Index '{index_name}' đã được xóa thành công.")
else:
    print(f"Lỗi: {response.json()}")
