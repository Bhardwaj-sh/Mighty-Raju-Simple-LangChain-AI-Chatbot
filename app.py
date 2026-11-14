import os
import base64
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

import database as db

# ---------------------------------------------------------
# Environment & Configuration
# ---------------------------------------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

# ---------------------------------------------------------
# Page Setup
# ---------------------------------------------------------
st.set_page_config(
    page_title="Mighty Raju AI Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Image Encoding Helpers (Transparent PNG Assets)
# ---------------------------------------------------------
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    return ""

mighty_raju_img_b64 = get_base64_image("assets/mighty_raju_transparent.png")
mighty_raju_avatar_b64 = get_base64_image("assets/mighty_raju_avatar_transparent.png")
avatar_path = "assets/mighty_raju_avatar_transparent.png" if os.path.exists("assets/mighty_raju_avatar_transparent.png") else "⚡"

# ---------------------------------------------------------
# Mighty Raju Warm White + Soft Red Design System
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Global Canvas: Clean, warm off-white */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        background-color: #FFFEFC !important;
        color: #302C2B !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Main Container: Crisp White with Subtle Warm Shadow */
    .block-container {
        background: #FFFFFF !important;
        border: 1px solid #EDE2DE !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 24px rgba(48, 44, 43, 0.04) !important;
        padding: 1.8rem 2.4rem 4rem 2.4rem !important;
        margin-top: 1.2rem !important;
        margin-bottom: 2rem !important;
        max-width: 920px !important;
    }

    /* Left Sidebar: Soft Warm Ivory/Blush */
    section[data-testid="stSidebar"] {
        background-color: #F9F4F1 !important;
        border-right: 1px solid #EDE2DE !important;
    }
    section[data-testid="stSidebar"] .block-container {
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
        padding: 1.2rem 0.9rem !important;
        margin: 0 !important;
    }

    /* Sidebar Branding */
    .brand-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 0.2rem 0.4rem 0.9rem 0.4rem;
    }
    .brand-avatar-img {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        object-fit: cover;
        background: #FFFFFF !important;
        border: 2px solid #B94B48;
        box-shadow: 0 3px 8px rgba(185, 75, 72, 0.22);
    }
    .brand-name {
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: 0.5px;
        color: #302C2B;
        line-height: 1.2;
    }
    .brand-sub {
        font-size: 0.74rem;
        color: #827674;
        font-weight: 600;
        letter-spacing: 0.3px;
    }

    /* Base Buttons Styling */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.18s ease-in-out !important;
        border: 1px solid #EDE2DE !important;
        color: #302C2B !important;
        background: #FFFFFF !important;
    }
    .stButton > button:hover {
        border-color: #B94B48 !important;
        color: #B94B48 !important;
        background: #FDF9F8 !important;
        box-shadow: 0 3px 10px rgba(185, 75, 72, 0.1) !important;
    }

    /* Primary New Chat Button: Raju Red Accent */
    div[data-testid="stVerticalBlock"] > div:has(button[key="sb_btn_new"]) button,
    button[key="sb_btn_new"] {
        background: #B94B48 !important;
        color: #FFFFFF !important;
        border: 1px solid #B94B48 !important;
        box-shadow: 0 4px 12px rgba(185, 75, 72, 0.25) !important;
    }
    button[key="sb_btn_new"]:hover {
        background: #A53C39 !important;
        color: #FFFFFF !important;
        border-color: #A53C39 !important;
        transform: translateY(-1px) !important;
    }

    /* Clear Button */
    button[key="sb_btn_clear_req"] {
        background: #FFFFFF !important;
        color: #827674 !important;
        border: 1px solid #EDE2DE !important;
    }
    button[key="sb_btn_clear_req"]:hover {
        color: #B94B48 !important;
        border-color: #D98278 !important;
        background: #FDF9F8 !important;
    }

    /* Sidebar Section Title */
    .sidebar-section-title {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #827674;
        margin: 1.1rem 0.2rem 0.5rem 0.2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* View Header */
    .view-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 0.5rem;
        margin-bottom: 0.8rem;
        border-bottom: 1px solid #EDE2DE;
    }
    .view-title {
        font-size: 0.92rem;
        font-weight: 700;
        color: #302C2B;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 1.4rem 1rem;
        color: #827674;
        font-size: 0.82rem;
        line-height: 1.5;
        background: #FAF6F4;
        border-radius: 12px;
        border: 1px dashed #DDD2CE;
        margin: 0.5rem 0;
    }

    /* ---------------------------------------------------------
       Mascot & Welcome Screen
       --------------------------------------------------------- */
    .welcome-container {
        text-align: center;
        padding: 0.6rem 0 0.4rem 0;
    }
    .avatar-stage {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0.4rem auto;
        position: relative;
        background: transparent !important;
    }
    .avatar-figure {
        position: relative;
        display: inline-block;
        animation: rajuIdle 5.5s ease-in-out infinite;
        transform-origin: 50% 95%;
        background: transparent !important;
    }
    .raju-standing-character {
        height: 180px;
        width: auto;
        display: block;
        object-fit: contain;
        background: transparent !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        user-select: none;
        pointer-events: none;
    }

    @keyframes rajuIdle {
        0% { transform: translateY(0px) scale(1, 1); }
        38% { transform: translateY(-2.2px) scale(1.006, 1.01); }
        65% { transform: translateY(-1.2px) scale(1.003, 1.006); }
        100% { transform: translateY(0px) scale(1, 1); }
    }

    .eyelid {
        position: absolute;
        background: #e8a838;
        border-radius: 50%;
        transform-origin: top center;
        transform: scaleY(0);
        opacity: 0;
        pointer-events: none;
        animation: naturalBlink 5.5s ease-in-out infinite;
    }
    .eyelid-left {
        top: 22.8%;
        left: 36.2%;
        width: 5.4%;
        height: 4.4%;
    }
    .eyelid-right {
        top: 22.8%;
        left: 61.8%;
        width: 5.4%;
        height: 4.4%;
    }
    @keyframes naturalBlink {
        0%, 95%, 100% { transform: scaleY(0); opacity: 0; }
        97%, 98.5% { transform: scaleY(1); opacity: 0.95; }
    }

    .avatar-ground-shadow {
        width: 100px;
        height: 10px;
        background: radial-gradient(ellipse at center, rgba(185, 75, 72, 0.18) 0%, rgba(217, 130, 120, 0.05) 55%, transparent 75%);
        border-radius: 50%;
        margin-top: -6px;
    }

    .welcome-heading {
        font-size: 2.1rem;
        font-weight: 800;
        color: #302C2B;
        letter-spacing: -0.5px;
        margin-top: 0.6rem;
        margin-bottom: 0.3rem;
    }
    .welcome-heading-accent {
        color: #B94B48;
    }
    .welcome-subheading {
        font-size: 0.98rem;
        color: #827674;
        font-weight: 400;
        margin-bottom: 2rem;
    }

    /* ---------------------------------------------------------
       Suggestion Cards (2x2 Grid)
       --------------------------------------------------------- */
    .card-col button {
        background: #FFFFFF !important;
        border: 1px solid #EDE2DE !important;
        border-radius: 14px !important;
        padding: 1.1rem 1.25rem !important;
        text-align: left !important;
        color: #302C2B !important;
        box-shadow: 0 2px 6px rgba(48, 44, 43, 0.02) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        height: auto !important;
        min-height: 84px !important;
        display: block !important;
        width: 100% !important;
        margin-bottom: 0.6rem !important;
    }
    .card-col button:hover {
        border-color: #B94B48 !important;
        background: #FCF7F5 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(185, 75, 72, 0.1) !important;
        color: #B94B48 !important;
    }

    /* ---------------------------------------------------------
       Chat Messages Styling
       --------------------------------------------------------- */
    div[data-testid="stChatMessage"] {
        padding: 1.1rem 1.3rem !important;
        border-radius: 16px !important;
        margin-bottom: 0.9rem !important;
        font-size: 0.95rem !important;
        line-height: 1.65 !important;
    }

    /* User Message: Warm Blush Tint */
    div[data-testid="stChatMessage"][aria-label*="user"],
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
        background: #F8EAE7 !important;
        border: 1px solid #F0DCD7 !important;
        color: #302C2B !important;
        border-bottom-right-radius: 4px !important;
        box-shadow: 0 2px 8px rgba(185, 75, 72, 0.05) !important;
    }
    div[data-testid="stChatMessage"][aria-label*="user"] p,
    div[data-testid="stChatMessage"][aria-label*="user"] span {
        color: #302C2B !important;
    }

    /* Assistant Message: Clean White with Warm Border */
    div[data-testid="stChatMessage"][aria-label*="assistant"],
    div[data-testid="stChatMessage"]:has(img[src*="mighty_raju_avatar"]) {
        background: #FFFFFF !important;
        border: 1px solid #EDE2DE !important;
        border-bottom-left-radius: 4px !important;
        box-shadow: 0 2px 10px rgba(48, 44, 43, 0.03) !important;
        color: #302C2B !important;
    }
    div[data-testid="stChatMessage"][aria-label*="assistant"] p,
    div[data-testid="stChatMessage"][aria-label*="assistant"] span {
        color: #302C2B !important;
    }

    /* Chat Avatar Image */
    div[data-testid="stChatMessage"] img {
        border-radius: 50% !important;
        object-fit: cover !important;
        background: #FFFFFF !important;
        border: 1.5px solid #B94B48 !important;
        box-shadow: 0 2px 6px rgba(185, 75, 72, 0.2) !important;
    }

    /* Message Action Buttons */
    .action-pill-btn button {
        padding: 3px 10px !important;
        font-size: 0.74rem !important;
        border-radius: 8px !important;
        color: #827674 !important;
        border: 1px solid #EDE2DE !important;
        background: #FFFFFF !important;
        min-height: auto !important;
        height: 28px !important;
    }
    .action-pill-btn button:hover {
        color: #B94B48 !important;
        border-color: #B94B48 !important;
        background: #FDF9F8 !important;
    }

    /* ---------------------------------------------------------
       Chat Input: Modern Warm-White Container
       --------------------------------------------------------- */
    div[data-testid="stChatInput"] {
        background: #FFFFFF !important;
        border-radius: 16px !important;
        border: 1px solid #EDE2DE !important;
        box-shadow: 0 4px 20px rgba(48, 44, 43, 0.05) !important;
        padding: 4px 12px !important;
    }
    div[data-testid="stChatInput"]:focus-within {
        border-color: #B94B48 !important;
        box-shadow: 0 0 0 3px rgba(185, 75, 72, 0.15) !important;
    }
    div[data-testid="stChatInput"] > div,
    div[data-testid="stChatInput"] [data-baseweb="base-input"],
    div[data-testid="stChatInput"] [data-baseweb="textarea"] {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        background: transparent !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #302C2B !important;
        font-size: 0.94rem !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        background: transparent !important;
    }
    div[data-testid="stChatInput"] button {
        border: none !important;
        outline: none !important;
        background: #B94B48 !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        padding: 4px 8px !important;
    }
    div[data-testid="stChatInput"] button:hover {
        background: #A53C39 !important;
    }

    /* Top Navigation Toolbar */
    .top-toolbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 0.8rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid #EDE2DE;
    }
    .top-title-pill {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.88rem;
        font-weight: 600;
        color: #302C2B;
    }
    .top-status-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
def extract_text(content):
    """Safely extract plain text from LangChain message content."""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and "text" in item:
                parts.append(item["text"])
            elif isinstance(item, str):
                parts.append(item)
            elif hasattr(item, "text"):
                parts.append(item.text)
        return "".join(parts)
    return str(content) if content is not None else ""

@st.cache_resource(show_spinner=False)
def load_llm():
    """Cache high-speed LangChain Gemini 3.5 Flash chat model instance."""
    return ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=api_key,
        temperature=0.7,
    )

def generate_title(first_prompt: str) -> str:
    """Generate a clean, readable conversation title from the first prompt."""
    cleaned = " ".join(first_prompt.strip().split())
    if len(cleaned) <= 38:
        return cleaned
    return cleaned[:35].rstrip() + "..."

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

if "sidebar_mode" not in st.session_state:
    st.session_state.sidebar_mode = "main"

if "search_term" not in st.session_state:
    st.session_state.search_term = ""

if "confirm_clear" not in st.session_state:
    st.session_state.confirm_clear = False

# If an active chat exists but messages are empty in session, load from SQLite
if st.session_state.active_chat_id and not st.session_state.messages:
    stored_msgs = db.get_messages(st.session_state.active_chat_id)
    st.session_state.messages = stored_msgs

# ---------------------------------------------------------
# Left Sidebar Implementation
# ---------------------------------------------------------
with st.sidebar:
    # A. Branding Section
    brand_icon_html = f'<img src="data:image/png;base64,{mighty_raju_avatar_b64}" class="brand-avatar-img" />' if mighty_raju_avatar_b64 else '<span style="font-size: 1.6rem;">⚡</span>'
    st.markdown(f"""
    <div class="brand-header">
        {brand_icon_html}
        <div>
            <div class="brand-name">MIGHTY RAJU</div>
            <div class="brand-sub">AI Assistant</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # B. New Chat & Clear Buttons
    col_new, col_clear = st.columns([1.8, 1])
    with col_new:
        if st.button("➕ New Chat", key="sb_btn_new", use_container_width=True, help="Start a new conversation"):
            st.session_state.active_chat_id = None
            st.session_state.messages = []
            st.session_state.pending_prompt = None
            st.session_state.sidebar_mode = "main"
            st.session_state.confirm_clear = False
            st.rerun()

    with col_clear:
        if not st.session_state.confirm_clear:
            if st.button("🗑️ Clear", key="sb_btn_clear_req", use_container_width=True, help="Clear the current conversation"):
                st.session_state.confirm_clear = True
                st.rerun()
        else:
            if st.button("✕ Cancel", key="sb_btn_clear_cancel", use_container_width=True):
                st.session_state.confirm_clear = False
                st.rerun()

    # Clear Confirmation Step
    if st.session_state.confirm_clear:
        st.markdown("<div style='font-size: 0.8rem; color: #B94B48; padding: 4px 6px; font-weight: 600;'>Clear current chat messages?</div>", unsafe_allow_html=True)
        col_c_yes, col_c_no = st.columns(2)
        with col_c_yes:
            if st.button("Yes, Clear", key="sb_btn_clear_confirm", use_container_width=True):
                if st.session_state.active_chat_id:
                    db.clear_conversation_messages(st.session_state.active_chat_id)
                st.session_state.messages = []
                st.session_state.confirm_clear = False
                st.rerun()
        with col_c_no:
            if st.button("Keep", key="sb_btn_clear_no", use_container_width=True):
                st.session_state.confirm_clear = False
                st.rerun()

    st.markdown("<hr style='margin: 0.7rem 0 0.9rem 0; border: none; border-top: 1px solid #EDE2DE;'>", unsafe_allow_html=True)

    # C. Main Navigation Options
    if st.session_state.sidebar_mode == "search":
        col_stitle, col_sback = st.columns([3, 1])
        with col_stitle:
            st.markdown("<div class='view-title'>🔍 Search Chats</div>", unsafe_allow_html=True)
        with col_sback:
            if st.button("✕", key="btn_close_search", help="Back to menu", use_container_width=True):
                st.session_state.sidebar_mode = "main"
                st.session_state.search_term = ""
                st.rerun()

        search_input = st.text_input(
            "Search query",
            value=st.session_state.search_term,
            placeholder="Type keyword or phrase...",
            label_visibility="collapsed"
        )
        st.session_state.search_term = search_input

        if search_input.strip():
            results = db.search_conversations(search_input.strip())
            st.markdown(f"<div style='font-size: 0.75rem; color: #827674; margin-bottom: 0.4rem;'>Found {len(results)} match{'es' if len(results) != 1 else ''}:</div>", unsafe_allow_html=True)

            if results:
                for r in results:
                    star = "⭐ " if r["is_saved"] else ""
                    btn_label = f"{star}{r['title']}"
                    snippet = r.get("matched_snippet")
                    if st.button(btn_label, key=f"search_res_{r['id']}", use_container_width=True):
                        st.session_state.active_chat_id = r["id"]
                        st.session_state.messages = db.get_messages(r["id"])
                        st.session_state.sidebar_mode = "main"
                        st.rerun()
                    if snippet:
                        clean_snip = snippet.replace("\n", " ")[:60]
                        st.caption(f"💬 \"...{clean_snip}...\"")
            else:
                st.markdown("<div class='empty-state'>No matching conversations found.<br>Try another search term.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='empty-state'>Type a topic or word to search across all your previous conversation titles and messages.</div>", unsafe_allow_html=True)

    elif st.session_state.sidebar_mode == "saved":
        col_stitle, col_sback = st.columns([3, 1])
        with col_stitle:
            st.markdown("<div class='view-title'>🔖 Saved Chats</div>", unsafe_allow_html=True)
        with col_sback:
            if st.button("✕", key="btn_close_saved", help="Back to menu", use_container_width=True):
                st.session_state.sidebar_mode = "main"
                st.rerun()

        saved_chats = db.get_saved_conversations()
        if saved_chats:
            st.markdown(f"<div style='font-size: 0.75rem; color: #827674; margin-bottom: 0.4rem;'>{len(saved_chats)} bookmarked conversation{'s' if len(saved_chats) != 1 else ''}:</div>", unsafe_allow_html=True)
            for sc in saved_chats:
                col_c1, col_c2 = st.columns([4, 1])
                with col_c1:
                    is_current = (sc["id"] == st.session_state.active_chat_id)
                    btn_label = f"⭐ {sc['title']}" if not is_current else f"👉 ⭐ {sc['title']}"
                    if st.button(btn_label, key=f"open_saved_{sc['id']}", use_container_width=True):
                        st.session_state.active_chat_id = sc["id"]
                        st.session_state.messages = db.get_messages(sc["id"])
                        st.session_state.sidebar_mode = "main"
                        st.rerun()
                with col_c2:
                    if st.button("✕", key=f"unsave_{sc['id']}", help="Remove from Saved Chats (keeps conversation intact)", use_container_width=True):
                        db.set_conversation_saved(sc["id"], False)
                        st.rerun()
        else:
            st.markdown("""
            <div class='empty-state'>
                <strong>No saved chats yet.</strong><br>
                Click the ⭐️ Bookmark icon on any chat to save it here!
            </div>
            """, unsafe_allow_html=True)

    elif st.session_state.sidebar_mode == "projects":
        col_stitle, col_sback = st.columns([3, 1])
        with col_stitle:
            st.markdown("<div class='view-title'>📁 Projects</div>", unsafe_allow_html=True)
        with col_sback:
            if st.button("✕", key="btn_close_proj", help="Back to menu", use_container_width=True):
                st.session_state.sidebar_mode = "main"
                st.rerun()

        with st.expander("➕ New Project", expanded=False):
            new_pname = st.text_input("Project Name", placeholder="e.g. Python Study, Vacation...", key="inp_new_project")
            if st.button("Create", key="btn_create_proj_submit", use_container_width=True):
                if new_pname.strip():
                    db.create_project(new_pname.strip())
                    st.success(f"Project created!")
                    st.rerun()

        if st.session_state.active_chat_id:
            active_conv = db.get_conversation(st.session_state.active_chat_id)
            current_pname = active_conv.get("project_name") if active_conv else None
            
            with st.expander("📌 Assign Current Chat", expanded=False):
                all_p = db.get_all_projects()
                p_options = {"None (Unassigned)": None}
                for p in all_p:
                    p_options[p["name"]] = p["id"]
                
                curr_idx = 0
                if current_pname and current_pname in p_options:
                    curr_idx = list(p_options.keys()).index(current_pname)

                selected_p_label = st.selectbox(
                    "Select project:",
                    options=list(p_options.keys()),
                    index=curr_idx,
                    key="sb_assign_proj_select"
                )
                if st.button("Assign", key="btn_assign_proj_submit", use_container_width=True):
                    db.set_conversation_project(st.session_state.active_chat_id, p_options[selected_p_label])
                    st.rerun()

        projects = db.get_all_projects()
        if projects:
            st.markdown(f"<div style='font-size: 0.75rem; color: #827674; margin: 0.5rem 0 0.3rem 0;'>{len(projects)} Project Folder{'s' if len(projects) != 1 else ''}:</div>", unsafe_allow_html=True)
            for p in projects:
                with st.expander(f"📁 {p['name']} ({p['chat_count']})"):
                    p_chats = db.get_project_conversations(p["id"])
                    if p_chats:
                        for pc in p_chats:
                            col_pc1, col_pc2 = st.columns([4, 1])
                            with col_pc1:
                                if st.button(f"💬 {pc['title']}", key=f"open_pchat_{pc['id']}", use_container_width=True):
                                    st.session_state.active_chat_id = pc["id"]
                                    st.session_state.messages = db.get_messages(pc["id"])
                                    st.session_state.sidebar_mode = "main"
                                    st.rerun()
                            with col_pc2:
                                if st.button("⏏️", key=f"unassign_{pc['id']}", help="Unassign from project", use_container_width=True):
                                    db.set_conversation_project(pc["id"], None)
                                    st.rerun()
                    else:
                        st.caption("No conversations in this project yet.")

                    st.markdown("<hr style='margin: 0.3rem 0;'>", unsafe_allow_html=True)
                    col_ren, col_del = st.columns(2)
                    with col_ren:
                        new_rname = st.text_input("Rename", value=p["name"], key=f"ren_input_{p['id']}", label_visibility="collapsed")
                        if st.button("Rename", key=f"ren_btn_{p['id']}", use_container_width=True):
                            if new_rname.strip() and new_rname.strip() != p["name"]:
                                db.rename_project(p["id"], new_rname.strip())
                                st.rerun()
                    with col_del:
                        if st.button("🗑️ Delete", key=f"del_proj_{p['id']}", help="Deletes project only; chats remain safe!", use_container_width=True):
                            db.delete_project(p["id"])
                            st.rerun()
        else:
            st.markdown("<div class='empty-state'>No projects created yet.</div>", unsafe_allow_html=True)

    elif st.session_state.sidebar_mode == "all_chats":
        col_stitle, col_sback = st.columns([3, 1])
        with col_stitle:
            st.markdown("<div class='view-title'>📜 All Conversations</div>", unsafe_allow_html=True)
        with col_sback:
            if st.button("✕", key="btn_close_all_chats", help="Back to menu", use_container_width=True):
                st.session_state.sidebar_mode = "main"
                st.rerun()

        all_chats = db.get_all_conversations()
        if all_chats:
            st.markdown(f"<div style='font-size: 0.75rem; color: #827674; margin-bottom: 0.4rem;'>{len(all_chats)} total conversation{'s' if len(all_chats) != 1 else ''}:</div>", unsafe_allow_html=True)
            for c in all_chats:
                col_ac1, col_ac2 = st.columns([4, 1])
                with col_ac1:
                    star = "⭐ " if c["is_saved"] else ""
                    proj = f" [{c['project_name']}]" if c.get("project_name") else ""
                    label = f"{star}{c['title']}{proj}"
                    if st.button(label, key=f"open_all_{c['id']}", use_container_width=True):
                        st.session_state.active_chat_id = c["id"]
                        st.session_state.messages = db.get_messages(c["id"])
                        st.session_state.sidebar_mode = "main"
                        st.rerun()
                with col_ac2:
                    if st.button("🗑️", key=f"del_all_{c['id']}", help="Delete this conversation", use_container_width=True):
                        db.delete_conversation(c["id"])
                        if st.session_state.active_chat_id == c["id"]:
                            st.session_state.active_chat_id = None
                            st.session_state.messages = []
                        st.rerun()
        else:
            st.markdown("<div class='empty-state'>No conversations stored yet.</div>", unsafe_allow_html=True)

    else:
        # Default Main Sidebar View
        if st.button("🔍  Search Chats", key="nav_btn_search", use_container_width=True):
            st.session_state.sidebar_mode = "search"
            st.rerun()

        saved_count = len(db.get_saved_conversations())
        saved_label = f"🔖  Saved Chats ({saved_count})" if saved_count > 0 else "🔖  Saved Chats"
        if st.button(saved_label, key="nav_btn_saved", use_container_width=True):
            st.session_state.sidebar_mode = "saved"
            st.rerun()

        proj_count = len(db.get_all_projects())
        proj_label = f"📁  Projects ({proj_count})" if proj_count > 0 else "📁  Projects"
        if st.button(proj_label, key="nav_btn_projects", use_container_width=True):
            st.session_state.sidebar_mode = "projects"
            st.rerun()

        # D. RECENT CHATS Section
        st.markdown("""
        <div class="sidebar-section-title">
            <span>Recent Chats</span>
            <span style="font-size: 0.85rem;">🕒</span>
        </div>
        """, unsafe_allow_html=True)

        recent_chats = db.get_recent_conversations(5)

        if recent_chats:
            for rc in recent_chats:
                is_active = (rc["id"] == st.session_state.active_chat_id)
                star = "⭐ " if rc["is_saved"] else ""
                display_title = f"{'👉 ' if is_active else '💬 '}{star}{rc['title']}"
                
                if st.button(display_title, key=f"rc_btn_{rc['id']}", use_container_width=True):
                    st.session_state.active_chat_id = rc["id"]
                    st.session_state.messages = db.get_messages(rc["id"])
                    st.rerun()
            
            # View All Chats Option
            all_count = len(db.get_all_conversations())
            if st.button(f"📜 View All Chats ({all_count})", key="btn_view_all_chats", use_container_width=True):
                st.session_state.sidebar_mode = "all_chats"
                st.rerun()
        else:
            st.markdown("""
            <div class='empty-state'>
                No conversations yet.<br>Send a message to start!
            </div>
            """, unsafe_allow_html=True)

    # E. Bottom Sidebar Engine / Model Info
    st.markdown("""
    <div style="margin-top: 1.8rem; padding: 10px 12px; background: #FFFFFF; border-radius: 12px; border: 1px solid #EDE2DE; font-size: 0.74rem; color: #827674; line-height: 1.5;">
        <strong style="color: #302C2B;">⚡ Engine:</strong> Gemini 3.5 Flash<br>
        <strong style="color: #302C2B;">🔗 LangChain:</strong> v1.5.0<br>
        <strong style="color: #302C2B;">💾 Database:</strong> SQLite Local
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Top Navigation Toolbar (Inside Main Card)
# ---------------------------------------------------------
current_conv = None
if st.session_state.active_chat_id:
    current_conv = db.get_conversation(st.session_state.active_chat_id)

col_top_left, col_top_right = st.columns([3, 1.8])

with col_top_left:
    if current_conv:
        proj_badge = f" • <span style='color: #B94B48;'>📁 {current_conv['project_name']}</span>" if current_conv.get("project_name") else ""
        st.markdown(f"""
        <div class="top-toolbar" style="border: none; margin: 0; padding: 0;">
            <div class="top-title-pill">
                <span class="top-status-dot"></span>
                <span>{current_conv['title']}</span>{proj_badge}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="top-toolbar" style="border: none; margin: 0; padding: 0;">
            <div class="top-title-pill">
                <span class="top-status-dot"></span>
                <span>Mighty Raju AI Assistant</span>
                <span style="color: #827674; font-size: 0.75rem; font-weight: 500;">(Gemini 3.5 Flash)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_top_right:
    if st.session_state.active_chat_id and current_conv:
        col_bm, col_del = st.columns([1.5, 1])
        with col_bm:
            is_saved = bool(current_conv.get("is_saved", 0))
            bm_label = "⭐ Saved" if is_saved else "☆ Bookmark"
            if st.button(bm_label, key="btn_top_bookmark", use_container_width=True, help="Toggle bookmark for this chat"):
                db.toggle_save_conversation(st.session_state.active_chat_id)
                st.rerun()
        with col_del:
            if st.button("🗑️ Delete", key="btn_top_delete", use_container_width=True, help="Delete this conversation"):
                db.delete_conversation(st.session_state.active_chat_id)
                st.session_state.active_chat_id = None
                st.session_state.messages = []
                st.rerun()

st.markdown("<hr style='margin: 0.4rem 0 1.2rem 0; border: none; border-top: 1px solid #EDE2DE;'>", unsafe_allow_html=True)

# ---------------------------------------------------------
# API Key Verification
# ---------------------------------------------------------
if not api_key:
    st.error("⚠️ API key is missing. Please ensure GOOGLE_API_KEY is configured in your .env file.")
    st.stop()

try:
    llm = load_llm()
except Exception as init_err:
    st.error(f"Failed to initialize Mighty Raju AI Engine: {init_err}")
    st.stop()

# ---------------------------------------------------------
# Main Welcome Screen (4 Brand-Inspired Interactive Cards)
# ---------------------------------------------------------
if len(st.session_state.messages) == 0:
    if mighty_raju_img_b64:
        mascot_html = f"""
        <div class="avatar-stage">
            <div class="avatar-figure">
                <img src="data:image/png;base64,{mighty_raju_img_b64}" class="raju-standing-character" alt="Mighty Raju" />
                <div class="eyelid eyelid-left"></div>
                <div class="eyelid eyelid-right"></div>
            </div>
            <div class="avatar-ground-shadow"></div>
        </div>
        """
    else:
        mascot_html = '<div style="text-align: center; font-size: 2.5rem;">⚡</div>'

    st.markdown(f"""
    <div class="welcome-container">
        {mascot_html}
        <div class="welcome-heading">Hey, I'm <span class="welcome-heading-accent">Mighty Raju</span>! 👋</div>
        <div class="welcome-subheading">Your AI companion. Ask me anything and let's figure it out together.</div>
    </div>
    """, unsafe_allow_html=True)

    # Four Minimalist Suggested Prompt Cards (2x2 Grid)
    card_col1, card_col2 = st.columns(2)
    
    with card_col1:
        st.markdown('<div class="card-col">', unsafe_allow_html=True)
        if st.button(
            "💻  Explain Code\n\nUnderstand programming concepts step by step.",
            key="card_btn_code",
            use_container_width=True
        ):
            st.session_state.pending_prompt = "Explain this programming concept step by step with clear code examples: "
            st.rerun()

        if st.button(
            "💡  Brainstorm Ideas\n\nExplore creative ideas and find inspiration.",
            key="card_btn_ideas",
            use_container_width=True
        ):
            st.session_state.pending_prompt = "Help me brainstorm 3 creative and practical ideas for: "
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with card_col2:
        st.markdown('<div class="card-col">', unsafe_allow_html=True)
        if st.button(
            "📖  Learn Something\n\nDiscover and understand new topics.",
            key="card_btn_learn",
            use_container_width=True
        ):
            st.session_state.pending_prompt = "Teach me something fascinating and new about science or technology: "
            st.rerun()

        if st.button(
            "✍️  Writing Help\n\nWrite, improve and refine your content.",
            key="card_btn_write",
            use_container_width=True
        ):
            st.session_state.pending_prompt = "Help me write and refine clear, engaging content about: "
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Render Chat Conversation History & Action Buttons
# ---------------------------------------------------------
num_messages = len(st.session_state.messages)

for idx, msg in enumerate(st.session_state.messages):
    role = msg["role"]
    current_avatar = "👤" if role == "user" else avatar_path
    
    with st.chat_message(role, avatar=current_avatar):
        st.markdown(msg["content"])
        
    # AI Response Action Toolbar (Copy, Regenerate, Bookmark)
    if role == "assistant":
        col_act1, col_act2, col_act3, _ = st.columns([1, 1.2, 1.2, 3.5])
        
        with col_act1:
            st.markdown('<div class="action-pill-btn">', unsafe_allow_html=True)
            if st.button("📋 Copy", key=f"btn_copy_{idx}", help="Copy response to clipboard"):
                st.toast("✅ Response copied to clipboard!")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_act2:
            # Only enable regenerate on the latest assistant message
            if idx == num_messages - 1:
                st.markdown('<div class="action-pill-btn">', unsafe_allow_html=True)
                if st.button("🔄 Regenerate", key=f"btn_regen_{idx}", help="Regenerate this response"):
                    if st.session_state.active_chat_id:
                        db.delete_last_assistant_message(st.session_state.active_chat_id)
                    st.session_state.messages.pop()
                    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                        last_user_prompt = st.session_state.messages[-1]["content"]
                        st.session_state.pending_prompt = last_user_prompt
                        st.session_state.messages.pop()
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        with col_act3:
            if st.session_state.active_chat_id:
                st.markdown('<div class="action-pill-btn">', unsafe_allow_html=True)
                is_bm = bool(current_conv.get("is_saved", 0)) if current_conv else False
                bm_text = "⭐ Saved" if is_bm else "☆ Bookmark"
                if st.button(bm_text, key=f"btn_bm_{idx}", help="Bookmark this conversation"):
                    new_val = db.toggle_save_conversation(st.session_state.active_chat_id)
                    st.toast("⭐ Saved to Bookmarks!" if new_val else "Removed from Bookmarks!")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Chat Input & Prompt Handling
# ---------------------------------------------------------
user_input = st.chat_input("Ask Mighty Raju anything...")

# Determine Active Prompt
active_prompt = None
if st.session_state.pending_prompt:
    active_prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None
elif user_input and user_input.strip():
    active_prompt = user_input.strip()

if active_prompt:
    # 1. Create conversation record in SQLite if new
    if not st.session_state.active_chat_id:
        new_title = generate_title(active_prompt)
        new_id = db.create_conversation(title=new_title)
        st.session_state.active_chat_id = new_id

    # 2. Append user message to database and session state
    db.add_message(st.session_state.active_chat_id, "user", active_prompt)
    st.session_state.messages.append({"role": "user", "content": active_prompt})

    with st.chat_message("user", avatar="👤"):
        st.markdown(active_prompt)

    # 3. Assemble multi-turn LangChain message history
    system_instruction = (
        "You are Mighty Raju, a highly intelligent, friendly, and respectful AI assistant. "
        "You are powered by LangChain and Google Gemini. "
        "Provide thorough, clear, accurate, and insightful responses. "
        "Use clean markdown formatting, headers, bullet points, and code blocks where helpful. "
        "Always maintain your identity as Mighty Raju."
    )
    langchain_messages = [SystemMessage(content=system_instruction)]

    for m in st.session_state.messages:
        if m["role"] == "user":
            langchain_messages.append(HumanMessage(content=m["content"]))
        elif m["role"] == "assistant":
            langchain_messages.append(AIMessage(content=m["content"]))

    # 4. Stream Assistant Response with Mighty Raju Avatar
    with st.chat_message("assistant", avatar=avatar_path):
        message_placeholder = st.empty()
        message_placeholder.markdown("⚡ *Mighty Raju is thinking...*")

        accumulated_text = ""
        try:
            for chunk in llm.stream(langchain_messages):
                text = extract_text(chunk.content)
                if text:
                    accumulated_text += text
                    message_placeholder.markdown(accumulated_text + " ▌")

            # Fallback to direct invoke if stream was empty
            if not accumulated_text.strip():
                fallback_res = llm.invoke(langchain_messages)
                accumulated_text = extract_text(fallback_res.content)

            if accumulated_text.strip():
                message_placeholder.markdown(accumulated_text)
                db.add_message(st.session_state.active_chat_id, "assistant", accumulated_text)
                st.session_state.messages.append({"role": "assistant", "content": accumulated_text})
            else:
                fallback_msg = "I'm here to help! Could you please repeat or rephrase your question?"
                message_placeholder.markdown(fallback_msg)
                db.add_message(st.session_state.active_chat_id, "assistant", fallback_msg)
                st.session_state.messages.append({"role": "assistant", "content": fallback_msg})

        except Exception as e:
            err_msg = str(e)
            if api_key and api_key in err_msg:
                err_msg = err_msg.replace(api_key, "[PROTECTED_API_KEY]")
            message_placeholder.markdown(f"⚠️ **Error encountered:** {err_msg}")

    # Rerun to update top toolbar and active status
    st.rerun()

