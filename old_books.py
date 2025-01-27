import pandas as pd
import os
from datetime import datetime

# 데이터 읽기
folder_path = r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data'
filtered_books_df = pd.read_csv(os.path.join(folder_path, 'filtered_books.txt'), 
                                 encoding='cp949', 
                                 sep='\t',  # 탭으로 구분된 파일
                                 header=0)

# 현재 연도 가져오기
current_year = datetime.now().year

# 10년 전 연도 계산
ten_years_ago = current_year - 10

# 10년 이상 된 책 필터링
old_books = filtered_books_df[filtered_books_df['출판년도'] <= ten_years_ago]  # '출판년도' 열 이름이 '출판년도'라고 가정

# 비율 계산
total_books = len(filtered_books_df)
old_books_count = len(old_books)

if total_books > 0:
    old_books_ratio = (old_books_count / total_books) * 100
else:
    old_books_ratio = 0

# 결과 출력
print(f"10년 이상 된 책의 비율: {old_books_ratio:.2f}%") 