import pandas as pd
import os
from datetime import datetime

# 데이터 읽기
folder_path = r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data'
books_df = pd.read_csv(os.path.join(folder_path, 'booksCleaned.txt'), 
                      encoding='cp949', 
                      header=0)

# 현재 연도 가져오기
current_year = datetime.now().year

# 10년 이상 된 책 계산
books_df['책_연도'] = books_df['출판년도']  # 출판년도 열 이름이 '출판년도'라고 가정
books_10_years_old = books_df[books_df['책_연도'] <= (current_year - 10)]
books_5_years_old = books_df[books_df['책_연도'] <= (current_year - 5)]

# 전체 책 수
total_books = len(books_df)

# 비율 계산
percentage_10_years_old = (len(books_10_years_old) / total_books) * 100 if total_books > 0 else 0
percentage_5_years_old = (len(books_5_years_old) / total_books) * 100 if total_books > 0 else 0

# 결과 출력
print(f"10년 이상 된 책의 비율: {percentage_10_years_old:.2f}%")
print(f"5년 이상 된 책의 비율: {percentage_5_years_old:.2f}%") 