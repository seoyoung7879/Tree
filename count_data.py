import pandas as pd
import os

# 데이터 읽기
folder_path = r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data'
filtered_books_df = pd.read_csv(os.path.join(folder_path, 'combined_books_with_loans.csv'), 
                                 encoding='cp949', 
                                 header=0)

# 데이터 수 세기
data_count = filtered_books_df.shape[0]
print(f"총 데이터 수: {data_count}개") 
