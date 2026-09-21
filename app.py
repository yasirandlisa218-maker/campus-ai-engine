import streamlit as st
import json
import base64
import os
from openai import OpenAI

# 1. 页面基本配置与全局防截断样式
st.set_page_config(page_title="校园信息智能抽取引擎", page_icon="🏫", layout="wide")

# 注入轻量 CSS
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


# 2. 侧边栏：项目背景与系统配置
with st.sidebar:
    # 顶部图片与赛道标识
    st.image("mylogo.jpg")
    st.markdown("<h4 style='text-align: center; color: #8A8178; margin-top: -10px;'>AI+场景创新赛道</h4>", unsafe_allow_html=True)
    
    # 赛道与项目背景解释（使用折叠面板收纳长文本）
    with st.expander("💡 赛道契合度与场景痛点", expanded=False):
        st.caption(
            "**痛点**：校园群聊通知冗长、多时间节点易遗漏。\n\n"
            "**创新**：本项目紧扣“场景创新”，利用大模型强大的语义理解与指令遵循能力，"
            "将非结构化文本降噪重组，并提供行程闭环服务，真正实现 AI 落地校园微场景。"
        )

    st.markdown("---")
    
    # 算法系统配置区
    st.header("⚙️ 算法系统配置")
    st.caption("在此配置大模型底座参数。系统采用动态提示词工程（Prompt Engineering），保障信息抽取的精确度与召回率。")
    
    st.write("📌 **项目名称**：非结构化校园通知智能抽取与多节点解构系统")
    st.write("👥 **参赛团队**：基米队")
    
    st.markdown("---")
    
    # API 密钥输入与帮助文档
    api_key = st.text_input("🔑 唤醒大模型 API Key", type="password", placeholder="sk-...")
    with st.expander("❓ 如何获取与配置密钥？"):
        st.caption(
            "1. 本系统支持 DeepSeek 或 硅基流动 等主流 OpenAI 格式接口。\n"
            "2. 前往对应开放平台注册并获取密钥（sk-...）。\n"
            "3. 粘贴至上方输入框即可动态激活云端大模型算力。"
        )


# 3. 主页面标题与视觉排版 (背景大图 + 悬浮半透明文字框)
# 读取你的本地图片，转换为网页背景图格式
image_path = "school.jpg"
if os.path.exists(image_path):
    with open(image_path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    bg_image_url = f"data:image/jpeg;base64,{encoded_string}"
else:
    # 备用网络图（防报错）
    bg_image_url = "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=1200&q=80"

st.markdown(f"""
<div style="
    background-image: url('{bg_image_url}');
    background-size: cover;
    background-position: center;
    border-radius: 16px;
    padding: 60px 20px; 
    margin-bottom: 24px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    display: flex;
    justify-content: center;
    align-items: center;
">
    <!-- 悬浮在图片上方的半透明白色文字卡片 -->
    <div style="
        background-color: rgba(255, 255, 255, 0.88); 
        backdrop-filter: blur(6px);
        padding: 30px 40px; 
        border-radius: 12px;
        text-align: center;
        max-width: 85%;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    ">
        <h1 style="margin-top: 0; margin-bottom: 12px; color: #3D342B; font-size: 32px; font-weight: bold;">
            🏫 校园非结构化通知 · 智能抽取引擎
        </h1>
        <p style="margin: 0; color: #8A8178; font-size: 16px; line-height: 1.6;">
            针对多截止日期、复杂考核门槛的通知，实现实体级细粒度抽取，并自动生成【专属行程规划】。
        </p >
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 4. 左右分栏交互
left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.subheader("📥 原始复杂通知输入")
    sample_text = (
        ""
    )
    user_input = st.text_area("请粘贴含多个时间或长文本要求的通知内容：", value=sample_text, height=240)
    
    start_btn = st.button("🚀 开始细粒度抽取与行程规划", type="primary", use_container_width=True)

with right_col:
    st.subheader("📤 智能输出面板")
    
    # 1. 只有当点击按钮时，才去呼叫大模型，并把结果“记”在脑子里
    if start_btn:
        if not api_key:
            st.error("⚠️ 请先在左侧边栏填入 API Key！")
        elif not user_input.strip():
            st.warning("⚠️ 输入内容不能为空！")
        else:
            with st.spinner("🤖 正在进行多节点解构并生成行程规划..."):
                try:
                    client = OpenAI(
                        api_key=api_key,
                        base_url="https://api.deepseek.com"  
                    )
                    
                    system_prompt = (
                        "你是一个专业的结构化实体抽取引擎和时间管理专家。从用户的复杂通知中精准解构信息，"
                        "并且根据截止时间和各项要求，倒推生成一个合理的准备行程/待办计划。"
                        "必须且仅输出标准 JSON 格式，严格符合以下字段定义：\n"
                        "{\n"
                        '  "theme": "通知/活动核心主题",\n'
                        '  "time_nodes": [{"event": "具体针对的事件/项目", "deadline": "对应截止时间或发生时间"}],\n'
                        '  "location": "办理/提交地点或线上方式",\n'
                        '  "requirements": ["具体要求条款1", "具体要求条款2"],\n'
                        '  "additional_notes": "其他补充提示",\n'
                        '  "suggested_itinerary": [{"time_point": "建议时间", "task": "待办任务描述"}]\n'
                        "}\n"
                    )
                    
                    response = client.chat.completions.create(
                        model="deepseek-chat",  
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_input}
                        ],
                        response_format={'type': 'json_object'}
                    )
                    
                    # 💥 【核心秘密武器】：把结果存进系统的“记忆体”中！
                    st.session_state.ai_result = json.loads(response.choices[0].message.content)
                    
                    st.toast('✅ 数据提取与行程规划完成！', icon='⚡')
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ 解析失败，错误信息：{str(e)}")

    # 2. 只要“记忆体”里有数据，我们就把它渲染出来（这样你去打勾，数据也不会丢了）
    if "ai_result" in st.session_state:
        parsed_json = st.session_state.ai_result
        
        tab1, tab2, tab3 = st.tabs(["📊 信息速览看板", "🗓️ 智能行程与待办", "💻 接口原始数据"])
        
        with tab1:
            st.info(f"📝 **通知核心主题**：\n\n### {parsed_json.get('theme', '未明确主题')}")
            time_nodes = parsed_json.get("time_nodes", [])
            if time_nodes:
                st.markdown("#### 📅 关键时间节点列表")
                for idx, item in enumerate(time_nodes, 1):
                    st.success(f"**{idx}. {item.get('event', '')}** ➔ `{item.get('deadline', '')}`")
            location_info = parsed_json.get("location")
            if location_info:
                st.warning(f"📍 **办理地点**：\n\n{location_info}")
            reqs = parsed_json.get("requirements", [])
            st.markdown("#### ⚠️ 申报门槛与硬性要求")
            if isinstance(reqs, list) and reqs:
                for req in reqs:
                    st.error(f"• {req}")
            elif isinstance(reqs, str):
                st.error(f"• {reqs}")
                
        with tab2:
            st.markdown("#### 📝 AI 倒推专属行动计划")
            itinerary = parsed_json.get("suggested_itinerary", [])
            if itinerary:
                # 现在你怎么打勾，系统都不会重置页面了！
                for idx, step in enumerate(itinerary):
                    st.checkbox(
                        f"**【{step.get('time_point', '待定')}】** ➔ {step.get('task', '准备事项')}", 
                        key=f"todo_{idx}"
                    )
            else:
                st.write("暂无行程建议")
                
        with tab3:
            st.json(parsed_json)
            
    else:
        # 只有在系统刚打开，记忆体完全为空时，才显示这句提示
        st.info("👈 填入 API Key 并点击左侧按钮，体验自动提取+行程规划功能。")