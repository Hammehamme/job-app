import streamlit as st
import pandas as pd
import webbrowser

# --- إعداد الصفحة ---
st.set_page_config(page_title="HaMmE Executive Search Pro", layout="wide")

# اختيار اللغة
language = st.sidebar.radio("Language / اللغة", ["English", "العربية"])

# النصوص والترجمة
text = {
    "English": {
        "title": "🏥 HaMmE Executive Search (Pro Edition)",
        "sidebar_filters": "1. Search Intelligence",
        "loc_label": "Target Location:",
        "job_label": "Select Job Strategy:",
        "platform_label": "Source:",
        "time_label": "Posting Date (Freshness):",
        "time_options": {"Any time": "", "Past 24 Hours": "d", "Past Week": "w", "Past Month": "m"},
        "launch_header": "🚀 Launch Precision Search",
        "launch_desc": "Searching for:",
        "btn_label": "🔍 Find Jobs (Google X-Ray)",
        "save_header": "📝 Opportunity Tracker (CRM)",
        "save_btn": "Save to List",
        "col_title": "Job Title",
        "col_company": "Company",
        "col_link": "Link",
        "col_notes": "Notes",
        "success_save": "Saved successfully!",
        "success_open": "Results opened! Check the new tab.",
        "cluster_exec": "⚡ BUNDLE: Top Executive (GM/Director)",
        "cluster_ops": "⚡ BUNDLE: Operations & Management",
        "cluster_strat": "⚡ BUNDLE: Strategy & Growth"
    },
    "العربية": {
        "title": "🏥 HaMmE غرفة عمليات البحث الاحترافي",
        "sidebar_filters": "1. ذكاء البحث",
        "loc_label": "الموقع الجغرافي:",
        "job_label": "اختر استراتيجية البحث:",
        "platform_label": "المصدر:",
        "time_label": "تاريخ النشر (حداثة الوظيفة):",
        "time_options": {"أي وقت": "", "آخر 24 ساعة": "d", "آخر أسبوع": "w", "آخر شهر": "m"},
        "launch_header": "🚀 إطلاق البحث الدقيق",
        "launch_desc": "جاري البحث عن:",
        "btn_label": "🔍 ابحث الآن (Google X-Ray)",
        "save_header": "📝 سجل متابعة الفرص (CRM)",
        "save_btn": "حفظ في القائمة",
        "col_title": "المسمى الوظيفي",
        "col_company": "الشركة",
        "col_link": "رابط الوظيفة",
        "col_notes": "ملاحظات",
        "success_save": "تم الحفظ بنجاح!",
        "success_open": "تم فتح النتائج! تفحص اللسان الجديد.",
        "cluster_exec": "⚡ حزمة: القيادة العليا (مدير عام/تنفيذي)",
        "cluster_ops": "⚡ حزمة: التشغيل والإدارة (مدير عيادة/عمليات)",
        "cluster_strat": "⚡ حزمة: الاستراتيجية والنمو (تطوير أعمال)"
    }
}

t = text[language]

st.title(t["title"])

# --- البيانات ---
emirates = [
    "Abu Dhabi", "Al Ain", "Dubai", "Sharjah", "Ajman", 
    "Umm Al Quwain", "Ras Al Khaimah", "Fujairah", "UAE"
]

# القوائم الذكية (Clusters)
exec_bundle = '"General Manager" OR "Managing Director" OR "CEO" OR "Regional Director"'
ops_bundle = '"Clinic Manager" OR "Operations Director" OR "Operations Manager" OR "Medical Center Manager" OR "Practice Manager" OR "Polyclinic Manager"'
strat_bundle = '"Business Development Manager" OR "Strategy Manager" OR "Patient Experience Manager" OR "Quality Manager" OR "Healthcare Administrator"'

# قائمة المسميات (تدمج الحزم مع المسميات الفردية)
job_options = [
    t["cluster_ops"],   # الأولوية للتشغيل
    t["cluster_exec"],  # ثم القيادة
    t["cluster_strat"], # ثم الاستراتيجية
    "--- Individual Titles / مسميات فردية ---",
    "Clinic Manager", "Operations Director", "General Manager Healthcare", 
    "Medical Director", "Healthcare Administrator", "Patient Experience Manager",
    "Business Development Manager", "Aesthetic Clinic Manager", "Dermatology Clinic Manager"
]

platforms = {
    "All Platforms (Unified)": "(site:linkedin.com/jobs OR site:bayt.com OR site:naukrigulf.com OR site:ae.indeed.com OR site:gulftalent.com)",
    "LinkedIn Jobs": "site:linkedin.com/jobs",
    "Bayt": "site:bayt.com",
    "Naukri Gulf": "site:naukrigulf.com",
    "Indeed AE": "site:ae.indeed.com"
}

# --- القائمة الجانبية (Sidebar) ---
st.sidebar.header(t["sidebar_filters"])

selected_locs = st.sidebar.multiselect(t["loc_label"], emirates, default=["Abu Dhabi", "Al Ain", "Dubai"])
selected_job_display = st.sidebar.selectbox(t["job_label"], job_options)
selected_platform = st.sidebar.selectbox(t["platform_label"], list(platforms.keys()))

# فلتر الوقت الجديد
time_selection = st.sidebar.radio(t["time_label"], list(t["time_options"].keys()), index=2) # الافتراضي: آخر أسبوع
time_code = t["time_options"][time_selection]

# --- المحرك الذكي (Smart Engine) ---
st.header(t["launch_header"])

# 1. تحديد كلمات البحث بناءً على الاختيار
if selected_job_display == t["cluster_exec"]:
    final_job_keywords = f"({exec_bundle})"
elif selected_job_display == t["cluster_ops"]:
    final_job_keywords = f"({ops_bundle})"
elif selected_job_display == t["cluster_strat"]:
    final_job_keywords = f"({strat_bundle})"
elif "---" in selected_job_display:
    final_job_keywords = '"Clinic Manager"' # Fallback
else:
    final_job_keywords = f'"{selected_job_display}"'

# 2. بناء جملة المواقع
loc_str = " OR ".join([f'"{loc}"' for loc in selected_locs])

# 3. كلمات الاستبعاد (Seniority Shield)
exclusions = '-"Nurse" -"Technician" -"Receptionist" -"Junior" -"Intern" -"Assistant" -"Entry level"'

# 4. تجميع المعادلة
site_operator = platforms[selected_platform]
query = f'{site_operator} {final_job_keywords} ({loc_str}) {exclusions}'

# 5. إضافة كود الوقت للرابط
google_base = "https://www.google.com/search?q="
time_param = f"&tbs=qdr:{time_code}" if time_code else ""
final_url = f"{google_base}{query}{time_param}"

st.markdown(f"**Target:** {selected_job_display}")
st.markdown(f"**Filter:** {time_selection} | {len(selected_locs)} Locations")

if st.button(t["btn_label"]):
    webbrowser.open(final_url)
    st.success(t["success_open"])
    st.markdown(f"[Click here manually if not opened]({final_url})")

st.divider()

# --- CRM (نظام الحفظ) ---
st.header(t["save_header"])
CSV_FILE = "HaMmE_Pro_Data.csv"

if 'search_results' not in st.session_state:
    try:
        st.session_state.search_results = pd.read_csv(CSV_FILE)
    except:
        st.session_state.search_results = pd.DataFrame(columns=[t["col_title"], t["col_company"], t["col_link"], t["col_notes"]])

with st.form("saver_form"):
    c1, c2 = st.columns(2)
    # تعبئة المسمى تلقائياً بشكل نظيف
    clean_title = selected_job_display.replace("⚡ ", "").replace("BUNDLE: ", "").replace("حزمة: ", "")
    if "---" in clean_title: clean_title = ""
    
    j_title = c1.text_input(t["col_title"], value=clean_title)
    j_company = c2.text_input(t["col_company"])
    j_link = st.text_input(t["col_link"])
    j_notes = st.text_area(t["col_notes"])
    
    submitted = st.form_submit_button(t["save_btn"])
    
    if submitted and j_company:
        new_row = pd.DataFrame({
            t["col_title"]: [j_title],
            t["col_company"]: [j_company],
            t["col_link"]: [j_link],
            t["col_notes"]: [j_notes]
        })
        st.session_state.search_results = pd.concat([st.session_state.search_results, new_row], ignore_index=True)
        st.session_state.search_results.to_csv(CSV_FILE, index=False)
        st.success(t["success_save"])

st.dataframe(st.session_state.search_results, use_container_width=True)