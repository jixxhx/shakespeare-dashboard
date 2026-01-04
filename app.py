# 3. 데이터 가져오기
@st.cache_data
def get_data():
    ticker = "^KS11"
    # [수정팁] auto_adjust=True를 넣으면 데이터 구조가 더 깔끔해져서 에러가 줄어듭니다.
    data = yf.download(ticker, start="2024-01-01", auto_adjust=True)
    
    # 데이터가 비어있을 경우를 대비해 예외 처리
    if data.empty:
        return pd.DataFrame() # 빈 껍데기 반환
        
    data.index = data.index.tz_localize(None)
    return data

df = get_data()

# [핵심 수정] 데이터가 텅 비었는지(Empty) 먼저 검사합니다.
if df.empty:
    st.error("⚠️ 데이터를 불러올 수 없습니다. 인터넷 연결을 확인하거나 잠시 후 다시 시도해주세요.")
    st.write("Debug Info: Yahoo Finance에서 데이터를 받아오지 못했습니다.")
    st.stop() # 여기서 코드 실행을 멈춰서 빨간 에러창을 방지합니다.

# 4. 상단 지표 계산 (데이터가 있을 때만 실행됨)
try:
    # yfinance 버전에 따라 컬럼 형태가 다를 수 있어 안전하게 처리
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

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
        y=df['Close'], # .values.flatten() 없이 바로 넣는 게 더 안전합니다
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

except Exception as e:
    st.error(f"차트를 그리는 중 오류가 발생했습니다: {e}")
