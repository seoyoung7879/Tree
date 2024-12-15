import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def create_visualizations():
    try:
        # 1. 데이터 읽기
        books_df = pd.read_csv('data/단행본(도서)정보.txt', encoding='cp949')
        loans_df = pd.read_csv('data/대출정보.txt', encoding='cp949')

        # 한글 폰트 설정
        plt.rcParams['font.family'] = 'AppleGothic'

        # 2. 월별 대출 추이
        loans_df['대출일시'] = pd.to_datetime(loans_df['대출일시'])
        monthly_loans = loans_df.groupby(loans_df['대출일시'].dt.strftime('%Y-%m'))['도서ID'].count()

        plt.figure(figsize=(15, 6))
        monthly_loans.plot(kind='bar')
        plt.title('Monthly Book Loans')
        plt.xlabel('Date')
        plt.ylabel('Number of Loans')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('monthly_book_loans.png', dpi=300)
        plt.close()

        # 3. 연도별 대출 추이
        yearly_loans = loans_df.groupby(loans_df['대출일시'].dt.year)['도서ID'].count()
        
        plt.figure(figsize=(12, 5))
        yearly_loans.plot(kind='bar')
        plt.title('Yearly Book Loans')
        plt.xlabel('Year')
        plt.ylabel('Number of Loans')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('yearly_book_loans.png', dpi=300)
        plt.close()

        # 4. 소장위치별 대출 분포
        # 대출 데이터와 도서 정보를 결합
        merged_df = pd.merge(loans_df, books_df, on='도서ID')
        location_loans = merged_df.groupby('소장위치')['도서ID'].count().sort_values(ascending=False)
        
        plt.figure(figsize=(12, 6))
        location_loans.plot(kind='bar')
        plt.title('Number of Loans by Location')
        plt.xlabel('Location')
        plt.ylabel('Number of Loans')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('location_loans.png', dpi=300)
        plt.close()

        # 5. 요일별 대출 분포
        loans_df['weekday'] = loans_df['대출일시'].dt.day_name()
        weekday_loans = loans_df.groupby('weekday')['도서ID'].count()
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_loans = weekday_loans.reindex(weekday_order)

        plt.figure(figsize=(10, 6))
        weekday_loans.plot(kind='bar')
        plt.title('Number of Loans by Weekday')
        plt.xlabel('Weekday')
        plt.ylabel('Number of Loans')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('weekday_loans.png', dpi=300)
        plt.close()

        # 6. 시간대별 대출 분포
        loans_df['hour'] = loans_df['대출일시'].dt.hour
        hourly_loans = loans_df.groupby('hour')['도서ID'].count()

        plt.figure(figsize=(12, 6))
        hourly_loans.plot(kind='bar')
        plt.title('Number of Loans by Hour')
        plt.xlabel('Hour')
        plt.ylabel('Number of Loans')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('hourly_loans.png', dpi=300)
        plt.close()

        # 7. 통계 정보 출력
        print("\n=== 대출 통계 ===")
        print(f"전체 대출 건수: {len(loans_df)}")
        print(f"월평균 대출 건수: {monthly_loans.mean():.2f}")
        print(f"최대 월간 대출 건수: {monthly_loans.max()}")
        print(f"최소 월간 대출 건수: {monthly_loans.min()}")
        
        # 8. 가장 많이 대출된 책 TOP 10
        top_books = merged_df.groupby(['도서ID', '서명'])['대출일시'].count()\
                            .sort_values(ascending=False)\
                            .head(10)
        
        print("\n=== 가장 많이 대출된 책 TOP 10 ===")
        print(top_books)

        print("\n모든 시각화가 완료되었습니다.")

    except Exception as e:
        print(f"에러 발생: {str(e)}")

if __name__ == "__main__":
    create_visualizations()