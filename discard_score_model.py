import pandas as pd
import os
from datetime import datetime
import numpy as np

# 데이터 폴더 경로 설정
folder_path = r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data'

# 1. 대출 정보 읽기
loans_df = pd.read_csv(os.path.join(folder_path, 'reser.txt'), encoding='cp949', header=None)
loans_df.columns = ['도서ID', '대출일시']

# 2. 도서 정보 읽기
books_df = pd.read_csv(os.path.join(folder_path, 'books.txt'), encoding='cp949', header=None)
books_df.columns = ["도서ID", "등록일자", "수서방법", "분류코드", "ISBN", "서명", "저자", "출판사", "출판년도", "소장위치"]

# 3. 현재 날짜
current_date = datetime.now()

# 4. 가중치 설정
weight_borrow_frequency = 0.5  # 대출 빈도 가중치
weight_publication_year = 0.3   # 출판 연도 가중치
weight_duplicate_ownership = 0.2 # 중복 소장 여부 가중치

# 5. 대출 빈도 계산
borrow_counts = loans_df['도서ID'].value_counts().reset_index()
borrow_counts.columns = ['도서ID', '대출횟수']

# 6. 출판 연도 계산
books_df['출판년도'] = pd.to_numeric(books_df['출판년도'], errors='coerce')
books_df['출판연도_경과'] = current_date.year - books_df['출판년도']

# 7. 중복 소장 여부 계산
duplicate_counts = books_df['도서ID'].value_counts().reset_index()
duplicate_counts.columns = ['도서ID', '중복소장횟수']

# 8. 데이터 병합
merged_df = books_df.merge(borrow_counts, on='도서ID', how='left').fillna(0)
merged_df = merged_df.merge(duplicate_counts, on='도서ID', how='left').fillna(0)

# 9. 폐기 점수 계산
merged_df['폐기점수'] = (
    (merged_df['대출횟수'] * weight_borrow_frequency) +
    (merged_df['출판연도_경과'] * weight_publication_year) +
    (merged_df['중복소장횟수'] * weight_duplicate_ownership)
)

# 10. 보존서고 이동 대상 도서 선정
# 장기 저조 대출 도서: 대출 횟수가 5년 또는 10년 동안 0인 도서
# 중복 소장 도서: 중복 소장 횟수가 2 이상인 도서
threshold_years = 5
threshold_borrow_count = 0

# 대출일시를 datetime 형식으로 변환
loans_df['대출일시'] = pd.to_datetime(loans_df['대출일시'], errors='coerce')

# 최근 5년 동안 대출된 도서 필터링
recent_loans = loans_df[loans_df['대출일시'] >= (current_date - pd.DateOffset(years=threshold_years))]

# 장기 저조 대출 도서
long_term_low_borrowed = merged_df[~merged_df['도서ID'].isin(recent_loans['도서ID'])]

# 중복 소장 도서
duplicate_ownership_books = merged_df[merged_df['중복소장횟수'] > 1]

# 보존서고 이동 대상 도서
preservation_candidates = pd.concat([long_term_low_borrowed, duplicate_ownership_books]).drop_duplicates()

# 11. 상위 N개 도서 선정
top_n = 10  # 상위 10개 도서
top_candidates = preservation_candidates.nlargest(top_n, '폐기점수')

# 12. 폐기할 도서 수 결정 (올림 처리)
top_candidates['폐기할도서수'] = np.ceil(top_candidates['중복소장횟수'] / 2).astype(int)

# 결과 출력
print("폐기 점수 계산 결과:")
print(merged_df[['도서ID', '서명', '출판년도', '대출횟수', '중복소장횟수', '폐기점수']].head(top_n))  # 상위 N개만 출력

print("\n보존서고 이동 대상 도서:")
# 폐기할 도서 수와 함께 출력
top_candidates['결과'] = top_candidates.apply(lambda row: f"{row['서명']} (현재 보유: {row['중복소장횟수']}, 폐기할 수: {row['폐기할도서수']})", axis=1)
print(top_candidates[['도서ID', '결과', '폐기점수']].head(top_n))  # 상위 N개만 출력 