import pandas as pd
import requests

def get_genre_by_isbn(isbn):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    response = requests.get(url).json()
    
    if 'items' in response:
        for item in response['items']:
            categories = item.get('volumeInfo', {}).get('categories', [])
            if categories:
                return categories  # 장르 리스트 반환
    return None  # 장르가 없을 경우 None 반환

# recommendations.csv 파일 읽기
recommendations_df = pd.read_csv('C:/Users/USER/Desktop/dataton/Tree/data/recommendations.csv', encoding='utf-8-sig')

# ISBN 열에서 장르 출력
for isbn in recommendations_df['ISBN']:
    genres = get_genre_by_isbn(isbn)
    if genres:
        print(f"ISBN: {isbn}, Genres: {', '.join(genres)}")
    else:
        print(f"ISBN: {isbn}, Genres: 정보 없음") 