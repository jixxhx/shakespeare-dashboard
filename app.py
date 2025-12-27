import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(page_title="Shakespeare Dashboard", layout="wide")
st.title("🎭 The Shakespeare Volatility Dashboard")
st.write("Fiduciary Risk Management System: Automating Discipline through Data.")

# 2. 데이터 가져오기
@st.cache_data
def get_data():
    ticker = "^KS11"
    # 데이터를 가져온 후 인덱스(날짜)의 시간대 정보를 제거하여 오류 방지
    data = yf.download(ticker, start="2024-01-01")
    data.index = data.index.tz_localize(None)
    return data

df = get_data()

# 3. 사이드바 설정 (포트폴리오 논리 반영)
st.sidebar.header("Risk Control Panel")
target_per = st.sidebar.number_input("Historical Avg PER Reference", value=9.31)

# 4. 상단 지표 계산
last_price = float(df['Close'].iloc[-1])
prev_price = float(df['Close'].iloc[-2])
change = last_price - prev_price

col1, col2, col3 = st.columns(3)
col1.metric("Current KOSPI", f"{last_price:,.2f}", f"{change:,.2f}")
col2.metric("Portfolio Status", "Monitoring")
col3.metric("Discipline Focus", "Humility over Hubris")

# 5. 차트 시각화 (KOSPI Index)
st.subheader("Market Trend and Exhaustion Analysis")
fig = go.Figure()

# 메인 지수 라인
fig.add_trace(go.Scatter(
    x=df.index, 
    y=df['Close'].values.flatten(), 
    name="KOSPI Index", 
    line=dict(color='#1f77b4', width=2)
))

# [핵심] 8월 22일 숏 진입 시점 표시 (빨간색 점선)
entry_date = pd.Timestamp("2025-08-22")
fig.add_vline(
    x=entry_date.timestamp() * 1000, 
    line_dash="dot", 
    line_color="red", 
    annotation_text="Aug 22 Case Study Entry",
    annotation_position="top left"
)

# [핵심] 9.31 PER 기준선 추가 (초록색 실선)
# 포트폴리오에서 언급한 가치 평가의 평형점(Equilibrium) 시각화
fig.add_hline(
    y=3100, 
    line_dash="solid", 
    line_color="green", 
    annotation_text="9.31 PER Equilibrium (Approx.)",
    annotation_position="bottom right"
)

# 차트 레이아웃 최적화
fig.update_layout(
    xaxis_title="Date", 
    yaxis_title="Price (Index)", 
    hovermode="x unified",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# 하단 메시지 (에세이 서사 연결)
st.info("System Note: This dashboard is designed to override psychological bias by providing objective valuation markers and historical risk thresholds.")