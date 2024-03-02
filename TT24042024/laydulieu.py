import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

# Khai báo các thông tin về tài khoản Spotify của bạn
client_id = 'b2bdc82da83d4a049186ff530d55c34f'
client_secret = 'c45b01848a9741faa4df2653685903ee'

# Khởi tạo Spotify Client Credentials Manager
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Lấy danh sách các bài hát phổ biến từ Spotify API và ghi vào tệp JSON
def get_top_tracks(limit=50, total=500):
    try:
        offset = 0
        data = []

        while len(data) < total:
            results = sp.search(q='year:2023', type='track', limit=limit, market='US', offset=offset)
            tracks = results['tracks']['items']
            
            for track in tracks:
                track_name = track['name']
                artist_names = ', '.join([artist['name'] for artist in track['artists']])
                track_url = track['external_urls']['spotify']
                track_id = track['id']

                # Lấy lời bài hát
                lyrics = sp.track(track_id)['album']['artists'][0]['external_urls']['spotify']
                
                # Thêm thông tin về bài hát vào danh sách data
                data.append({
                    'Tên bài hát': track_name,
                    'Nghệ sĩ': artist_names,
                    'Lời bài hát': lyrics,
                    'URL của bài hát': track_url
                })

            offset += limit

            if len(tracks) < limit:
                break

        # Ghi danh sách data vào tệp JSON
        with open('top_tracks.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print("Error:", e)

# Gọi hàm để lấy danh sách 500 bài hát phổ biến và ghi vào tệp JSON
get_top_tracks()
