import streamlit as st
import json
from datetime import datetime

# أبسط إصدار يعمل 100%
def main():
    st.set_page_config(page_title="مدير المهام", layout="centered")
    
    st.title("📋 مدير المهام البسيط")
    st.write("مشروع التدريب الميداني - برمجة بايثون")
    
    # إدارة المهام
    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    
    # إضافة مهمة
    with st.form("add_task"):
        title = st.text_input("أدخل المهمة:")
        if st.form_submit_button("إضافة"):
            if title:
                st.session_state.tasks.append({
                    "id": len(st.session_state.tasks) + 1,
                    "title": title,
                    "time": datetime.now().strftime("%H:%M"),
                    "done": False
                })
                st.rerun()
    
    # عرض المهام
    st.subheader("مهامك:")
    for i, task in enumerate(st.session_state.tasks):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"{'✅' if task['done'] else '⭕'} {task['title']}")
        with col2:
            if st.button("✓", key=f"done{i}"):
                task["done"] = not task["done"]
                st.rerun()
        with col3:
            if st.button("🗑️", key=f"del{i}"):
                del st.session_state.tasks[i]
                st.rerun()
    
    # إحصائيات
    st.sidebar.write(f"**المهام:** {len(st.session_state.tasks)}")
    st.sidebar.write(f"**المكتملة:** {sum(1 for t in st.session_state.tasks if t['done'])}")

if __name__ == "__main__":
    main()