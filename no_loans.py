import pandas as pd
from datetime import datetime

def get_category_name(code):
    """
    분류코드를 분야명으로 변환하는 함수
    """
    # 앞 세 자리를 기준으로 분류
    code_str = str(code)[:3]
    
    categories = {
        '000': '총류',
        '100': '철학',
        '200': '종교',
        '300': '사회과학',
        '400': '자연과학',
        '500': '기술과학',
        '600': '예술',
        '700': '언어',
        '800': '문학',
        '900': '역사'
    }
    
    return categories.get(code_str, '기타')

def analyze_old_books():
    try:
        # 데이터 로드
        books_df = pd.read_csv('data/단행본(도서)정보.txt', encoding='cp949')
        loans_df = pd.read_csv('data/대출정보.txt', encoding='cp949')

        # 날짜 형식 변환
        loans_df['대출일시'] = pd.to_datetime(loans_df['대출일시'])
        books_df['등록일자'] = pd.to_datetime(books_df['등록일자'])
        
        # 분류 코드로 분야 추가
        books_df['분야'] = books_df['분류코드'].apply(get_category_name)
        
        # 현재 날짜 기준으로 미래 데이터 제외
        current_date = pd.Timestamp.now()
        books_df = books_df[books_df['등록일자'] <= current_date]
        
        # 2014년 기준일 설정
        cutoff_date = pd.Timestamp('2014-12-31')
        
        # ISBN 기준 대출 통계
        isbn_loan_stats = loans_df.merge(books_df[['도서ID', 'ISBN']], on='도서ID', how='left')
        isbn_loan_counts = isbn_loan_stats.groupby('ISBN').size().reset_index(name='대출횟수')
        
        # 도서별 마지막 대출일 계산 (이미 있는 코드 활용)
        last_loan_dates = loans_df.groupby('도서ID')['대출일시'].max().reset_index()
        last_loan_dates.columns = ['도서ID', '마지막_대출일']
        
        # 현재 날짜 기준으로 5년, 10년 전 날짜 계산
        five_years_ago = current_date - pd.DateOffset(years=5)
        ten_years_ago = current_date - pd.DateOffset(years=10)
        
        # 도서 정보와 마지막 대출일자 병합
        merged_df = pd.merge(books_df, last_loan_dates, on='도서ID', how='left')
        
        # 5년, 10년 미대출 도서 계산
        not_loaned_5y = merged_df[
            (merged_df['마지막_대출일'].isna()) | 
            (merged_df['마지막_대출일'] <= five_years_ago)
        ]
        not_loaned_10y = merged_df[
            (merged_df['마지막_대출일'].isna()) | 
            (merged_df['마지막_대출일'] <= ten_years_ago)
        ]
        
        # 결과 데이터프레임 생성
        result_df = merged_df[[
            '도서ID', '서명', '저자', '분야', 'ISBN', '출판년도', '마지막_대출일'
        ]].copy()
        
        # ISBN별 대출 통계 추가
        result_df = result_df.merge(isbn_loan_counts, on='ISBN', how='left')
        
        # 미대출 기간 정보 추가
        result_df['5년이상_미대출'] = result_df['도서ID'].isin(not_loaned_5y['도서ID'])
        result_df['10년이상_미대출'] = result_df['도서ID'].isin(not_loaned_10y['도서ID'])
        
        # 전체 통계 계산
        total_books = len(merged_df)
        never_loaned = len(result_df[result_df['대출횟수'].fillna(0) == 0])
        stats = {
            '5년이상_미대출_비율': (len(not_loaned_5y) / total_books * 100),
            '10년이상_미대출_비율': (len(not_loaned_10y) / total_books * 100),
            '대출이력없는_도서_비율': (never_loaned / total_books * 100)
        }
        
        # CSV 파일로 저장
        result_df.to_csv('data/book_loan_analysis.csv', index=False, encoding='utf-8-sig')
        
        # 통계 출력
        print("\n=== 도서 대출 분석 결과 ===")
        print(f"• 전체 도서 수: {total_books:,}권")
        print(f"• 대출 이력이 없는 도서 비율: {stats['대출이력없는_도서_비율']:.1f}%")
        print(f"• 5년 이상 미대출 도서 비율: {stats['5년이상_미대출_비율']:.1f}%")
        print(f"• 10년 이상 미대출 도서 비율: {stats['10년이상_미대출_비율']:.1f}%")
        print("data/book_loan_analysis.csv 파일로 저장되었습니다.")
        return result_df, stats

    except Exception as e:
        print(f"에러 발생: {str(e)}")
        return None, None

if __name__ == "__main__":
    analyze_old_books()