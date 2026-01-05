import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# -----------------------------------------------------------
# 1. 페이지 설정
# -----------------------------------------------------------
st.set_page_config(page_title="Shakespeare Dashboard by Jihu Park", layout="wide")

# -----------------------------------------------------------
# 2. 사이드바
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
# 4. 데이터 가져오기 (SPY 자동 대체 기능 포함)
# -----------------------------------------------------------
@st.cache_data(ttl=600)
def get_data():
    # 1차 시도: KOSPI
    try:
        ticker = "^KS11"
        data = yf.download(ticker, start="2024-01-01", auto_adjust=True, progress=False)
        if not data.empty:
            data.index = data.index.tz_localize(None)
            return data, "KOSPI"
    except Exception:
        pass

    # 2차 시도: SPY (KOSPI 실패 시)
    try:
        data = yf.download("SPY", start="2024-01-01", auto_adjust=True, progress=False)
        if not data.empty:
            data.index = data.index.tz_localize(None)
            return data, "SPY"
    except Exception:
        pass
        
    return pd.DataFrame(), "None"

df, source = get_data()

# 데이터 로드 실패 시 중단
if df is None or df.empty:
    st.error("⚠️ 데이터를 불러오지 못했습니다. (야후 파이낸스 서버 오류)")
    st.stop()

# -----------------------------------------------------------
# 5. 지표 계산 및 시각화
# -----------------------------------------------------------
try:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    last_price = float(df['Close'].iloc[-1])
    prev_price = float(df['Close'].iloc[-2])
    change = last_price - prev_price

    col1, col2, col3 = st.columns(3)
    col1.metric("Current Market", f"{last_price:,.2f}", f"{change:,.2f}")
    col2.metric("Portfolio Status", "Monitoring")
    col3.metric("Discipline Focus", "Humility over Hubris")

    st.subheader("📉 Market Trend and Exhaustion Analysis")
    
    # 차트 그리기
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df['Close'], 
        name=f"{source} Index", 
        line=dict(color='#1f77b4', width=2)
    ))

    # [핵심 수정] 날짜를 숫자로 변환해서 넣어야 Pandas 2.0 에러가 안 남!
    entry_date = pd.Timestamp("2025-08-22")
    
    # 차트에 표시될 범위 안에 날짜가 있을 때만 선 그리기
    if df.index.min() <= entry_date <= df.index.max():
        fig.add_vline(
            x=entry_date.timestamp() * 1000,  # <-- 여기를 숫자로 변환 (에러 해결!)
            line_dash="dot", 
            line_color="red", 
            annotation_text="Aug 22 Case Study Entry",
            annotation_position="top left"
        )

    fig.add_hline(
        y=3100 if source == "KOSPI" else 5800, # SPY일 경우 기준선 조정
        line_dash="solid", 
        line_color="green", 
        annotation_text="Valuation Equilibrium",
        annotation_position="bottom right"
    )

    fig.update_layout(
        xaxis_title="Date", 
        yaxis_title="Price", 
        hovermode="x unified",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"차트 생성 중 오류가 발생했습니다: {e}")

# -----------------------------------------------------------
# 6. 푸터
# -----------------------------------------------------------
st.markdown("---")
st.info("System Note: This dashboard is designed to override psychological bias.")
if source == "SPY":
    st.toast("KOSPI 데이터 지연으로 인해 SPY 데이터로 대체되었습니다.", icon="ℹ️")
