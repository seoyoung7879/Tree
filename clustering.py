import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 불러오기
checkouts = pd.read_csv(r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data\reser.txt', encoding='cp949')
books = pd.read_csv(r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data\books.txt', encoding='cp949')

# 데이터 병합 및 전처리
data_merged = pd.merge(checkouts, books, on='도서ID').dropna()
data_merged['대출일시'] = pd.to_datetime(data_merged['대출일시'])
data_merged['연식'] = 2024 - pd.to_datetime(data_merged['등록일자']).dt.year

# 도서별 대출 건수 계산
loan_count = data_merged.groupby('도서ID').agg(대출건수=('대출일시', 'count')).reset_index()

# 데이터 병합
cluster_data = pd.merge(loan_count, data_merged[['도서ID', '연식']].drop_duplicates(), on='도서ID')

# 데이터 스케일링
scaler = StandardScaler()
scaled_data = scaler.fit_transform(cluster_data[['대출건수', '연식']])

# 최적의 클러스터 수 결정 (Elbow Method)
inertia = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_data)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(8, 4))
plt.plot(range(1, 11), inertia, marker='o')
plt.title('Elbow Method')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.show()

# k-means 클러스터링
k = 4 # elbow로 결정
kmeans = KMeans(n_clusters=k, random_state=42)
cluster_data['Cluster'] = kmeans.fit_predict(scaled_data)

# 결과 시각화
plt.figure(figsize=(10, 6))
sns.set(style="whitegrid")  # 스타일 설정
sns.scatterplot(data=cluster_data, x='연식', y='대출건수', hue='Cluster', palette='deep', s=80, edgecolor='w', linewidth=0.5)
plt.title('K-means Clustering of Books')
plt.xlabel('Book Age')
plt.ylabel('Number of Loans')
plt.legend(title='Cluster', loc='upper right')
plt.show()