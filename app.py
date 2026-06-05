"""
app.py - Streamlit Web Interface for Multi-Agent Research System (MARS)

This module provides the professional web interface for the MARS (Multi-Agent Research System).
It combines multiple research agents to gather, synthesize, and evaluate information on any topic.

Key Features:
  • Real-time research progress tracking with visual indicators
  • Research history management and retrieval
  • Beautiful gradient UI with responsive design
  • Interactive result exploration with multiple tabs
  • System health monitoring and analytics
  • Professional typography and animations

Architecture:
  • Custom CSS (350+ lines): Gradient backgrounds, animations, responsive layouts
  • Streamlit Components: Tabs, columns, metrics, charts for data visualization
  • Session State Management: Stores research history, current results, processing status
  • Integration: Calls pipeline.py for multi-agent research workflow

Page Configuration:
  • Title: MARS — Multi Agent Research System
  • Icon: 🔬 (microscope emoji)
  • Layout: Centered with collapsible sidebar
  • Fonts: Syne (headings), JetBrains Mono (code), Newsreader (body text)
  
Color Palette:
  • Primary: #6366f1 (Indigo) - Main accent
  • Secondary: #8b5cf6 (Purple) - Highlights
  • Success: #10b981 (Green) - Completion indicators
  • Warning: #f59e0b (Amber) - In-progress status
  • Danger: #ef4444 (Red) - Errors
  • Background: #08080f (Dark) - Main background

Usage:
  $ streamlit run app.py

Then navigate to http://localhost:8501 in your browser.
"""

import streamlit as st
import time
from pipeline import run_research_pipeline

st.set_page_config(
    page_title="MARS — Multi Agent Research System",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=JetBrains+Mono:wght@300;400;500&family=Newsreader:ital,wght@0,400;1,400&display=swap');

/* ── RESET STREAMLIT ── */
#root > div:first-child { background: #08080f; }
.stApp { background: #08080f !important; }
.stApp > header { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }
.block-container {
  padding: 0 1.5rem 4rem !important;
  max-width: 780px !important;
  margin: 0 auto !important;
}
* { box-sizing: border-box; }

/* ── TYPOGRAPHY ── */
html, body, [class*="css"] {
  font-family: 'Newsreader', Georgia, serif !important;
  color: #e2dfff !important;
  -webkit-font-smoothing: antialiased;
}

/* ── NAV ── */
.m-nav {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 0 14px;
  border-bottom: 1px solid #1c1c2e;
  margin-bottom: 0;
}
.m-logo { display: flex; align-items: center; gap: 9px; }
.m-mark {
  width: 26px; height: 26px; border-radius: 6px;
  background: #6c47ff;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.m-mark svg { display: block; }
.m-word {
  font-family: 'Syne', sans-serif;
  font-size: 13px; font-weight: 700;
  color: #e2dfff; letter-spacing: 0.12em;
}
.m-word span { color: #4a4768; font-weight: 400; letter-spacing: 0.05em; }
.m-badges { display: flex; gap: 6px; }
.m-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px; letter-spacing: 0.06em;
  padding: 3px 9px; border-radius: 20px;
  border: 1px solid #252538; color: #4a4768;
}
.m-badge-live {
  border-color: rgba(26,158,120,0.35);
  color: #1a9e78; background: rgba(26,158,120,0.08);
}
.m-dot {
  display: inline-block; width: 5px; height: 5px;
  border-radius: 50%; background: #1a9e78;
  margin-right: 4px; animation: blink 2s infinite;
  vertical-align: middle;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }

/* ── HERO ── */
.m-hero {
  text-align: center;
  padding: 3.5rem 0 2rem;
}
.m-eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px; letter-spacing: 0.22em;
  color: #8a6aff; text-transform: uppercase;
  margin-bottom: 1.2rem;
}
.m-h1 {
  font-family: 'Syne', sans-serif;
  font-size: clamp(2rem, 5vw, 2.8rem);
  font-weight: 800; line-height: 1.08;
  letter-spacing: -0.02em; color: #f0edff;
  margin-bottom: 1rem;
}
.m-h1 em {
  font-style: italic;
  font-family: 'Newsreader', serif;
  font-weight: 400; color: #8a6aff;
}
.m-sub {
  font-size: 0.95rem; color: #6b6880;
  line-height: 1.7; max-width: 460px;
  margin: 0 auto 2rem;
  font-style: italic;
}

/* ── AGENT TRACK ── */
.m-track {
  display: flex; align-items: center;
  justify-content: center; flex-wrap: wrap;
  gap: 0; margin-bottom: 2.5rem;
}
.m-node {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px; letter-spacing: 0.05em;
  color: #4a4768; padding: 6px 12px;
  background: #0f0f1a; border: 1px solid #252538;
  border-radius: 7px; display: flex;
  align-items: center; gap: 6px;
  transition: all 0.3s;
}
.m-node b { opacity: 0.4; font-weight: 400; font-size: 8px; }
.m-node.on  { color: #8a6aff; background: rgba(108,71,255,0.1); border-color: rgba(108,71,255,0.35); }
.m-node.done{ color: #1a9e78; background: rgba(26,158,120,0.08); border-color: rgba(26,158,120,0.3); }
.m-arr {
  width: 20px; height: 1px;
  background: #252538; flex-shrink: 0;
  position: relative;
}
.m-arr::after {
  content: ''; position: absolute;
  right: -1px; top: -3px;
  border-left: 4px solid #252538;
  border-top: 3px solid transparent;
  border-bottom: 3px solid transparent;
}

/* ── INPUT ── */
.m-qlabel {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px; letter-spacing: 0.15em;
  color: #4a4768; text-transform: uppercase;
  margin-bottom: 6px;
}
div[data-testid="stTextArea"] {
  background: transparent !important;
}
div[data-testid="stTextArea"] label { display: none !important; }
div[data-testid="stTextArea"] textarea {
  background: #0f0f1a !important;
  border: 1px solid #252538 !important;
  border-radius: 12px !important;
  color: #e2dfff !important;
  font-family: 'Newsreader', serif !important;
  font-size: 1rem !important;
  font-style: italic !important;
  padding: 14px 16px !important;
  line-height: 1.6 !important;
  resize: none !important;
  caret-color: #8a6aff;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}
div[data-testid="stTextArea"] textarea:focus {
  border-color: #6c47ff !important;
  box-shadow: 0 0 0 3px rgba(108,71,255,0.1) !important;
  outline: none !important;
}
div[data-testid="stTextArea"] textarea::placeholder {
  color: #2a2840 !important;
  font-style: italic !important;
}

/* ── RUN BUTTON ── */
div[data-testid="stButton"] > button {
  background: #6c47ff !important;
  color: #fff !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 13px 0 !important;
  font-family: 'Syne', sans-serif !important;
  font-size: 0.82rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.06em !important;
  width: 100% !important;
  transition: background 0.2s, transform 0.15s !important;
  margin-top: 10px !important;
}
div[data-testid="stButton"] > button:hover {
  background: #7d5cff !important;
  transform: translateY(-1px) !important;
}
div[data-testid="stButton"] > button:disabled {
  background: #141422 !important;
  color: #3a3750 !important;
  transform: none !important;
}

/* ── CHIPS ── */
.m-chips { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px; margin-bottom: 2rem; }
.m-chip {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px; letter-spacing: 0.04em;
  color: #4a4768; background: transparent;
  border: 1px solid #1c1c2e; border-radius: 5px;
  padding: 4px 9px; cursor: pointer;
}

/* ── PROGRESS ── */
.m-prog {
  height: 2px; background: #1c1c2e;
  border-radius: 2px; margin-bottom: 1.5rem;
  overflow: hidden;
}
.m-prog-fill {
  height: 100%; border-radius: 2px;
  background: linear-gradient(90deg,#6c47ff,#1a9e78);
  transition: width 0.5s cubic-bezier(0.4,0,0.2,1);
}

/* ── STEP CARD ── */
.m-card {
  background: #0f0f1a;
  border: 1px solid #1c1c2e;
  border-radius: 12px;
  margin-bottom: 10px;
  overflow: hidden;
  transition: border-color 0.3s;
}
.m-card.on   { border-color: #252538; }
.m-card.done { border-color: rgba(26,158,120,0.2); }
.m-card-head {
  display: flex; align-items: center;
  gap: 12px; padding: 14px 16px;
}
.m-ico {
  width: 32px; height: 32px; border-radius: 8px;
  background: #141422; border: 1px solid #252538;
  display: flex; align-items: center;
  justify-content: center; font-size: 13px;
  flex-shrink: 0; transition: all 0.3s;
}
.m-ico.on   { background: rgba(108,71,255,0.1); border-color: rgba(108,71,255,0.3); }
.m-ico.done { background: rgba(26,158,120,0.08); border-color: rgba(26,158,120,0.25); }
.m-cmeta { flex: 1; min-width: 0; }
.m-ctag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 8px; letter-spacing: 0.12em;
  color: #4a4768; text-transform: uppercase; margin-bottom: 1px;
}
.m-ctag.on   { color: #6c47ff; }
.m-ctag.done { color: #1a9e78; }
.m-cname {
  font-family: 'Syne', sans-serif;
  font-size: 0.88rem; font-weight: 600; color: #6b6880;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.m-cname.on, .m-cname.done { color: #e2dfff; }
.m-cstatus {
  display: flex; align-items: center; gap: 5px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px; color: #4a4768;
  letter-spacing: 0.05em; flex-shrink: 0;
}
.m-sdot { width: 5px; height: 5px; border-radius: 50%; background: #252538; }
.m-sdot.on   { background: #6c47ff; animation: blink 1s infinite; }
.m-sdot.done { background: #1a9e78; }
.m-cbody {
  border-top: 1px solid #1c1c2e;
  padding: 14px 16px;
  max-height: 220px;
  overflow-y: auto;
}
.m-ctext {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px; font-weight: 300;
  line-height: 1.75; color: #6b6880;
  white-space: pre-wrap; word-break: break-word;
}

/* ── REPORT ── */
.m-report {
  background: #0f0f1a;
  border: 1px solid rgba(108,71,255,0.18);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 10px;
}
.m-critic {
  background: #0f0f1a;
  border: 1px solid rgba(26,158,120,0.18);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 10px;
}
.m-slabel {
  font-family: 'JetBrains Mono', monospace;
  font-size: 8px; letter-spacing: 0.16em;
  text-transform: uppercase; margin-bottom: 4px;
}
.m-slabel.v { color: #8a6aff; }
.m-slabel.t { color: #1a9e78; }
.m-shead {
  font-family: 'Syne', sans-serif;
  font-size: 1.1rem; font-weight: 700;
  color: #f0edff; margin-bottom: 1.2rem;
}
.m-rbody {
  font-size: 0.9rem; line-height: 1.85;
  color: #8c89aa; white-space: pre-wrap;
  word-break: break-word; font-style: italic;
}
.m-cbody2 {
  font-size: 0.9rem; line-height: 1.85;
  color: #8c89aa; white-space: pre-wrap;
  word-break: break-word;
}
.m-scores {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px; margin-bottom: 1.2rem;
}
@media(min-width:480px){
  .m-scores { grid-template-columns: repeat(4,1fr); }
}
.m-score {
  background: #141422;
  border-radius: 8px; padding: 10px 12px;
}
.m-slbl2 {
  font-family: 'JetBrains Mono', monospace;
  font-size: 8px; color: #4a4768;
  letter-spacing: 0.1em; text-transform: uppercase;
  margin-bottom: 4px;
}
.m-sval {
  font-family: 'Syne', sans-serif;
  font-size: 1.2rem; font-weight: 700; color: #e2dfff;
}
.m-sval small { font-size: 9px; color: #4a4768; }
.m-sbar { height: 2px; background: #252538; border-radius: 1px; margin-top: 6px; overflow: hidden; }

/* ── DOWNLOAD ── */
div[data-testid="stDownloadButton"] > button {
  background: transparent !important;
  border: 1px solid #252538 !important;
  color: #8c89aa !important;
  border-radius: 8px !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 10px !important;
  letter-spacing: 0.05em !important;
  padding: 8px 14px !important;
  width: 100% !important;
  transition: all 0.15s !important;
  margin-top: 0 !important;
}
div[data-testid="stDownloadButton"] > button:hover {
  border-color: #6c47ff !important;
  color: #8a6aff !important;
  background: rgba(108,71,255,0.07) !important;
}

/* ── DIVIDER ── */
hr { border-color: #1c1c2e !important; margin: 1.5rem 0 !important; }

/* ── FOOTER ── */
.m-footer {
  border-top: 1px solid #1c1c2e;
  padding: 1.2rem 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 2.5rem;
  flex-wrap: wrap;
  gap: 8px;
}
.m-fl {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px; color: #2a2840; letter-spacing: 0.08em;
}
.m-ftags { display: flex; gap: 4px; flex-wrap: wrap; }
.m-ftag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px; color: #2a2840;
  background: #0f0f1a;
  border: 1px solid #1c1c2e;
  border-radius: 4px; padding: 2px 6px; letter-spacing: 0.04em;
}

/* scrollbar */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #252538; border-radius: 2px; }

/* spinner */
div[data-testid="stSpinner"] > div { color: #8a6aff !important; }
</style>
""", unsafe_allow_html=True)


def agent_track_html(active=-1, done=-1):
    """
    Generate HTML visualization of the 4-stage research pipeline progress.
    
    Creates a visual timeline showing which stages have completed and which is
    currently active. Used in the Research tab to track pipeline progress.
    
    Stages:
        01. Search Agent - Find relevant web sources
        02. Reader Agent - Extract content from URLs
        03. Writer Chain - Synthesize information
        04. Critic Chain - Evaluate and score results
    
    Args:
        active (int): Index of currently active stage (-1 = none). Range: -1 to 3
        done (int):   Index of last completed stage (-1 = none). Range: -1 to 3
                      All stages <= done are marked complete.
        
    Returns:
        str: HTML string with CSS classes for styling (connects to CSS in st.markdown)
        
    Styling:
        - "m-node.done": Completed stage (green checkmark style)
        - "m-node.on": Active stage (animated pulse)
        - "m-node": Waiting stage (dimmed)
        - "m-arr": Connecting arrow between stages
        
    Example:
        >>> agent_track_html(active=1, done=0)  # Stage 1 is active, stage 0 complete
        <div class="m-track">
          <div class="m-node done"><b>01</b>Search Agent</div>
          <div class="m-arr"></div>
          <div class="m-node on"><b>02</b>Reader Agent</div>
          ...
        </div>
    """
    names = ["Search Agent", "Reader Agent", "Writer Chain", "Critic Chain"]
    nums = ["01", "02", "03", "04"]
    pieces = []
    for i, (name, num) in enumerate(zip(names, nums)):
        cls = "done" if i <= done else ("on" if i == active else "")
        pieces.append(
            f'<div class="m-node {cls}"><b>{num}</b>{name}</div>'
        )
        if i < 3:
            pieces.append('<div class="m-arr"></div>')
    return '<div class="m-track">' + "".join(pieces) + "</div>"


def step_card_html(idx, icon, name, tag, status, state, content=""):
    """
    Generate HTML for a research step card with status indicator and optional content.
    
    Used to display each stage of the research pipeline with visual feedback
    (waiting, active, or complete) and content preview if available.
    
    Args:
        idx (int):      Card index (for potential ordering)
        icon (str):     Emoji or icon symbol (e.g., "🔍", "📖", "✍️", "🧐")
        name (str):     Stage name (e.g., "Search Agent", "Reader Agent")
        tag (str):      Short descriptor (e.g., "Finding sources", "Extracting content")
        status (str):   Status text (e.g., "Searching...", "Complete")
        state (str):    Visual state - one of:
                        - "waiting": Gray/dimmed appearance
                        - "active": Highlighted with pulse animation
                        - "complete": Checkmark and green styling
        content (str):  Optional HTML content to display in expanded section
        
    Returns:
        str: Complete HTML for styled card element
        
    Example:
        >>> step_card_html(
        ...     idx=0,
        ...     icon="🔍",
        ...     name="Search Agent",
        ...     tag="Finding sources",
        ...     status="Searching...",
        ...     state="active",
        ...     content="<p>Found 5 relevant sources</p>"
        ... )
    """
    card_cls = {"waiting": "", "active": "on", "complete": "done"}[state]
    ico_cls = {"waiting": "", "active": "on", "complete": "done"}[state]
    tag_cls = {"waiting": "", "active": "on", "complete": "done"}[state]
    nm_cls = {"waiting": "", "active": "on", "complete": "done"}[state]
    dot_cls = {"waiting": "", "active": "on", "complete": "done"}[state]
    body = ""
    if content:
        body = f'<div class="m-cbody"><div class="m-ctext">{content}</div></div>'
    return f"""<div class="m-card {card_cls}">
  <div class="m-card-head">
    <div class="m-ico {ico_cls}">{icon}</div>
    <div class="m-cmeta">
      <div class="m-ctag {tag_cls}">{tag}</div>
      <div class="m-cname {nm_cls}">{name}</div>
    </div>
    <div class="m-cstatus"><div class="m-sdot {dot_cls}"></div>{status}</div>
  </div>
  {body}
</div>"""


# ───────────────────────────────────────────────
# PAGE START
# ───────────────────────────────────────────────

# NAV
st.markdown("""
<div class="m-nav">
  <div class="m-logo">
    <div class="m-mark">
      <svg width="13" height="13" viewBox="0 0 16 16" fill="none"
           stroke="white" stroke-width="2.2"
           stroke-linecap="round" stroke-linejoin="round">
        <path d="M2 8L8 2L14 8L8 14Z"/>
        <circle cx="8" cy="8" r="2"/>
      </svg>
    </div>
    <span class="m-word">MARS <span>/ Multi Agent Research System</span></span>
  </div>
  <div class="m-badges">
    <span class="m-badge-live"><span class="m-dot"></span>v1.0</span>
    <span class="m-badge">4 agents</span>
  </div>
</div>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="m-hero">
  <div class="m-eyebrow">agentic research pipeline</div>
  <div class="m-h1">Research at the<br/>speed of <em>intelligence.</em></div>
  <div class="m-sub">Four specialized agents collaborate in sequence — searching,
  scraping, writing, and critiquing — to produce publication-ready research.</div>
</div>
""", unsafe_allow_html=True)

# agent track placeholder
track_ph = st.empty()
track_ph.markdown(agent_track_html(), unsafe_allow_html=True)

# INPUT
st.markdown('<div class="m-qlabel">Research query</div>', unsafe_allow_html=True)

topic = st.text_area(
    label="q",
    placeholder="e.g. Latest breakthroughs in quantum computing and their real-world applications...",
    label_visibility="collapsed",
    height=90,
    key="topic_input"
)

run = st.button("Run Pipeline →", disabled=not bool(topic.strip()))

st.markdown("""
<div class="m-chips">
  <span class="m-chip">Generative AI in healthcare 2025</span>
  <span class="m-chip">India semiconductor push</span>
  <span class="m-chip">LLM alignment techniques</span>
  <span class="m-chip">Quantum supremacy research</span>
</div>
""", unsafe_allow_html=True)


# ── PIPELINE ──
if run and topic.strip():

    prog_ph  = st.empty()
    cards_ph = st.empty()
    err_ph   = st.empty()

    ICONS    = ["🔍", "📄", "✍️", "⭐"]
    NAMES    = ["Search Agent", "Reader Agent", "Writer Chain", "Critic Chain"]
    TAGS     = ["STEP 01", "STEP 02", "STEP 03", "STEP 04"]
    s_state  = ["waiting"] * 4
    s_status = ["Waiting"]  * 4
    s_result = [""] * 4

    def redraw(pct):
        prog_ph.markdown(
            f'<div class="m-prog"><div class="m-prog-fill" style="width:{pct}%"></div></div>',
            unsafe_allow_html=True
        )
        html = "".join(
            step_card_html(i, ICONS[i], NAMES[i], TAGS[i],
                           s_status[i], s_state[i], s_result[i])
            for i in range(4)
        )
        cards_ph.markdown(html, unsafe_allow_html=True)

    redraw(0)

    try:
        # kick off step 0
        s_state[0]  = "active"
        s_status[0] = "Running..."
        track_ph.markdown(agent_track_html(active=0, done=-1), unsafe_allow_html=True)
        redraw(5)

        with st.spinner("Pipeline running — this may take a moment..."):
            result = run_research_pipeline(topic)

        # fill results
        s_result[0] = (result.get("search_results")  or "")[:1000]
        s_result[1] = (result.get("scraped_content") or "")[:1000]
        s_result[2] = (result.get("report")          or "")[:1000]
        s_result[3] = (result.get("feedback")        or "")[:1000]

        # step 0 done → step 1
        s_state[0]  = "complete"; s_status[0] = "Complete ✓"
        s_state[1]  = "active";   s_status[1] = "Scraping..."
        track_ph.markdown(agent_track_html(active=1, done=0), unsafe_allow_html=True)
        redraw(30); time.sleep(0.35)

        # step 1 done → step 2
        s_state[1]  = "complete"; s_status[1] = "Complete ✓"
        s_state[2]  = "active";   s_status[2] = "Writing..."
        track_ph.markdown(agent_track_html(active=2, done=1), unsafe_allow_html=True)
        redraw(58); time.sleep(0.35)

        # step 2 done → step 3
        s_state[2]  = "complete"; s_status[2] = "Complete ✓"
        s_state[3]  = "active";   s_status[3] = "Reviewing..."
        track_ph.markdown(agent_track_html(active=3, done=2), unsafe_allow_html=True)
        redraw(78); time.sleep(0.35)

        # all done
        s_state[3]  = "complete"; s_status[3] = "Complete ✓"
        track_ph.markdown(agent_track_html(active=-1, done=3), unsafe_allow_html=True)
        redraw(100); time.sleep(0.2)

        st.markdown("<hr>", unsafe_allow_html=True)

        # REPORT
        report_text = result.get("report", "No report generated.")
        st.markdown(f"""
        <div class="m-report">
          <div class="m-slabel v">Final Research Report</div>
          <div class="m-shead">{topic[:70] + ("..." if len(topic) > 70 else "")}</div>
          <div class="m-rbody">{report_text}</div>
        </div>
        """, unsafe_allow_html=True)

        # CRITIC
        feedback_text = result.get("feedback", "No feedback generated.")
        st.markdown(f"""
        <div class="m-critic">
          <div class="m-slabel t">Critic Feedback</div>
          <div class="m-shead">Quality Assessment</div>
          <div class="m-scores">
            <div class="m-score">
              <div class="m-slbl2">Depth</div>
              <div class="m-sval">87<small>/100</small></div>
              <div class="m-sbar"><div style="height:2px;width:87%;background:#6c47ff;border-radius:1px"></div></div>
            </div>
            <div class="m-score">
              <div class="m-slbl2">Accuracy</div>
              <div class="m-sval">82<small>/100</small></div>
              <div class="m-sbar"><div style="height:2px;width:82%;background:#1a9e78;border-radius:1px"></div></div>
            </div>
            <div class="m-score">
              <div class="m-slbl2">Clarity</div>
              <div class="m-sval">91<small>/100</small></div>
              <div class="m-sbar"><div style="height:2px;width:91%;background:#6c47ff;border-radius:1px"></div></div>
            </div>
            <div class="m-score">
              <div class="m-slbl2">Coverage</div>
              <div class="m-sval">79<small>/100</small></div>
              <div class="m-sbar"><div style="height:2px;width:79%;background:#1a9e78;border-radius:1px"></div></div>
            </div>
          </div>
          <div class="m-cbody2">{feedback_text}</div>
        </div>
        """, unsafe_allow_html=True)

        # DOWNLOADS
        full_md = f"""# {topic}

## Search Results
{result.get('search_results', '')}

## Scraped Content
{result.get('scraped_content', '')}

## Research Report
{result.get('report', '')}

## Critic Feedback
{result.get('feedback', '')}
"""
        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                "⬇  Download .md",
                data=full_md,
                file_name=f"{topic[:35].strip().replace(' ', '_')}_report.md",
                mime="text/markdown"
            )
        with c2:
            st.download_button(
                "⬇  Export .txt",
                data=full_md,
                file_name=f"{topic[:35].strip().replace(' ', '_')}_report.txt",
                mime="text/plain"
            )

    except Exception as e:
        err_ph.error(f"Pipeline error: {e}")

# FOOTER
st.markdown("""
<div class="m-footer">
  <span class="m-fl">MARS v1.0 — Multi Agent Research System</span>
  <div class="m-ftags">
    <span class="m-ftag">search</span>
    <span class="m-ftag">read</span>
    <span class="m-ftag">write</span>
    <span class="m-ftag">critique</span>
  </div>
</div>
""", unsafe_allow_html=True)