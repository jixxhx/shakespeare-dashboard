import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# -----------------------------------------------------------
# 1. 페이지 설정 (반드시 맨 처음에 와야 함)
# -----------------------------------------------------------
st.set_page_config(page_title="Shakespeare Dashboard by Jihu Park", layout="wide")

# -----------------------------------------------------------
# 2. 사이드바: 제작자 정보 (Jihu Park's Profile)
# -----------------------------------------------------------
with st.sidebar:
    st.title("👨‍💻 Creator Profile")
    st.markdown("**Developed by Jihu Park**")
    st.markdown("Grade 12 | Future Quant/Investor")
    st.info("This dashboard demonstrates my commitment to data-driven risk management.")
    st.divider()

    st.header("⚙️ Risk Control Panel")
    target_per = st.number_input("Historical Avg PER Reference", value=9.31)

# -----------------------------------------------------------
# 3. 메인 타이틀
# -----------------------------------------------------------
st.title("🎭 The Shakespeare Volatility Dashboard")
st.markdown("**Project Owner: Jihu Park**")
st.write("Fiduciary Risk Management System: Automating Discipline through Data.")
st.markdown("---")

# -----------------------------------------------------------
# 4. 데이터 가져오기 & 안전장치 (핵심 수정 부분)
# -----------------------------------------------------------
@st.cache_data
def get_data():
    ticker = "^KS11" # 코스피 지수
    try:
        # auto_adjust=True로 설정하여 데이터 포맷을 통일합니다.
        data = yf.download(ticker, start="2024-01-01", auto_adjust=True, progress=False)
        
        # 데이터가 비어있으면 빈 껍데기를 반환합니다.
        if data.empty:
            return pd.DataFrame()
            
        # 날짜 시간대 정보를 제거합니다 (Plotly 오류 방지)
        data.index = data.index.tz_localize(None)
        return data
    except Exception:
        return pd.DataFrame()

df = get_data()

# [중요] 데이터가 텅 비었는지 확인하는 안전장치
if df is None or df.empty:
    st.error("⚠️ 데이터를 불러오지 못했습니다. 잠시 후 다시 시도해주세요.")
    st.write("Tip: 야후 파이낸스 서버가 일시적으로 응답하지 않을 수 있습니다. 새로고침(F5) 해보세요.")
    st.stop() # 여기서 멈춰서 빨간 에러창이 뜨는 것을 막습니다.

# -----------------------------------------------------------
# 5. 지표 계산 및 시각화
# -----------------------------------------------------------
try:
    # 컬럼 이름이 이중으로 되어있을 경우 정리 (yfinance 최신버전 대응)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # 마지막 가격 가져오기
    last_price = float(df['Close'].iloc[-1])
    prev_price = float(df['Close'].iloc[-2])
    change = last_price - prev_price

    # 상단 지표 표시
    col1, col2, col3 = st.columns(3)
    col1.metric("Current KOSPI", f"{last_price:,.2f}", f"{change:,.2f}")
    col2.metric("Portfolio Status", "Monitoring")
    col3.metric("Discipline Focus", "Humility over Hubris")

    # 차트 그리기
    st.subheader("📉 Market Trend and Exhaustion Analysis")
    fig = go.Figure()

    # 메인 지수 라인
    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df['Close'], 
        name="KOSPI Index", 
        line=dict(color='#1f77b4', width=2)
    ))

    # 8월 22일 숏 진입 시점 (날짜 형식 호환성 강화)
    entry_date = pd.Timestamp("2025-08-22")
    
    # 만약 데이터 기간 내에 해당 날짜가 포함되어 있다면 세로선 표시
    if df.index.min() <= entry_date <= df.index.max():
        fig.add_vline(
            x=entry_date,  # timestamp() * 1000 대신 날짜 객체 자체를 넣는 게 더 안전합니다.
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

except Exception as e:
    st.error(f"예상치 못한 오류가 발생했습니다: {e}")

# -----------------------------------------------------------
# 6. 하단 푸터 (Footer)
# -----------------------------------------------------------
st.markdown("---")
st.caption("© 2025 Jihu Park. All Rights Reserved. | Built with Python & Streamlit for University Application Portfolio.")
st.info("System Note: This dashboard is designed to override psychological bias by providing objective valuation markers and historical risk thresholds.")
