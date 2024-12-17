import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.family'] = 'Malgun Gothic'

def load_and_preprocess_data():
    try:
        # 데이터 로드
        checkouts = pd.read_csv(r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data\대출정보.txt', 
                              encoding='cp949')
        books = pd.read_csv(r'C:\Users\hg226\Downloads\안내 및 데이터 송부\Tree\data\단행본(도서)정보.txt', 
                           encoding='cp949')
        
        # 날짜/시간 변환
        checkouts['대출일시'] = pd.to_datetime(checkouts['대출일시'])
        books['등록일자'] = pd.to_datetime(books['등록일자'])
        
        # 데이터 정렬
        checkouts = checkouts.sort_values('대출일시')
        
        print("📚 데이터 로드 완료")
        print(f"• 전체 대출 건수: {len(checkouts):,}건")
        print(f"• 전체 도서 수: {len(books):,}권")
        
        return checkouts, books
        
    except Exception as e:
        print(f"데이터 로드 중 오류 발생: {str(e)}")
        return None, None

def create_time_based_transactions(checkouts_df, time_window=100, sample_days=5000):  # 시간 간격 15분으로 늘림
    """15분 간격으로 트랜잭션 생성 (샘플링 적용)"""
    # 최근 데이터 위주로 샘플링
    latest_date = checkouts_df['대출일시'].max()
    date_range = pd.date_range(end=latest_date, periods=sample_days, freq='D')
    
    sampled_checkouts = checkouts_df[checkouts_df['대출일시'].dt.date.isin(date_range.date)]
    sampled_checkouts = sampled_checkouts.sort_values('대출일시')
    
    transactions = []
    current_transaction = []
    last_time = None
    
    for _, row in sampled_checkouts.iterrows():
        if last_time is None:
            current_transaction = [row['도서ID']]
            last_time = row['대출일시']
        else:
            time_diff = (row['대출일시'] - last_time).total_seconds() / 60
            
            if time_diff <= time_window:
                if row['도서ID'] not in current_transaction:  # 중복 제거
                    current_transaction.append(row['도서ID'])
            else:
                if len(current_transaction) > 1:  # 2권 이상 대출된 경우만 포함
                    transactions.append(current_transaction)
                current_transaction = [row['도서ID']]
            last_time = row['대출일시']
    
    # 마지막 트랜잭션 처리
    if len(current_transaction) > 1:
        transactions.append(current_transaction)
    
    print(f"\n📊 트랜잭션 생성 결과")
    print(f"• 분석 기간: {min(date_range.date)} ~ {max(date_range.date)}")
    print(f"• 생성된 트랜잭션 수: {len(transactions):,}개")
    if transactions:
        print(f"• 평균 트랜잭션 크기: {np.mean([len(t) for t in transactions]):.2f}권")
        print(f"• 최대 트랜잭션 크기: {max([len(t) for t in transactions])}권")
    
    return transactions

def create_transaction_matrix(transactions):
    """트랜잭션 매트릭스 생성"""
    # 모든 고유 도서 ID 수집
    unique_books = sorted(list(set([book for trans in transactions for book in trans])))
    
    # 트랜잭션 매트릭스 초기화
    matrix = np.zeros((len(transactions), len(unique_books)), dtype=bool)
    book_to_idx = {book: idx for idx, book in enumerate(unique_books)}
    
    # 매트릭스 채우기
    for trans_idx, transaction in enumerate(transactions):
        for book in transaction:
            book_idx = book_to_idx[book]
            matrix[trans_idx, book_idx] = True
    
    return pd.DataFrame(matrix, columns=unique_books)

def analyze_category(transactions, category_name, min_support=0.001):  # 지지도 더 낮춤
    """카테고리별 연관규칙 분석"""
    # 트랜잭션 매트릭스 생성
    matrix = create_transaction_matrix(transactions)
    
    print(f"\n매트릭스 크기: {matrix.shape}")
    
    # 연관규칙 생성
    frequent_itemsets = apriori(matrix, 
                              min_support=min_support, 
                              use_colnames=True,
                              max_len=2)  # 2개 아이템 조합만 고려
    
    if len(frequent_itemsets) == 0:
        print(f"\n❌ {category_name}: 발견된 빈발 아이템셋이 없습니다.")
        return None
    
    print(f"• 발견된 빈발 아이템셋 수: {len(frequent_itemsets)}개")
    
    rules = association_rules(frequent_itemsets, 
                            metric="confidence",
                            min_threshold=0.05)  # 신뢰도 더 낮춤
    
    if len(rules) == 0:
        print(f"\n❌ {category_name}: 발견된 연관규칙이 없습니다.")
        return None
    
    # 향상도가 1 이상인 규칙만 선택
    rules = rules[rules['lift'] >= 1]
    rules = rules[rules['lift'] <= 10]  # 비정상적으로 높은 향상도 제외
    
    # 최소 발생 횟수 필터링
    rules = rules[rules['support'] * len(transactions) >= 3]  
    
    print(f"\n📈 {category_name} 분석 결과")
    print(f"• 발견된 규칙 수: {len(rules):,}개")
    if len(rules) > 0:
        print(f"• 향상도 범위: {rules['lift'].min():.2f} ~ {rules['lift'].max():.2f}")
        print("\n상위 5개 규칙:")
        top_rules = rules.nlargest(5, 'lift')
        for idx, rule in top_rules.iterrows():
            print(f"\n[규칙 {idx+1}]")
            print(f"IF {list(rule['antecedents'])[0]}")
            print(f"THEN {list(rule['consequents'])[0]}")
            print(f"• 지지도: {rule['support']:.4f}")
            print(f"• 신뢰도: {rule['confidence']:.4f}")
            print(f"• 향상도: {rule['lift']:.4f}")
    
    return rules

def main():
    # 데이터 로드
    checkouts, books = load_and_preprocess_data()
    if checkouts is None or books is None:
        return
    
    # 15분 간격 트랜잭션 생성 (30일 샘플링)
    transactions = create_time_based_transactions(checkouts, time_window=15, sample_days=30)
    
    # 연관규칙 분석
    rules = analyze_category(transactions, "전체", min_support=0.001)
    
    # 시각화
    if rules is not None and len(rules) > 0:
        plt.figure(figsize=(10, 6))
        plt.scatter(rules['support'], rules['confidence'], 
                   c=rules['lift'], cmap='viridis', alpha=0.6)
        plt.colorbar(label='향상도')
        plt.xlabel('지지도')
        plt.ylabel('신뢰도')
        plt.title('전체 도서 연관규칙 분포')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    main()
