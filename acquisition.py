import pandas as pd
import matplotlib.pyplot as plt
import sys
import io
import os
import platform

# 표준 출력 인코딩을 UTF-8로 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def set_korean_font():
    """운영체제별 한글 폰트 설정"""
    system_name = platform.system()
    
    if system_name == "Darwin":  # macOS
        plt.rcParams['font.family'] = 'AppleGothic'
    elif system_name == "Windows":
        plt.rcParams['font.family'] = 'Malgun Gothic'
    elif system_name == "Linux":
        plt.rcParams['font.family'] = 'NanumGothic'
        
    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

def analyze_acquisition_loans():
    try:
        # img 디렉토리 생성
        if not os.path.exists('img'):
            os.makedirs('img')

        # 데이터 로드
        books_df = pd.read_csv('data/단행본(도서)정보.txt', encoding='cp949')
        loans_df = pd.read_csv('data/대출정보.txt', encoding='cp949')

        # 한글 폰트 설정
        set_korean_font()

        # 데이터 병합
        merged_df = pd.merge(loans_df, books_df, on='도서ID')

        # 수서방법별 대출 건수 계산
        acquisition_loans = merged_df.groupby('수서방법')['도서ID'].count()

        # 통계 데이터 계산
        total_loans = acquisition_loans.sum()
        loan_percentages = (acquisition_loans / total_loans * 100).round(2)
        
        # 통계 결과를 DataFrame으로 변환 - 단위 추가
        stats_df = pd.DataFrame({
            '대출 건수': acquisition_loans.apply(lambda x: f"{x:,}건"),
            '비율': loan_percentages.apply(lambda x: f"{x:.2f}%")
        })

        # 시각화 - 한글 레이블 적용
        plt.figure(figsize=(10, 6))
        bars = acquisition_loans.plot(kind='bar')
        
        plt.title('수서방법별 대출 현황')
        plt.xlabel('수서방법')
        plt.ylabel('대출량(건)')
        plt.xticks(range(len(acquisition_loans)), acquisition_loans.index, rotation=45)
        plt.grid(True, alpha=0.3)
        
        # 막대 위에 값 표시
        for i, v in enumerate(acquisition_loans):
            plt.text(i, v, f'{v:,}건', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('img/acquisition_method_loans.png', dpi=300, bbox_inches='tight')
        plt.close()
       
        # 통계 출력
        print("\n=== 수서방법별 대출 통계 ===")
        print(stats_df)
        print(f"\n전체 대출 건수: {total_loans:,}권")

        print("\n분석 결과가 img 폴더에 저장되었습니다:")
        print("1. 시각화 결과: img/acquisition_method_loans.png")
        print("2. 통계 데이터: img/acquisition_stats.csv")

    except Exception as e:
        print(f"에러 발생: {str(e)}")

if __name__ == "__main__":
    analyze_acquisition_loans()
