import requests
import xml.etree.ElementTree as ET
from config import LBAPI_AUTH_KEY

# API 인증키 및 URL 설정
auth_key = LBAPI_AUTH_KEY

isbn = '9788972978589'  # 입력한 ISBN
base_url = 'http://data4library.kr/api/usageAnalysisList'

# 요청할 파라미터 설정
params = {
    'authKey': auth_key,
    'isbn13': isbn,
    'format': 'xml'
}

def fetch_book_analysis():
    try:
        # API 요청
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # 요청이 성공했는지 확인

        # XML 응답 처리
        root = ET.fromstring(response.content)

        # 도서 정보 출력
        print("=== 도서 정보 ===")
        for book in root.findall('.//book'):
            book_isbn = book.find('isbn13').text if book.find('isbn13') is not None else "정보 없음"
            if book_isbn == isbn:  # 입력한 ISBN과 일치하는 경우만 출력
                bookname = book.find('bookname').text if book.find('bookname') is not None else "정보 없음"
                authors = book.find('authors').text if book.find('authors') is not None else "정보 없음"
                publisher = book.find('publisher').text if book.find('publisher') is not None else "정보 없음"
                publication_year = book.find('publication_year').text if book.find('publication_year') is not None else "정보 없음"
                print(f"도서명: {bookname}, 저자: {authors}, 출판사: {publisher}, 출판 연도: {publication_year}")

        # 대출 이력 출력
        print("\n=== 대출 이력 ===")
        loan_history = root.find('loanHistory')
        if loan_history is not None:
            for loan in loan_history.findall('loan'):
                month = loan.find('month').text if loan.find('month') is not None else "정보 없음"
                loan_count = loan.find('loanCnt').text if loan.find('loanCnt') is not None else "정보 없음"
                print(f"{month}: {loan_count}회 대출")
        else:
            print("대출 이력 정보 없음")

        # 키워드 정보 출력
        print("\n=== 키워드 정보 ===")
        keywords = root.find('keywords')
        if keywords is not None:
            for keyword in keywords.findall('keyword'):
                word = keyword.find('word').text if keyword.find('word') is not None else "정보 없음"
                weight = keyword.find('weight').text if keyword.find('weight') is not None else "정보 없음"
                print(f"키워드: {word}, 가중치: {weight}")
        else:
            print("키워드 정보 없음")

        # 추천 도서 출력
        print("\n=== 추천 도서 ===")
        rec_books = root.find('maniaRecBooks')
        if rec_books is not None:
            for book in rec_books.findall('book'):
                rec_bookname = book.find('bookname').text if book.find('bookname') is not None else "정보 없음"
                rec_authors = book.find('authors').text if book.find('authors') is not None else "정보 없음"
                rec_publisher = book.find('publisher').text if book.find('publisher') is not None else "정보 없음"
                rec_publication_year = book.find('publication_year').text if book.find('publication_year') is not None else "정보 없음"
                print(f"도서명: {rec_bookname}, 저자: {rec_authors}, 출판사: {rec_publisher}, 출판 연도: {rec_publication_year}")
        else:
            print("추천 도서 정보 없음")

    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    fetch_book_analysis()
