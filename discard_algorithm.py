import pandas as pd
import os
from datetime import datetime

# 데이터 읽기
folder_path = r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data'
filtered_books_df = pd.read_csv(os.path.join(folder_path, 'combined_books_with_loans.csv'), 
                                 encoding='cp949', 
                                 header=0)

# 점수 계산을 위한 데이터프레임 생성
score_df = filtered_books_df.copy()

# 현재 연도
current_year = datetime.now().year

# 오래된 책 점수 계산 (출판년도 최대에서 현재를 빼고 정규화)
score_df['오래된_점수'] = current_year - score_df['출판년도']
score_df['오래된_점수'] = (score_df['오래된_점수'] - score_df['오래된_점수'].min()) / (score_df['오래된_점수'].max() - score_df['오래된_점수'].min()) * 10

# 대출량 점수 계산 (대출량 최대에서 현재를 빼고 정규화)
score_df['대출_점수'] = score_df['대출량'].max() - score_df['대출량']
score_df['대출_점수'] = (score_df['대출_점수'] - score_df['대출_점수'].min()) / (score_df['대출_점수'].max() - score_df['대출_점수'].min()) * 10

# 최근 대출일시 점수 계산 (최근 대출일시가 오래된 책일수록 점수가 높아짐)
score_df['최근대출일시_점수'] = (datetime.now() - pd.to_datetime(score_df['최근대출일시'], errors='coerce')).dt.days

# 최근 대출일시 점수 정규화
score_df['최근대출일시_점수'] = (score_df['최근대출일시_점수'] - score_df['최근대출일시_점수'].min()) / (score_df['최근대출일시_점수'].max() - score_df['최근대출일시_점수'].min()) * 10

# 최근 대출일시가 없을 경우 10년 이상 된 책에 대해 만점 부여 아니면 5점
score_df['최근대출일시_점수'] = score_df.apply(
    lambda row: 10 if pd.isnull(row['최근대출일시']) and (current_year - row['출판년도'] >= 10) 
    else (5 if pd.isnull(row['최근대출일시']) else row['최근대출일시_점수']), axis=1)

# 중복 도서 찾기
duplicate_books = score_df[score_df.duplicated(subset=['서명', '저자'], keep=False)]

# 중복 도서에 대한 점수 계산
if not duplicate_books.empty:
    # 가장 최근 출판년도 찾기
    latest_books = duplicate_books.loc[duplicate_books.groupby(['서명', '저자'])['출판년도'].idxmax()]

    # 가장 최근 출판년도에 해당하지 않는 책 찾기
    not_latest_books = duplicate_books[~duplicate_books.index.isin(latest_books.index)]

    # 중복 도서 점수 부여 (가장 최근 출판년도에 해당하지 않는 책에 5점 부여)
    score_df.loc[not_latest_books.index, '중복도서_점수'] = 5
else:
    # 중복 도서가 아닐 경우 기본 점수 부여
    score_df['중복도서_점수'] = 0

# 최종 점수 계산
score_df['discard_score'] = (score_df['중복도서_점수'] * 0.50 + 
                              score_df['오래된_점수'] * 1.50 + 
                              score_df['최근대출일시_점수'] *1.00 + 
                              score_df['대출_점수'] * 2.00)

# 결과를 점수 높은 순으로 정렬
sorted_score_df = score_df.sort_values(by='discard_score', ascending=False)

# 상위 20% 책들만 선택
top_20_percent_df = sorted_score_df.head(int(len(sorted_score_df) * 0.2))

# 결과를 CSV 파일로 저장
output_file_path = os.path.join(folder_path, 'discard_result.csv')
top_20_percent_df.to_csv(output_file_path, index=False, encoding='cp949')

# 결과 출력
print(f"결과가 {output_file_path}에 저장되었습니다.")

# 하위 10% 책들만 선택
bottom_10_percent_df = sorted_score_df.tail(int(len(sorted_score_df) * 0.1))
# ISBN별로 중복 제거
distinct_bottom_10_percent_df = bottom_10_percent_df.drop_duplicates(subset=['ISBN'])

# 결과를 CSV 파일로 저장
output_file_path = os.path.join(folder_path, 'popular_result.csv')
bottom_10_percent_df.to_csv(output_file_path, index=False, encoding='cp949')

# 결과 출력
print(f"결과가 {output_file_path}에 저장되었습니다.")