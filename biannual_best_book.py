import pandas as pd
from datetime import datetime

def analyze_biannual_popular_books():
    try:
        # 데이터 읽기
        books_df = pd.read_csv('data/단행본(도서)정보.txt', encoding='cp949')
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
            top_books = period_data.groupby(['도서ID', '서명', '저자'])['대출일시'].count()\
                                .reset_index(name='대출횟수')\
                                .sort_values('대출횟수', ascending=False)\
                                .head(10)
            top_books['반기'] = period
            biannual_popular_books.append(top_books)
        
        # 모든 반기의 결과를 하나의 DataFrame으로 합치기
        result_df = pd.concat(biannual_popular_books, ignore_index=True)
        
        # 결과를 CSV 파일로 저장
        result_df = result_df[['반기', '서명', '저자', '도서ID', '대출횟수']]
        # 반기(내림차순)와 대출횟수(내림차순)로 정렬
        result_df = result_df.sort_values(['반기', '대출횟수'], ascending=[False, False])
        result_df.to_csv('data/biannual_popular_books.csv', index=False, encoding='utf-8-sig')
        
        print("\n반기별 인기 도서 TOP 10이 data/biannual_popular_books.csv 파일로 저장되었습니다.")
        print(f"분석된 기간: {result_df['반기'].min()} ~ {result_df['반기'].max()}")
        print(f"전체 데이터 수: {len(result_df)}개")

    except Exception as e:
        print(f"에러 발생: {str(e)}")

if __name__ == "__main__":
    analyze_biannual_popular_books()
