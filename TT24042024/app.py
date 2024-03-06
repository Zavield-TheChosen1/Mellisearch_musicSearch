import tkinter as tk
from tkinter import ttk, messagebox
import requests
import time

treeview = None  # Biến toàn cục để lưu trữ treeview
status_var = None  # Biến toàn cục để lưu trữ thanh trạng thái
genre_combobox = None
release_year_combobox = None
def login():
    global genre_combobox
    global release_year_combobox
    # Lấy thông tin đăng nhập từ các ô nhập
    api_key = api_key_entry.get()
    index_name = index_name_entry.get()

    # Kiểm tra xem có dữ liệu được nhập hay không
    if not api_key or not index_name:
        messagebox.showerror("Error", "Please enter API key and index name.")
        return

    # Thực hiện xác thực thông tin đăng nhập
    if authenticate(api_key, index_name):
        # Nếu xác thực thành công, hiển thị cửa sổ tìm kiếm tương ứng
        if index_name.lower() == "movies":
            show_movies_search_window(api_key, index_name)
        elif index_name.lower() == "music":
            show_music_search_window(api_key, index_name)
        else:
            messagebox.showerror("Error", "Invalid index name.")
    else:
        messagebox.showerror("Error", "Invalid API key or index name.")

def authenticate(api_key, index_name):
    # URL của MeiliSearch API
    url = f"http://127.0.0.1:7700/indexes/{index_name}/search"

    # Headers chứa API key
    headers = {
        "Content-Type": "application/json",
        "X-Meili-API-Key": api_key
    }

    # Dữ liệu JSON của truy vấn tìm kiếm
    data = {"q": ""}

    # Gửi yêu cầu POST để thực hiện tìm kiếm
    response = requests.post(url, headers=headers, json=data)

    # Kiểm tra phản hồi từ MeiliSearch
    if response.status_code == 200:  # 200: OK
        return True
    else:
        return False

def show_movies_search_window(api_key, index_name):
    global treeview, status_var,genre_combobox,release_year_combobox  # Sử dụng các biến toàn cục

    # Đóng cửa sổ đăng nhập
    login_window.destroy()

    # Tạo cửa sổ tìm kiếm cho movies
    movies_search_window = tk.Tk()
    movies_search_window.title("Search Movies")

    # Tạo frame chứa các widget
    frame = tk.Frame(movies_search_window)
    frame.pack(padx=10, pady=10)

    # Tạo nhãn và ô nhập để nhập từ khóa tìm kiếm
    keyword_label = tk.Label(frame, text="Từ khóa tìm kiếm:")
    keyword_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    keyword_entry = tk.Entry(frame, width=30)
    keyword_entry.grid(row=0, column=1, padx=5, pady=5)

    # Gán sự kiện Enter cho ô nhập từ khóa tìm kiếm
    keyword_entry.bind("<Return>", lambda event: search_movies(event, api_key, index_name, keyword_entry))

    # Tạo button để thực hiện tìm kiếm
    search_button = tk.Button(frame, text="Search Movies", command=lambda: search_movies(None, api_key, index_name, keyword_entry))
    search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    # Tạo dropdown cho genre
    genre_label = tk.Label(frame, text="Genre:")
    genre_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
    genre_combobox = ttk.Combobox(frame, width=27)
    genre_combobox.grid(row=3, column=1, padx=5, pady=5)
    # Cập nhật dữ liệu cho dropdown genre tại đây
    genres = ["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Romance", "Science Fiction", "Thriller", "Western"]
    genre_combobox['values'] = genres
    
    # Tạo dropdown cho release year
    release_year_label = tk.Label(frame, text="Release Year:")
    release_year_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
    release_year_combobox = ttk.Combobox(frame, width=27)
    release_year_combobox.grid(row=2, column=1, padx=5, pady=5)
    # Cập nhật dữ liệu cho dropdown release year tại đây
    release_years = [str(year) for year in range(2000, 2025)]  # Ví dụ: danh sách các năm từ 2000 đến 2024
    release_year_combobox['values'] = release_years

    # Tạo treeview để hiển thị kết quả
    treeview = ttk.Treeview(frame, columns=("ID", "Title", "Genre", "Release Date"), show="headings")
    treeview.heading("ID", text="ID")
    treeview.heading("Title", text="Title")
    treeview.heading("Genre", text="Genre")
    treeview.heading("Release Date", text="Release Date")
    treeview.column("ID", width=50, anchor="center")
    treeview.column("Title", width=200, anchor="w")
    treeview.column("Genre", width=100, anchor="center")
    treeview.column("Release Date", width=100, anchor="center")
    treeview.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    # Thiết lập trọng lực cho các cột
    frame.grid_rowconfigure(4, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    # Tạo thanh trạng thái để hiển thị số lượng kết quả và thời gian tìm kiếm
    status_var = tk.StringVar()
    status_bar = tk.Label(movies_search_window, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    movies_search_window.mainloop()


def search_movies(api_key, index_name, keyword_entry):
    global treeview, status_var, genre_combobox, release_year_combobox  # Sử dụng các biến toàn cục
    keyword = keyword_entry.get()

    # Lấy giá trị được chọn từ các dropdown
    selected_genre = genre_combobox.get()
    selected_release_year = release_year_combobox.get()

    # Kiểm tra các trường hợp và xây dựng truy vấn tìm kiếm tương ứng
    if not keyword and selected_genre and not selected_release_year:
        # Trường hợp 1: textbox trống và genre được chọn, release year không được chọn
        data = {
            "filter": f"genres=\"{selected_genre}\"",
            "limit": 99,
            "attributesToRetrieve": ["id", "title", "genres", "release_date"]
        }
    elif not keyword and not selected_genre and selected_release_year:
        # Trường hợp 2: textbox trống và genre không được chọn, release year được chọn
        data = {
            "filter": f"release_date=\"{selected_release_year}\"",
            "limit": 99,
            "attributesToRetrieve": ["id", "title", "genres", "release_date"]
        }
    elif not keyword and selected_genre and selected_release_year:
        # Trường hợp : textbox trống và genre được chọn, release year  được chọn
        data = {
            "filter": f"genres=\"{selected_genre}\" AND release_date=\"{selected_release_year}\"",
            "limit": 99,
            "attributesToRetrieve": ["id", "title", "genres", "release_date"]
        }
    elif keyword and selected_genre and selected_release_year:
        # Trường hợp 3: textbox có giá trị và cả 2 dropdown được chọn
        data = {
            "q": keyword,
            "filter": f"genres=\"{selected_genre}\" AND release_date=\"{selected_release_year}\"",
            "limit": 99,
            "attributesToRetrieve": ["id", "title", "genres", "release_date"]
        }
    elif keyword and selected_genre and not selected_release_year:
        # Trường hợp 4: textbox có giá trị, genre được chọn, release year không được chọn
        data = {
            "q": keyword,
            "filter": f"genres=\"{selected_genre}\"",
            "limit": 99,
            "attributesToRetrieve": ["id", "title", "genres", "release_date"]
        }
    elif keyword and not selected_genre and selected_release_year:
        # Trường hợp 5: textbox có giá trị, genre không được chọn, release year được chọn
        data = {
            "q": keyword,
            "filter": f"release_date=\"{selected_release_year}\"",
            "limit": 99,
            "attributesToRetrieve": ["id", "title", "genres", "release_date"]
        }
    else:
        # Trường hợp còn lại: chỉ có textbox hoặc không có điều kiện nào được áp dụng
        data = {
            "q": keyword,
            "limit": 99,
            "attributesToRetrieve": ["id", "title", "genres", "release_date"]
        }

    # Thời điểm bắt đầu tìm kiếm
    start_time = time.time()

    # URL của MeiliSearch API
    url = f"http://127.0.0.1:7700/indexes/{index_name}/search"

    # Headers chứa API key
    headers = {
        "Content-Type": "application/json",
        "X-Meili-API-Key": api_key
    }

    # Gửi yêu cầu POST để thực hiện tìm kiếm
    response = requests.post(url, headers=headers, json=data)

    # Thời gian tìm kiếm
    search_time = round(time.time() - start_time, 2)

    # Kiểm tra phản hồi từ MeiliSearch
    if response.status_code == 200:  # 200: OK
        # Lấy kết quả từ phản hồi JSON
        search_result = response.json()["hits"]

        # Xóa tất cả dữ liệu trong treeview
        for row in treeview.get_children():
            treeview.delete(row)

        # Hiển thị kết quả trong treeview
        for movie in sorted(search_result, key=lambda x: x["title"]):
            # Lấy thông tin về thể loại (genre) của bộ phim
            genres = ", ".join(movie.get("genres", []))
            treeview.insert("", "end", values=(movie["id"], movie["title"], genres, movie["release_date"]))

        # Cập nhật số lượng kết quả và thời gian tìm kiếm trên thanh trạng thái
        status_var.set(f"Found {len(search_result)} results in {search_time} seconds.")
    else:
        messagebox.showerror("Error", response.json())

def show_music_search_window(api_key, index_name):
    global treeview, status_var,genre_combobox,release_year_combobox  # Sử dụng các biến toàn cục

    # Đóng cửa sổ đăng nhập
    login_window.destroy()

    # Tạo cửa sổ tìm kiếm cho music
    music_search_window = tk.Tk()
    music_search_window.title("Search Music")

    # Tạo frame chứa các widget
    frame = tk.Frame(music_search_window)
    frame.pack(padx=10, pady=10)

    # Tạo nhãn và ô nhập để nhập từ khóa tìm kiếm
    keyword_label = tk.Label(frame, text="Từ khóa tìm kiếm:")
    keyword_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    keyword_entry = tk.Entry(frame, width=30)
    keyword_entry.grid(row=0, column=1, padx=5, pady=5)

    # Gán sự kiện Enter cho ô nhập từ khóa tìm kiếm
    keyword_entry.bind("<Return>", lambda event: search_music(event, api_key, index_name, keyword_entry))

    # Tạo button để thực hiện tìm kiếm
    search_button = tk.Button(frame, text="Search Music", command=lambda: search_music(None, api_key, index_name, keyword_entry))

    search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
    # Tạo dropdown cho genre
    genre_label = tk.Label(frame, text="Genre:")
    genre_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
    genre_combobox = ttk.Combobox(frame, width=27)
    genre_combobox.grid(row=3, column=1, padx=5, pady=5)
    # Cập nhật dữ liệu cho dropdown genre tại đây
    genres = ["Solo","Piano","Cello"]
    genre_combobox['values'] = genres
    
    # Tạo dropdown cho release year
    release_year_label = tk.Label(frame, text="Release Year:")
    release_year_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
    release_year_combobox = ttk.Combobox(frame, width=27)
    release_year_combobox.grid(row=2, column=1, padx=5, pady=5)
    # Cập nhật dữ liệu cho dropdown release year tại đây
    release_years = [str(year) for year in range(1650,2002)]  # Ví dụ: danh sách các năm 
    release_year_combobox['values'] = release_years
    

    # Tạo treeview để hiển thị kết quả
    treeview = ttk.Treeview(frame, columns=("ID", "Title", "Genre", "Release Date"), show="headings")
    treeview.heading("ID", text="ID")
    treeview.heading("Title", text="Song name")
    treeview.heading("Genre", text="Genre")
    treeview.heading("Release Date", text="Release Date")
    treeview.column("ID", width=50, anchor="center")
    treeview.column("Title", width=200, anchor="w")
    treeview.column("Genre", width=100, anchor="center")
    treeview.column("Release Date", width=100, anchor="center")
    treeview.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    # Thiết lập trọng lực cho các cột
    frame.grid_rowconfigure(4, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    # Tạo thanh trạng thái để hiển thị số lượng kết quả và thời gian tìm kiếm
    status_var = tk.StringVar()
    status_bar = tk.Label(music_search_window, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    music_search_window.mainloop()

def search_music(event, api_key, index_name, keyword_entry):
    global treeview, status_var, genre_combobox, release_year_combobox  # Sử dụng các biến toàn cục
    keyword = keyword_entry.get()

    # Lấy giá trị được chọn từ các dropdown
    selected_genre = genre_combobox.get()
    selected_release_year = release_year_combobox.get()

    # Kiểm tra các trường hợp và xây dựng truy vấn tìm kiếm tương ứng
    if not keyword and selected_genre and not selected_release_year:
        # Trường hợp 1: textbox trống và genre được chọn, release year không được chọn
        data = {
            "filter": f"genres=\"{selected_genre}\"",
            "limit": 99,
            "attributesToRetrieve": ["id", "title", "genres", "release_date"]
        }
    elif not keyword and not selected_genre and selected_release_year:
        # Trường hợp 2: textbox trống và genre không được chọn, release year được chọn
        data = {
            "filter": f"release_date=\"{selected_release_year}\"",
            "limit": 99,
            "attributesToRetrieve": ["id", "title", "genres", "release_date"]
        }
    elif not keyword and selected_genre and selected_release_year:
        # Trường hợp : textbox trống và genre được chọn, release year  được chọn
        data = {
            "filter": f"genres=\"{selected_genre}\"",
            "filter": f"release_date=\"{selected_release_year}\"",
            "limit": 99,
            "attributesToRetrieve": ["id", "title", "genres", "release_date"]
        }
    elif keyword and selected_genre and selected_release_year:
        # Trường hợp 3: textbox có giá trị và cả 2 dropdown được chọn
        data = {
            "q": keyword,
            "filter": f"genres=\"{selected_genre}\" AND release_date=\"{selected_release_year}\"",
            "limit": 99,
            "attributesToRetrieve": ["id", "title", "genres", "release_date"]
        }
    elif keyword and selected_genre and not selected_release_year:
        # Trường hợp 4: textbox có giá trị, genre được chọn, release year không được chọn
        data = {
            "q": keyword,
            "filter": f"genres=\"{selected_genre}\"",
            "limit": 99,
            "attributesToRetrieve": ["id", "title", "genres", "release_date"]
        }
    elif keyword and not selected_genre and selected_release_year:
        # Trường hợp 5: textbox có giá trị, genre không được chọn, release year được chọn
        data = {
            "q": keyword,
            "filter": f"release_date=\"{selected_release_year}\"",
            "limit": 99,
            "attributesToRetrieve": ["id", "title", "genres", "release_date"]
        }
    else:
        # Trường hợp còn lại: chỉ có textbox hoặc không có điều kiện nào được áp dụng
        data = {
            "q": keyword,
            "limit": 99,
            "attributesToRetrieve": ["id", "title", "genres", "release_date"]
        }

    # Thời điểm bắt đầu tìm kiếm
    start_time = time.time()

    # URL của MeiliSearch API
    url = f"http://127.0.0.1:7700/indexes/{index_name}/search"

    # Headers chứa API key
    headers = {
        "Content-Type": "application/json",
        "X-Meili-API-Key": api_key
    }

    # Gửi yêu cầu POST để thực hiện tìm kiếm
    response = requests.post(url, headers=headers, json=data)

    # Thời gian tìm kiếm
    search_time = round(time.time() - start_time, 2)

    # Kiểm tra phản hồi từ MeiliSearch
    if response.status_code == 200:  # 200: OK
        # Lấy kết quả từ phản hồi JSON
        search_result = response.json()["hits"]

        # Xóa tất cả dữ liệu trong treeview
        for row in treeview.get_children():
            treeview.delete(row)

        # Hiển thị kết quả trong treeview
        for song in sorted(search_result, key=lambda x: x["title"]):
            # Lấy thông tin về thể loại (genre) của bài hát
            genres = ", ".join(song.get("genres", []))
            treeview.insert("", "end", values=(song["id"], song["title"], genres, song["release_date"]))

        # Cập nhật số lượng kết quả và thời gian tìm kiếm trên thanh trạng thái
        status_var.set(f"Found {len(search_result)} results in {search_time} seconds.")
    else:
        messagebox.showerror("Error", response.json())

# Tạo cửa sổ Tkinter cho đăng nhập
login_window = tk.Tk()
login_window.title("Login")

# Tạo frame chứa các widget cho đăng nhập
login_frame = tk.Frame(login_window)
login_frame.pack(padx=10, pady=10)

# Nhãn và ô nhập cho API key
api_key_label = tk.Label(login_frame, text="API Key:")
api_key_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
api_key_entry = tk.Entry(login_frame, width=30)
api_key_entry.grid(row=0, column=1, padx=5, pady=5)

# Nhãn và ô nhập cho tên index
index_name_label = tk.Label(login_frame, text="Index Name:")
index_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
index_name_entry = tk.Entry(login_frame, width=30)
index_name_entry.grid(row=1, column=1, padx=5, pady=5)

# Button đăng nhập
login_button = tk.Button(login_frame, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

login_window.mainloop()
