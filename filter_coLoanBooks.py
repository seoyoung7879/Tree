import pandas as pd
import requests
import xml.etree.ElementTree as ET
from config import LBAPI_AUTH_KEY
from datetime import datetime
import os

# 데이터 읽기
folder_path = r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data'
filtered_books_df = pd.read_csv(os.path.join(folder_path, 'combined_books_with_loans.csv'), 
                                 encoding='cp949', 
                                 header=0)

# 점수 계산을 위한 데이터프레임 생성
score_df = filtered_books_df.copy()

# 현재 연도
current_year = datetime.now().year

# 최종 점수 계산 (여기서는 간단히 예시로 점수 계산)
score_df['discard_score'] = (score_df['대출량'].max() - score_df['대출량'])  # 대출량을 기준으로 점수 계산

# 하위 10%의 ISBN 선택
threshold = score_df['discard_score'].quantile(0.1)
low_score_isbns = score_df[score_df['discard_score'] >= threshold]['ISBN'].tolist()

# API 호출 및 coLoanBooks 필터링
co_loan_books_list = []

for isbn in low_score_isbns:
    # API 요청
    params = {
        'authKey': LBAPI_AUTH_KEY,
        'isbn13': isbn,
        'format': 'xml'
    }
    response = requests.get('http://data4library.kr/api/usageAnalysisList', params=params)
    response.raise_for_status()  # 요청이 성공했는지 확인

    # XML 응답 처리
    root = ET.fromstring(response.content)

    # 함께 빌려진 책 정보 출력
    co_loan_books = root.find('coLoanBooks')
    if co_loan_books is not None:
        for book in co_loan_books.findall('book'):
            co_bookname = book.find('bookname').text if book.find('bookname') is not None else "정보 없음"
            co_authors = book.find('authors').text if book.find('authors') is not None else "정보 없음"
            co_publisher = book.find('publisher').text if book.find('publisher') is not None else "정보 없음"
            co_publication_year = int(book.find('publication_year').text) if book.find('publication_year') is not None else 0
            co_isbn = book.find('isbn13').text if book.find('isbn13') is not None else "정보 없음"
            loan_count = int(book.find('loanCnt').text) if book.find('loanCnt') is not None else 0
            
            # 신간 도서 필터링 (1-2년 사이)
            if current_year - co_publication_year in [1, 2]:
                co_loan_books_list.append({
                    '도서명': co_bookname,
                    '저자': co_authors,
                    '출판사': co_publisher,
                    '출판 연도': co_publication_year,
                    'ISBN': co_isbn,
                    '대출 횟수': loan_count
                })

# 대출량 기준으로 정렬
sorted_co_loan_books = sorted(co_loan_books_list, key=lambda x: x['대출 횟수'], reverse=True)

# 결과 출력
print("=== 신간 도서 (1-2년 사이) - 함께 빌려진 책 ===")
for book in sorted_co_loan_books:
    print(f"도서명: {book['도서명']}, 저자: {book['저자']}, 출판사: {book['출판사']}, 출판 연도: {book['출판 연도']}, ISBN: {book['ISBN']}, 대출 횟수: {book['대출 횟수']}") 
