import streamlit as st
import pandas as pd
import webbrowser
import time

# --- إعداد الصفحة ---
st.set_page_config(
    page_title="HaMmE Executive Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- التنسيق الجمالي (CSS بسيط) ---
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    /* تحسين زر البحث */
    div.stButton > button:first-child {
        background-color: #004e98;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# اختيار اللغة
language = st.sidebar.radio("Language / اللغة", ["English", "العربية"])

# النصوص
text = {
    "English": {
        "title": "HaMmE Executive Dashboard 🏥",
        "subtitle": "Advanced Talent Intelligence & Market Scan",
        "sidebar_filters": "🎯 Search Parameters",
        "kpi_saved": "Total Opportunities Saved",
        "kpi_target": "Target Locations",
        "launch_header": "🚀 Launch X-Ray Search",
        "save_header": "📝 Application Tracker (CRM)",
        "save_btn": "💾 Save Opportunity",
        "toast_msg": "Opportunity Saved Successfully!",
        "cluster_ops": "⚡ Operations Bundle",
        "cluster_exec": "⚡ Executive Bundle",
        "cluster_strat": "⚡ Strategy Bundle"
    },
    "العربية": {
        "title": "HaMmE لوحة القيادة التنفيذية 🏥",
        "subtitle": "نظام استخبارات السوق والبحث المتقدم",
        "sidebar_filters": "🎯 معايير البحث",
        "kpi_saved": "إجمالي الفرص المحفوظة",
        "kpi_target": "مناطق الاستهداف",
        "launch_header": "🚀 إطلاق البحث الشعاعي (X-Ray)",
        "save_header": "📝 نظام تتبع الطلبات (CRM)",
        "save_btn": "💾 حفظ الفرصة",
        "toast_msg": "تم حفظ الفرصة بنجاح! 🚀",
        "cluster_ops": "⚡ حزمة: العمليات والتشغيل",
        "cluster_exec": "⚡ حزمة: الإدارة العليا",
        "cluster_strat": "⚡ حزمة: الاستراتيجية"
    }
}
t = text[language]

# --- تحميل البيانات ---
CSV_FILE = "HaMmE_Gold_Data.csv"
if 'search_results' not in st.session_state:
    try:
        st.session_state.search_results = pd.read_csv(CSV_FILE)
    except:
        st.session_state.search_results = pd.DataFrame(columns=["Title", "Company", "Link", "Notes", "Date"])

# --- لوحة المؤشرات (KPIs) ---
st.title(t["title"])
st.caption(t["subtitle"])
st.divider()

# عرض إحصائيات سريعة (Visual Appeal)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label=t["kpi_saved"], value=len(st.session_state.search_results), delta="+1 New")
with col2:
    st.metric(label="System Status", value="Active", delta="Online")
with col3:
    st.metric(label=t["kpi_target"], value="7 Emirates")

st.divider()

# --- القوائم والبحث ---
emirates = ["Abu Dhabi", "Al Ain", "Dubai", "Sharjah", "Ajman", "UAE"]
job_options = [
    t["cluster_ops"], t["cluster_exec"], t["cluster_strat"],
    "Clinic Manager", "Operations Director", "General Manager Healthcare", 
    "Patient Experience Manager", "Business Development Manager"
]
platforms = {
    "All Platforms": "(site:linkedin.com/jobs OR site:bayt.com OR site:naukrigulf.com)",
    "LinkedIn": "site:linkedin.com/jobs",
    "Indeed": "site:ae.indeed.com"
}

# Sidebar
st.sidebar.header(t["sidebar_filters"])
selected_locs = st.sidebar.multiselect("Location", emirates, default=["Abu Dhabi", "Al Ain"])
selected_job = st.sidebar.selectbox("Role Strategy", job_options)
selected_platform = st.sidebar.selectbox("Platform", list(platforms.keys()))
freshness = st.sidebar.select_slider("Job Freshness", options=["Any", "Month", "Week", "24h"], value="Week")
fresh_map = {"Any": "", "Month": "m", "Week": "w", "24h": "d"}

# منطق البحث
if selected_job == t["cluster_ops"]:
    keywords = '("Clinic Manager" OR "Operations Director" OR "Medical Center Manager")'
elif selected_job == t["cluster_exec"]:
    keywords = '("General Manager" OR "CEO" OR "Managing Director")'
elif selected_job == t["cluster_strat"]:
    keywords = '("Strategy" OR "Business Development" OR "Quality")'
else:
    keywords = f'"{selected_job}"'

loc_str = " OR ".join([f'"{loc}"' for loc in selected_locs])
exclusions = '-"Nurse" -"Technician" -"Assistant"'
query = f'{platforms[selected_platform]} {keywords} ({loc_str}) {exclusions}'
google_url = f"https://www.google.com/search?q={query}&tbs=qdr:{fresh_map[freshness]}"

# زر البحث
st.subheader(t["launch_header"])
if st.button(f"🔍 {t['title'].split()[0]} SEARCH"):
    webbrowser.open(google_url)
    st.toast("Opening Search Engine...", icon="🔍")
    time.sleep(1)
    st.markdown(f"**Direct Link:** [Click Here]({google_url})")

# --- CRM ---
st.subheader(t["save_header"])
with st.expander("Add New Opportunity ⬇️", expanded=True):
    with st.form("save_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        j_title = c1.text_input("Job Title", value=selected_job if "⚡" not in selected_job else "")
        j_company = c2.text_input("Company Name")
        j_link = st.text_input("Link")
        j_notes = st.text_area("Strategic Notes")
        
        if st.form_submit_button(t["save_btn"]):
            new_row = pd.DataFrame({
                "Title": [j_title], "Company": [j_company], 
                "Link": [j_link], "Notes": [j_notes],
                "Date": [pd.Timestamp.now()]
            })
            st.session_state.search_results = pd.concat([st.session_state.search_results, new_row], ignore_index=True)
            st.session_state.search_results.to_csv(CSV_FILE, index=False)
            st.toast(t["toast_msg"], icon="✅") # رسالة جمالية
            time.sleep(0.5)
            st.rerun() # تحديث الصفحة لتظهر الأرقام الجديدة

# عرض الجدول
st.dataframe(
    st.session_state.search_results, 
    use_container_width=True,
    column_config={
        "Link": st.column_config.LinkColumn("Apply Link")
    }
)
