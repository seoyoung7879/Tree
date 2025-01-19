import pandas as pd
import os

# 데이터 읽기
folder_path = r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data'
filtered_books_df = pd.read_csv(os.path.join(folder_path, 'filtered_books.txt'), 
                                 encoding='cp949', 
                                 sep='\t',  # 탭으로 구분된 파일
                                 header=0)

# 대출 기록 데이터 읽기 (reser 파일)
reser_df = pd.read_csv(os.path.join(folder_path, 'reser.txt'), 
                       encoding='cp949', 
                       header=0)

# 대출 기록에서 대출량 계산 및 가장 최근 대출일시 찾기
reser_df['대출일시'] = pd.to_datetime(reser_df['대출일시'], errors='coerce')
reser_counts = reser_df.groupby('도서ID').agg(
    대출량=('대출일시', 'count'),  # 대출량 계산
    최근대출일시=('대출일시', 'max')  # 가장 최근 대출일시 찾기
).reset_index()

# filtered_books_df와 대출량 데이터 병합
filtered_books_df = filtered_books_df.merge(reser_counts, on='도서ID', how='left')

# 대출량이 없는 경우 0으로 채우기
filtered_books_df['대출량'] = filtered_books_df['대출량'].fillna(0)

# 새로운 데이터셋 저장
output_file_path = os.path.join(folder_path, 'combined_books_with_loans.csv')
filtered_books_df.to_csv(output_file_path, index=False, encoding='cp949')

# 결과 확인
print(f"결합된 데이터셋이 '{output_file_path}'에 저장되었습니다.")
