"""RagFlow chat UI.

A deliberately simple 2022 era interface: a single column chat, a sidebar to
upload and list documents. Later rungs of the line carry richer interfaces.
"""

from __future__ import annotations

import uuid

import api_utils
import streamlit as st

st.set_page_config(page_title="RagFlow", layout="centered")

if "session_id" not in st.session_state:
    st.session_state.session_id = uuid.uuid4().hex
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("RagFlow")
st.caption("Naive retrieval augmented generation, 2022 baseline")

with st.sidebar:
    st.header("Documents")
    uploaded = st.file_uploader("Upload a document", type=["txt", "pdf", "md"])
    if uploaded is not None and st.button("Index document"):
        with st.spinner("Indexing"):
            try:
                res = api_utils.upload(uploaded.name, uploaded.getvalue())
                st.success(f"Indexed {res['filename']} into {res['chunks']} chunks")
            except Exception as exc:
                st.error(str(exc))
    st.divider()
    try:
        docs = api_utils.list_docs()
        if docs:
            st.write("Indexed documents")
            for d in docs:
                st.write(f"- {d['filename']} ({d['chunks']} chunks)")
        else:
            st.write("No documents indexed yet")
    except Exception:
        st.write("API not reachable")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask a question about your documents")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking"):
            try:
                res = api_utils.ask(prompt, st.session_state.session_id)
                answer = res["answer"]
                sources = res.get("sources", [])
                st.write(answer)
                if sources:
                    st.caption("Sources: " + ", ".join(sources))
            except Exception as exc:
                answer = f"Error: {exc}"
                st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
