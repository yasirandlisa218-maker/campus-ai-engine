import streamlit as st
import json
import base64
import os
from datetime import datetime, timedelta
from openai import OpenAI

# 1. 页面基本配置与全局防截断样式
st.set_page_config(page_title="校园信息智能抽取引擎", page_icon="🏫", layout="wide")

st.markdown("""
<style>
div[data-testid="stMarkdownContainer"] p {
    word-break: break-word;
    white-space: pre-wrap;
}
div.stButton > button {
    border-radius: 8px;
    font-weight: bold;
    border: none;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# ===== 核心功能函数：纯手工构建 ICS 日历文件 =====
def generate_ics_content(itinerary, theme):
    """根据 AI 生成的行程，自动打包成手机可识别的 .ics 文件内容"""
    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Hainan University//Campus AI Engine//CN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH"
    ]
    
    # 遍历每一项待办，生成一个全天日程（默认安排在明天，并在描述中写明建议时间）
    for idx, step in enumerate(itinerary):
        task_name = step.get('task', '准备事项')
        time_point = step.get('time_point', '待定')
        
        # 设定日程为明天，避免时区解析报错，确保全端兼容
        target_date = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")
        
        ics_lines.extend([
            "BEGIN:VEVENT",
            f"SUMMARY:【待办】{task_name}",
            f"DESCRIPTION:关联通知：{theme}\\n建议完成节点：{time_point}\\n(由基米队智能引擎自动生成)",
            f"DTSTART;VALUE=DATE:{target_date}",
            "END:VEVENT"
        ])
        
    ics_lines.append("END:VCALENDAR")
    return "\n".join(ics_lines)
# =================================================

# # 2. 侧边栏：项目背景与系统配置
# 将你的专属 Logo 固定在网页左上角的专业导航栏位置
st.logo("mylogo.jpg")

with st.sidebar:
    # 侧边栏的宣传大图也替换为你的自定义图片
    st.image("mylogo.jpg", use_container_width=True)
    st.markdown("<h4 style='text-align: center; color: #8A8178; margin-top: -10px;'>AI+场景创新赛道</h4>", unsafe_allow_html=True)
    
    with st.expander("💡 赛道契合度与场景痛点", expanded=False):
        st.caption(
            "**痛点**：校园群聊通知冗长、多时间节点易遗漏。\n\n"
            "**创新**：本项目紧扣“场景创新”，提供从多模态降噪到行程闭环（原生日历导出）的 AI 落地服务。"
        )

    st.markdown("---")
    st.header("⚙️ 算法系统配置")
    st.write("📌 **项目名称**：非结构化校园通知智能抽取引擎")
    st.write("👥 **参赛团队**：基米队")
    
    st.markdown("#### 🔑 引擎密钥配置")
    
    # 将混元替换为 Qwen-VL
    engine_choice = st.radio(
        "请选择要使用的解析引擎：",
        ("DeepSeek (纯文本极速版)", "Qwen-VL (图文多模态旗舰版)"),
        index=0
    )
    
    deepseek_key = ""
    vision_key = ""
    
    if engine_choice == "DeepSeek (纯文本极速版)":
        st.info("💡 **提示**：DeepSeek 仅支持识别纯文本。适合处理复制粘贴的文字通知。")
        deepseek_key = st.text_input("填入 DeepSeek API Key", type="password", placeholder="sk-...")
    else:
        st.info("🖼️ **提示**：如需上传【通知截图】识图，请选择此引擎。")
        vision_key = st.text_input("填入硅基流动 API Key", type="password", placeholder="sk-...")
# 3. 主页面标题与视觉排版 (背景大图 + 悬浮半透明文字框)
image_path = "school.jpg"
if os.path.exists(image_path):
    with open(image_path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    bg_image_url = f"data:image/jpeg;base64,{encoded_string}"
else:
    bg_image_url = "mylogo.jpg"

# 读取你的专属动态图标
icon_path = "schoollogo.jpg"  # 👈 把这里改成你自己的图标文件名！
if os.path.exists(icon_path):
    with open(icon_path, "rb") as f:
        icon_encoded = base64.b64encode(f.read()).decode()
    # 如果你的图片是 jpg，把下面的 image/png 改成 image/jpeg
    icon_url = f"data:image/jpeg;base64,{icon_encoded}"
else:
    # 如果找不到你的本地图片，就用这个默认的网络图片顶替防报错
    icon_url = "https://cdn-icons-png.flaticon.com/512/8297/8297073.png"

st.markdown(f"""
<style>
/* 定义一个名为 subtle-pulse 的平滑呼吸动画 */
@keyframes subtle-pulse {{
    0% {{ transform: scale(1); opacity: 0.9; }}
    50% {{ transform: scale(1.08); opacity: 1; }}
    100% {{ transform: scale(1); opacity: 0.9; }}
}}
</style>
<div style="background-image: url('{bg_image_url}'); background-size: cover; background-position: center; border-radius: 16px; padding: 60px 20px; margin-bottom: 24px; display: flex; justify-content: center; align-items: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
<div style="background-color: rgba(255, 255, 255, 0.88); backdrop-filter: blur(6px); padding: 30px 40px; border-radius: 12px; text-align: center; max-width: 85%; box-shadow: 0 8px 24px rgba(0,0,0,0.15);">
<div style="display: flex; align-items: center; justify-content: center; gap: 14px; margin-bottom: 12px;">
<!-- 这里自动调用了你刚才转换的本地图片 -->
<img src="{icon_url}" style="width: 42px; height: 42px; animation: subtle-pulse 2.5s infinite ease-in-out;">
<h1 style="margin: 0; color: #3D342B; font-size: 32px; font-weight: bold;">
校园非结构化通知 · 智能抽取引擎
</h1>
</div>
<p style="margin: 0; color: #8A8178; font-size: 16px; line-height: 1.6;">
支持截图识图上传，实现多时间节点细粒度抽取，并自动生成【专属原生行程规划】。
</p>
</div>
</div>
""", unsafe_allow_html=True)
# 4. 左右分栏交互
left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.subheader("📥 复杂通知输入端")
    
    # 【杀手锏 1】：多模态视觉上传组件
    uploaded_image = st.file_uploader("📷 上传通知截图 (选填，自动 OCR)", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        st.success("✅ 图片已就绪，将在抽取时同步进行视觉解构。")
        
    sample_text = (
        "示例：关于开展2026年度大学生创新创业训练计划（大创）项目申报的通知：\n"
        "1. 申报时间：系统线上填报截止时间为10月15日23:59；纸质版申报书一式三份，需指导教师签字后，于10月17日17:00前交至学院教务科（教学楼A栋302）。逾期不予受理。\n"
        "2. 申报门槛：项目负责人需为全日制在校大二或大三本科生，且已修必修课程无不及格记录。每个团队总人数不得超过5人。\n"
        "3. 答辩安排：学院初审通过的项目，将于10月22日下午14:00进行立项答辩，请提前准备5分钟的演示PPT。"
    )
    user_input = st.text_area("或直接粘贴纯文本通知内容：", value=sample_text, height=200)
    start_btn = st.button("🚀 启动细粒度抽取与规划", type="primary", use_container_width=True)

with right_col:
    st.subheader("📤 智能输出与闭环面板")
    
    if start_btn:
        # --- 防呆拦截 ---
        if engine_choice == "DeepSeek (纯文本极速版)":
            if not deepseek_key:
                st.error("⚠️ 请在左侧填入 DeepSeek API Key！")
                st.stop()
            if uploaded_image:
                st.warning("⚠️ 发现截图！DeepSeek只能处理纯文字，请在左侧切换为【Qwen-VL】引擎。")
                st.stop()
            if not user_input.strip():
                st.warning("⚠️ 请输入纯文本内容！")
                st.stop()
        else:
            if not vision_key:
                st.error("⚠️ 请在左侧填入硅基流动 API Key！")
                st.stop()
            if not user_input.strip() and not uploaded_image:
                st.warning("⚠️ 请上传通知截图或输入文字内容！")
                st.stop()
                
        # --- 核心引擎调用 ---
        with right_col:
            with st.spinner("🤖 引擎已启动，正在解构多节点与行程排布..."):
                system_prompt = (
                    "你是一个结构化实体抽取引擎和时间管理专家。从用户的通知中解构信息并倒推行程。"
                    "必须输出标准 JSON 格式：\n"
                    "{\n"
                    '  "theme": "通知核心主题",\n'
                    '  "time_nodes": [{"event": "事件", "deadline": "时间"}],\n'
                    '  "location": "办理地点",\n'
                    '  "requirements": ["要求1", "要求2"],\n'
                    '  "suggested_itinerary": [{"time_point": "建议时间", "task": "待办描述"}]\n'
                    "}\n"
                )

                try:
                    if engine_choice == "Qwen-VL (图文多模态旗舰版)":
                        # 🚀 视觉大模型处理（通义千问 Qwen2.5-VL）
                        client = OpenAI(
                            api_key=vision_key,
                            base_url="https://api.siliconflow.cn/v1" 
                        )
                        
                        messages = [{"role": "system", "content": system_prompt}]
                        user_content = []
                        if user_input.strip():
                            user_content.append({"type": "text", "text": "请严格按照 JSON 格式输出。补充说明：" + user_input})
                        else:
                            user_content.append({"type": "text", "text": "请解析这张通知截图，并严格按照 JSON 格式输出。"})
                            
                        if uploaded_image:
                            base64_image = base64.b64encode(uploaded_image.getvalue()).decode('utf-8')
                            user_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})
                            
                        messages.append({"role": "user", "content": user_content})
                        
                        response = client.chat.completions.create(
                            # 硅基流动付费稳定模型名称
                            model="Qwen/Qwen3-VL-30B-A3B-Instruct", 
                            messages=messages,
                            response_format={'type': 'json_object'}
                        )
                        
                    else:
                        # 🚀 纯文本极速处理（DeepSeek-Chat）
                        client = OpenAI(
                            api_key=deepseek_key,
                            base_url="https://api.deepseek.com"  
                        )
                        
                        response = client.chat.completions.create(
                            model="deepseek-chat",  
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_input}
                            ],
                            response_format={'type': 'json_object'}
                        )
                    
                    st.session_state.ai_result = json.loads(response.choices[0].message.content)
                    st.toast('✅ 提取与规划完成！', icon='⚡')
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ 引擎请求中断，错误详情：{str(e)}")
    if "ai_result" in st.session_state:
        parsed_json = st.session_state.ai_result
        
        tab1, tab2, tab3 = st.tabs(["📊 可视化速览", "🗓️ 行程与日历", "💻 接口级数据"])
        
        with tab1:
            st.info(f"📝 **通知核心主题**：\n\n### {parsed_json.get('theme', '未明确主题')}")
            time_nodes = parsed_json.get("time_nodes", [])
            if time_nodes:
                st.markdown("#### 📅 关键时间节点")
                for idx, item in enumerate(time_nodes, 1):
                    st.success(f"**{idx}. {item.get('event', '')}** ➔ `{item.get('deadline', '')}`")
            location_info = parsed_json.get("location")
            if location_info:
                st.warning(f"📍 **办理地点**：\n\n{location_info}")
            reqs = parsed_json.get("requirements", [])
            st.markdown("#### ⚠️️ 申报门槛与要求")
            if isinstance(reqs, list) and reqs:
                for req in reqs:
                    st.error(f"• {req}")
                
        with tab2:
            st.markdown("#### 📝 AI 倒推专属行动计划")
            itinerary = parsed_json.get("suggested_itinerary", [])
            
            if itinerary:
                for idx, step in enumerate(itinerary):
                    st.checkbox(f"**【{step.get('time_point', '待定')}】** ➔ {step.get('task', '准备事项')}", key=f"todo_{idx}")
                
                st.markdown("---")
                
                # 【杀手锏 3】：生成并提供真正的 .ics 日历文件下载
                ics_data = generate_ics_content(itinerary, parsed_json.get('theme', '校园通知'))
                
                st.download_button(
                    label="📲 立即导入手机系统日历",
                    data=ics_data,
                    file_name="campus_schedule.ics",
                    mime="text/calendar",
                    type="primary"
                )
                st.caption("✨ 点击下载后发送至手机，可一键在 Apple/Android 原生系统内设定闹钟提醒。")
            else:
                st.write("暂无行程建议")
                
        with tab3:
            st.json(parsed_json)