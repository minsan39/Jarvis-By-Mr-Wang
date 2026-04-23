import streamlit as st
from src.agent.agent import get_ai_response_stream
from src.session.session import load_session, new_session, save_session
from datetime import datetime
import os
from src.rag.loader import load_documents
from src.rag.chunker import split_text
from src.rag.vectorstore import add_to_vectorstore, similarity_search
from src.rag.chain import create_rag_chain
st.title("🤖 微信智能助手")

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_session" not in st.session_state:
    st.session_state.current_session = None

# 渲染已有消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

#上传文件
uploaded_file = st.file_uploader("📎 上传文档", type=["txt","pdf","docx"],label_visibility="collapsed")

if uploaded_file is not None:
    save_path = os.path.join("knowledge_base", uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    with st.spinner("正在加载到向量库..."):
        docs = load_documents(save_path)
        chunks = split_text(docs)
        add_to_vectorstore(chunks)
    

# 获取用户输入
prompt = st.chat_input("输入你的问题...")

# 处理用户发送消息
if prompt:
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 获取AI响应
    with st.chat_message("assistant"):
        placeholder = st.empty()
        response = ""
        docs = []

        #尝试使用RAG回答
        try:
            docs = similarity_search(prompt,k=3)
            if docs:
                # 如果有相关文档，使用RAG回答
                response = create_rag_chain(prompt)
            else:
                # 如果没有相关文档，使用默认回答
                for chunk in get_ai_response_stream(prompt, st.session_state.messages[:-1]):
                    response += chunk
                    placeholder.markdown(response, unsafe_allow_html=True)
        except Exception:
            # 如果RAG回答失败，使用默认回答
            for chunk in get_ai_response_stream(prompt, st.session_state.messages[:-1]):
                response += chunk
                placeholder.markdown(response, unsafe_allow_html=True)
        
        # 处理换行符
        while response.endswith("<br>"):
            response = response[:-4]
        
        # 显示最终回答
        placeholder.markdown(response, unsafe_allow_html=True)

    # 添加AI响应到消息列表
    st.session_state.messages.append({"role": "assistant", "content": response})

    # 为新会话生成会话ID
    if st.session_state.current_session is None:
        st.session_state.current_session = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# 侧边栏：历史会话管理
with st.sidebar:
    st.write("历史记录")

    # 新建会话按钮
    if st.button("新建会话", use_container_width=True):
        # 保存当前会话
        if st.session_state.current_session is not None:
            save_session(
                {"time": st.session_state.current_session, "content": st.session_state.messages[0]["content"] if st.session_state.messages else ""},
                st.session_state.messages
            )
        # 重置会话
        st.session_state.current_session = None
        new_session(st.session_state.messages)

    # 遍历所有会话文件，点击加载对应会话
    for sess_file in os.listdir("data"):
        if st.button(sess_file.replace(".json", ""), use_container_width=True):
            # 保存当前会话
            if st.session_state.current_session is not None:
                save_session(
                    {"time": st.session_state.current_session, "content": st.session_state.messages[0]["content"] if st.session_state.messages else ""},
                    st.session_state.messages
                )
            # 加载选中的会话
            loaded = load_session(os.path.join("data", sess_file))
            if loaded:
                st.session_state.messages = loaded["messages"]
                st.session_state.current_session = sess_file.replace(".json", "")
