import json
import os

from datetime import date

import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="AI Intelligence & Risk Advisor", page_icon="🧠", layout="wide")

DEFAULT_API = os.getenv("FASTAPI_BASE_URL", "http://localhost:8000")
st.sidebar.title("🧠 AI Intelligence")
st.sidebar.caption("Project & Risk Advisor")
api_url = st.sidebar.text_input("FastAPI Base URL", value=st.session_state.get("api_url", DEFAULT_API)).rstrip("/")
st.session_state.api_url = api_url

PAGES = ["Health", "Scope", "Deliverables", "Risks", "Blockers", "Documentation", "AI Assistant"]
INITIAL = {"health": None, "scope": None, "deliverables": None, "risk": None, "blocker": None, "documentation": None}
for key, value in [("project", None), ("documents", []), ("analysis", INITIAL.copy()), ("messages", [])]:
    if key not in st.session_state:
        st.session_state[key] = value

def post(path, **kwargs):
    try:
        response = requests.post(f"{st.session_state.api_url}{path}", timeout=180, **kwargs)
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return {"response_text": response.text}
    except requests.RequestException as exc:
        detail = ""
        if getattr(exc, "response", None) is not None:
            detail = f" — {exc.response.text[:500]}"
        raise RuntimeError(f"{path}: {exc}{detail}") from exc

def unwrap(data):
    for _ in range(3):
        if isinstance(data, dict) and isinstance(data.get("result"), dict):
            data = data["result"]
        else:
            break
    return data

def show_section(title, value):
    if value is None or value == "" or value == [] or value == {}:
        return
    st.subheader(title)
    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                st.markdown(f"- **{item.get('title') or item.get('name') or item.get('description') or 'Item'}**")
                st.json(item, expanded=False)
            else:
                st.markdown(f"- {item}")
    elif isinstance(value, dict):
        st.json(value)
    else:
        st.write(value)

def run_agents():
    tasks = [("scope", "/agents/scope"), ("risk", "/agents/risk"), ("blocker", "/agents/blocker"),
             ("documentation", "/agents/documentation"), ("health", "/agents/health")]
    failures = []
    progress = st.progress(0, text="Starting AI agents...")
    for i, (key, endpoint) in enumerate(tasks, 1):
        try:
            st.session_state.analysis[key] = post(endpoint)
        except RuntimeError as exc:
            failures.append(str(exc))
        progress.progress(i / len(tasks), text=f"Processed {key.title()} agent")
    progress.empty()
    scope = unwrap(st.session_state.analysis.get("scope"))
    docs = unwrap(st.session_state.analysis.get("documentation"))
    deliverables = []
    if isinstance(scope, dict):
        deliverables += scope.get("major_deliverables") or scope.get("deliverables") or []
    if isinstance(docs, dict):
        deliverables += docs.get("deliverables") or []
    st.session_state.analysis["deliverables"] = {"items": deliverables}
    return failures

def json_report():
    return json.dumps({"project": st.session_state.project, "documents": st.session_state.documents,
                       "analysis": st.session_state.analysis}, indent=2, ensure_ascii=False)

st.sidebar.divider()
page = st.sidebar.radio("Project Workspace", PAGES, key="active_page")
if st.sidebar.button("＋ New Project", use_container_width=True):
    st.session_state.project = None
    st.session_state.documents = []
    st.session_state.analysis = INITIAL.copy()
    st.session_state.messages = []
    st.rerun()

if st.session_state.project:
    st.sidebar.success(st.session_state.project["projectName"])
    if st.sidebar.button("▶ Run AI Analysis", type="primary", use_container_width=True):
        with st.spinner("Running agents..."):
            errors = run_agents()
        for error in errors:
            st.error(error)
        if not errors:
            st.success("All five agents completed.")
        st.rerun()

st.markdown("""
<style>
.stApp { background: #070d19; color: #f8fafc; }
[data-testid="stSidebar"] { background: #0b1220; }
.block-container { padding-top: 2rem; }
div[data-testid="stMetric"] { background: #111b2d; border: 1px solid #273449; padding: 16px; border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

if not st.session_state.project:
    st.title("Project Intelligence Workspace")
    st.write("Create a project and upload documents to analyze scope, risks, blockers, documentation and project health.")
    with st.form("create_project"):
        left, right = st.columns(2)
        with left:
            name = st.text_input("Project name *", placeholder="AI Research Assistant")
            manager = st.text_input("Project manager")
            start = st.date_input("Start date", value=date.today())
            team_size = st.number_input("Team size", min_value=1, value=5)
        with right:
            status = st.selectbox("Status", ["Planning", "In Progress", "On Hold", "Completed"])
            deadline = st.date_input("Deadline", value=date.today())
            technology = st.text_input("Technology stack", placeholder="React, FastAPI, PostgreSQL")
        description = st.text_area("Project description")
        uploads = st.file_uploader("Project documents (PDF, DOCX, CSV, TXT)",
                                   type=["pdf", "docx", "csv", "txt"], accept_multiple_files=True)
        submitted = st.form_submit_button("Create Project", type="primary", use_container_width=True)
    if submitted:
        if not name.strip():
            st.error("Project name is required.")
        elif deadline < start:
            st.error("Deadline cannot be earlier than the start date.")
        else:
            if uploads:
                with st.spinner("Uploading documents..."):
                    try:
                        multipart = [("files", (f.name, f.getvalue(), f.type or "application/octet-stream")) for f in uploads]
                        post("/upload-multiple", files=multipart)
                    except RuntimeError as exc:
                        st.error(str(exc))
                        st.stop()
            st.session_state.project = {
                "projectName": name.strip(), "projectManager": manager.strip(),
                "startDate": start.isoformat(), "deadline": deadline.isoformat(),
                "teamSize": team_size, "status": status, "technology": technology.strip(),
                "description": description.strip(), "createdAt": date.today().isoformat()
            }
            st.session_state.documents = [f.name for f in uploads] if uploads else []
            st.session_state.analysis = INITIAL.copy()
            st.success("Project created. Run AI Analysis from the sidebar to populate results.")
            st.rerun()
else:
    project = st.session_state.project
    st.title("Current Agent Results")
    st.caption(f"{project['projectName']} · {project['status']}")

    if page == "AI Assistant":
        st.subheader("💬 Project AI Assistant")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        prompt = st.chat_input("Ask about scope, risks, deadlines, or project documents...")
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Searching project knowledge..."):
                    try:
                        result = post("/assistant/ask", json={"query": prompt, "top_k": 6})
                        answer = result.get("answer", result.get("response", result))
                        answer_text = answer if isinstance(answer, str) else json.dumps(answer, indent=2, ensure_ascii=False)
                        st.markdown(answer_text)
                        st.session_state.messages.append({"role": "assistant", "content": answer_text})
                    except RuntimeError as exc:
                        st.error(str(exc))
        st.stop()

    if page == "Health":
        data = unwrap(st.session_state.analysis.get("health"))
        score = None
        if isinstance(data, dict):
            for key in ("overall_score", "health_score", "score", "project_health_score"):
                if isinstance(data.get(key), (int, float)):
                    score = data[key]
                    break
        c1, c2, c3 = st.columns(3)
        c1.metric("Health Score", f"{score}/100" if score is not None else "Not calculated")
        c2.metric("Status", str(data.get("status", data.get("health_status", "—"))) if isinstance(data, dict) else "—")
        c3.metric("Documents", len(st.session_state.documents))
        if isinstance(data, dict) and data:
            for key, value in data.items():
                show_section(key.replace("_", " ").title(), value)
            history = data.get("health_history") or data.get("score_history") or data.get("history") or []
            if isinstance(history, list) and history:
                st.subheader("Health Score History")
                st.line_chart(pd.DataFrame(history))
        else:
            st.info("No health results yet. Click Run AI Analysis in the sidebar.")

    elif page == "Scope":
        data = unwrap(st.session_state.analysis.get("scope"))
        if isinstance(data, dict) and data:
            show_section("Project Goal", data.get("project_goal") or data.get("scope_summary") or data.get("summary"))
            show_section("Major Deliverables", data.get("major_deliverables") or data.get("deliverables"))
            show_section("Milestones", data.get("milestones"))
            show_section("Deadlines", data.get("deadlines") or data.get("important_project_dates"))
            show_section("Team Responsibilities", data.get("team_responsibilities"))
            with st.expander("Raw backend response"):
                st.json(data)
        else:
            st.info("No scope results yet. Click Run AI Analysis.")

    elif page == "Deliverables":
        scope, docs = unwrap(st.session_state.analysis.get("scope")), unwrap(st.session_state.analysis.get("documentation"))
        items = []
        if isinstance(scope, dict):
            items += scope.get("major_deliverables") or scope.get("deliverables") or []
        if isinstance(docs, dict):
            items += docs.get("deliverables") or []
        if items:
            show_section("Deliverables", items)
        else:
            st.info("No deliverables found yet. Run AI Analysis.")

    elif page == "Risks":
        data = unwrap(st.session_state.analysis.get("risk"))
        if isinstance(data, dict) and data:
            for key, value in data.items():
                show_section(key.replace("_", " ").title(), value)
            with st.expander("Raw backend response"):
                st.json(data)
        else:
            st.info("No risk results yet. Click Run AI Analysis.")

    elif page == "Blockers":
        data = unwrap(st.session_state.analysis.get("blocker"))
        if isinstance(data, dict) and data:
            for key, value in data.items():
                show_section(key.replace("_", " ").title(), value)
            with st.expander("Raw backend response"):
                st.json(data)
        else:
            st.info("No blocker results yet. Click Run AI Analysis.")

    elif page == "Documentation":
        data = unwrap(st.session_state.analysis.get("documentation"))
        if isinstance(data, dict) and data:
            for key, value in data.items():
                show_section(key.replace("_", " ").title(), value)
            with st.expander("Raw backend response"):
                st.json(data)
        else:
            st.info("No documentation results yet. Click Run AI Analysis.")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("Download Project Report (JSON)", data=json_report(),
                           file_name=f"{project['projectName'].replace(' ', '_')}_report.json",
                           mime="application/json", use_container_width=True)
    with col2:
        with st.expander("Project Details"):
            st.json(project)
            st.write("Uploaded documents:", st.session_state.documents)
