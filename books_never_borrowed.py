import pandas as pd
import os
from datetime import datetime

# 데이터 읽기
folder_path = r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data'
books_df = pd.read_csv(os.path.join(folder_path, 'booksCleaned.txt'), 
                      encoding='cp949', 
                      header=0)

# 대출 기록 데이터 읽기 (reser 파일)
reser_df = pd.read_csv(os.path.join(folder_path, 'reser.txt'), 
                       encoding='cp949', 
                       header=0)

# 현재 연도 가져오기
current_year = datetime.now().year

# 10년 이상 된 책 계산
books_df['책_연도'] = books_df['출판년도']  # 출판년도 열 이름이 '출판년도'라고 가정
books_10_years_old = books_df[books_df['책_연도'] <= (current_year - 10)]

# 10년 이상 된 책 중 대출이 한 번도 안된 책 찾기
# 대출 기록에서 도서ID별로 대출 횟수 세기
reser_counts = reser_df['도서ID'].value_counts().reset_index()
reser_counts.columns = ['도서ID', '대출량']

# 10년 이상 된 책과 대출량 데이터 병합
books_10_years_old = books_10_years_old.merge(reser_counts, on='도서ID', how='left')

# NaN 값을 0으로 대체 (대출이 없는 경우)
books_10_years_old['대출량'] = books_10_years_old['대출량'].fillna(0)

# 한 번도 대출되지 않은 책 필터링
never_borrowed_books = books_10_years_old[books_10_years_old['대출량'] == 0]

# 비율 계산
total_10_years_old = len(books_10_years_old)
never_borrowed_percentage = (len(never_borrowed_books) / total_10_years_old) * 100 if total_10_years_old > 0 else 0

# 결과 출력
print(f"10년 이상 된 책 중 한 번도 대출되지 않은 책의 비율: {never_borrowed_percentage:.2f}%") 