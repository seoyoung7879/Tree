import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 사용할 한글 폰트 경로
font_prop = fm.FontProperties(fname=font_path, size=12)

# 데이터 불러오기 (인코딩 지정)
books = pd.read_csv(r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data\books.txt', encoding='cp949')
reser = pd.read_csv(r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data\reser.txt', encoding='cp949')

# 대출량 계산: 도서 아이디별로 대출된 횟수 카운트
loan_counts = reser.groupby('도서ID')['대출일시'].count().reset_index(name='대출량')

# books 데이터와 대출량 데이터 병합
books = books.merge(loan_counts, on='도서ID', how='left')

# NaN 값을 0으로 대체 (대출량이 없는 경우)
books['대출량'] = books['대출량'].fillna(0)

# 문자형 변수를 숫자로 변환
books['수서방법'] = books['수서방법'].map({
    '학과신청': 0,
    '수서정보없음': 1,
    '이용자희망': 2,
    '사서선정': 3,
    '수업지정': 4,
    '기타': 5
})

books['소장위치'] = books['소장위치'].map({
    '4층인문': 0,
    '보존서고': 1
})

# 출판년도와 분류코드의 데이터 타입 확인 및 변환
books['출판년도'] = pd.to_numeric(books['출판년도'], errors='coerce')
books['분류코드'] = pd.to_numeric(books['분류코드'], errors='coerce')

# NaN 값을 0으로 대체
books['출판년도'] = books['출판년도'].fillna(0)
books['분류코드'] = books['분류코드'].fillna(0)

# 대출량(y)과 독립 변수(X) 설정
y = books['대출량']  # 대출량 컬럼
X = books[['수서방법', '출판년도', '소장위치', '분류코드']]  # 독립 변수

# 데이터 분할 (훈련 세트와 테스트 세트)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest 모델 생성 및 훈련
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 예측
y_pred = model.predict(X_test)

# 성능 평가
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Mean Squared Error:", mse)
print("R^2 Score:", r2)

# 새로운 데이터 예측 (예시)
new_data = pd.DataFrame({
    '수서방법': [0],  # 예시 값
    '출판년도': [2000],  # 예시 값
    '소장위치': [0],  # 예시 값
    '분류코드': [160]  # 예시 값
})

predicted_loan_count = model.predict(new_data)
print("예측된 대출량:", predicted_loan_count[0])
