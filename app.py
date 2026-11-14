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
# Mighty Raju Superhero Theme Styling
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Global canvas in bright Mighty Raju superhero red matching avatar */
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background: linear-gradient(135deg, #FF221E 0%, #E51D1D 32%, #BA0001 72%, #850001 100%) !important;
        background-attachment: fixed !important;
        background-size: cover !important;
        height: 100vh !important;
        max-height: 100vh !important;
        overflow: hidden !important;
        color: #1e293b !important;
    }

    [data-testid="stHeader"], footer {
        display: none !important;
    }

    /* Main fixed glassmorphic card container */
    main#stMain,
    [data-testid="stAppScrollToBottomContainer"] {
        background: rgba(255, 255, 255, 0.96) !important;
        backdrop-filter: blur(28px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(28px) saturate(180%) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.95) !important;
        border-radius: 28px !important;
        box-shadow: 0 25px 65px -12px rgba(133, 0, 1, 0.38), 0 0 0 1px rgba(255, 255, 255, 0.8) !important;
        max-width: 980px !important;
        width: 92% !important;
        height: calc(100vh - 2.4rem) !important;
        max-height: calc(100vh - 2.4rem) !important;
        margin: 1.2rem auto !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
        position: relative !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
    }

    .block-container {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0.5rem 2rem 0.1rem 2rem !important;
        margin: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
        flex: 1 1 auto !important;
        min-height: 0 !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        scrollbar-width: thin;
        scrollbar-color: #fca5a5 transparent;
    }

    /* Fixed chat input anchored cleanly inside the bottom of the main white card container */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div {
        background: transparent !important;
        background-color: transparent !important;
        box-shadow: none !important;
    }

    [data-testid="stBottom"] {
        position: relative !important;
        bottom: 0 !important;
        width: 100% !important;
        padding: 0.2rem 2rem 0.8rem 2rem !important;
        margin: 0 !important;
        box-sizing: border-box !important;
        z-index: 10 !important;
        flex-shrink: 0 !important;
    }

    [data-testid="stBottomBlockContainer"] {
        max-width: 100% !important;
        width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: rgba(255, 252, 252, 0.96) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-right: 1.5px solid rgba(254, 226, 226, 0.85) !important;
    }
    section[data-testid="stSidebar"] .block-container {
        background: transparent !important;
        backdrop-filter: none !important;
        box-shadow: none !important;
        border: none !important;
        padding: 1.5rem 1rem !important;
        margin: 0 !important;
    }

    /* Sidebar Branding */
    .brand-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 0.2rem 0.2rem 1rem 0.2rem;
    }
    .brand-avatar-img {
        width: 46px;
        height: 46px;
        border-radius: 50%;
        object-fit: contain;
        background: #ffffff !important;
        padding: 2px;
        border: 2.5px solid #BA0001 !important;
        box-shadow: 0 4px 14px rgba(186, 0, 1, 0.35) !important;
    }
    .brand-name {
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: 0.5px;
        color: #0f172a;
    }
    .brand-name span {
        color: #BA0001;
    }
    .brand-sub {
        font-size: 0.75rem;
        color: #991b1b;
        font-weight: 600;
    }

    /* Primary Sidebar Buttons */
    div.st-key-sb_btn_new button {
        background: linear-gradient(135deg, #FF2E2E 0%, #E51D1D 50%, #BA0001 100%) !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 14px rgba(186, 0, 1, 0.35) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div.st-key-sb_btn_new button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(186, 0, 1, 0.45) !important;
        background: linear-gradient(135deg, #FF4545 0%, #F02828 50%, #C70001 100%) !important;
        color: #ffffff !important;
    }
    div.st-key-sb_btn_clear button {
        background: #ffffff !important;
        color: #475569 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    div.st-key-sb_btn_clear button:hover {
        border-color: #fca5a5 !important;
        color: #BA0001 !important;
        background: #fff5f5 !important;
    }

    /* Sidebar Navigation Buttons */
    div.st-key-nav_btn_search button,
    div.st-key-nav_btn_saved button,
    div.st-key-nav_btn_projects button,
    div.st-key-btn_view_all_chats button {
        background: #ffffff !important;
        border: 1px solid #fee2e2 !important;
        border-radius: 12px !important;
        color: #334155 !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.02) !important;
        transition: all 0.2s ease !important;
    }
    div.st-key-nav_btn_search button:hover,
    div.st-key-nav_btn_saved button:hover,
    div.st-key-nav_btn_projects button:hover,
    div.st-key-btn_view_all_chats button:hover {
        border-color: #f87171 !important;
        color: #BA0001 !important;
        background: #fff5f5 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(186, 0, 1, 0.1) !important;
    }

    /* Sidebar Section Divider & Header */
    .sidebar-section-title {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #991b1b;
        margin: 1.2rem 0.2rem 0.6rem 0.2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Sidebar View Header */
    .view-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 0.6rem;
        margin-bottom: 0.8rem;
        border-bottom: 1px solid #fee2e2;
    }
    .view-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #1e293b;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Sidebar Item Cards */
    .sidebar-card {
        background: #ffffff;
        border: 1px solid #fee2e2;
        border-radius: 10px;
        padding: 8px 10px;
        margin-bottom: 6px;
        font-size: 0.85rem;
        transition: all 0.15s ease;
    }
    .sidebar-card:hover {
        border-color: #fca5a5;
        background: #fff5f5;
    }

    /* Recent chat buttons */
    div[class*="st-key-rc_btn_"] button {
        border-radius: 10px !important;
        border: 1px solid #f8fafc !important;
        background: #ffffff !important;
        color: #334155 !important;
        font-size: 0.85rem !important;
        transition: all 0.15s ease !important;
    }
    div[class*="st-key-rc_btn_"] button:hover {
        border-color: #fca5a5 !important;
        color: #BA0001 !important;
        background: #fff5f5 !important;
    }

    /* Empty state info */
    .empty-state {
        text-align: center;
        padding: 1.5rem 1rem;
        color: #64748b;
        font-size: 0.85rem;
        line-height: 1.5;
        background: rgba(254, 242, 242, 0.6);
        border-radius: 12px;
        border: 1px dashed #fca5a5;
        margin: 0.6rem 0;
    }

    /* Integrated Avatar Stage without decorative circle */
    .avatar-stage {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: -0.15rem auto 0.1rem auto !important;
        position: relative;
        background: transparent !important;
    }

    .avatar-figure {
        position: relative;
        display: inline-block;
        animation: rajuIdle 5.5s ease-in-out infinite;
        transform-origin: 50% 95%;
        background: transparent !important;
        z-index: 1;
    }

    .raju-standing-character {
        height: 236px !important;
        max-height: 236px !important;
        width: auto !important;
        display: block !important;
        object-fit: contain !important;
        background: transparent !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        user-select: none;
        pointer-events: none;
    }

    @keyframes rajuIdle {
        0% { transform: translateY(0px) scale(1, 1) rotate(0deg); }
        38% { transform: translateY(-2.8px) scale(1.008, 1.014) rotate(0.35deg); }
        65% { transform: translateY(-1.5px) scale(1.004, 1.008) rotate(-0.25deg); }
        100% { transform: translateY(0px) scale(1, 1) rotate(0deg); }
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
        width: 136px;
        height: 11px;
        background: radial-gradient(ellipse at center, rgba(186, 0, 1, 0.28) 0%, rgba(229, 29, 29, 0.08) 55%, transparent 75%);
        border-radius: 50%;
        margin-top: -6px;
        z-index: 1;
        animation: shadowPulse 5.5s ease-in-out infinite;
    }
    @keyframes shadowPulse {
        0%, 100% { transform: scale(1); opacity: 0.8; }
        38%, 65% { transform: scale(0.92, 0.88); opacity: 0.6; }
    }

    .center-greeting {
        text-align: center;
        font-size: 1.8rem;
        font-weight: 800;
        color: #0f172a;
        margin: 0.2rem 0 0.05rem 0;
        letter-spacing: -0.5px;
    }
    .center-subgreeting {
        text-align: center;
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 500;
        margin-bottom: 0.55rem;
    }

    /* Four Compact Slim Horizontal Action Boxes */
    div[data-testid="stColumn"]:has(.compact-action-box),
    div[data-testid="column"]:has(.compact-action-box) {
        position: relative !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.compact-action-box) {
        margin-bottom: 0.5rem !important;
    }

    .compact-action-box {
        background: #ffffff;
        border: 1.5px solid #fee2e2;
        border-radius: 14px;
        padding: 0 15px;
        height: 46px;
        box-sizing: border-box;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
        box-shadow: 0 2px 8px rgba(186, 0, 1, 0.04);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        user-select: none;
        width: 100%;
    }

    div[data-testid="stColumn"]:has(.compact-action-box):hover .compact-action-box,
    div[data-testid="column"]:has(.compact-action-box):hover .compact-action-box {
        background: #fff5f5;
        border-color: #BA0001;
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(186, 0, 1, 0.16);
    }

    .compact-left {
        display: flex;
        align-items: center;
        gap: 10px;
        overflow: hidden;
    }

    .compact-card-icon {
        font-size: 1.15rem;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }

    .red-code-icon {
        font-family: monospace;
        font-weight: 800;
        color: #BA0001;
        font-size: 1.05rem;
    }

    .compact-card-title {
        font-size: 0.88rem;
        font-weight: 700;
        color: #1e293b;
        white-space: nowrap;
        transition: color 0.2s ease;
    }

    div[data-testid="stColumn"]:has(.compact-action-box):hover .compact-card-title,
    div[data-testid="column"]:has(.compact-action-box):hover .compact-card-title {
        color: #BA0001;
    }

    .compact-card-arrow {
        color: #fca5a5;
        font-weight: 700;
        font-size: 14px;
        flex-shrink: 0;
        transition: all 0.2s ease;
    }

    div[data-testid="stColumn"]:has(.compact-action-box):hover .compact-card-arrow,
    div[data-testid="column"]:has(.compact-action-box):hover .compact-card-arrow {
        color: #BA0001;
        transform: translateX(2px);
    }

    /* Invisible overlay button covering each compact action box */
    div[data-testid="stColumn"]:has(.compact-action-box) div.stButton,
    div[data-testid="column"]:has(.compact-action-box) div.stButton,
    div[data-testid="stColumn"]:has(.compact-action-box) div[data-testid="stButton"],
    div[data-testid="column"]:has(.compact-action-box) div[data-testid="stButton"] {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        z-index: 10 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    div[data-testid="stColumn"]:has(.compact-action-box) div.stButton > button,
    div[data-testid="column"]:has(.compact-action-box) div.stButton > button,
    div[data-testid="stColumn"]:has(.compact-action-box) div[data-testid="stButton"] > button,
    div[data-testid="column"]:has(.compact-action-box) div[data-testid="stButton"] > button {
        width: 100% !important;
        height: 100% !important;
        opacity: 0 !important;
        cursor: pointer !important;
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Base Chat Message */
    div[data-testid="stChatMessage"] {
        padding: 1.1rem 1.3rem !important;
        border-radius: 18px !important;
        margin-bottom: 1rem !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
    }

    /* User Message Bubble: Superhero Red Gradient */
    div[data-testid="stChatMessage"][aria-label*="user"],
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
        background: linear-gradient(135deg, #FF2E2E 0%, #E51D1D 45%, #BA0001 100%) !important;
        border: none !important;
        border-bottom-right-radius: 4px !important;
        box-shadow: 0 6px 20px rgba(186, 0, 1, 0.25) !important;
    }
    div[data-testid="stChatMessage"][aria-label*="user"] p,
    div[data-testid="stChatMessage"][aria-label*="user"] span,
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) p,
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) span {
        color: #ffffff !important;
    }

    /* Assistant Message Bubble: Crisp White with Soft Red Accent */
    div[data-testid="stChatMessage"][aria-label*="assistant"],
    div[data-testid="stChatMessage"]:has(img[src*="mighty_raju_avatar"]) {
        background: #ffffff !important;
        border: 1px solid #fee2e2 !important;
        border-bottom-left-radius: 4px !important;
        box-shadow: 0 4px 16px rgba(186, 0, 1, 0.06) !important;
    }
    div[data-testid="stChatMessage"][aria-label*="assistant"] p,
    div[data-testid="stChatMessage"][aria-label*="assistant"] span,
    div[data-testid="stChatMessage"]:has(img[src*="mighty_raju_avatar"]) p,
    div[data-testid="stChatMessage"]:has(img[src*="mighty_raju_avatar"]) span {
        color: #1e293b !important;
    }

    /* Chat Avatar Image */
    div[data-testid="stChatMessage"] img {
        border-radius: 50% !important;
        object-fit: cover !important;
        background: #ffffff !important;
        border: 2px solid #BA0001 !important;
        box-shadow: 0 2px 8px rgba(186, 0, 1, 0.25) !important;
    }

    /* Chat Input Pill - Anchored neatly inside the white card */
    div[data-testid="stChatInput"] {
        background: #ffffff !important;
        border-radius: 9999px !important;
        border: 1.5px solid #fee2e2 !important;
        box-shadow: 0 8px 30px rgba(186, 0, 1, 0.12) !important;
        padding: 4px 14px !important;
    }
    div[data-testid="stChatInput"]:focus-within {
        border-color: #BA0001 !important;
        box-shadow: 0 0 0 3px rgba(186, 0, 1, 0.18) !important;
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
        color: #0f172a !important;
        font-size: 0.95rem !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        background: transparent !important;
    }
    div[data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #FF2E2E 0%, #E51D1D 50%, #BA0001 100%) !important;
        border-radius: 50% !important;
        color: #ffffff !important;
        border: none !important;
        width: 38px !important;
        height: 38px !important;
        min-height: 38px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 3px 10px rgba(186, 0, 1, 0.35) !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stChatInput"] button:hover {
        transform: scale(1.06) !important;
        box-shadow: 0 5px 16px rgba(186, 0, 1, 0.5) !important;
        background: linear-gradient(135deg, #FF4545 0%, #F02828 50%, #C70001 100%) !important;
    }
    div[data-testid="stChatInput"] button svg {
        fill: #ffffff !important;
        color: #ffffff !important;
    }

    /* Top Navigation bar */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 0.9rem;
        margin-bottom: 1.2rem;
        border-bottom: 1px solid rgba(254, 226, 226, 0.8);
    }
    .top-model-pill {
        display: flex;
        align-items: center;
        gap: 6px;
        background: #ffffff;
        border: 1px solid #fee2e2;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #334155;
        box-shadow: 0 2px 6px rgba(186, 0, 1, 0.05);
    }
    .top-status-dot {
        width: 8px;
        height: 8px;
        background-color: #10b981;
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
    """Cache high-speed LangChain Gemini 3.5 Flash-Lite chat model instance."""
    return ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        google_api_key=api_key,
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
    st.session_state.sidebar_mode = "main"  # Options: 'main', 'search', 'saved', 'projects', 'all_chats'

if "search_term" not in st.session_state:
    st.session_state.search_term = ""

if "selected_project_id" not in st.session_state:
    st.session_state.selected_project_id = None

# If an active chat exists but messages are empty in session, load from SQLite
if st.session_state.active_chat_id and not st.session_state.messages:
    stored_msgs = db.get_messages(st.session_state.active_chat_id)
    st.session_state.messages = stored_msgs

# ---------------------------------------------------------
# Sidebar Component Implementation
# ---------------------------------------------------------
with st.sidebar:
    # 1. Mighty Raju Brand Header
    brand_icon_html = f'<img src="data:image/png;base64,{mighty_raju_avatar_b64}" class="brand-avatar-img" />' if mighty_raju_avatar_b64 else '<span style="font-size: 1.8rem;">⚡</span>'
    st.markdown(f"""
    <div class="brand-header">
        {brand_icon_html}
        <div>
            <div class="brand-name">MIGHTY RAJU</div>
            <div class="brand-sub">AI Assistant</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Primary Action Buttons: New Chat & Clear Conversation
    col_new, col_clear = st.columns(2)
    with col_new:
        if st.button("➕ New Chat", key="sb_btn_new", use_container_width=True, help="Start a new conversation"):
            st.session_state.active_chat_id = None
            st.session_state.messages = []
            st.session_state.pending_prompt = None
            st.session_state.sidebar_mode = "main"
            st.rerun()

    with col_clear:
        if st.button("🗑️ Clear", key="sb_btn_clear", use_container_width=True, help="Clear the current conversation"):
            if st.session_state.active_chat_id:
                db.clear_conversation_messages(st.session_state.active_chat_id)
            st.session_state.messages = []
            st.session_state.pending_prompt = None
            st.rerun()

    st.markdown("<hr style='margin: 0.8rem 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)

    # =========================================================
    # SIDEBAR MODE: SEARCH CHATS
    # =========================================================
    if st.session_state.sidebar_mode == "search":
        col_title, col_back = st.columns([3, 1])
        with col_title:
            st.markdown("<div class='view-title'>🔍 Search Chats</div>", unsafe_allow_html=True)
        with col_back:
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
            st.markdown(f"<div style='font-size: 0.78rem; color: #64748b; margin-bottom: 0.4rem;'>Found {len(results)} match{'es' if len(results) != 1 else ''}:</div>", unsafe_allow_html=True)

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

    # =========================================================
    # SIDEBAR MODE: SAVED CHATS (BOOKMARKS)
    # =========================================================
    elif st.session_state.sidebar_mode == "saved":
        col_title, col_back = st.columns([3, 1])
        with col_title:
            st.markdown("<div class='view-title'>🔖 Saved Chats</div>", unsafe_allow_html=True)
        with col_back:
            if st.button("✕", key="btn_close_saved", help="Back to menu", use_container_width=True):
                st.session_state.sidebar_mode = "main"
                st.rerun()

        saved_chats = db.get_saved_conversations()
        if saved_chats:
            st.markdown(f"<div style='font-size: 0.78rem; color: #64748b; margin-bottom: 0.4rem;'>{len(saved_chats)} bookmarked conversation{'s' if len(saved_chats) != 1 else ''}:</div>", unsafe_allow_html=True)
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
                Click the ⭐️ Bookmark icon at the top of any active chat to pin it here!
            </div>
            """, unsafe_allow_html=True)

    # =========================================================
    # SIDEBAR MODE: PROJECTS
    # =========================================================
    elif st.session_state.sidebar_mode == "projects":
        col_title, col_back = st.columns([3, 1])
        with col_title:
            st.markdown("<div class='view-title'>📁 Projects</div>", unsafe_allow_html=True)
        with col_back:
            if st.button("✕", key="btn_close_proj", help="Back to menu", use_container_width=True):
                st.session_state.sidebar_mode = "main"
                st.session_state.selected_project_id = None
                st.rerun()

        # Create New Project
        with st.expander("➕ Create New Project", expanded=False):
            new_pname = st.text_input("Project Name", placeholder="e.g. Python Study, Vacation Plan...", key="inp_new_project")
            if st.button("Create Project", key="btn_create_proj_submit", use_container_width=True):
                if new_pname.strip():
                    created_id = db.create_project(new_pname.strip())
                    st.success(f"Project '{new_pname}' created!")
                    st.rerun()
                else:
                    st.warning("Please enter a valid project name.")

        # Assign Active Chat to a Project
        if st.session_state.active_chat_id:
            active_conv = db.get_conversation(st.session_state.active_chat_id)
            current_pname = active_conv.get("project_name") if active_conv else None
            
            with st.expander("📌 Assign Current Chat", expanded=False):
                all_p = db.get_all_projects()
                p_options = {"None (Unassigned)": None}
                for p in all_p:
                    p_options[p["name"]] = p["id"]
                
                current_selection_idx = 0
                if current_pname and current_pname in p_options:
                    current_selection_idx = list(p_options.keys()).index(current_pname)

                selected_p_label = st.selectbox(
                    "Project folder for current chat:",
                    options=list(p_options.keys()),
                    index=current_selection_idx,
                    key="sb_assign_proj_select"
                )
                if st.button("Update Chat Project", key="btn_assign_proj_submit", use_container_width=True):
                    db.set_conversation_project(st.session_state.active_chat_id, p_options[selected_p_label])
                    st.success(f"Assigned to {selected_p_label}!")
                    st.rerun()

        # List Existing Projects
        projects = db.get_all_projects()
        if projects:
            st.markdown(f"<div style='font-size: 0.78rem; color: #64748b; margin: 0.6rem 0 0.4rem 0;'>{len(projects)} Project Folder{'s' if len(projects) != 1 else ''}:</div>", unsafe_allow_html=True)
            for p in projects:
                with st.expander(f"📁 {p['name']} ({p['chat_count']})", expanded=(st.session_state.selected_project_id == p["id"])):
                    # Chats in this project
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

                    st.markdown("<hr style='margin: 0.4rem 0;'>", unsafe_allow_html=True)
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
            st.markdown("""
            <div class='empty-state'>
                <strong>No projects created yet.</strong><br>
                Use the box above to create project folders and organize your chats!
            </div>
            """, unsafe_allow_html=True)

    # =========================================================
    # SIDEBAR MODE: VIEW ALL CHATS
    # =========================================================
    elif st.session_state.sidebar_mode == "all_chats":
        col_title, col_back = st.columns([3, 1])
        with col_title:
            st.markdown("<div class='view-title'>📜 All Conversations</div>", unsafe_allow_html=True)
        with col_back:
            if st.button("✕", key="btn_close_all_chats", help="Back to menu", use_container_width=True):
                st.session_state.sidebar_mode = "main"
                st.rerun()

        all_chats = db.get_all_conversations()
        if all_chats:
            st.markdown(f"<div style='font-size: 0.78rem; color: #64748b; margin-bottom: 0.4rem;'>{len(all_chats)} total conversation{'s' if len(all_chats) != 1 else ''}:</div>", unsafe_allow_html=True)
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

    # =========================================================
    # SIDEBAR MODE: DEFAULT MAIN VIEW
    # =========================================================
    else:
        # A. Search Chats
        if st.button("🔍 Search Chats", key="nav_btn_search", use_container_width=True):
            st.session_state.sidebar_mode = "search"
            st.rerun()

        # B. Saved Chats (shows count)
        saved_count = len(db.get_saved_conversations())
        saved_label = f"🔖 Saved Chats ({saved_count})" if saved_count > 0 else "🔖 Saved Chats"
        if st.button(saved_label, key="nav_btn_saved", use_container_width=True):
            st.session_state.sidebar_mode = "saved"
            st.rerun()

        # C. Projects (shows count)
        proj_count = len(db.get_all_projects())
        proj_label = f"📁 Projects ({proj_count})" if proj_count > 0 else "📁 Projects"
        if st.button(proj_label, key="nav_btn_projects", use_container_width=True):
            st.session_state.sidebar_mode = "projects"
            st.rerun()

        # -----------------------------------------------------
        # RECENT CHATS (Real, Functional History)
        # -----------------------------------------------------
        st.markdown("""
        <div class="sidebar-section-title">
            <span>Recent Chats</span>
            <span style="font-size: 0.9rem;">🕒</span>
        </div>
        """, unsafe_allow_html=True)

        recent_chats = db.get_recent_conversations(5)

        if recent_chats:
            for rc in recent_chats:
                is_active = (rc["id"] == st.session_state.active_chat_id)
                star = "⭐ " if rc["is_saved"] else ""
                display_title = f"{'👉 ' if is_active else ''}{star}{rc['title']}"
                
                if st.button(display_title, key=f"rc_btn_{rc['id']}", use_container_width=True):
                    st.session_state.active_chat_id = rc["id"]
                    st.session_state.messages = db.get_messages(rc["id"])
                    st.rerun()
            
            # View All Chats Button
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

    # Sidebar Bottom Tech Stack Footer
    st.markdown("""
    <div style="margin-top: 1.8rem; padding: 12px; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; font-size: 0.78rem; color: #64748b;">
        <strong style="color: #334155;">⚡ Engine:</strong> Gemini 3.5 Flash-Lite (High Speed)<br>
        <strong style="color: #334155;">🔗 LangChain:</strong> v1.5.0<br>
        <strong style="color: #334155;">💾 Storage:</strong> SQLite (Persistent)
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Top Navigation Toolbar (Inside Main Glass Card)
# ---------------------------------------------------------
current_conv = None
if st.session_state.active_chat_id:
    current_conv = db.get_conversation(st.session_state.active_chat_id)

col_top_left, col_top_right = st.columns([3, 2])

with col_top_left:
    status_title = "⚡ Mighty Raju Digital Assistant"
    if current_conv:
        proj_badge = f" • 📁 {current_conv['project_name']}" if current_conv.get("project_name") else ""
        st.markdown(f"""
        <div class="top-nav" style="border: none; margin: 0; padding: 0;">
            <div class="top-model-pill">
                <span class="top-status-dot"></span>
                <strong>{current_conv['title']}</strong>{proj_badge}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="top-nav" style="border: none; margin: 0; padding: 0;">
            <div class="top-model-pill">
                <span class="top-status-dot"></span>
                <span>{status_title}</span>
                <span style="color: #6366f1; font-weight: 700; font-size: 0.75rem;">(Gemini 3.5 Flash-Lite)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_top_right:
    # Active Conversation Controls: Bookmark, Project, and Delete
    if st.session_state.active_chat_id and current_conv:
        col_bm, col_del = st.columns([2, 1])
        with col_bm:
            is_saved = bool(current_conv.get("is_saved", 0))
            bm_label = "⭐ Saved" if is_saved else "☆ Bookmark"
            if st.button(bm_label, key="btn_top_bookmark", use_container_width=True, help="Toggle bookmark status for this chat"):
                db.toggle_save_conversation(st.session_state.active_chat_id)
                st.rerun()
        with col_del:
            if st.button("🗑️ Delete", key="btn_top_delete", use_container_width=True, help="Delete this conversation"):
                db.delete_conversation(st.session_state.active_chat_id)
                st.session_state.active_chat_id = None
                st.session_state.messages = []
                st.rerun()

st.markdown("<hr style='margin: 0.15rem 0 0.35rem 0; border: none; border-top: 1px solid rgba(226, 232, 240, 0.8);'>", unsafe_allow_html=True)

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
# Welcome Screen (Displayed when current conversation is empty)
# ---------------------------------------------------------
if len(st.session_state.messages) == 0:
    st.markdown("""
    <style>
        /* Landing page layout: strictly 100% fixed with zero scrolling */
        .block-container {
            overflow: hidden !important;
        }
    </style>
    """, unsafe_allow_html=True)

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
        mascot_html = '<div style="text-align: center; font-size: 3rem;">⚡</div>'

    st.markdown(f"""
    {mascot_html}
    <div class="center-greeting">Hey, I'm <span style="color: #BA0001; font-weight: 800;">Mighty Raju</span>! 👋</div>
    <div class="center-subgreeting">Your AI companion. Ask me anything and let's figure it out together.</div>
    """, unsafe_allow_html=True)

    # Action cards row matching uploaded design reference
    chip_col1, chip_col2, chip_col3, chip_col4 = st.columns(4)
    with chip_col1:
        st.markdown("""
        <div class="compact-action-box">
            <div class="compact-left">
                <span class="compact-card-icon red-code-icon">&lt;/&gt;</span>
                <span class="compact-card-title">Explain Code</span>
            </div>
            <span class="compact-card-arrow">→</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explain Code", key="chip_1", use_container_width=True):
            st.session_state.pending_prompt = "Explain programming concepts step by step with clear, intuitive examples."
            st.rerun()

    with chip_col2:
        st.markdown("""
        <div class="compact-action-box">
            <div class="compact-left">
                <span class="compact-card-icon">💡</span>
                <span class="compact-card-title">Brainstorm Ideas</span>
            </div>
            <span class="compact-card-arrow">→</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Brainstorm Ideas", key="chip_2", use_container_width=True):
            st.session_state.pending_prompt = "Explore creative ideas and find inspiration for an exciting project."
            st.rerun()

    with chip_col3:
        st.markdown("""
        <div class="compact-action-box">
            <div class="compact-left">
                <span class="compact-card-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="#BA0001">
                        <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                        <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                    </svg>
                </span>
                <span class="compact-card-title">Learn Something</span>
            </div>
            <span class="compact-card-arrow">→</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Learn Something", key="chip_3", use_container_width=True):
            st.session_state.pending_prompt = "Discover and understand new topics across science, technology, and learning."
            st.rerun()

    with chip_col4:
        st.markdown("""
        <div class="compact-action-box">
            <div class="compact-left">
                <span class="compact-card-icon">
                    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#BA0001" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"></path>
                    </svg>
                </span>
                <span class="compact-card-title">Writing Help</span>
            </div>
            <span class="compact-card-arrow">→</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Writing Help", key="chip_4", use_container_width=True):
            st.session_state.pending_prompt = "Write, improve, and refine content with creative and articulate phrasing."
            st.rerun()

# ---------------------------------------------------------
# Render Chat History
# ---------------------------------------------------------
for msg in st.session_state.messages:
    role = msg["role"]
    current_avatar = "👤" if role == "user" else avatar_path
    with st.chat_message(role, avatar=current_avatar):
        st.markdown(msg["content"])

# ---------------------------------------------------------
# Chat Input & Prompt Handling
# ---------------------------------------------------------
user_input = st.chat_input("Chat here...")

# Determine Active Prompt
active_prompt = None
if st.session_state.pending_prompt:
    active_prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None
elif user_input and user_input.strip():
    active_prompt = user_input.strip()

if active_prompt:
    # 1. If starting a new conversation, create record in SQLite database
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
        "You are Mighty Raju, a highly intelligent, supercharged, friendly, and respectful AI assistant. "
        "You are powered by LangChain and Google Gemini. "
        "Provide thorough, clear, accurate, and insightful responses. "
        "Use clear markdown formatting, bullet points, and code blocks where helpful. "
        "Always embody the helpful, sharp, and fearless spirit of Mighty Raju."
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

    # Rerun to update the top toolbar with the newly created chat title if it was the first message
    st.rerun()

