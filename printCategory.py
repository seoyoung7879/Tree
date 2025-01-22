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

isbn = "9788936434120"  # 예시 ISBN
genres = get_genre_by_isbn(isbn)

if genres:
    print(f"ISBN {isbn}의 장르: {', '.join(genres)}")
else:
    print(f"ISBN {isbn}에 대한 장르 정보를 찾을 수 없습니다.")