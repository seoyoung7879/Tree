import pandas as pd

# 데이터 불러오기 (인코딩 지정)
books = pd.read_csv(r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data\books.txt', encoding='cp949')

# 소장위치가 '보존서고'인 도서의 분류코드 최대값과 최소값
preservation_codes = books[books['소장위치'] == '보존서고']['분류코드']
preservation_min = preservation_codes.min()
preservation_max = preservation_codes.max()

# 소장위치가 '4층인문'인 도서의 분류코드 최대값과 최소값
fourth_floor_codes = books[books['소장위치'] == '4층인문']['분류코드']
fourth_floor_min = fourth_floor_codes.min()
fourth_floor_max = fourth_floor_codes.max()

# 결과 출력
print("보존서고의 분류코드 최소값:", preservation_min)
print("보존서고의 분류코드 최대값:", preservation_max)
print("4층인문의 분류코드 최소값:", fourth_floor_min)
print("4층인문의 분류코드 최대값:", fourth_floor_max)
 
print(preservation_codes.head())
print(fourth_floor_codes.head())
