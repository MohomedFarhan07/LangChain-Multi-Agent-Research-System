import time

import streamlit as st

from src.agents.agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Researcher Agent",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Styling (minimal, neutral, single soft accent) ───────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: #0e1117; }

/* Hide default chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { max-width: 760px; padding-top: 3.5rem; padding-bottom: 7rem; }

/* Header */
.app-title {
    font-size: 2.1rem; font-weight: 700; letter-spacing: -0.02em;
    color: #f3f4f6; margin: 0;
}
.app-sub {
    font-size: 0.85rem; color: #8b919c; margin: 0.35rem 0 1.8rem;
}

/* Empty state */
.empty {
    border: 1px dashed #272c37; border-radius: 12px;
    padding: 1.6rem 1.4rem; color: #8b919c; font-size: 0.9rem;
    line-height: 1.6; margin-bottom: 1rem;
}
.empty b { color: #e5e7eb; font-weight: 500; }
.hint {
    font-size: 0.72rem; color: #6b7280; letter-spacing: 0.06em;
    text-transform: uppercase; margin: 1.2rem 0 0.5rem;
}

/* Example buttons */
.stButton > button {
    background: #161a22; color: #d1d5db; border: 1px solid #272c37;
    border-radius: 10px; font-size: 0.82rem; font-weight: 400;
    padding: 0.55rem 0.9rem; text-align: left; transition: all .15s ease;
}
.stButton > button:hover {
    border-color: #4b5563; color: #fff; background: #1a1f29;
}
.stButton > button:focus { box-shadow: none; border-color: #6b7280; color: #fff; }

/* Pipeline tracker */
.pipe { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin: 0.2rem 0 1.2rem; }
@media (max-width: 640px) { .pipe { grid-template-columns: repeat(2, 1fr); } }
.pstep {
    background: #141821; border: 1px solid #252a35; border-radius: 10px;
    padding: 0.7rem 0.85rem; transition: border-color .2s ease;
}
.pstep.running { border-color: #5b6475; }
.pstep.done    { border-color: #25362d; }
.pstep .row { display: flex; align-items: center; gap: 7px; }
.dot { width: 7px; height: 7px; border-radius: 50%; background: #3b4150; flex: none; }
.running .dot { background: #e5e7eb; animation: pulse 1.2s infinite ease-in-out; }
.done .dot    { background: #4ade80; }
@keyframes pulse { 0%,100% { opacity: .35; } 50% { opacity: 1; } }
.pstep .t { font-size: 0.83rem; font-weight: 500; color: #e5e7eb; }
.pstep .d { font-size: 0.7rem; color: #6b7280; margin-top: 0.35rem; line-height: 1.4; }
.pstep .s { font-size: 0.66rem; color: #6b7280; margin-top: 0.4rem; letter-spacing: .06em; text-transform: uppercase; }
.running .s { color: #d1d5db; }
.done .s    { color: #4ade80; }

/* Chat messages */
[data-testid="stChatMessage"] {
    background: transparent; padding: 0.6rem 0;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: #151922; border-radius: 12px; padding: 0.8rem 1rem;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 1.2rem; border-bottom: 1px solid #1f2430; }
.stTabs [data-baseweb="tab"] {
    background: transparent; color: #8b919c; font-size: 0.85rem; padding: 0.5rem 0;
}
.stTabs [aria-selected="true"] { color: #f3f4f6; }
.stTabs [data-baseweb="tab-highlight"] { background: #e5e7eb; height: 1px; }

/* Expander */
details {
    background: #11151c; border: 1px solid #1f2430 !important; border-radius: 10px;
}
details summary { font-size: 0.82rem !important; color: #9ca3af !important; }

/* Download button */
.stDownloadButton > button {
    background: #e5e7eb; color: #0e1117; border: none; border-radius: 10px;
    font-weight: 500; font-size: 0.85rem; padding: 0.55rem 1rem;
}
.stDownloadButton > button:hover { background: #fff; color: #0e1117; }

/* Chat input */
[data-testid="stChatInput"] { border-radius: 12px; }

.footer-note {
    text-align: center; font-size: 0.7rem; color: #5b6270; margin-top: 3rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# ── Pipeline definition ──────────────────────────────────────────────────────
STEPS = [
    ("search", "Search", "Gathers recent web information"),
    ("reader", "Reader", "Scrapes and extracts deep content"),
    ("writer", "Writer", "Drafts the full research report"),
    ("critic", "Critic", "Reviews and scores the report"),
]
STATE_LABEL = {"waiting": "Waiting", "running": "Running", "done": "Done"}


def step_states(results: dict, active: str | None = None) -> dict:
    states = {}
    for key, _, _ in STEPS:
        if key in results:
            states[key] = "done"
        elif key == active:
            states[key] = "running"
        else:
            states[key] = "waiting"
    return states


def pipeline_html(states: dict) -> str:
    cards = ""
    for key, title, desc in STEPS:
        state = states.get(key, "waiting")
        cards += (
            f'<div class="pstep {state}">'
            f'<div class="row"><span class="dot"></span><span class="t">{title}</span></div>'
            f'<div class="d">{desc}</div>'
            f'<div class="s">{STATE_LABEL[state]}</div>'
            f"</div>"
        )
    return f'<div class="pipe">{cards}</div>'


# ── Session state ────────────────────────────────────────────────────────────
defaults = {"topic": "", "results": {}, "needs_run": False, "error": None}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def start_research(topic: str):
    st.session_state.topic = topic.strip()
    st.session_state.results = {}
    st.session_state.needs_run = True
    st.session_state.error = None


def reset():
    st.session_state.topic = ""
    st.session_state.results = {}
    st.session_state.needs_run = False
    st.session_state.error = None


# ── Pipeline execution ───────────────────────────────────────────────────────
def run_pipeline(topic: str, slot):
    results: dict = {}

    def update(active):
        slot.markdown(pipeline_html(step_states(results, active)), unsafe_allow_html=True)

    def save():
        st.session_state.results = dict(results)

    try:
        # Step 1: Search
        update("search")
        search_agent = build_search_agent()
        sr = search_agent.invoke(
            {"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]}
        )
        results["search"] = sr["messages"][-1].content
        save()

        # Step 2: Reader
        update("reader")
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Based on the following search results about '{topic}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{results['search'][:800]}",
                    )
                ]
            }
        )
        results["reader"] = rr["messages"][-1].content
        save()

        # Step 3: Writer
        update("writer")
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({"topic": topic, "research": research_combined})
        save()

        # Step 4: Critic
        update("critic")
        results["critic"] = critic_chain.invoke({"report": results["writer"]})
        save()

        update(None)
    except Exception as e:  # surface failures instead of crashing the page
        st.session_state.error = str(e)
        update(None)


# ── Header ───────────────────────────────────────────────────────────────────
st.markdown('<p class="app-title">🔬 Researcher Agent</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="app-sub">Four AI agents search, read, write and critique to produce '
    "a research report on any topic.</p>",
    unsafe_allow_html=True,
)

# ── Input ────────────────────────────────────────────────────────────────────
EXAMPLES = [
    "Future of LLMs in the tech industry",
    "Latest AI agents in 2026",
    "Roadmap for AGI development in the next 5 years",
]

prompt = st.chat_input("Enter a research topic…")
if prompt and prompt.strip():
    start_research(prompt)

# ── Empty state ──────────────────────────────────────────────────────────────
if not st.session_state.topic:
    st.markdown(
        '<div class="empty"><b>What would you like to research?</b><br>'
        "Type a topic below, or start from an example.</div>",
        unsafe_allow_html=True,
    )
    st.markdown('<div class="hint">Try</div>', unsafe_allow_html=True)
    for i, ex in enumerate(EXAMPLES):
        st.button(ex, key=f"ex_{i}", use_container_width=True, on_click=start_research, args=(ex,))

# ── Conversation ─────────────────────────────────────────────────────────────
else:
    topic = st.session_state.topic

    with st.chat_message("user"):
        st.markdown(topic)

    with st.chat_message("assistant"):
        slot = st.empty()

        if st.session_state.needs_run:
            st.session_state.needs_run = False
            run_pipeline(topic, slot)
        else:
            slot.markdown(
                pipeline_html(step_states(st.session_state.results)),
                unsafe_allow_html=True,
            )

        if st.session_state.error:
            st.error(f"Something went wrong: {st.session_state.error}")

        r = st.session_state.results

        if "writer" in r:
            tab_names = ["Report"]
            if "critic" in r:
                tab_names.append("Critic feedback")
            if "search" in r or "reader" in r:
                tab_names.append("Sources")
            tabs = st.tabs(tab_names)
            tab_map = dict(zip(tab_names, tabs))

            with tab_map["Report"]:
                st.markdown(r["writer"])
                st.download_button(
                    "Download report (.md)",
                    data=r["writer"],
                    file_name=f"research_report_{int(time.time())}.md",
                    mime="text/markdown",
                    key="dl_report",
                )

            if "Critic feedback" in tab_map:
                with tab_map["Critic feedback"]:
                    st.markdown(r["critic"])

            if "Sources" in tab_map:
                with tab_map["Sources"]:
                    if "search" in r:
                        with st.expander("Search agent output (raw)"):
                            st.markdown(r["search"])
                    if "reader" in r:
                        with st.expander("Scraped content (raw)"):
                            st.markdown(r["reader"])

    if not st.session_state.needs_run:
        st.button("New research", on_click=reset, key="new_research")

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer-note">Powered by a LangChain multi-agent pipeline · Built with Streamlit</div>',
    unsafe_allow_html=True,
)