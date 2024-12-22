import pandas as pd
from datetime import datetime, timedelta

def analyze_no_loan_books():
    try:
        # 데이터 로드
        books_df = pd.read_csv('data/단행본(도서)정보.txt', encoding='cp949')
        loans_df = pd.read_csv('data/대출정보.txt', encoding='cp949')

        # 날짜 형식 변환
        loans_df['대출일시'] = pd.to_datetime(loans_df['대출일시'])
        books_df['등록일자'] = pd.to_datetime(books_df['등록일자'])
        
        # 최근 대출일자 확인
        latest_loan_date = loans_df['대출일시'].max()
        five_years_ago = latest_loan_date - timedelta(days=365*5)
        
        # 각 도서의 마지막 대출일자 확인
        last_loan_dates = loans_df.groupby('도서ID')['대출일시'].max().reset_index()
        last_loan_dates.columns = ['도서ID', '마지막_대출일']
        
        # 도서 정보와 마지막 대출일자 병합
        merged_df = pd.merge(books_df, last_loan_dates, on='도서ID', how='left')
        
        # 5년 이상 대출되지 않은 도서 필터링
        no_loan_books = merged_df[
            (merged_df['마지막_대출일'].isna()) |  # 한번도 대출되지 않은 책
            (merged_df['마지막_대출일'] < five_years_ago)  # 5년 이상 대출되지 않은 책
        ]
        
        # 결과 정리
        result_df = no_loan_books[['도서ID', '서명', '저자', '등록일자', '마지막_대출일', '소장위치']]
        result_df = result_df.sort_values('등록일자', ascending=False)
        
        # CSV 파일로 저장
        result_df.to_csv('data/no_loan_books.csv', index=False, encoding='utf-8-sig')
        
        # 통계 출력
        print("\n=== 5년 이상 미대출 도서 분석 결과 ===")
        print(f"• 전체 도서 수: {len(books_df):,}권")
        print(f"• 5년 이상 미대출 도서 수: {len(no_loan_books):,}권")
        print(f"• 미대출 비율: {(len(no_loan_books) / len(books_df) * 100):.1f}%")
        
        # 소장위치별 미대출 도서 수
        location_stats = no_loan_books.groupby('소장위치').size().sort_values(ascending=False)
        print("\n=== 소장위치별 미대출 도서 현황 ===")
        for location, count in location_stats.items():
            print(f"• {location}: {count:,}권")
        
        print("\n분석 결과가 data/no_loan_books.csv 파일로 저장되었습니다.")
        
        return result_df

    except Exception as e:
        print(f"에러 발생: {str(e)}")
        return None

if __name__ == "__main__":
    analyze_no_loan_books() 