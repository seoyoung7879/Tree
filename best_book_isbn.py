import pandas as pd
from datetime import datetime
import sys
import io
import os

# 표준 출력 인코딩을 UTF-8로 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def analyze_biannual_popular_books():
    try:
        # Tree/data 디렉토리 확인 및 생성
        if not os.path.exists('Tree/data'):
            os.makedirs('Tree/data')

        # 데이터 읽기
        books_df = pd.read_csv('data/books_final_cleaned.txt', encoding='cp949')
        loans_df = pd.read_csv('data/대출정보.txt', encoding='cp949')
        
        # 날짜 형식 변환
        loans_df['대출일시'] = pd.to_datetime(loans_df['대출일시'])
        
        # 대출 데이터와 도서 정보를 결합
        merged_df = pd.merge(loans_df, books_df, on='도서ID')
        
        # 반기 구분을 위한 함수
        def get_biannual_period(date):
            year = date.year
            month = date.month
            if 3 <= month <= 8:
                return f"{year}년 상반기(3월-8월)"
            elif month >= 9:
                return f"{year}년 하반기(9월-2월)"
            else:  # 1,2월인 경우 전년도 하반기
                return f"{year-1}년 하반기(9월-2월)"
        
        # 반기 정보 추가
        merged_df['반기'] = merged_df['대출일시'].apply(get_biannual_period)
        
        # 반기별 상위 10개 도서 추출
        biannual_popular_books = []
        
        for period in merged_df['반기'].unique():
            period_data = merged_df[merged_df['반기'] == period]
            top_books = period_data.groupby(['ISBN', '서명', '저자'])['대출일시'].count()\
                                .reset_index(name='대출횟수')\
                                .sort_values('대출횟수', ascending=False)\
                                .head(10)
            top_books['반기'] = period
            biannual_popular_books.append(top_books)
        
        # 모든 반기의 결과를 하나의 DataFrame으로 합치기
        result_df = pd.concat(biannual_popular_books, ignore_index=True)
        
        # 결과를 CSV 파일로 저장
        result_df = result_df[['반기', 'ISBN', '서명', '저자', '대출횟수']]
        # 반기(내림차순)와 대출횟수(내림차순)로 정렬
        result_df = result_df.sort_values(['반기', '대출횟수'], ascending=[False, False])
        
        # 대출횟수에 '건' 단위 추가
        result_df['대출횟수'] = result_df['대출횟수'].apply(lambda x: f"{x:,}건")
        
        # CSV 파일로 저장
        result_df.to_csv('data/popular_isbn.csv', index=False, encoding='utf-8-sig')
        
        print("\n반기별 인기 도서 TOP 10이 Tree/data/popular_isbn.csv 파일로 저장되었습니다.")
        print(f"분석된 기간: {result_df['반기'].min()} ~ {result_df['반기'].max()}")
        print(f"전체 데이터 수: {len(result_df)}개")

    except Exception as e:
        print(f"에러 발생: {str(e)}")

if __name__ == "__main__":
    analyze_biannual_popular_books()