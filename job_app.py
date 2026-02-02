import streamlit as st
import pandas as pd
import webbrowser
from datetime import datetime

# --- إعداد الصفحة ---
st.set_page_config(
    page_title="HaMmE Executive Search",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 🎨 نظام الثيمات (Theme Engine) ---
# هذا الجزء يسمح لك بتغيير شكل التطبيق فوراً
themes = {
    "👑 Royal Executive (فخم)": """
        <style>
        .stApp {background-color: #f8f9fa;}
        div[data-testid="stSidebar"] {background-color: #0f172a;}
        h1, h2, h3 {color: #0f172a !important; font-family: 'Segoe UI', serif;}
        .stButton>button {
            background: linear-gradient(90deg, #1e3a8a 0%, #1e40af 100%);
            color: white; border: none; border-radius: 8px; height: 50px; font-size: 18px;}
        .metric-card {background: white; border-left: 5px solid #d4af37; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
        div[data-testid="stExpander"] {border: 1px solid #e2e8f0; border-radius: 8px;}
        </style>
    """,
    "❄️ Modern Minimalist (نظيف)": """
        <style>
        .stApp {background-color: #ffffff;}
        div[data-testid="stSidebar"] {background-color: #f1f5f9;}
        h1, h2, h3 {color: #334155 !important; font-weight: 300;}
        .stButton>button {
            background-color: #0f766e; color: white; border-radius: 20px; border: none;}
        .metric-card {background: #f8fafc; border: 1px solid #e2e8f0;}
        </style>
    """,
    "🌃 Cyber Dashboard (ليلي)": """
        <style>
        .stApp {background-color: #0e1117;}
        div[data-testid="stSidebar"] {background-color: #262730;}
        h1, h2, h3 {color: #00ff9d !important;}
        .stButton>button {
            background: transparent; border: 2px solid #00ff9d; color: #00ff9d; border-radius: 0px;}
        .stButton>button:hover {background: #00ff9d; color: black;}
        .metric-card {background: #1f1f1f; border: 1px solid #333;}
        p, label {color: #e0e0e0 !important;}
        </style>
    """
}

# --- القائمة الجانبية: إعدادات المظهر واللغة ---
st.sidebar.header("🎨 Interface Settings")
selected_theme_name = st.sidebar.selectbox("Choose Theme / اختر الواجهة", list(themes.keys()))
st.markdown(themes[selected_theme_name], unsafe_allow_html=True) # تطبيق الثيم المختار
st.sidebar.divider()

language = st.sidebar.radio("Language / اللغة", ["English", "العربية"])

# --- النصوص والترجمة ---
text = {
    "English": {
        "title": "HaMmE Executive Suite",
        "subtitle": "Advanced Healthcare Leadership Intelligence",
        "tab1": "🔍 Market Scan",
        "tab2": "⚡ Action Center",
        "tab3": "🎤 Interview Prep",
        "tab4": "📊 CRM Tracker",
        "sidebar_title": "🎯 Search Parameters",
        "loc_label": "Target Locations",
        "job_label": "Target Role",
        "freshness_label": "Job Freshness (Posting Date)",
        "freshness_opts": ["Any Time", "Past Month", "Past Week", "Past 24 Hours"],
        "plat_label": "Search Platform",
        "btn_search": "🚀 Launch Strategic Search",
        "cover_head": "📝 Instant Cover Letter",
        "net_head": "🤝 Networking Message",
        "prep_head": "🛡️ Interview War Room",
        "save_btn": "💾 Save to CRM",
        "download_btn": "📥 Export Report (Excel)",
        "cl_template": "Dear Hiring Team at {company},\n\nI am writing to express my strong interest in the {role} position. With over 14 years of leadership experience in the UAE healthcare sector (Al Ain/Abu Dhabi), specifically in managing multi-specialty and aesthetic clinics, I am confident in my ability to drive operational excellence at {company}.\n\nSincerely,\nHaitham El-Meslemani",
        "net_template": "Hi [Name],\n\nI noticed the {role} opening at {company}. Given my 14 years in UAE healthcare operations, I see great alignment with your goals. Would love to connect.\n\nBest,\nHaitham"
    },
    "العربية": {
        "title": "HaMmE الجناح التنفيذي",
        "subtitle": "نظام استخبارات القيادة الصحية المتقدم",
        "tab1": "🔍 مسح السوق",
        "tab2": "⚡ مركز الإجراءات",
        "tab3": "🎤 غرفة المقابلات",
        "tab4": "📊 سجل المتابعة",
        "sidebar_title": "🎯 معايير البحث",
        "loc_label": "المناطق المستهدفة",
        "job_label": "المنصب المستهدف",
        "freshness_label": "حداثة الوظيفة (تاريخ النشر)",
        "freshness_opts": ["أي وقت", "آخر شهر", "آخر أسبوع", "آخر 24 ساعة"],
        "plat_label": "منصة البحث",
        "btn_search": "🚀 إطلاق البحث الاستراتيجي",
        "cover_head": "📝 رسالة تغطية فورية",
        "net_head": "🤝 رسالة تعارف",
        "prep_head": "🛡️ غرفة عمليات المقابلات",
        "save_btn": "💾 حفظ في السجل",
        "download_btn": "📥 تصدير التقرير (Excel)",
        "cl_template": "السادة في {company}،\n\nأتقدم بطلب لمنصب {role}. خبرتي التي تتجاوز 14 عاماً في إدارة العيادات والمراكز الطبية في الإمارات (العين/أبوظبي) تؤهلني لتحقيق نقلة نوعية في عملياتكم التشغيلية.\n\nتحياتي،\nهيثم المسلماني",
        "net_template": "مرحباً [الاسم]،\n\nلفتت انتباهي فرصة {role} في {company}. بحكم خبرتي الطويلة في إدارة العيادات في الدولة، أرى تقاطعاً كبيراً في الأهداف ويسعدني التواصل معك.\n\nتحياتي،\nهيثم"
    }
}
t = text[language]

# --- البيانات والقوائم (الكاملة) ---
emirates = [
    "Abu Dhabi", "Al Ain", "Dubai", "Sharjah", 
    "Ajman", "Umm Al Quwain", "Ras Al Khaimah", "Fujairah", "UAE"
]

# قائمة الوظائف (الحزم + القائمة الكاملة)
job_roles = [
    "⚡ Operations Bundle (Clinic/Ops Manager)",
    "⚡ Executive Bundle (GM/Director)",
    "⚡ Strategy Bundle (Bus. Dev/Quality)",
    "--- Individual Roles / مسميات فردية ---",
    "General Manager Healthcare", "Managing Director Healthcare", "Regional Operations Manager Healthcare",
    "Operations Director Clinic", "Operations Director Aesthetics", "Operations Manager",
    "Clinic Manager", "Senior Clinic Manager", "Clinic Supervisor", "Clinic Operations Manager",
    "Clinic Performance & Growth Manager", "Healthcare Operations Manager", "Healthcare Administrator",
    "Healthcare Facility Manager", "Healthcare Manager", "Healthcare Strategy Manager",
    "Healthcare Quality Manager", "Healthcare Projects Manager", "Healthcare Services Manager",
    "Polyclinic Manager", "Medical Operations Manager", "Medical Manager", "Medical Administration Manager",
    "Medical Center Manager", "Medical Center Development Manager", "Aesthetic Clinic Manager",
    "Aesthetic Business Development Manager", "Aesthetic Operations Manager", "Medical Aesthetics Operations Manager",
    "Dermatology Clinic Manager", "Derma & Laser Center Manager", "Laser Center Manager",
    "Cosmetic Center Manager", "Cosmetic Clinic Operations Manager", "Business Development Manager Healthcare",
    "Business Development Manager Aesthetics", "Business Operations Manager Clinics",
    "Strategy and Growth Manager", "Patient Experience Manager", "Patient Experience Leadership"
]

platforms = {
    "All Platforms (Unified)": "(site:linkedin.com/jobs OR site:bayt.com OR site:naukrigulf.com OR site:ae.indeed.com OR site:gulftalent.com)",
    "LinkedIn Jobs": "site:linkedin.com/jobs",
    "Bayt": "site:bayt.com",
    "Naukri Gulf": "site:naukrigulf.com",
    "Indeed UAE": "site:ae.indeed.com",
    "Gulf Talent": "site:gulftalent.com",
    "Glassdoor": "site:glassdoor.com",
    "Google Jobs": "site:google.com/search/about/jobs"
}

# --- بنك أسئلة المقابلات ---
interview_intel = {
    "Clinic Manager / Operations": {
        "Qs": ["كيف تدير التوازن بين رضا المرضى وضغط التكاليف؟", "حدثنا عن مشكلة تنظيمية (DOH) واجهتها؟", "كيف تتعامل مع الأطباء ذوي الدخل العالي عند الخلاف؟", "استراتيجيتك لرفع نسبة عودة المرضى؟", "كيف تدير مخزون المواد باهظة الثمن؟"],
        "Keys": "Patient Experience, Revenue Cycle, Cost Optimization, Compliance"
    },
    "General Manager / Executive": {
        "Qs": ["كيف تبني ثقافة ولاء في المؤسسة؟", "أسلوبك في إدارة الـ P&L والخسائر؟", "رؤيتك للتحول الرقمي؟", "كيف تدير العلاقة مع الملاك/المستثمرين؟", "خطة التوسع لـ 5 سنوات؟"],
        "Keys": "P&L Management, Stakeholder Mgmt, Scalability, Governance"
    }
}

# --- حالة التطبيق (Session State) ---
if 'search_results' not in st.session_state:
    st.session_state.search_results = pd.DataFrame(columns=["Title", "Company", "Status", "Notes", "Date"])

# --- الواجهة الرئيسية ---
st.title(t["title"])
st.caption(t["subtitle"])

tab1, tab2, tab3, tab4 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"]])

# ================= TAB 1: SEARCH (محرك البحث) =================
with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"### {t['sidebar_title']}")
        # 1. Location
        sel_loc = st.multiselect(t["loc_label"], emirates, default=["Abu Dhabi", "Al Ain", "UAE"])
        
        # 2. Platform
        sel_plat_name = st.selectbox(t["plat_label"], list(platforms.keys()))
        
        # 3. Freshness (Radio Buttons now)
        sel_fresh_name = st.radio(t["freshness_label"], t["freshness_opts"], index=0)
        
    with col2:
        # 4. Role
        st.write(" ") # Spacer
        st.write(" ")
        sel_role = st.selectbox(t["job_label"], job_roles)
        
        # المنطق البرمجي للبحث
        fresh_map = {
            "Any Time": "", "أي وقت": "",
            "Past Month": "m", "آخر شهر": "m",
            "Past Week": "w", "آخر أسبوع": "w",
            "Past 24 Hours": "d", "آخر 24 ساعة": "d"
        }
        time_code = fresh_map.get(sel_fresh_name, "")
        
        # معالجة المسميات الوظيفية
        if "Operations Bundle" in sel_role: query_keywords = '("Clinic Manager" OR "Operations Director" OR "Center Manager")'
        elif "Executive Bundle" in sel_role: query_keywords = '("General Manager" OR "CEO" OR "Managing Director")'
        elif "Strategy Bundle" in sel_role: query_keywords = '("Business Development" OR "Strategy Manager")'
        elif "---" in sel_role: query_keywords = '"Clinic Manager"' # Fallback
        else: query_keywords = f'"{sel_role}"'
        
        loc_query = " OR ".join([f'"{l}"' for l in sel_loc])
        site_op = platforms[sel_plat_name]
        
        final_query = f'{site_op} {query_keywords} ({loc_query}) -"Nurse" -"Technician"'
        google_url = f"https://www.google.com/search?q={final_query}&tbs=qdr:{time_code}"
        
        st.markdown("---")
        if st.button(t["btn_search"]):
            webbrowser.open(google_url)
            st.success(f"Searching for: {sel_role} in {', '.join(sel_loc)}")
            st.markdown(f"**[Click here to open results manually]({google_url})**")

# ================= TAB 2: ACTIONS (الإجراءات) =================
with tab2:
    st.header(t["tab2"])
    c1, c2 = st.columns(2)
    with c1:
        st.subheader(t["cover_head"])
        cl_comp = st.text_input("Company Name", key="cl_c")
        cl_role = st.text_input("Job Title", key="cl_r")
        if cl_comp and cl_role:
            st.text_area("Result", t["cl_template"].format(company=cl_comp, role=cl_role), height=200)
    with c2:
        st.subheader(t["net_head"])
        if cl_comp and cl_role:
            st.code(t["net_template"].format(company=cl_comp, role=cl_role), language="text")

# ================= TAB 3: INTERVIEW (المقابلات) =================
with tab3:
    st.header(t["prep_head"])
    cat = st.selectbox("Select Role Category", list(interview_intel.keys()))
    data = interview_intel[cat]
    
    st.info(f"🔑 Keywords: {data['Keys']}")
    for i, q in enumerate(data['Qs'], 1):
        st.markdown(f"**{i}.** {q}")

# ================= TAB 4: CRM (السجل) =================
with tab4:
    st.header(t["tab4"])
    with st.expander("➕ Add New Opportunity", expanded=True):
        with st.form("crm_form"):
            c1, c2, c3 = st.columns(3)
            f_tit = c1.text_input("Role")
            f_com = c2.text_input("Company")
            f_sta = c3.selectbox("Status", ["Applied", "Interview", "Offer", "Rejected"])
            f_not = st.text_area("Notes")
            
            if st.form_submit_button(t["save_btn"]):
                new_row = pd.DataFrame({
                    "Title": [f_tit], "Company": [f_com], "Status": [f_sta],
                    "Notes": [f_not], "Date": [datetime.now().strftime("%Y-%m-%d")]
                })
                st.session_state.search_results = pd.concat([st.session_state.search_results, new_row], ignore_index=True)
                st.success("Saved!")
                st.rerun()
    
    st.dataframe(st.session_state.search_results, use_container_width=True)
    
    csv = st.session_state.search_results.to_csv(index=False).encode('utf-8')
    st.download_button(t["download_btn"], csv, "HaMmE_Report.csv", "text/csv")
