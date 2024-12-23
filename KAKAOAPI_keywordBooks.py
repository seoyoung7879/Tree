import requests
from config import KAKAO_API_KEY  # config.py에서 API 키를 가져옵니다.

# 카카오 API 설정
base_url = 'https://dapi.kakao.com/v3/search/book'

# 검색할 키워드 설정
keyword = '용서'

# 요청 헤더 설정
headers = {
    'Authorization': f'KakaoAK {KAKAO_API_KEY}'  # API 키를 사용합니다.
}

# 요청 파라미터 설정
params = {
    'query': keyword,
    'sort': 'accuracy',  # 정렬 방식 (accuracy 또는 latest)
    'size': 10  # 한 페이지에 보여줄 문서 수
}

try:
    # API 요청
    response = requests.get(base_url, headers=headers, params=params)
    response.raise_for_status()  # 요청이 성공했는지 확인

    # JSON 응답 처리
    data = response.json()

    # 도서 정보 출력
    print(f"키워드 '{keyword}'에 대한 추천 도서:")
    for book in data['documents']:
        title = book['title']
        authors = ', '.join(book['authors'])
        publisher = book['publisher']
        datetime = book['datetime']
        url = book['url']
        thumbnail = book['thumbnail']

        print(f"도서명: {title}")
        print(f"저자: {authors}")
        print(f"출판사: {publisher}")
        print(f"출판일: {datetime}")
        print(f"URL: {url}")
        print(f"썸네일: {thumbnail}")
        print("-" * 40)

except Exception as e:
    print(f"오류 발생: {e}") 