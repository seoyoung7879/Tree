import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

folder_path = '데이터톤2024(도서관정보)'

try:
    # 1. 데이터 읽기
    books_df = pd.read_csv(os.path.join(folder_path, '단행본(도서)정보.txt'), encoding='cp949')
    loans_df = pd.read_csv(os.path.join(folder_path, '대출정보.txt'), encoding='cp949')
    
    # 2. 연도별 전체 대출량 계산
    loans_df['대출년도'] = pd.to_datetime(loans_df['대출일시']).dt.year
    yearly_total_df = loans_df.groupby('대출년도').size().reset_index(name='전체대출수')
    
    # 3. 도서별 연도별 대출량 계산
    book_yearly_loans = loans_df.groupby(['도서ID', '대출년도']).size().reset_index(name='도서별대출수')
    
    # 4. 연도별 상대적 대출 비율 계산
    book_yearly_loans = book_yearly_loans.merge(
        yearly_total_df,
        on='대출년도',
        how='left'
    )
    book_yearly_loans['상대적대출비율'] = book_yearly_loans['도서별대출수'] / book_yearly_loans['전체대출수']
    
    # 5. 상위 5개 도서 선정 (수정된 부분)
    total_loans_by_book = book_yearly_loans.groupby('도서ID')['도서별대출수'].sum().reset_index()
    top_5_books = total_loans_by_book.nlargest(5, '도서별대출수')['도서ID'].tolist()
    
    # 6. Plotly를 사용한 인터랙티브 시각화
    fig = make_subplots(rows=2, cols=1, 
                       subplot_titles=('연도별 전체 대출량 추이', '상위 대출 도서의 연도별 상대적 대출 비율'))
    
    # 6-1. 연도별 전체 대출량 그래프
    fig.add_trace(
        go.Scatter(x=yearly_total_df['대출년도'], y=yearly_total_df['전체대출수'], 
                  mode='lines+markers', name='전체 대출량'),
        row=1, col=1
    )
    
    # 코로나19 시기 표시
    fig.add_vline(x=2020, line_dash="dash", line_color="red", 
                 annotation_text="코로나19", row=1, col=1)
    
    # 6-2. 상위 5개 도서의 상대적 대출 비율 그래프
    for book_id in top_5_books:
        book_data = book_yearly_loans[book_yearly_loans['도서ID'] == book_id]
        book_name = books_df[books_df['도서ID'] == book_id]['서명'].iloc[0]
        fig.add_trace(
            go.Scatter(x=book_data['대출년도'], y=book_data['상대적대출비율'],
                      mode='lines+markers', name=book_name[:20]+'...'),
            row=2, col=1
        )
    
    # 레이아웃 설정
    fig.update_layout(height=800, width=1200, showlegend=True,
                     title_text="도서관 대출 분석")
    fig.update_xaxes(title_text="연도", row=1, col=1)
    fig.update_xaxes(title_text="연도", row=2, col=1)
    fig.update_yaxes(title_text="대출 건수", row=1, col=1)
    fig.update_yaxes(title_text="상대적 대출 비율", row=2, col=1)
    
    # 그래프 표시
    fig.show()
    
    # 7. 통계 출력
    print("\n=== 연도별 전체 대출량 통계 ===")
    print(yearly_total_df['전체대출수'].describe())
    
    print("\n=== 코로나19 전후 대출량 비교 ===")
    pre_covid = yearly_total_df[yearly_total_df['대출년도'] < 2020]['전체대출수'].mean()
    post_covid = yearly_total_df[yearly_total_df['대출년도'] >= 2020]['전체대출수'].mean()
    print(f"코로나19 이전 평균 대출량: {pre_covid:.0f}")
    print(f"코로나19 이후 평균 대출량: {post_covid:.0f}")
    print(f"감소율: {((pre_covid - post_covid) / pre_covid * 100):.1f}%")

    # 7. 도서별 대출 횟수 (수정된 부분)
    print("\n가장 많이 대출된 도서 Top 5:")
    loan_counts = loans_df['도서ID'].value_counts().reset_index()
    loan_counts.columns = ['도서ID', '대출횟수']
    
    top_loans = pd.merge(
        loan_counts.head(),
        books_df[['도서ID', '서명']],
        on='도서ID'
    )
    
    print(top_loans[['도서ID', '서명', '대출횟수']])

except Exception as e:
    print(f"오류 발생: {e}")