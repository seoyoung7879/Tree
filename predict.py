import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

def predict_loan_counts():
    try:
        # 1. 데이터 읽기
        books_df = pd.read_csv('data/단행본(도서)정보.txt', encoding='cp949')
        loans_df = pd.read_csv('data/대출정보.txt', encoding='cp949')

        # 2. 대출 횟수 계산
        book_loan_counts = loans_df['도서ID'].value_counts().reset_index()
        book_loan_counts.columns = ['도서ID', '대출횟수']

        # 3. 도서 정보와 대출 정보 결합
        books_with_loans = pd.merge(books_df, book_loan_counts, 
                                   on='도서ID', how='left')
        books_with_loans['대출횟수'] = books_with_loans['대출횟수'].fillna(0)

        # 4. 특성 전처리
        le_location = LabelEncoder()
        le_method = LabelEncoder()
        le_publisher = LabelEncoder()  # 출판사 추가
        
        books_with_loans['소장위치_인코딩'] = le_location.fit_transform(books_with_loans['소장위치'])
        books_with_loans['수서방법_인코딩'] = le_method.fit_transform(books_with_loans['수서방법'])
        books_with_loans['출판사_인코딩'] = le_publisher.fit_transform(books_with_loans['출판사'])
        books_with_loans['출판년도'] = pd.to_numeric(books_with_loans['출판년도'], errors='coerce')

        # 5. 예측 특성 선택 (특성 추가)
        features = ['소장위치_인코딩', '수서방법_인코딩', '출판사_인코딩', '출판년도']
        X = books_with_loans[features].fillna(-1)
        y = books_with_loans['대출횟수']  # 실제 대출 횟수를 예측

        # 6. 모델 학습 (RandomForestRegressor 사용)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # 7. 모델 평가
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print("\n=== 모델 성능 ===")
        print(f"Mean Squared Error: {mse:.2f}")
        print(f"R-squared Score: {r2:.2f}")

        # 8. 전체 데이터에 대한 예측
        books_with_loans['예측_대출횟수'] = model.predict(X)
        
        # 9. 특성 중요도 계산
        feature_importance = pd.DataFrame({
            '특성': features,
            '중요도': model.feature_importances_
        }).sort_values('중요도', ascending=False)
        
        print("\n=== 특성 중요도 ===")
        print(feature_importance)

        # 10. 결과 저장
        prediction_results = books_with_loans[['도서ID', '서명', '저자', '출판사', 
                                             '소장위치', '대출횟수', '예측_대출횟수']]
        prediction_results.to_csv('loan_count_predictions.csv', index=False, encoding='utf-8-sig')
        
        # 11. 가장 많은 대출이 예측되는 도서 출력
        print("\n=== 높은 대출 예측 TOP 10 도서 ===")
        top_predicted = prediction_results.nlargest(10, '예측_대출횟수')
        print(top_predicted[['서명', '저자', '대출횟수', '예측_대출횟수']])
        
        # 12. 실제 대출과 예측 대출의 차이 분석
        prediction_results['예측_오차'] = abs(prediction_results['대출횟수'] - prediction_results['예측_대출횟수'])
        
        print("\n=== 예측 정확도 통계 ===")
        print(f"평균 예측 오차: {prediction_results['예측_오차'].mean():.2f}")
        print(f"중앙값 예측 오차: {prediction_results['예측_오차'].median():.2f}")
        
        return prediction_results, feature_importance

    except Exception as e:
        print(f"에러 발생: {str(e)}")
        return None, None

def create_visualizations():
    try:
        # img 폴더 생성
        if not os.path.exists('img'):
            os.makedirs('img')
            print("'img' 폴더가 생성되었습니다.")

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
        plt.savefig('img/monthly_book_loans.png', dpi=300)
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
        plt.savefig('img/yearly_book_loans.png', dpi=300)
        plt.close()

        # 4. 소장위치별 대출 분포
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
        plt.savefig('img/location_loans.png', dpi=300)
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
        plt.savefig('img/weekday_loans.png', dpi=300)
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
        plt.savefig('img/hourly_loans.png', dpi=300)
        plt.close()

        print("모든 시각화가 'img' 폴더에 저장되었습니다.")

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

    except Exception as e:
        print(f"에러 발생: {str(e)}")

if __name__ == "__main__":
    results, importance = predict_loan_counts()
    create_visualizations()