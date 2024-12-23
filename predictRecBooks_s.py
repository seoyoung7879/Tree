import pandas as pd
import requests
import xml.etree.ElementTree as ET
import os

# 카카오 API 설정
REST_API_KEY = '2285d27fe6c44031cfa9347c62883c1f'  # 여기에 발급받은 REST API 키를 입력하세요.
base_url = 'https://dapi.kakao.com/v3/search/book'

# API 인증키 및 URL 설정 (LBAPI)
auth_key = '476eefbbd0bcbaa9490e343ed7604a4092f0891abf026d30984908ca469e79c1'
base_url_lbapi = 'http://data4library.kr/api/usageAnalysisList'

# 데이터 폴더 경로 설정
folder_path = r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data'

# 1. reser.txt 파일 읽기 (대출 기록)
reser_df = pd.read_csv(os.path.join(folder_path, r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data\reser.txt'), encoding='cp949', header=None)

# 2. 열 이름 수동 지정
reser_df.columns = ['도서ID', '대출일시']  # 원하는 열 이름으로 수정

# 3. 도서ID별 대출 횟수 계산
book_counts = reser_df['도서ID'].value_counts().reset_index()
book_counts.columns = ['도서ID', '대출횟수']  # 열 이름 변경

# 4. 대출횟수 기준으로 정렬하여 상위 1개 도서 선택
top_book = book_counts.sort_values(by='대출횟수', ascending=False).head(1)

# 5. books.txt 파일 읽기 (도서 정보) - os.path.join 사용
books_df = pd.read_csv(os.path.join(folder_path, r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data\books.txt'), encoding='cp949', header=None)

# 6. 열 이름 수동 지정
books_df.columns = ["도서ID", "등록일자", "수서방법", "분류코드", "ISBN", "서명", "저자", "출판사", "출판년도", "소장위치"]

# 7. 도서 ID로 ISBN 조인
merged_df = top_book.merge(books_df[['도서ID', 'ISBN', '서명']], on='도서ID', how='left')

# 8. 결과 출력
isbn = merged_df['ISBN'].values[0]  # ISBN 추출
book_title = merged_df['서명'].values[0]  # 도서 이름 추출
print("대출량이 가장 많은 도서 1개의 도서 이름:", book_title)
print("대출량이 가장 많은 도서 1개의 ISBN:")
print(merged_df[['도서ID', '대출횟수', 'ISBN']])

# 9. ISBN을 사용하여 LBAPI에서 키워드와 가중치 정보 가져오기
def fetch_keywords(isbn):
    params = {
        'authKey': auth_key,
        'isbn13': isbn,
        'format': 'xml'
    }
    try:
        response = requests.get(base_url_lbapi, params=params)
        response.raise_for_status()  # 요청이 성공했는지 확인

        # XML 응답 처리
        root = ET.fromstring(response.content)

        # 키워드 정보 출력
        keywords = root.find('keywords')
        if keywords is not None:
            keyword_weights = {}
            for keyword in keywords.findall('keyword'):
                word = keyword.find('word').text if keyword.find('word') is not None else "정보 없음"
                weight = keyword.find('weight').text if keyword.find('weight') is not None else "정보 없음"
                keyword_weights[word] = int(weight)  # 가중치를 정수로 변환

            # 가중치가 가장 높은 키워드 찾기
            max_keyword = max(keyword_weights, key=keyword_weights.get)
            return max_keyword
        else:
            print("키워드 정보 없음")
            return None

    except Exception as e:
        print(f"오류 발생: {e}")
        return None

# 10. 키워드 가져오기
keyword = fetch_keywords(isbn)
if keyword:
    print(f"가장 높은 가중치를 가진 키워드: {keyword}")

    # 11. 카카오 API를 사용하여 추천 도서 가져오기
    def fetch_books_by_keyword(keyword):
        headers = {
            'Authorization': f'KakaoAK {REST_API_KEY}'
        }
        params = {
            'query': keyword,
            'sort': 'accuracy',  # 정렬 방식 (accuracy 또는 latest)
            'size': 10  # 한 페이지에 보여줄 문서 수
        }

        try:
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

    # 12. 추천 도서 가져오기
    fetch_books_by_keyword(keyword)