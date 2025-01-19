import pandas as pd
import os

# 데이터 읽기
folder_path = r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data'
filtered_books_df = pd.read_csv(os.path.join(folder_path, 'filtered_books.txt'), 
                                 encoding='cp949', 
                                 sep='\t',  # 탭으로 구분된 파일
                                 header=0)

# 서명과 저자가 같은 책들 찾기
duplicate_books = filtered_books_df[filtered_books_df.duplicated(subset=['서명', '저자'], keep=False)]

# 중복 도서 중 가장 최신 출판년도만 남기기
latest_books = duplicate_books.loc[duplicate_books.groupby(['서명', '저자'])['출판년도'].idxmax()]

# 전체 책 수
total_books_count = len(filtered_books_df)

# 중복 도서 수
duplicate_books_count = len(duplicate_books)

# 남은 책 수
remaining_books_count = len(latest_books)

# 제거된 책 수
removed_books_count = duplicate_books_count - remaining_books_count

# 비율 계산
removal_ratio = (removed_books_count / total_books_count) * 100 if total_books_count > 0 else 0

# 결과 출력
print(f"중복 도서 중 가장 최신 출판년도만 남긴 후 남은 책 수: {remaining_books_count}")
print(f"제거된 책 수: {removed_books_count}")
print(f"전체 책 수 대비 제거된 책 비율: {removal_ratio:.2f}%")

# 최신 도서만 남긴 데이터프레임을 저장 (선택 사항)
# latest_books.to_csv(os.path.join(folder_path, 'latest_books.txt'), index=False, sep='\t', encoding='cp949') 