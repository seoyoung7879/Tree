import pandas as pd
import os

# 데이터 읽기
folder_path = r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data'
books_df = pd.read_csv(os.path.join(folder_path, 'booksCleaned.txt'), 
                      encoding='cp949', 
                      header=0)

# 소장 위치가 '보존서고'가 아닌 책 필터링
filtered_books = books_df[books_df['소장위치'] != '보존서고']  # '소장위치' 열 이름이 '소장위치'라고 가정

# 새로운 데이터셋으로 저장 (txt 형식)
filtered_books.to_csv(os.path.join(folder_path, 'filtered_books.txt'), index=False, sep='\t', encoding='cp949')

print("소장 위치가 '보존서고'가 아닌 책들이 'filtered_books.txt'로 저장되었습니다.") 