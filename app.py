import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(
    page_title="مدير المهام الذكي - التدريب الميداني",
    page_icon="✅",
    layout="wide"
)

# عنوان التطبيق
st.title("📝 مدير المهام الذكي")
st.markdown("### 🎓 مشروع التدريب الميداني | دورة برمجة بايثون")

# تهيئة المهام
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# الشريط الجانبي
with st.sidebar:
    st.markdown("### 👨‍🎓 معلومات الطالب")
    st.markdown("**الاسم:** [اسمك هنا]")
    st.markdown("**الرقم الجامعي:** [رقمك هنا]")
    
    st.markdown("---")
    st.markdown("### 📝 إضافة مهمة جديدة")
    
    task_title = st.text_input("عنوان المهمة")
    task_category = st.selectbox("التصنيف", ["دراسة", "عمل", "شخصي"])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ إضافة", use_container_width=True):
            if task_title:
                new_task = {
                    "id": len(st.session_state.tasks) + 1,
                    "title": task_title,
                    "category": task_category,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "completed": False
                }
                st.session_state.tasks.append(new_task)
                st.success(f"تمت إضافة: {task_title}")
                st.rerun()
    
    with col2:
        if st.button("🔄 مهام تجريبية", use_container_width=True):
            st.session_state.tasks = [
                {"id": 1, "title": "إنهاء تقرير التدريب", "category": "دراسة", "completed": False},
                {"id": 2, "title": "تسليم المشروع", "category": "عمل", "completed": True}
            ]
            st.rerun()
    
    st.markdown("---")
    st.markdown(f"**إجمالي المهام:** {len(st.session_state.tasks)}")

# المنطقة الرئيسية
st.markdown("### 📋 قائمة المهام")

if st.session_state.tasks:
    for task in st.session_state.tasks:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            status = "✅" if task["completed"] else "⭕"
            st.markdown(f"{status} **{task['title']}**")
            st.caption(f"التصنيف: {task['category']}")
        
        with col2:
            if st.button("✓", key=f"complete_{task['id']}"):
                task["completed"] = not task["completed"]
                st.rerun()
        
        with col3:
            if st.button("🗑️", key=f"delete_{task['id']}"):
                st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task["id"]]
                st.rerun()
        
        st.divider()
else:
    st.info("لا توجد مهام. أضف مهمة جديدة من الشريط الجانبي")

# تذييل الصفحة
st.markdown("---")
st.markdown("**مشروع التدريب الميداني** | دورة برمجة بايثون")