import pandas as pd
import os

# 데이터 읽기
folder_path = r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data'
books_df = pd.read_csv(os.path.join(folder_path, 'booksCleaned.txt'), 
                      encoding='cp949', 
                      header=0)

# 출판년도 기준으로 오래된 순으로 정렬
books_df_sorted = books_df.sort_values(by='출판년도')

# 상위 5%의 책 수 계산
oldest_5_percent_count = int(len(books_df_sorted) * 0.05)

# 상위 5%의 오래된 책 선택
oldest_5_percent_books = books_df_sorted.head(oldest_5_percent_count)

# 가장 최신 도서의 정보 확인
latest_book = oldest_5_percent_books.loc[oldest_5_percent_books['출판년도'].idxmax()]

# 결과 출력
print("오래된 5%의 책 중 가장 최신 도서의 정보:")
print(f"제목: {latest_book['서명']}")  # 제목 열 이름이 '제목'이라고 가정
print(f"저자: {latest_book['저자']}")  # 저자 열 이름이 '저자'라고 가정
print(f"출판년도: {latest_book['출판년도']}") 