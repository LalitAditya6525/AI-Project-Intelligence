import io
import json
import os
import re
from datetime import datetime
from xml.sax.saxutils import escape

import requests
import streamlit as st

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Intelligence & Risk Advisor",
    page_icon="🧭",
    layout="wide",
)

API_URL = os.getenv(
    "FASTAPI_BASE_URL",
    "http://localhost:8000"
)

SUPPORTED_TYPES = ["pdf", "docx", "csv", "txt"]


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>
.stApp {
    background-color: #07111f;
    color: #e5edf8;
}

[data-testid="stSidebar"] {
    background-color: #0b1728;
    border-right: 1px solid #1b2a40;
}

.block-container {
    padding-top: 1.5rem;
    max-width: 1450px;
}

.hero {
    padding: 1.3rem 1.5rem;
    border: 1px solid #20334d;
    border-radius: 18px;
    background: linear-gradient(
        120deg,
        #10223b,
        #111a32,
        #17234a
    );
    margin-bottom: 1rem;
}

.hero h1 {
    margin: 0;
    color: #f4f8ff;
    font-size: 1.8rem;
}

.hero p {
    margin-top: 0.5rem;
    color: #aabbd2;
}

div[data-testid="stMetric"] {
    background: #0d1b2d;
    border: 1px solid #1d3048;
    padding: 14px;
    border-radius: 14px;
}

div[data-testid="stChatMessage"] {
    background: #0c1a2b;
    border: 1px solid #1c2d43;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# API HELPERS
# =========================================================

def make_url(path):
    return f"{API_URL.rstrip('/')}/{path.lstrip('/')}"


def parse_response(response):
    try:
        return response.json()
    except ValueError:
        return response.text


def api_request(method, path, **kwargs):
    try:
        response = requests.request(
            method,
            make_url(path),
            timeout=180,
            **kwargs
        )

        if not response.ok:
            detail = parse_response(response)

            st.error(
                f"Backend error: HTTP {response.status_code}"
            )

            st.caption(readable(detail))
            return None

        return parse_response(response)

    except requests.RequestException as exc:
        st.error(
            f"Could not connect to FastAPI at {API_URL}."
        )
        st.caption(str(exc))
        return None


# =========================================================
# JSON-TO-TEXT FORMATTING
# =========================================================

def unwrap(data):
    """Remove common nested result wrappers."""
    for _ in range(4):
        if (
            isinstance(data, dict)
            and isinstance(
                data.get("result"),
                (dict, list, str)
            )
        ):
            data = data["result"]
        else:
            break

    return data


def humanize_key(key):
    key = re.sub(
        r"([a-z0-9])([A-Z])",
        r"\1 \2",
        str(key)
    )

    return key.replace("_", " ").strip().capitalize()


def readable(data):
    """
    Convert JSON dictionaries and lists into readable
    headings, sentences, and bullet points.
    """

    data = unwrap(data)

    if data is None:
        return "No information was returned."

    if isinstance(data, str):
        text = data.strip()

        if text.startswith(("{", "[")):
            try:
                return readable(json.loads(text))
            except json.JSONDecodeError:
                pass

        return text

    if isinstance(data, (int, float, bool)):
        return str(data)

    if isinstance(data, list):
        lines = []

        for item in data:
            item_text = readable(item)

            if item_text:
                lines.append(f"- {item_text}")

        return "\n".join(lines) or "No information was returned."

    if isinstance(data, dict):

        # Prefer natural-language answer fields.
        preferred_keys = [
            "answer",
            "response",
            "message",
            "summary",
            "text",
            "content",
            "explanation",
        ]

        for key in preferred_keys:
            if data.get(key) not in (None, ""):
                main_text = readable(data[key])

                additional = []

                for other_key, value in data.items():
                    if (
                        other_key != key
                        and value not in (None, "", [], {})
                    ):
                        additional.append(
                            f"**{humanize_key(other_key)}:** "
                            f"{readable(value)}"
                        )

                if additional:
                    return (
                        main_text
                        + "\n\n"
                        + "\n\n".join(additional)
                    )

                return main_text

        lines = []

        for key, value in data.items():

            if value in (None, "", [], {}):
                continue

            label = humanize_key(key)

            if isinstance(value, list):
                lines.append(f"**{label}**")

                for item in value:
                    lines.append(f"- {readable(item)}")

            elif isinstance(value, dict):
                lines.append(f"**{label}**")
                lines.append(readable(value))

            else:
                lines.append(
                    f"**{label}:** {readable(value)}"
                )

        return "\n\n".join(lines) or "No information was returned."

    return str(data)


def extract_answer(data):
    """Extract the chatbot's answer from common response shapes."""

    data = unwrap(data)

    if isinstance(data, dict):
        for key in [
            "answer",
            "response",
            "message",
            "output",
            "text",
            "content",
        ]:
            value = data.get(key)

            if isinstance(value, str) and value.strip():
                return value.strip()

    return readable(data)


# =========================================================
# DATA HELPERS
# =========================================================

def extract_items(data):
    data = unwrap(data)

    if data is None:
        return []

    if isinstance(data, list):
        return data

    if isinstance(data, dict):

        for key in [
            "risks",
            "items",
            "blockers",
            "deliverables",
            "major_deliverables",
            "actions",
        ]:
            if isinstance(data.get(key), list):
                return data[key]

        return [data]

    if isinstance(data, str):
        try:
            return extract_items(json.loads(data))
        except json.JSONDecodeError:
            return [
                line.strip(" •-\t")
                for line in data.splitlines()
                if line.strip()
            ]

    return [data]


def get_field(item, *keys, default=""):
    if not isinstance(item, dict):
        return item if item is not None else default

    values = {
        str(key).lower(): value
        for key, value in item.items()
    }

    for key in keys:
        value = values.get(key.lower())

        if value not in (None, ""):
            return value

    return default


# =========================================================
# RISK SORTING
# =========================================================

def severity_rank(item):
    severity = str(
        get_field(
            item,
            "severity",
            "risk_level",
            "priority",
            "impact",
            "level",
            default="medium",
        )
    ).lower()

    if any(
        word in severity
        for word in [
            "critical",
            "very high",
            "urgent",
            "severe",
        ]
    ):
        return 5

    if "high" in severity:
        return 4

    if "medium" in severity or "moderate" in severity:
        return 3

    if "low" in severity:
        return 2

    try:
        score = float(severity)

        if score >= 8:
            return 5
        elif score >= 6:
            return 4
        elif score >= 4:
            return 3
        elif score >= 2:
            return 2
        else:
            return 1

    except ValueError:
        return 3


def sort_risks(risks):
    return sorted(
        risks,
        key=severity_rank,
        reverse=True
    )


# =========================================================
# PDF REPORT GENERATION
# =========================================================

def create_pdf(title, sections, subtitle=None):
    buffer = io.BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=17 * mm,
        bottomMargin=18 * mm,
        title=title,
    )

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontSize=20,
            leading=25,
            textColor=colors.HexColor("#17365d"),
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="ReportSubtitle",
            parent=styles["Normal"],
            fontSize=9,
            textColor=colors.HexColor("#617087"),
            alignment=TA_CENTER,
            spaceAfter=16,
        )
    )

    styles.add(
        ParagraphStyle(
            name="ReportHeading",
            parent=styles["Heading2"],
            fontSize=13,
            leading=17,
            textColor=colors.HexColor("#174a7e"),
            spaceBefore=10,
            spaceAfter=6,
        )
    )

    styles.add(
        ParagraphStyle(
            name="ReportBody",
            parent=styles["BodyText"],
            fontSize=9.5,
            leading=14,
            spaceAfter=6,
            textColor=colors.HexColor("#243247"),
        )
    )

    story = [
        Paragraph(
            escape(title),
            styles["ReportTitle"]
        ),
        Paragraph(
            escape(
                subtitle
                or f"Generated on {datetime.now():%d %b %Y, %H:%M}"
            ),
            styles["ReportSubtitle"],
        ),
    ]

    for heading, content in sections:

        story.append(
            Paragraph(
                escape(heading),
                styles["ReportHeading"]
            )
        )

        content = unwrap(content)

        if content in (None, "", [], {}):
            story.append(
                Paragraph(
                    "No information is available for this section.",
                    styles["ReportBody"],
                )
            )
            continue

        if isinstance(content, dict):

            for key, value in content.items():

                if value in (None, "", [], {}):
                    continue

                text = readable(value).replace("\n", "<br/>")
                text = escape(text).replace(
                    "&lt;br/&gt;",
                    "<br/>"
                )

                story.append(
                    Paragraph(
                        f"<b>{escape(humanize_key(key))}:</b> {text}",
                        styles["ReportBody"],
                    )
                )

        elif isinstance(content, list):

            for index, item in enumerate(content, 1):

                text = readable(item).replace("\n", "<br/>")
                text = escape(text).replace(
                    "&lt;br/&gt;",
                    "<br/>"
                )

                story.append(
                    Paragraph(
                        f"{index}. {text}",
                        styles["ReportBody"],
                    )
                )

        else:
            text = readable(content).replace("\n", "<br/>")
            text = escape(text).replace(
                "&lt;br/&gt;",
                "<br/>"
            )

            story.append(
                Paragraph(
                    text,
                    styles["ReportBody"]
                )
            )

    def footer(canvas, doc):
        canvas.saveState()

        canvas.setStrokeColor(
            colors.HexColor("#d9e2ef")
        )

        canvas.line(
            18 * mm,
            13 * mm,
            A4[0] - 18 * mm,
            13 * mm,
        )

        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(
            colors.HexColor("#718096")
        )

        canvas.drawString(
            18 * mm,
            8 * mm,
            "AI Intelligence & Risk Advisor",
        )

        canvas.drawRightString(
            A4[0] - 18 * mm,
            8 * mm,
            f"Page {doc.page}",
        )

        canvas.restoreState()

    document.build(
        story,
        onFirstPage=footer,
        onLaterPages=footer,
    )

    return buffer.getvalue()


def pdf_download_button(label, filename, title, data, key):
    pdf = create_pdf(
        title,
        [(title, data)]
    )

    st.download_button(
        label=label,
        data=pdf,
        file_name=filename,
        mime="application/pdf",
        key=key,
    )


# =========================================================
# RENDERING HELPER
# =========================================================

def render_section(title, data):
    st.subheader(title)

    data = unwrap(data)

    if isinstance(data, dict):

        for key, value in data.items():

            if value in (None, "", [], {}):
                continue

            st.markdown(f"**{humanize_key(key)}**")

            if isinstance(value, list):
                for item in value:
                    st.markdown(f"- {readable(item)}")
            else:
                st.markdown(readable(value))

    elif isinstance(data, list):

        for item in data:
            st.markdown(f"- {readable(item)}")

    else:
        st.markdown(readable(data))


# =========================================================
# SESSION STATE
# =========================================================

if "analysis" not in st.session_state:
    st.session_state.analysis = {}

if "uploaded_names" not in st.session_state:
    st.session_state.uploaded_names = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:

    st.markdown("## 🧭 AI Risk Advisor")

    st.caption("Document-grounded project intelligence")

    page = st.radio(
        "Navigation",
        [
            "Upload Documents",
            "Health",
            "Scope & Deliverables",
            "Risks",
            "Blockers",
            "Documentation",
            "Chatbot",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("**Backend connection**")

    API_URL = st.text_input(
        "FastAPI URL",
        value=API_URL,
    ).strip()

    if not API_URL:
        API_URL = "http://localhost:8000"

    if st.button(
        "Test connection",
        use_container_width=True,
    ):
        result = api_request("GET", "/health")

        if result is not None:
            st.success("FastAPI is reachable.")

    st.caption(
        "Run backend: uvicorn main:app --reload --port 8000"
    )


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">
        <h1>AI Intelligence &amp; Risk Advisor</h1>
        <p>
            Upload documents to extract scope, identify risks,
            review blockers, generate documentation, and ask
            questions grounded in your files.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

analysis = st.session_state.analysis


# =========================================================
# PAGE 1: DOCUMENT UPLOAD
# No project details form
# =========================================================

if page == "Upload Documents":

    col1, col2 = st.columns([1.5, 1])

    with col1:

        st.subheader("Upload project documents")

        st.write(
            "Upload one or more files to start the analysis."
        )

        uploaded_files = st.file_uploader(
            "Choose files",
            type=SUPPORTED_TYPES,
            accept_multiple_files=True,
        )

        st.caption(
            "Supported formats: PDF, DOCX, CSV, TXT"
        )

        submit = st.button(
            "Upload and analyze documents",
            type="primary",
            use_container_width=True,
            disabled=not uploaded_files,
        )

    with col2:

        st.subheader("What you’ll get")

        st.markdown(
            "- Project health assessment\n"
            "- Scope and deliverables\n"
            "- Risks sorted from high to low\n"
            "- Blockers and suggested actions\n"
            "- Project documentation as a PDF\n"
            "- A separate chatbot for questions"
        )

        if st.session_state.uploaded_names:

            st.divider()
            st.markdown("**Uploaded this session**")

            for filename in st.session_state.uploaded_names:
                st.markdown(f"- {filename}")

    if submit and uploaded_files:

        files = [
            (
                "files",
                (
                    file.name,
                    file.getvalue(),
                    file.type or "application/octet-stream",
                ),
            )
            for file in uploaded_files
        ]

        with st.spinner("Uploading documents..."):

            upload_result = api_request(
                "POST",
                "/upload-multiple",
                files=files,
            )

        if upload_result is not None:

            st.session_state.uploaded_names = [
                file.name for file in uploaded_files
            ]

            st.success("Documents uploaded successfully.")

            endpoints = [
                ("scope", "/agents/scope"),
                ("risk", "/agents/risk"),
                ("blocker", "/agents/blocker"),
                ("documentation", "/agents/documentation"),
                ("health", "/agents/health"),
            ]

            results = {}
            failures = []

            progress = st.progress(
                0,
                text="Analyzing documents..."
            )

            for index, (name, endpoint) in enumerate(
                endpoints,
                start=1,
            ):

                result = api_request(
                    "POST",
                    endpoint,
                )

                if result is not None:
                    results[name] = result
                else:
                    failures.append(name)

                progress.progress(
                    index / len(endpoints),
                    text=f"Analyzed {name.title()}...",
                )

            progress.empty()

            st.session_state.analysis = results
            st.session_state.analysis_done = bool(results)
            st.session_state.chat_history = []

            if results:
                st.success(
                    "Analysis complete. Use the sidebar to review results."
                )

            if failures:
                st.warning(
                    "Could not complete: "
                    + ", ".join(failures)
                )

    if st.session_state.analysis_done:

        st.info(
            f"Analysis is ready for "
            f"{len(st.session_state.uploaded_names)} document(s)."
        )


# =========================================================
# PAGE 2: HEALTH
# =========================================================

elif page == "Health":

    data = analysis.get("health")

    if data is None:
        st.info("Upload documents first to calculate project health.")

    else:

        raw = unwrap(data)
        score = None

        if isinstance(raw, dict):

            for key in [
                "overall_score",
                "health_score",
                "project_health_score",
                "score",
            ]:

                try:
                    if raw.get(key) is not None:
                        score = float(raw[key])
                        break
                except (ValueError, TypeError):
                    pass

        if score is not None:

            st.metric(
                "Health score",
                f"{score:g}/100" if score > 1 else f"{score:g}",
            )

            st.progress(
                max(
                    0,
                    min(
                        1,
                        score / 100 if score > 1 else score
                    ),
                )
            )

        render_section("Health assessment", data)

        pdf_download_button(
            "Download health report (PDF)",
            "project_health_report.pdf",
            "Project Health Report",
            data,
            "health_pdf",
        )


# =========================================================
# PAGE 3: SCOPE AND DELIVERABLES
# =========================================================

elif page == "Scope & Deliverables":

    data = analysis.get("scope")

    if data is None:
        st.info("Upload documents first to extract scope and deliverables.")

    else:

        render_section("Scope and deliverables", data)

        pdf_download_button(
            "Download scope report (PDF)",
            "scope_deliverables.pdf",
            "Scope and Deliverables",
            data,
            "scope_pdf",
        )


# =========================================================
# PAGE 4: RISKS
# Sorted from highest to lowest
# =========================================================

elif page == "Risks":

    data = analysis.get("risk")

    if data is None:
        st.info("Upload documents first to identify risks.")

    else:

        risks = sort_risks(extract_items(data))

        st.subheader("Risk register")
        st.caption("Highest severity appears first.")

        if not risks:
            st.info("No risks were returned by the risk agent.")

        for index, risk in enumerate(risks, start=1):

            name = get_field(
                risk,
                "risk",
                "title",
                "name",
                "description",
                default=f"Risk {index}",
            )

            severity = str(
                get_field(
                    risk,
                    "severity",
                    "risk_level",
                    "priority",
                    "level",
                    default="Medium",
                )
            )

            details = get_field(
                risk,
                "description",
                "impact",
                "details",
                default="",
            )

            mitigation = get_field(
                risk,
                "mitigation",
                "mitigation_strategy",
                "recommendation",
                "action",
                default="",
            )

            with st.container(border=True):

                left, right = st.columns([4, 1])

                left.markdown(
                    f"**{index}. {readable(name)}**"
                )

                if (
                    "high" in severity.lower()
                    or "critical" in severity.lower()
                ):
                    right.error(severity.upper())

                elif "low" in severity.lower():
                    right.success(severity.upper())

                else:
                    right.warning(severity.upper())

                if details:
                    st.write(readable(details))

                if mitigation:
                    st.markdown(
                        "**Recommended mitigation:** "
                        + readable(mitigation)
                    )

        pdf_download_button(
            "Download prioritized risks (PDF)",
            "prioritized_risks.pdf",
            "Prioritized Risk Register",
            risks,
            "risks_pdf",
        )


# =========================================================
# PAGE 5: BLOCKERS
# =========================================================

elif page == "Blockers":

    data = analysis.get("blocker")

    if data is None:
        st.info("Upload documents first to identify blockers.")

    else:

        render_section(
            "Blockers and recommended actions",
            data,
        )

        pdf_download_button(
            "Download blockers report (PDF)",
            "blockers_report.pdf",
            "Blockers and Recommended Actions",
            data,
            "blockers_pdf",
        )


# =========================================================
# PAGE 6: DOCUMENTATION
# Separate PDF download
# =========================================================

elif page == "Documentation":

    data = analysis.get("documentation")

    st.subheader("Project documentation")

    if data is None:
        st.info("Upload documents first to generate documentation.")

    else:

        render_section(
            "Documentation preview",
            data,
        )

        pdf = create_pdf(
            "Project Documentation",
            [
                (
                    "Project Documentation",
                    data,
                )
            ],
            subtitle=(
                "Generated from uploaded documents · "
                f"{datetime.now():%d %b %Y}"
            ),
        )

        st.download_button(
            "Download project documentation (PDF)",
            data=pdf,
            file_name="project_documentation.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True,
        )

        st.caption(
            "This is a formatted PDF report, not a JSON download."
        )


# =========================================================
# PAGE 7: CHATBOT
# Replaces the old AI Assistant page
# =========================================================

elif page == "Chatbot":

    st.subheader("Project chatbot")

    st.caption(
        "Ask questions about the documents you uploaded."
    )

    if not st.session_state.uploaded_names:
        st.info(
            "Upload documents first so the chatbot can use "
            "your project context."
        )

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input(
        "Ask about scope, risks, blockers, dependencies, or recommendations..."
    )

    if prompt:

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("Searching your documents..."):

                result = api_request(
                    "POST",
                    "/assistant/ask",
                    json={
                        "query": prompt,
                        "top_k": 6,
                    },
                )

            if result is None:

                answer = (
                    "I couldn't retrieve an answer. "
                    "Please check the FastAPI backend and try again."
                )

            else:
                answer = extract_answer(result)

            st.markdown(answer)

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        st.rerun()
