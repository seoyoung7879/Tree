import pandas as pd
import os

# 데이터 읽기
folder_path = r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data'
filtered_books_df = pd.read_csv(os.path.join(folder_path, 'filtered_books.txt'), 
                                 encoding='cp949', 
                                 sep='\t',  # 탭으로 구분된 파일
                                 header=0)

# 도서 ID별로 그룹화하여 고유한 서명 수 확인
duplicate_books = filtered_books_df.groupby('도서ID')['서명'].nunique().reset_index()

# 고유 서명 수가 1보다 큰 도서 ID 필터링
duplicate_books = duplicate_books[duplicate_books['서명'] > 1]

# 결과 출력
if not duplicate_books.empty:
    print("도서 ID가 같은 다른 책이 있는 도서 ID 목록:")
    print(duplicate_books)
else:
    print("도서 ID가 같은 다른 책이 없습니다.") 