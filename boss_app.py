import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# [1] 페이지 기본 설정
# ---------------------------------------------------------
st.set_page_config(page_title="실시간 보스 알리미", page_icon="🔥", layout="centered")

# ---------------------------------------------------------
# [2] 데이터 연동 설정
# ---------------------------------------------------------
# 봇이 갱신하고 있는 실시간 보스 시트의 CSV 주소
LIVE_BOSS_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTkGZax4hdu1ufWEFPIRWhLyKCUs33tLBAvHNCFe9jxZIkFBKPY0fZDeoTnBA28Dro2xbK1sGFNqhA7/pub?gid=1043308785&single=true&output=csv"

@st.cache_data(ttl=10) # 10초마다 데이터를 새로 읽어옵니다.
def load_live_bosses():
    try:
        return pd.read_csv(LIVE_BOSS_CSV_URL)
    except Exception:
        return pd.DataFrame()

df_live = load_live_bosses()

# ---------------------------------------------------------
# [3] 화면 구성
# ---------------------------------------------------------
st.title("🔥 크라켄서버 실시간 보스 현황판")
st.markdown("---")

if not df_live.empty:
    # 1행 3열에 있는 '업데이트 시간'을 가져옵니다.
    update_time = df_live.iloc[0, 2] if len(df_live.columns) > 2 else "알 수 없음"
    st.caption(f"⏱️ 마지막 서버 확인 시간: {update_time} (10초마다 자동 갱신)")
    
    # 봇이 보스가 없다고 기록한 경우
    if "생존한 보스가 없습니다" in str(df_live.iloc[0, 0]):
        st.success("✨ **현재 출몰한 보스가 없습니다. 평화롭네요!**")
        st.image("https://cdn-icons-png.flaticon.com/512/3003/3003280.png", width=150) # 평화로운 아이콘 (원하시면 삭제 가능)
    else:
        # 보스가 생존한 경우
        st.error(f"🚨 **비상! 현재 총 {len(df_live)}마리의 보스가 생존해 있습니다!**")
        
        # 보기 깔끔하게 시간 컬럼은 빼고 보스명과 맵만 보여줍니다.
        display_df = df_live[["생존 보스", "출몰 맵"]]
        
        # 표를 조금 더 크고 예쁘게 출력
        st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.warning("⚠️ 보스 정보를 불러오는 중이거나 봇이 꺼져있습니다.")

st.markdown("---")
st.markdown("💡 *이 페이지를 켜두시면 실시간 생존 현황을 파악할 수 있습니다.*")
