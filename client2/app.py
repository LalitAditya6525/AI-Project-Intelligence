import json
import os
from datetime import date

import pandas as pd
import requests
import streamlit as st

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="AI Intelligence | Project Advisor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = os.getenv("FASTAPI_BASE_URL", "http://localhost:8000").rstrip("/")

PAGES = [
    "Health",
    "Scope",
    "Deliverables",
    "Risks",
    "Blockers",
    "Documentation",
    "AI Assistant",
]

AGENT_ENDPOINTS = {
    "scope": "/agents/scope",
    "risk": "/agents/risk",
    "blocker": "/agents/blocker",
    "documentation": "/agents/documentation",
    "health": "/agents/health",
}

INITIAL_ANALYSIS = {
    "health": None,
    "scope": None,
    "risk": None,
    "blocker": None,
    "documentation": None,
    "deliverables": None,
}

# --------------------------------------------------
# SaaS dashboard styling
# --------------------------------------------------
st.markdown(
    """
    <style>
    :root {
        --background: #070d19;
        --panel: #0c172a;
        --panel-light: #101e34;
        --border: #203653;
        --text: #edf3ff;
        --muted: #91a5c5;
        --purple: #6d6aff;
        --blue: #4268f5;
        --teal: #18d6b0;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 75% 0%,
            #111e3c 0%, #070d19 48%);
        color: var(--text);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1426, #081120);
        border-right: 1px solid var(--border);
    }

    .block-container {
        max-width: 1600px;
        padding-top: 1.4rem;
        padding-bottom: 2.5rem;
    }

    h1, h2, h3 {
        color: #f2f6ff !important;
        letter-spacing: -0.025em;
    }

    p, label {
        color: #d9e5fb;
    }

    .brand {
        padding: 0.5rem 0.25rem 1.3rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1.3rem;
    }

    .brand-name {
        color: #f4f7ff;
        font-size: 1.2rem;
        font-weight: 800;
    }

    .brand-subtitle {
        color: #9bb0d1;
        font-size: 0.82rem;
    }

    .hero {
        padding: 1.25rem 1.5rem;
        border: 1px solid #293f78;
        border-radius: 18px;
        margin-bottom: 1.2rem;
        background: linear-gradient(
            115deg,
            rgba(67, 69, 177, 0.32),
            rgba(14, 30, 55, 0.94) 65%,
            rgba(15, 68, 78, 0.25)
        );
    }

    .hero-kicker {
        color: #aab7ff;
        font-size: 0.74rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    .hero-title {
        color: #f4f7ff;
        font-size: 1.7rem;
        font-weight: 800;
        margin: 0.4rem 0;
    }

    .hero-subtitle {
        color: #a8bad8;
        font-size: 0.92rem;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #101f36, #0a1527);
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 18px;
        min-height: 120px;
    }

    div[data-testid="stMetricLabel"] {
        color: #9fb3d4;
    }

    div[data-testid="stMetricValue"] {
        color: #f3f7ff;
        font-weight: 800;
    }

    .panel {
        background: linear-gradient(145deg, #101d32, #0a1526);
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 1.1rem 1.2rem;
        margin-bottom: 0.8rem;
    }

    .panel-title {
        color: #f3f7ff;
        font-weight: 750;
        font-size: 1rem;
    }

    .panel-description {
        color: var(--muted);
        font-size: 0.82rem;
        margin-top: 0.35rem;
    }

    .status-pill {
        display: inline-block;
        padding: 0.25rem 0.7rem;
        border-radius: 99px;
        font-size: 0.75rem;
        font-weight: 750;
        background: #08372f;
        color: #71f0d4;
        border: 1px solid #11634f;
    }

    .insight {
        background: linear-gradient(
            110deg,
            rgba(63, 59, 174, 0.35),
            rgba(12, 30, 57, 0.95)
        );
        border: 1px solid #3c4bb3;
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        margin: 1rem 0;
    }

    .insight-title {
        color: #c4c6ff;
        font-weight: 800;
        font-size: 1.05rem;
    }

    .stButton > button,
    .stDownloadButton > button,
    [data-testid="stFormSubmitButton"] > button {
        border-radius: 10px;
        min-height: 2.65rem;
        background: linear-gradient(115deg, #655cf6, #4268f5);
        color: white;
        border: 1px solid #3b55a5;
        font-weight: 650;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        border-color: #a3a0ff;
        filter: brightness(1.08);
    }

    .stTextInput input,
    .stTextArea textarea,
    .stDateInput input,
    .stNumberInput input {
        background: #091426 !important;
        color: #f3f7ff !important;
        border-color: #263b5a !important;
        border-radius: 9px !important;
    }

    [data-testid="stFileUploader"] {
        background: #0a1628;
        border: 1px dashed #3b5276;
        border-radius: 13px;
        padding: 10px;
    }

    [data-testid="stExpander"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        background: rgba(12, 23, 42, 0.8);
    }

    hr {
        border-color: var(--border) !important;
    }

    @media (max-width: 800px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero-title {
            font-size: 1.35rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Session state
# --------------------------------------------------
defaults = {
    "project": None,
    "documents": [],
    "analysis": INITIAL_ANALYSIS.copy(),
    "messages": [],
    "active_page": "Health",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# API utilities
# --------------------------------------------------
def api_post(endpoint, **kwargs):
    try:
        response = requests.post(
            f"{st.session_state.api_url.rstrip('/')}{endpoint}",
            timeout=180,
            **kwargs,
        )
        response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            return {"response_text": response.text}

    except requests.RequestException as exc:
        detail = ""
        if getattr(exc, "response", None) is not None:
            detail = exc.response.text[:400]

        raise RuntimeError(
            f"Request failed at {endpoint}: {exc} {detail}"
        ) from exc


def unwrap(data):
    for _ in range(3):
        if isinstance(data, dict) and isinstance(data.get("result"), dict):
            data = data["result"]
        else:
            break
    return data


def get_score(data):
    if not isinstance(data, dict):
        return None

    for key in (
        "overall_score",
        "health_score",
        "score",
        "project_health_score",
    ):
        value = data.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return value

    return None


def show_section(title, value):
    if value is None or value == "" or value == [] or value == {}:
        return

    st.markdown(f"#### {title}")

    if isinstance(value, list):
        for index, item in enumerate(value, 1):
            if isinstance(item, dict):
                heading = (
                    item.get("title")
                    or item.get("name")
                    or item.get("description")
                    or f"Item {index}"
                )
                with st.expander(str(heading)):
                    st.json(item)
            else:
                st.markdown(f"- {item}")

    elif isinstance(value, dict):
        st.json(value)

    else:
        st.write(value)


def render_agent(data, empty_message):
    data = unwrap(data)

    if isinstance(data, dict) and data:
        for key, value in data.items():
            show_section(key.replace("_", " ").title(), value)

        with st.expander("View raw backend response"):
            st.json(data)

    elif data:
        st.write(data)

    else:
        st.info(empty_message)


def run_analysis():
    errors = []
    progress = st.progress(0, text="Starting AI agents...")

    tasks = list(AGENT_ENDPOINTS.items())

    for index, (agent, endpoint) in enumerate(tasks, start=1):
        try:
            st.session_state.analysis[agent] = api_post(endpoint)
        except RuntimeError as exc:
            errors.append(str(exc))

        progress.progress(
            index / len(tasks),
            text=f"Processed {agent.title()} agent",
        )

    progress.empty()

    scope = unwrap(st.session_state.analysis.get("scope"))
    docs = unwrap(st.session_state.analysis.get("documentation"))

    deliverables = []

    if isinstance(scope, dict):
        items = scope.get("major_deliverables") or scope.get("deliverables") or []
        deliverables.extend(items if isinstance(items, list) else [items])

    if isinstance(docs, dict):
        items = docs.get("deliverables") or []
        deliverables.extend(items if isinstance(items, list) else [items])

    st.session_state.analysis["deliverables"] = {
        "items": deliverables
    }

    return errors


def hero(title, subtitle, icon="✦"):
    project = st.session_state.project
    project_name = project["projectName"] if project else "New project"

    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-kicker">{icon} &nbsp; PROJECT INTELLIGENCE</div>
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
            <div style="color:#91a5c5;font-size:.82rem;margin-top:.7rem">
                📁 {project_name}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div style="font-size:2rem">🧠</div>
            <div class="brand-name">AI Intelligence</div>
            <div class="brand-subtitle">Project & Risk Advisor</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("PROJECT WORKSPACE")

    st.radio(
        "Navigation",
        PAGES,
        key="active_page",
        label_visibility="collapsed",
    )

    st.divider()

    st.text_input(
        "FastAPI Base URL",
        value=st.session_state.get("api_url", API_URL),
        key="api_url",
        help="Address of your running FastAPI backend",
    )

    if st.button("＋  New Project", use_container_width=True):
        st.session_state.project = None
        st.session_state.documents = []
        st.session_state.analysis = INITIAL_ANALYSIS.copy()
        st.session_state.messages = []
        st.rerun()

    if st.session_state.project:
        project = st.session_state.project

        st.markdown("**CURRENT PROJECT**")
        st.markdown(
            f"""
            <div class="panel">
                <div class="panel-title">📁 {project["projectName"]}</div>
                <div style="margin-top:.6rem">
                    <span class="status-pill">{project["status"]}</span>
                </div>
                <div class="panel-description">📅 Due {project["deadline"]}</div>
                <div class="panel-description">
                    📄 {len(st.session_state.documents)} document(s)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "▶  Run AI Analysis",
            type="primary",
            use_container_width=True,
        ):
            with st.spinner("Running project agents..."):
                errors = run_analysis()

            for error in errors:
                st.error(error)

            if not errors:
                st.success("All five agents completed.")

            st.rerun()

    st.caption("Powered by your FastAPI backend")


# --------------------------------------------------
# Project creation
# --------------------------------------------------
page = st.session_state.active_page
project = st.session_state.project

if not project:
    hero(
        "Project Intelligence Workspace",
        "Create a project workspace to analyze its scope, risks, blockers, and health.",
    )

    left, right = st.columns([1.3, 0.8], gap="large")

    with left:
        st.markdown("### Create a project")
        st.caption("Enter project details and upload supporting documents.")

        with st.form("create_project"):
            name = st.text_input(
                "Project name *",
                placeholder="AI Research Assistant",
            )
            manager = st.text_input(
                "Project manager",
                placeholder="Name or team",
            )

            c1, c2 = st.columns(2)

            with c1:
                start = st.date_input("Start date", value=date.today())
                team_size = st.number_input(
                    "Team size",
                    min_value=1,
                    value=5,
                )
                status = st.selectbox(
                    "Project status",
                    ["Planning", "In Progress", "On Hold", "Completed"],
                )

            with c2:
                deadline = st.date_input("Target deadline", value=date.today())
                technology = st.text_input(
                    "Technology stack",
                    placeholder="React, FastAPI, PostgreSQL",
                )

            description = st.text_area(
                "Project description",
                placeholder="What are you building, and what outcomes do you expect?",
                height=100,
            )

            uploads = st.file_uploader(
                "Project documents",
                type=["pdf", "docx", "csv", "txt"],
                accept_multiple_files=True,
            )

            submitted = st.form_submit_button(
                "Create Project Workspace  →",
                type="primary",
                use_container_width=True,
            )

        if submitted:
            if not name.strip():
                st.error("Project name is required.")

            elif deadline < start:
                st.error("Deadline cannot be earlier than the start date.")

            else:
                if uploads:
                    multipart = [
                        (
                            "files",
                            (
                                file.name,
                                file.getvalue(),
                                file.type or "application/octet-stream",
                            ),
                        )
                        for file in uploads
                    ]

                    with st.spinner("Uploading documents..."):
                        try:
                            api_post("/upload-multiple", files=multipart)
                        except RuntimeError as exc:
                            st.error(str(exc))
                            st.stop()

                st.session_state.project = {
                    "projectName": name.strip(),
                    "projectManager": manager.strip(),
                    "startDate": start.isoformat(),
                    "deadline": deadline.isoformat(),
                    "teamSize": int(team_size),
                    "status": status,
                    "technology": technology.strip(),
                    "description": description.strip(),
                    "createdAt": date.today().isoformat(),
                }

                st.session_state.documents = (
                    [file.name for file in uploads] if uploads else []
                )
                st.session_state.analysis = INITIAL_ANALYSIS.copy()
                st.rerun()

    with right:
        st.markdown("### What you’ll get")

        benefits = [
            ("💚", "Project health", "Health score and status summary."),
            ("🎯", "Scope intelligence", "Goals, milestones, and deliverables."),
            ("⚠️", "Risk detection", "Potential risks and blockers."),
            ("📚", "Documentation insights", "Requirements and action items."),
            ("💬", "AI assistant", "Ask questions about project knowledge."),
        ]

        for icon, title, description in benefits:
            st.markdown(
                f"""
                <div class="panel">
                    <div class="panel-title">{icon} &nbsp; {title}</div>
                    <div class="panel-description">{description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.info(
            "Start your FastAPI backend first. "
            "Default address: http://localhost:8000"
        )

    st.stop()


# --------------------------------------------------
# Health dashboard
# --------------------------------------------------
if page == "Health":
    data = unwrap(st.session_state.analysis.get("health"))
    risk = unwrap(st.session_state.analysis.get("risk"))

    hero(
        "Project Health",
        "Overall project health, important signals, and recommended next steps.",
        "♥",
    )

    score = get_score(data)

    project_status = (
        data.get("status", data.get("health_status", project["status"]))
        if isinstance(data, dict)
        else project["status"]
    )

    risk_level = "Not assessed"

    if isinstance(risk, dict):
        risk_level = risk.get(
            "overall_risk_level",
            risk.get("risk_level", risk.get("severity", "Assessed")),
        )

    deliverables = (
        st.session_state.analysis.get("deliverables") or {}
    ).get("items", [])

    c1, c2, c3, c4 = st.columns(4, gap="medium")

    c1.metric(
        "Health Score",
        f"{score:g}/100" if score is not None else "—",
        "AI assessed" if score is not None else "Not calculated",
    )

    c2.metric(
        "Project Status",
        str(project_status),
        "Current project",
    )

    c3.metric(
        "Key Risk Level",
        str(risk_level),
        "From risk agent" if risk_level != "Not assessed" else "Not assessed",
    )

    c4.metric(
        "Documents",
        len(st.session_state.documents),
        f"{len(deliverables)} deliverables identified",
    )

    st.write("")

    left, right = st.columns([1.25, 1], gap="large")

    with left:
        st.markdown("### Health Analysis")

        if isinstance(data, dict) and data:
            for key, value in data.items():
                show_section(key.replace("_", " ").title(), value)

            history = (
                data.get("health_history")
                or data.get("score_history")
                or data.get("history")
                or []
            )

            if isinstance(history, list) and history:
                st.markdown("### Health Score Trend")
                try:
                    frame = pd.DataFrame(history)
                    if not frame.empty:
                        st.line_chart(frame)
                except (ValueError, TypeError):
                    st.caption("Trend data could not be displayed.")

            with st.expander("View raw health response"):
                st.json(data)

        else:
            st.info(
                "No health results yet. Select **Run AI Analysis** "
                "in the sidebar to calculate project health."
            )

    with right:
        st.markdown("### Agent Status")

        for key, title in [
            ("scope", "Scope analysis"),
            ("risk", "Risk analysis"),
            ("blocker", "Blocker analysis"),
            ("documentation", "Documentation analysis"),
            ("health", "Health analysis"),
        ]:
            completed = bool(st.session_state.analysis.get(key))
            color = "#18d6b0" if completed else "#7e90ad"
            text = "Completed" if completed else "Pending"

            st.markdown(
                f"""
                <div class="panel" style="padding:.8rem 1rem">
                    <span style="color:{color}">●</span>
                    <b>{title}</b>
                    <span style="float:right;color:{color};font-size:.8rem">
                        {text}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div class="insight">
                <div class="insight-title">✧ AI Insight</div>
                <div class="panel-description" style="font-size:.9rem">
                    Run the agents to identify strengths, concerns, and
                    practical next steps for your project.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("💬  Ask AI Assistant", use_container_width=True):
            st.session_state.active_page = "AI Assistant"
            st.rerun()


# --------------------------------------------------
# Scope page
# --------------------------------------------------
elif page == "Scope":
    hero(
        "Scope & Milestones",
        "Review project goals, delivery plans, deadlines, and ownership.",
        "◎",
    )

    data = unwrap(st.session_state.analysis.get("scope"))

    if isinstance(data, dict) and data:
        show_section(
            "Project Goal",
            data.get("project_goal")
            or data.get("scope_summary")
            or data.get("summary"),
        )

        left, right = st.columns(2, gap="large")

        with left:
            show_section(
                "Major Deliverables",
                data.get("major_deliverables") or data.get("deliverables"),
            )
            show_section("Milestones", data.get("milestones"))

        with right:
            show_section(
                "Deadlines & Important Dates",
                data.get("deadlines") or data.get("important_project_dates"),
            )
            show_section(
                "Team Responsibilities",
                data.get("team_responsibilities"),
            )

        with st.expander("View raw scope response"):
            st.json(data)

    else:
        st.info("No scope results yet. Run AI Analysis to populate this page.")


# --------------------------------------------------
# Deliverables page
# --------------------------------------------------
elif page == "Deliverables":
    hero(
        "Deliverables",
        "Review outputs identified by scope and documentation analysis.",
        "⬡",
    )

    scope = unwrap(st.session_state.analysis.get("scope"))
    docs = unwrap(st.session_state.analysis.get("documentation"))

    items = []

    if isinstance(scope, dict):
        value = scope.get("major_deliverables") or scope.get("deliverables") or []
        items.extend(value if isinstance(value, list) else [value])

    if isinstance(docs, dict):
        value = docs.get("deliverables") or []
        items.extend(value if isinstance(value, list) else [value])

    if items:
        st.metric("Identified Deliverables", len(items))
        show_section("Delivery Items", items)
    else:
        st.info("No deliverables found yet. Run AI Analysis first.")


# --------------------------------------------------
# Risks, blockers, and documentation
# --------------------------------------------------
elif page == "Risks":
    hero(
        "Risk Register",
        "Review risks identified by the risk analysis agent.",
        "⚠",
    )
    render_agent(
        st.session_state.analysis.get("risk"),
        "No risk results yet. Run AI Analysis to assess project risks.",
    )

elif page == "Blockers":
    hero(
        "Blockers & Dependencies",
        "Identify issues that could delay progress or require escalation.",
        "!",
    )
    render_agent(
        st.session_state.analysis.get("blocker"),
        "No blocker results yet. Run AI Analysis to identify blockers.",
    )

elif page == "Documentation":
    hero(
        "Documentation Insights",
        "Explore requirements, user stories, action items, and extracted notes.",
        "▤",
    )
    render_agent(
        st.session_state.analysis.get("documentation"),
        "No documentation results yet. Run AI Analysis to process project documents.",
    )


# --------------------------------------------------
# AI assistant
# --------------------------------------------------
elif page == "AI Assistant":
    hero(
        "Project AI Assistant",
        "Ask questions about scope, risks, deadlines, blockers, and documents.",
        "✧",
    )

    st.markdown("#### Suggested Questions")

    suggestions = [
        "What are the biggest project risks?",
        "Summarize the project scope",
        "Which deadlines need attention?",
    ]

    cols = st.columns(3)

    for index, suggestion in enumerate(suggestions):
        if cols[index].button(suggestion, use_container_width=True):
            st.session_state.pending_prompt = suggestion
            st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask something about your project...")

    if not prompt and st.session_state.get("pending_prompt"):
        prompt = st.session_state.pop("pending_prompt")

    if prompt:
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching project knowledge..."):
                try:
                    result = api_post(
                        "/assistant/ask",
                        json={"query": prompt, "top_k": 6},
                    )

                    answer = (
                        result.get("answer", result.get("response", result))
                        if isinstance(result, dict)
                        else result
                    )

                    answer_text = (
                        answer
                        if isinstance(answer, str)
                        else json.dumps(answer, indent=2, ensure_ascii=False)
                    )

                    st.markdown(answer_text)

                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer_text}
                    )

                except RuntimeError as exc:
                    st.error(str(exc))


# --------------------------------------------------
# Footer tools
# --------------------------------------------------
st.divider()

left, right = st.columns(2, gap="medium")

with left:
    st.download_button(
        "↓  Download Project Report (JSON)",
        data=json.dumps(
            {
                "project": project,
                "documents": st.session_state.documents,
                "analysis": st.session_state.analysis,
            },
            indent=2,
            ensure_ascii=False,
            default=str,
        ),
        file_name=f"{project['projectName'].replace(' ', '_')}_report.json",
        mime="application/json",
        use_container_width=True,
    )

with right:
    with st.expander("Project Details & Uploaded Documents"):
        st.json(project)
        st.write("Uploaded documents:", st.session_state.documents)
