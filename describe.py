import pandas as pd
import numpy as np

try:
    # 데이터 출력 옵션 설정
    pd.set_option('display.max_columns', None)  # 모든 열 표시
    pd.set_option('display.width', None)        # 너비 제한 해제
    pd.set_option('display.max_colwidth', None) # 열 너비 제한 해제
    
    # 데이터 읽기
    books_df = pd.read_csv('data/단행본(도서)정보.txt', encoding='cp949')
    loans_df = pd.read_csv('data/대출정보.txt', encoding='cp949')

    # 데이터 구조 확인
    print("\n=== 도서 정보 데이터 컬럼 ===")
    print(books_df.columns.tolist())
    
    print("\n=== 도서 정보 첫 5행 ===")
    print(books_df.head().to_string())

    print("\n=== 대출 정보 데이터 컬럼 ===")
    print(loans_df.columns.tolist())
    
    print("\n=== 대출 정보 첫 5행 ===")
    print(loans_df.head().to_string())

except FileNotFoundError:
    print("파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
except Exception as e:
    print(f"에러 발생: {str(e)}")