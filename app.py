import streamlit as st
import json
import pandas as pd
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(
    page_title="مدير المهام الذكي - التدريب الميداني",
    page_icon="🌙",
    layout="wide"
)

# تنسيق CSS متقدم مع تأثيرات
st.markdown("""
<style>
    /* خلفية متحركة بالنقاط */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
    }
    
    /* تأثير النقاط المتحركة */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .particle {
        position: absolute;
        width: 3px;
        height: 3px;
        background: rgba(59, 130, 246, 0.5);
        border-radius: 50%;
        animation: float 15s infinite linear;
    }
    
    @keyframes float {
        0% {
            transform: translateY(100vh) translateX(0);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100px) translateX(100px);
            opacity: 0;
        }
    }
    
    /* أزرار بتأثيرات */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 12px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5);
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
    }
    
    /* بطاقات المهام بتصميم حديث */
    .task-card {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid rgba(59, 130, 246, 0.2);
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    .task-card:hover {
        transform: translateY(-4px);
        border-color: rgba(59, 130, 246, 0.5);
        box-shadow: 0 12px 40px rgba(59, 130, 246, 0.3);
    }
    
    /* العنوان الرئيسي */
    .main-header {
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 2.8rem;
        margin-bottom: 20px;
        text-shadow: 0 2px 20px rgba(59, 130, 246, 0.3);
        font-weight: 800;
    }
    
    /* الشريط الجانبي */
    .sidebar-content {
        background: rgba(15, 23, 42, 0.9);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* إحصائيات */
    .stat-card {
        background: rgba(30, 41, 59, 0.7);
        border-radius: 12px;
        padding: 15px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        text-align: center;
    }
    
    /* أشرطة التقدم */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #3b82f6 0%, #60a5fa 100%);
        border-radius: 10px;
    }
    
    /* أزرار خاصة */
    .delete-btn {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
    }
    
    .delete-btn:hover {
        background: linear-gradient(135deg, #f87171 0%, #ef4444 100%) !important;
    }
    
    .success-btn {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    }
    
    .success-btn:hover {
        background: linear-gradient(135deg, #34d399 0%, #10b981 100%) !important;
    }
    
    /* حاويات النصوص */
    .info-box {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #3b82f6;
        margin: 15px 0;
    }
    
    /* تأثيرات النصوص */
    .gradient-text {
        background: linear-gradient(135deg, #60a5fa 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    
    /* شريط التمرير مخصص */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
    }
    
    /* بطاقات التحليلات */
    .analytics-card {
        background: rgba(30, 41, 59, 0.7);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        transition: all 0.3s ease;
    }
    
    .analytics-card:hover {
        transform: translateY(-3px);
        border-color: rgba(59, 130, 246, 0.4);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.2);
    }
</style>

<div class="particles" id="particles"></div>

<script>
// إنشاء تأثير النقاط المتحركة
function createParticles() {
    const container = document.getElementById('particles');
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // مواقع عشوائية
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        
        // أحجام عشوائية
        const size = Math.random() * 3 + 1;
        particle.style.width = size + 'px';
        particle.style.height = size + 'px';
        
        // ألوان عشوائية
        const colors = [
            'rgba(59, 130, 246, 0.6)',
            'rgba(96, 165, 250, 0.5)',
            'rgba(168, 85, 247, 0.4)',
            'rgba(34, 211, 238, 0.3)'
        ];
        particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        
        // سرعات عشوائية
        particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
        particle.style.animationDelay = Math.random() * 5 + 's';
        
        container.appendChild(particle);
    }
}

// تأثير تفاعلي مع الماوس
document.addEventListener('mousemove', function(e) {
    const particles = document.querySelectorAll('.particle');
    const mouseX = e.clientX / window.innerWidth;
    const mouseY = e.clientY / window.innerHeight;
    
    particles.forEach(particle => {
        const speed = 0.3;
        const x = (mouseX - 0.5) * speed * 100;
        const y = (mouseY - 0.5) * speed * 100;
        
        particle.style.transform += ` translate(${x}px, ${y}px)`;
    });
});

// تشغيل التأثيرات عند تحميل الصفحة
window.addEventListener('load', createParticles);
</script>
""", unsafe_allow_html=True)

# العنوان الرئيسي مع تأثيرات
st.markdown("""
<div style="text-align: center; padding: 30px 0;">
    <h1 class="main-header">🌙 مدير المهام الذكي</h1>
    <h3 style="color: #94a3b8; margin-top: -10px;">🎓 مشروع التدريب الميداني | دورة برمجة بايثون</h3>
</div>
""", unsafe_allow_html=True)

# تهيئة حالة الجلسة للمهام
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
    # إضافة مهام تجريبية للعرض
    st.session_state.tasks = [
        {
            "id": 1,
            "title": "إكمال تقرير التدريب الميداني",
            "category": "دراسة",
            "priority": "عالي",
            "due_date": datetime.now().strftime("%Y-%m-%d"),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "completed": False
        },
        {
            "id": 2,
            "title": "تحضير عرض مشروع بايثون",
            "category": "عمل",
            "priority": "متوسط",
            "due_date": "",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "completed": True
        },
        {
            "id": 3,
            "title": "تصميم واجهة المستخدم",
            "category": "تصميم",
            "priority": "عالي",
            "due_date": (datetime.now().date().replace(day=datetime.now().day + 2)).strftime("%Y-%m-%d"),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "completed": False
        }
    ]

# الشريط الجانبي بتصميم داكن
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    
    st.markdown("### 👨‍🎓 معلومات الطالب")
    col_info1, col_info2 = st.columns([1, 3])
    with col_info1:
        st.markdown("👤")
    with col_info2:
        st.markdown("الاسم : محمود قرضايا")
        st.markdown("الرقم الجامعي : 120210476")
    
    st.markdown("---")
    
    st.markdown("### 📝 إضافة مهمة جديدة")
    
    with st.form("task_form", clear_on_submit=True):
        task_title = st.text_input("📌 عنوان المهمة", placeholder="أدخل وصف المهمة...")
        
        col_cat, col_pri = st.columns(2)
        with col_cat:
            task_category = st.selectbox("📁 التصنيف", ["دراسة", "عمل", "شخصي", "تسوق", "تصميم", "أخرى"])
        with col_pri:
            task_priority = st.selectbox("🎯 الأولوية", ["عالي", "متوسط", "منخفض"])
        
        due_date = st.date_input("📅 تاريخ الاستحقاق", value=None)
        
        col_sub1, col_sub2 = st.columns(2)
        with col_sub1:
            submitted = st.form_submit_button("✨ إضافة المهمة", use_container_width=True)
        with col_sub2:
            demo_clicked = st.form_submit_button("🔄 مهام تجريبية", use_container_width=True)
    
    if demo_clicked:
        st.session_state.tasks.extend([
            {
                "id": len(st.session_state.tasks) + 1,
                "title": "مراجعة أساسيات بايثون",
                "category": "دراسة",
                "priority": "عالي",
                "due_date": "",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "completed": False
            },
            {
                "id": len(st.session_state.tasks) + 2,
                "title": "اختبار تأثيرات التصميم",
                "category": "تصميم",
                "priority": "متوسط",
                "due_date": "",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "completed": False
            }
        ])
        st.rerun()
    
    if submitted and task_title:
        new_task = {
            "id": len(st.session_state.tasks) + 1,
            "title": task_title,
            "category": task_category,
            "priority": task_priority,
            "due_date": due_date.strftime("%Y-%m-%d") if due_date else "",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "completed": False
        }
        st.session_state.tasks.append(new_task)
        st.success(f"✅ تمت إضافة المهمة: **{task_title}**")
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 📊 الإحصائيات")
    
    total_tasks = len(st.session_state.tasks)
    completed_tasks = sum(1 for task in st.session_state.tasks if task.get("completed", False))
    pending_tasks = total_tasks - completed_tasks
    
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.markdown(f'<div class="stat-card"><h3 style="margin:0;color:#60a5fa">{total_tasks}</h3><p style="margin:0;color:#94a3b8">المهام</p></div>', unsafe_allow_html=True)
    with col_stat2:
        st.markdown(f'<div class="stat-card"><h3 style="margin:0;color:#10b981">{completed_tasks}</h3><p style="margin:0;color:#94a3b8">مكتملة</p></div>', unsafe_allow_html=True)
    
    if total_tasks > 0:
        progress = completed_tasks / total_tasks
        st.progress(progress)
        st.caption(f"معدل الإنجاز: **{progress*100:.1f}%**")
    
    st.markdown("---")
    
    st.markdown("### ⚡ إجراءات سريعة")
    
    col_act1, col_act2 = st.columns(2)
    with col_act1:
        if st.button("🗑️ حذف الكل", use_container_width=True, key="clear_all"):
            st.session_state.tasks = []
            st.rerun()
    with col_act2:
        if st.button("📥 تصدير", use_container_width=True, key="export"):
            if st.session_state.tasks:
                tasks_json = json.dumps(st.session_state.tasks, indent=2, default=str)
                st.download_button(
                    label="تنزيل JSON",
                    data=tasks_json,
                    file_name=f"المهام_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json",
                    use_container_width=True
                )
    
    st.markdown('</div>', unsafe_allow_html=True)

# المنطقة الرئيسية
st.markdown("### 📋 المهام الحالية")

# عناصر التحكم في التصفية
col_filter1, col_filter2, col_filter3 = st.columns([2, 2, 2])
with col_filter1:
    show_completed = st.checkbox("عرض المكتملة", value=True, key="show_completed")
with col_filter2:
    categories = ["الكل"] + list(set(task.get("category", "أخرى") for task in st.session_state.tasks))
    filter_category = st.selectbox("التصنيف", categories, key="filter_category", label_visibility="collapsed")
    st.caption("🔍 تصفية حسب التصنيف")
with col_filter3:
    sort_options = ["الأولوية", "تاريخ الاستحقاق", "الأحدث", "الأقدم"]
    sort_by = st.selectbox("الترتيب", sort_options, key="sort_by", label_visibility="collapsed")
    st.caption("📊 ترتيب المهام")

# تصفية وترتيب المهام
filtered_tasks = st.session_state.tasks.copy()

if not show_completed:
    filtered_tasks = [task for task in filtered_tasks if not task.get("completed", False)]

if filter_category != "الكل":
    filtered_tasks = [task for task in filtered_tasks if task.get("category") == filter_category]

if sort_by == "الأولوية":
    priority_order = {"عالي": 1, "متوسط": 2, "منخفض": 3}
    filtered_tasks.sort(key=lambda x: priority_order.get(x.get("priority", "منخفض"), 3))
elif sort_by == "تاريخ الاستحقاق":
    filtered_tasks.sort(key=lambda x: x.get("due_date", "9999-99-99"))
elif sort_by == "الأحدث":
    filtered_tasks.sort(key=lambda x: x.get("created_at", ""), reverse=True)
else:
    filtered_tasks.sort(key=lambda x: x.get("created_at", ""))

# عرض المهام
if filtered_tasks:
    for task in filtered_tasks:
        with st.container():
            st.markdown('<div class="task-card">', unsafe_allow_html=True)
            
            col_task1, col_task2, col_task3 = st.columns([6, 2, 2])
            
            with col_task1:
                # أيقونة الأولوية
                priority_icon = {"عالي": "🔴", "متوسط": "🟡", "منخفض": "🟢"}.get(task.get("priority", "منخفض"), "⚪")
                
                # حالة الإكمال
                if task.get("completed", False):
                    st.markdown(f"### ✅ ~~{task['title']}~~")
                else:
                    st.markdown(f"### {priority_icon} {task['title']}")
                
                # معلومات إضافية
                col_info1, col_info2, col_info3 = st.columns(3)
                with col_info1:
                    st.caption(f"📁 {task.get('category', 'أخرى')}")
                with col_info2:
                    due_date = task.get('due_date', '')
                    if due_date:
                        st.caption(f"📅 {due_date}")
                with col_info3:
                    st.caption(f"⏰ {task.get('created_at', '')}")
            
            with col_task2:
                # زر تغيير الحالة
                current_status = task.get("completed", False)
                button_text = "✓ إكمال" if not current_status else "↶ إلغاء"
                button_class = "success-btn" if not current_status else ""
                
                if st.button(button_text, key=f"toggle_{task['id']}", use_container_width=True):
                    task["completed"] = not current_status
                    st.rerun()
            
            with col_task3:
                # زر الحذف
                if st.button("🗑️ حذف", key=f"delete_{task['id']}", use_container_width=True):
                    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task["id"]]
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="info-box" style="text-align: center;">
        <h3 style="color: #94a3b8;">📭 لا توجد مهام</h3>
        <p style="color: #64748b;">أضف مهمتك الأولى باستخدام النموذج في الشريط الجانبي</p>
    </div>
    """, unsafe_allow_html=True)

# قسم التحليلات بدون رسم بياني
st.markdown("---")
st.markdown("### 📈 تحليلات متقدمة")

if st.session_state.tasks:
    df = pd.DataFrame(st.session_state.tasks)
    
    col_anal1, col_anal2, col_anal3 = st.columns(3)
    
    with col_anal1:
        st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 توزيع التصنيفات")
        if 'category' in df.columns:
            category_counts = df['category'].value_counts()
            for category, count in category_counts.items():
                progress = count / len(df)
                st.markdown(f"**{category}**: {count} مهمة")
                st.progress(progress)
                st.caption(f"{progress*100:.1f}% من إجمالي المهام")
        else:
            st.info("لا توجد بيانات عن التصنيفات")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_anal2:
        st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
        st.markdown("#### 🎯 توزيع الأولويات")
        if 'priority' in df.columns:
            priority_counts = df['priority'].value_counts()
            for priority, count in priority_counts.items():
                # ألوان حسب الأولوية
                color = {
                    "عالي": "#ef4444",
                    "متوسط": "#f59e0b",
                    "منخفض": "#10b981"
                }.get(priority, "#94a3b8")
                
                st.markdown(f"<span style='color:{color}'>● {priority}</span>: {count} مهمة", unsafe_allow_html=True)
        else:
            st.info("لا توجد بيانات عن الأولويات")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_anal3:
        st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
        st.markdown("#### 📈 معدلات الإنجاز")
        completed_count = df['completed'].sum() if 'completed' in df.columns else 0
        total_count = len(df)
        
        if total_count > 0:
            completion_rate = (completed_count / total_count) * 100
            
            # بطاقات المقاييس
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.5); padding: 15px; border-radius: 10px; margin: 10px 0;">
                <h3 style="color: #60a5fa; margin: 0; font-size: 2rem;">{completion_rate:.1f}%</h3>
                <p style="color: #94a3b8; margin: 5px 0;">معدل الإنجاز</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.5); padding: 15px; border-radius: 10px; margin: 10px 0;">
                <h3 style="color: #10b981; margin: 0; font-size: 2rem;">{completed_count}</h3>
                <p style="color: #94a3b8; margin: 5px 0;">مهام مكتملة</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.5); padding: 15px; border-radius: 10px; margin: 10px 0;">
                <h3 style="color: #f59e0b; margin: 0; font-size: 2rem;">{total_count - completed_count}</h3>
                <p style="color: #94a3b8; margin: 5px 0;">مهام قيد التنفيذ</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("لا توجد بيانات للإحصائيات")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # معلومات إضافية
    st.markdown("---")
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown("#### 📅 الإحصائيات الزمنية")
        if 'created_at' in df.columns:
            # حساب المهام حسب اليوم
            try:
                df['created_date'] = pd.to_datetime(df['created_at']).dt.date
                daily_counts = df['created_date'].value_counts().sort_index()
                
                if len(daily_counts) > 0:
                    latest_date = daily_counts.index[-1]
                    latest_count = daily_counts.iloc[-1]
                    st.info(f"**آخر نشاط**: {latest_date} ({latest_count} مهمة)")
            except:
                st.info("تعذر تحليل البيانات الزمنية")
    
    with col_info2:
        st.markdown("#### ⚡ معلومات سريعة")
        if 'due_date' in df.columns:
            overdue_tasks = len([d for d in df['due_date'] if d and d < datetime.now().strftime('%Y-%m-%d')])
            if overdue_tasks > 0:
                st.warning(f"**⚠️ مهام متأخرة**: {overdue_tasks}")
            else:
                st.success("**✅ جميع المهام في الموعد**")
    
else:
    st.markdown("""
    <div class="info-box" style="text-align: center;">
        <h3 style="color: #94a3b8;">📊 لا توجد بيانات للتحليل</h3>
        <p style="color: #64748b;">أضف بعض المهام لرؤية الإحصائيات والتحليلات</p>
    </div>
    """, unsafe_allow_html=True)

# تذييل الصفحة
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; background: rgba(15, 23, 42, 0.7); border-radius: 15px; margin-top: 30px;">
    <h4 style="color: #60a5fa; margin-bottom: 10px;">🎓 مشروع التدريب الميداني</h4>
    <p style="color: #94a3b8; margin: 5px 0;">دورة برمجة بايثون | تخصص تكنولوجيا المعلومات</p>
    <p style="color: #64748b; margin: 5px 0; font-size: 0.9em;">تم التطوير باستخدام Python, Streamlit, Pandas</p>
    <p style="color: #475569; margin: 5px 0; font-size: 0.8em;">📅 ديسمبر 2025 | 🎯 تصميم تفاعلي مع Dark Mode</p>
</div>
""", unsafe_allow_html=True)

# تأثيرات JavaScript إضافية
st.markdown("""
<script>
// تأثيرات تفاعلية إضافية
document.addEventListener('DOMContentLoaded', function() {
    // تأثير عند تمرير الماوس على البطاقات
    const cards = document.querySelectorAll('.task-card, .analytics-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 15px 45px rgba(59, 130, 246, 0.4)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.boxShadow = '';
        });
    });
    
    // تأثير على الأزرار
    const buttons = document.querySelectorAll('.stButton button');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    // تحديث النقاط المتحركة بشكل دوري
    setInterval(() => {
        const particles = document.querySelectorAll('.particle');
        particles.forEach(particle => {
            // حركة عشوائية خفيفة
            const randomX = (Math.random() - 0.5) * 2;
            const randomY = (Math.random() - 0.5) * 2;
            particle.style.transform += ` translate(${randomX}px, ${randomY}px)`;
        });
    }, 3000);
});
</script>
""", unsafe_allow_html=True)