import numpy as np

def calculate_weights_ahp():
    # 수정된 쌍대비교 행렬 (1-9척도 사용)
    comparison_matrix = np.array([
        [1, 2, 1],     # 중복도서 vs 대출량, 중복도서 vs 출판년도
        [1/2, 1, 2],   # 대출량 vs 중복도서, 대출량 vs 출판년도
        [1, 1/2, 1]    # 출판년도 vs 중복도서, 출판년도 vs 대출량
    ])
    
    # 고유값과 고유벡터 계산
    eigenvalues, eigenvectors = np.linalg.eig(comparison_matrix)
    
    # 최대 고유값에 해당하는 고유벡터 선택
    max_idx = np.argmax(eigenvalues)
    weights = np.real(eigenvectors[:, max_idx])
    
    # 정규화
    weights = weights / np.sum(weights)
    
    return {
        'weight_borrow_frequency': weights[0],
        'weight_publication_year': weights[1],
        'weight_duplicate_ownership': weights[2]
    }

# 가중치 계산 및 결과 출력
weights = calculate_weights_ahp()

print("\n=== AHP 분석을 통한 가중치 계산 결과 ===")
print(f"대출 빈도 가중치: {weights['weight_borrow_frequency']:.3f}")
print(f"출판 연도 가중치: {weights['weight_publication_year']:.3f}")
print(f"중복 소장 가중치: {weights['weight_duplicate_ownership']:.3f}")

# 일관성 비율(CR) 계산
def calculate_consistency_ratio(comparison_matrix):
    n = len(comparison_matrix)
    eigenvalues = np.linalg.eigvals(comparison_matrix)
    lambda_max = max(eigenvalues.real)
    
    # 일관성 지수 (CI) 계산
    ci = (lambda_max - n) / (n - 1)
    
    # 무작위 지수 (RI) - AHP에서 일반적으로 사용되는 값
    ri_values = {3: 0.58, 4: 0.90, 5: 1.12}
    ri = ri_values[n]
    
    # 일관성 비율 (CR) 계산
    cr = ci / ri
    return cr

cr = calculate_consistency_ratio(np.array([
    [1, 2, 1],
    [1/2, 1, 2],
    [1, 1/2, 1]
]))

print(f"\n일관성 비율(CR): {cr:.3f}")
print("(CR이 0.1 이하면 일관성이 있다고 판단)")
