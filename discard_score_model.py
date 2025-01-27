import pandas as pd
import os
import numpy as np
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

# 오래된 책 필터링
old_books = filtered_books_df[filtered_books_df['출판년도'] <= ten_years_ago]

# 대출 기록 데이터 읽기 (reser 파일)
reser_df = pd.read_csv(os.path.join(folder_path, 'reser.txt'), 
                       encoding='cp949', 
                       header=0)

# 근 10년간 대출량 집계
reser_df['대출일시'] = pd.to_datetime(reser_df['대출일시'], errors='coerce')
reser_df = reser_df[reser_df['대출일시'] >= pd.Timestamp(year=ten_years_ago, month=1, day=1)]

# 대출량 계산: 도서ID별로 대출 횟수 세기
reser_counts = reser_df['도서ID'].value_counts().reset_index()
reser_counts.columns = ['도서ID', '대출량']

# books_df와 대출량 데이터 병합
filtered_books_df = filtered_books_df.merge(reser_counts, on='도서ID', how='left')
filtered_books_df['대출량'] = filtered_books_df['대출량'].fillna(0)

# 중복 소장 여부 계산 (중복 소장 수가 1보다 큰 경우)
filtered_books_df['중복소장여부'] = filtered_books_df['도서ID'].duplicated(keep=False).astype(int)

# 점수 계산
# 오래된 책 점수 계산: 출판년도에 따라 점수 부여
old_books['오래된_점수'] = (current_year - old_books['출판년도'])  # 오래된 책일수록 점수가 높음

# 대출 점수 계산: 대출량이 많을수록 점수가 낮아짐
max_borrowed = filtered_books_df['대출량'].max()
filtered_books_df['대출_점수'] = max_borrowed - filtered_books_df['대출량']  # 대출량이 많을수록 점수가 낮아짐

# 중복 소장 점수
filtered_books_df['중복소장_점수'] = filtered_books_df['중복소장여부']  # 중복 소장 여부 점수

# 점수 정규화 함수
def normalize_scores(df, score_column):
    min_score = df[score_column].min()
    max_score = df[score_column].max()
    df[score_column] = (df[score_column] - min_score) / (max_score - min_score) * 10  # 0~10으로 정규화

# 정규화 적용
normalize_scores(old_books, '오래된_점수')
normalize_scores(filtered_books_df, '대출_점수')
normalize_scores(filtered_books_df, '중복소장_점수')

# 최종 점수 계산
old_books['discard_score'] = (old_books['오래된_점수'] * 0.6 + 
                               filtered_books_df['대출_점수'].reindex(old_books.index, fill_value=0) * 0.3 + 
                               filtered_books_df['중복소장_점수'].reindex(old_books.index, fill_value=0) * 0.1)

# 상위 5개 책 선택
top_5_books = old_books.nlargest(5, 'discard_score')

# 상위 10%의 대출량 평균과 출판년도 평균 계산
top_10_percent_count = int(len(filtered_books_df) * 0.10)
top_10_percent_books = filtered_books_df.nlargest(top_10_percent_count, '대출량')

average_borrowed = top_10_percent_books['대출량'].mean()
average_year = top_10_percent_books['출판년도'].mean()

# 결과 출력
print("오래된 책의 discard_score_model 상위 5개:")
print(top_5_books[['도서ID', '서명', '저자', '출판년도', 'discard_score']].to_string(index=False))
print(f"\n상위 10%의 대출량 평균: {average_borrowed:.2f}")
print(f"상위 10%의 출판년도 평균: {average_year:.2f}")
