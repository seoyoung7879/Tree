import pandas as pd
import requests
import xml.etree.ElementTree as ET
from config import LBAPI_AUTH_KEY
from datetime import datetime
import os
# 데이터 읽기
folder_path = r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data'
discard_results_df = pd.read_csv(os.path.join(folder_path, 'discard_result.csv'), encoding='cp949')

# 현재 연도
current_year = datetime.now().year

# 마지막 5개 ISBN 선택
last_five_isbns = discard_results_df['ISBN'].tail(5).tolist()

# API 호출 및 추천 도서 출력
for isbn in last_five_isbns:
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
                co_publication_year = int(book.find('publication_year').text) if book.find('publication_year') is not None else 0
                
                # 신간 도서 필터링 (1-2년 사이)
                if current_year - co_publication_year in [1, 2,3,4,5]:
                    co_bookname = book.find('bookname').text if book.find('bookname') is not None else "정보 없음"
                    co_authors = book.find('authors').text if book.find('authors') is not None else "정보 없음"
                    co_publisher = book.find('publisher').text if book.find('publisher') is not None else "정보 없음"
                    co_isbn = book.find('isbn13').text if book.find('isbn13') is not None else "정보 없음"
                    loan_count = int(book.find('loanCnt').text) if book.find('loanCnt') is not None else 0
                    
                    recommendations.append({
                        '도서명': co_bookname,
                        '저자': co_authors,
                        '출판사': co_publisher,
                        '출판 연도': co_publication_year,
                        'ISBN': co_isbn,
                        '대출 횟수': loan_count
                    })

            # 대출량 기준으로 정렬
            sorted_recommendations = sorted(recommendations, key=lambda x: x['대출 횟수'], reverse=True)

            # 추천 도서 출력
            print("추천된 신간 도서:")
            for rec in sorted_recommendations:
                print(f"도서명: {rec['도서명']}, 저자: {rec['저자']}, 출판사: {rec['출판사']}, 출판 연도: {rec['출판 연도']}, ISBN: {rec['ISBN']}, 대출 횟수: {rec['대출 횟수']}")
        else:
            print(f"{isbn}에 대한 함께 빌려진 책 정보 없음")
    else:
        print(f"{isbn}에 대한 책 정보 없음")
