import pandas as pd
import requests
import xml.etree.ElementTree as ET
from config import LBAPI_AUTH_KEY
from datetime import datetime
import os
import time

# 데이터 읽기
folder_path = r'data'
popular_results_df = pd.read_csv(os.path.join(folder_path, 'popular_result.csv'), encoding='cp949')
combined_books_df = pd.read_csv(os.path.join(folder_path, 'combined_books_with_loans.csv'), encoding='cp949')

# 현재 연도
current_year = datetime.now().year

# 마지막 5개 ISBN 선택
last_five_isbns = popular_results_df['ISBN'].tail(5).tolist()

# '서명' 열에서 책 제목을 읽고 중복 제거
popular_titles_set = set(popular_results_df['서명'].dropna().unique())

# 결과 저장 리스트
csv_data = []

for isbn in last_five_isbns:
    # API 요청 파라미터
    params = {
        'authKey': LBAPI_AUTH_KEY,
        'isbn13': isbn,
        'format': 'xml'
    }
    
    # Retry mechanism
    response = None
    for attempt in range(3):
        try:
            response = requests.get(
                'http://data4library.kr/api/usageAnalysisList', 
                params=params, 
                timeout=10  # 타임아웃 설정
            )
            response.raise_for_status()  # HTTP 상태 코드 확인
            if response.content.strip():  # 응답 내용이 비어있지 않은지 확인
                break
        except requests.exceptions.Timeout:
            print(f"Timeout Error for ISBN {isbn}. Retrying... ({attempt + 1}/3)")
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}. Retrying... ({attempt + 1}/3)")
        time.sleep(5)  # 재시도 전 대기

    # 응답 검증
    if not response or not response.content.strip():
        print(f"ISBN {isbn}: 유효한 응답을 받지 못했습니다.")
        continue

    try:
        # XML 응답 처리
        root = ET.fromstring(response.content)

        # 입력한 ISBN에 대한 책 정보 출력
        book_info = root.find('.//book')
        if book_info is not None:
            bookname = book_info.find('bookname').text if book_info.find('bookname') is not None else "정보 없음"
            print(f"\n입력한 ISBN: {isbn}, 도서명: {bookname}")

            # 함께 빌려진 책 정보 출력
            co_loan_books = root.find('coLoanBooks')
            if co_loan_books is not None:
                recommendations = []
                for book in co_loan_books.findall('book'):
                    publication_year_text = book.find('publication_year').text
                    co_publication_year = int(publication_year_text) if publication_year_text is not None else 0
                    
                    # 신간 도서 필터링 (1-5년 사이)
                    if current_year - co_publication_year in [1, 2, 3, 4, 5]:
                        co_bookname = book.find('bookname').text if book.find('bookname') is not None else "정보 없음"
                        co_authors = book.find('authors').text if book.find('authors') is not None else "정보 없음"
                        co_publisher = book.find('publisher').text if book.find('publisher') is not None else "정보 없음"
                        co_isbn = book.find('isbn13').text if book.find('isbn13') is not None else "정보 없음"
                        loan_count = int(book.find('loanCnt').text) if book.find('loanCnt').text is not None else 0
                        
                        # 제목에 "흔한남매" 또는 "장편소설"이 포함되지 않은 경우에만 추가
                        if "흔한남매" not in co_bookname and "장편소설" not in co_bookname:
                            recommendations.append({
                                '도서명': co_bookname,
                                '저자': co_authors,
                                '출판사': co_publisher,
                                '출판 연도': co_publication_year,
                                'ISBN': co_isbn,
                                '대출 횟수': loan_count
                            })
                            # 추천 도서 데이터를 csv_data에 추가
                            csv_data.append({
                                'ISBN': co_isbn,
                                '도서명': co_bookname,
                                '저자': co_authors,
                                '출판 연도': co_publication_year
                            })

                # 대출량 기준으로 정렬
                sorted_recommendations = sorted(recommendations, key=lambda x: x['대출 횟수'], reverse=True)

                # 추천 도서 출력
                print("추천된 신간 도서:")
                for rec in sorted_recommendations:
                    # 추천 도서가 combined_books_with_loans.csv의 '서명'에 있는지 확인
                    is_held = rec['도서명'] in combined_books_df['ISBN'].dropna().unique()
                    if is_held:
                        print(f"도서명: {rec['도서명']}, 저자: {rec['저자']}, 출판사: {rec['출판사']}, 출판 연도: {rec['출판 연도']}, ISBN: {rec['ISBN']}, 대출 횟수: {rec['대출 횟수']}, 숭실대 보유: True")
                    else:
                        print(f"도서명: {rec['도서명']}, 저자: {rec['저자']}, 출판사: {rec['출판사']}, 출판 연도: {rec['출판 연도']}, ISBN: {rec['ISBN']}, 대출 횟수: {rec['대출 횟수']}")
            else:
                print(f"{isbn}에 대한 함께 빌려진 책 정보 없음")
        else:
            print(f"ISBN {isbn}에 대한 책 정보 없음.")
    except ET.ParseError as e:
        print(f"XML Parse Error for ISBN {isbn}: {e}")

# CSV 파일 저장
output_csv_path = os.path.join(folder_path, 'recommended_books.csv')
csv_df = pd.DataFrame(csv_data)
csv_df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
print(f"\n추천 도서 데이터가 {output_csv_path}에 저장되었습니다.")
