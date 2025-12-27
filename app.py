import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(page_title="Shakespeare Dashboard by Jihu Park", layout="wide")

# 2. [추가됨] 사이드바: 제작자 정보 표시 (가장 눈에 잘 띔)
with st.sidebar:
    st.title("👨‍💻 Creator Profile")
    st.markdown("**Developed by Jihu Park**")
    st.markdown("Grade 12 | Future Quant/Investor")
    st.info("This dashboard demonstrates my commitment to data-driven risk management.")
    st.divider() # 구분선

    # 기존 리스크 설정 패널
    st.header("⚙️ Risk Control Panel")
    target_per = st.number_input("Historical Avg PER Reference", value=9.31)

# 메인 타이틀
st.title("🎭 The Shakespeare Volatility Dashboard")
st.markdown("**Project Owner: Jihu Park**") # [추가됨] 제목 바로 아래 이름 표시
st.write("Fiduciary Risk Management System: Automating Discipline through Data.")
st.markdown("---") # 구분선 추가

# 3. 데이터 가져오기
@st.cache_data
def get_data():
    ticker = "^KS11"
    data = yf.download(ticker, start="2024-01-01")
    data.index = data.index.tz_localize(None)
    return data

df = get_data()

# 4. 상단 지표 계산
last_price = float(df['Close'].iloc[-1])
prev_price = float(df['Close'].iloc[-2])
change = last_price - prev_price

col1, col2, col3 = st.columns(3)
col1.metric("Current KOSPI", f"{last_price:,.2f}", f"{change:,.2f}")
col2.metric("Portfolio Status", "Monitoring")
col3.metric("Discipline Focus", "Humility over Hubris")

# 5. 차트 시각화
st.subheader("📉 Market Trend and Exhaustion Analysis")
fig = go.Figure()

# 메인 지수 라인
fig.add_trace(go.Scatter(
    x=df.index, 
    y=df['Close'].values.flatten(), 
    name="KOSPI Index", 
    line=dict(color='#1f77b4', width=2)
))

# 8월 22일 숏 진입 시점
entry_date = pd.Timestamp("2025-08-22")
fig.add_vline(
    x=entry_date.timestamp() * 1000, 
    line_dash="dot", 
    line_color="red", 
    annotation_text="Aug 22 Case Study Entry",
    annotation_position="top left"
)

# 9.31 PER 기준선
fig.add_hline(
    y=3100, 
    line_dash="solid", 
    line_color="green", 
    annotation_text="9.31 PER Equilibrium (Approx.)",
    annotation_position="bottom right"
)

fig.update_layout(
    xaxis_title="Date", 
    yaxis_title="Price (Index)", 
    hovermode="x unified",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# 6. [추가됨] 하단 저작권 표시 (Footer)
st.markdown("---")
st.caption("© 2025 Jihu Park. All Rights Reserved. | Built with Python & Streamlit for University Application Portfolio.")
st.info("System Note: This dashboard is designed to override psychological bias by providing objective valuation markers and historical risk thresholds.")
