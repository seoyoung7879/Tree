import pandas as pd
import os

# 데이터 경로
folder_path = r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data'
file_path = os.path.join(folder_path, 'filtered_books.txt')

# 데이터 읽기
filtered_books_df = pd.read_csv(file_path, encoding='cp949', sep='\t', header=0)

# 중복 서명과 저자를 가진 그룹 필터링
duplicated_books = (
    filtered_books_df.groupby(['서명', '저자'])['출판년도']
    .nunique()  # 출판년도 고유값 수
    .reset_index()
    .query('출판년도 > 1')  # 출판년도 종류가 1개 초과인 경우
)

# 결과 데이터프레임 생성
result = pd.merge(filtered_books_df, duplicated_books[['서명', '저자']], on=['서명', '저자'])

# 서명 기준 정렬
result = result.sort_values(by=['서명', '저자', '출판년도'])

# 예시 출력
print(result)
