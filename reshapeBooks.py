import pandas as pd
import re
import os

# 데이터 읽기
folder_path = r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data'
books_df = pd.read_csv(os.path.join(folder_path, 'books.txt'), 
                      encoding='cp949', 
                      header=0)

# 연도 변환 함수
def convert_year(year):
    if pd.isna(year):
        return None
    
    # 4자리 숫자 추출
    match = re.search(r'\d{4}', str(year))
    if not match:
        return None
    
    year = int(match.group())
    
    # 1954-2024 범위 체크
    if 1954 <= year <= 2024:
        return year
    
    # 2자리수로 변환하여 체크
    year_2digit = year % 100
    if year_2digit <= 24:
        new_year = 2000 + year_2digit
    else:
        new_year = 1900 + year_2digit
    
    # 다시 범위 체크
    if 1954 <= new_year <= 2024:
        return new_year
    
    return None

# 출판년도 변환
books_df['출판년도'] = books_df['출판년도'].apply(convert_year)

# 중앙값 계산
median_year = books_df['출판년도'].median()

# 결측값 및 이상치 처리: 중앙값으로 대체
books_df['출판년도'] = books_df['출판년도'].fillna(median_year)

# 저자와 서명을 결합한 새로운 열 추가
books_df['저자서명'] = books_df.apply(lambda x: 
    (str(x['저자']) if pd.notna(x['저자']) else '정보없음') + 
    (str(x['서명']) if pd.notna(x['서명']) else '정보없음'), axis=1)

# 나머지 결측값을 '정보없음'으로 대체
books_df = books_df.fillna('정보없음')

# 새로운 파일로 저장
output_path = os.path.join(folder_path, 'books_final_cleaned.txt')
books_df.to_csv(output_path, index=False, encoding='cp949')

print("\n=== 데이터 처리 완료 ===")
print(f"처리된 파일 저장 위치: {output_path}") 