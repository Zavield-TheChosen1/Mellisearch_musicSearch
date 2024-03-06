import requests

url = 'http://127.0.0.1:7700/indexes/movies/settings'  # Thay đổi 'movies' thành tên chỉ mục của bạn
api_key = 'VvHhkQfCrxsrlFGz-tmpu8coM0c65yhUKdJZgNmrN9w'  # Thay đổi thành API key của bạn

data = {
    "filterableAttributes": ["release_date","genres"],
 
}

headers = {
    "Content-Type": "application/json",
    "X-Meili-API-Key": api_key
}

response = requests.patch(url, json=data, headers=headers)

if response.status_code == 200:
    print("Cấu hình chỉ mục đã được cập nhật thành công.")
else:
    print("Đã xảy ra lỗi khi cập nhật cấu hình chỉ mục.")
    print(response.json())  # In ra thông tin lỗi (nếu có)
