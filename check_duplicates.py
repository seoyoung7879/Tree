import pandas as pd
import os

# 데이터 읽기
folder_path = r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data'
books_df = pd.read_csv(os.path.join(folder_path, 'books.txt'), 
                      encoding='cp949', header=None)
books_df.columns = ["도서ID", "등록일자", "수서방법", "분류코드", "ISBN", 
                   "서명", "저자", "출판사", "출판년도", "소장위치"]

# ISBN 전처리
books_df['ISBN'] = books_df['ISBN'].str.replace('-', '').str.strip()

# ISBN별 중복 소장 현황
duplicate_counts = books_df.groupby('ISBN').agg({
    '도서ID': 'count',
    '서명': 'first',
    '저자': 'first',
    '출판사': 'first'
}).reset_index()

duplicate_counts.columns = ['ISBN', '소장권수', '서명', '저자', '출판사']
duplicate_counts = duplicate_counts.sort_values('소장권수', ascending=False)

print("\n=== 중복 소장 현황 (상위 20개) ===")
print(duplicate_counts.head(20).to_string(index=False))

print("\n=== 통계 ===")
print(f"전체 도서 수: {len(books_df)}")
print(f"고유 ISBN 수: {len(duplicate_counts)}")
print(f"2권 이상 소장된 도서 수: {len(duplicate_counts[duplicate_counts['소장권수'] > 1])}")
