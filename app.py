import streamlit as st
import google.generativeai as genai

# --- ตั้งค่าหน้าตาแอปแบบ Minimal Professional ---
st.set_page_config(page_title="Siam Energy AI", layout="centered")

st.markdown("# 🌐 Siam Energy Intelligence")
st.markdown("### ระบบติดตามสถานการณ์และวิเคราะห์วิกฤตพลังงานไทย")
st.write("โดย: บริษัทสยามภัณฑ์ที่ปรึกษา - สนับสนุนภารกิจกระทรวงพลังงาน")
st.markdown("---")

# --- การดึง API Key จากระบบความปลอดภัย ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.warning("กรุณาติดตั้งระบบความปลอดภัย (Secrets) ก่อนใช้งาน")
    st.stop()

# --- กฎเหล็กของ AI (System Instruction) อัปเดตพิเศษ ---
instruction = """
คุณคือที่ปรึกษาเชิงกลยุทธ์ของบริษัทสยามภัณฑ์ ทำงานร่วมกับกระทรวงพลังงาน
หน้าที่: วิเคราะห์ข่าวและกระแสสังคมเกี่ยวกับวิกฤตพลังงานในไทย
กฎ:
1. ต้องใช้เครื่องมือ Google Search ทุกครั้งก่อนตอบ
2. บังคับหาข้อมูลจาก: ประชาชาติธุรกิจ (Prachachat.net), ฐานเศรษฐกิจ, กรุงเทพธุรกิจ เป็นลำดับแรก
3. สรุปรายงานเป็น 3 ส่วน: (1) สถานการณ์สด (2) กระแสวิจารณ์ในโซเชียล (3) ข้อเสนอแนะต่อกระทรวง
4. ทุกข่าวต้องมี Link อ้างอิงชัดเจน
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=instruction
)

# --- ส่วนช่องค้นหา ---
with st.form("search_form"):
    user_query = st.text_input("ระบุประเด็นที่ต้องการวิเคราะห์:", placeholder="เช่น กระแสค่าไฟ, วิกฤตน้ำมันดีเซลวันนี้")
    submit = st.form_submit_button("วิเคราะห์ข้อมูล Real-time")

if submit and user_query:
    with st.spinner('กำลังเจาะลึกฐานข้อมูลข่าวสาร...'):
        try:
            # สั่งให้ AI ใช้เครื่องมือค้นหา Google
            response = model.generate_content(
                user_query, 
                tools=[{'google_search_retrieval': {}}]
            )
            st.markdown("#### 📄 บทวิเคราะห์โดย Siam Energy AI")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดในการดึงข้อมูล: {e}")

st.markdown("---")
st.caption("© 2026 Siamphan Advisory Group. Confidential & Professional Intelligence.")
