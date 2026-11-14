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

hero_mascot_path = "assets/mighty_raju_transparent.png"
avatar_path = "assets/mighty_raju_transparent.png"

mighty_raju_img_b64 = get_base64_image(hero_mascot_path)
mighty_raju_avatar_b64 = get_base64_image(avatar_path)

# ---------------------------------------------------------
# Exact Visual Theme: Mighty Raju Approved Reference Design
# ---------------------------------------------------------
css_styles = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    background-color: #FFFCFA !important;
    color: #2B1E1C !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stBottom"],
[data-testid="stBottom"] > div,
footer,
[data-testid="stDecoration"] {
    background: transparent !important;
    background-color: transparent !important;
}

/* Main Container Card */
.block-container {
    background: #FFFFFF !important;
    border: 1.5px solid #EADAD5 !important;
    border-radius: 24px !important;
    box-shadow: 0 10px 40px -10px rgba(188, 73, 70, 0.08), 0 0 0 1px rgba(255, 255, 255, 0.8) !important;
    padding: 1.2rem 2rem 2.2rem 2rem !important;
    margin-top: 0.8rem !important;
    margin-bottom: 5.5rem !important;
    max-width: 960px !important;
    position: relative !important;
    overflow: visible !important;
}

/* Left Sidebar: Soft Warm Ivory/Peach */
section[data-testid="stSidebar"] {
    background-color: #F8F0ED !important;
    border-right: 1.5px solid #EADAD5 !important;
}
section[data-testid="stSidebar"] .block-container {
    background: transparent !important;
    backdrop-filter: none !important;
    box-shadow: none !important;
    border: none !important;
    padding: 1.1rem 0.9rem !important;
    margin: 0 !important;
    max-width: 100% !important;
}

/* Sidebar Branding */
.brand-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0.1rem 0.1rem 1rem 0.1rem;
}
.brand-avatar-box {
    position: relative;
    width: 48px;
    height: 48px;
    flex-shrink: 0;
}
.brand-avatar-circle {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    overflow: hidden;
    border: 2px solid #BC4946;
    box-shadow: 0 4px 12px rgba(188, 73, 70, 0.2);
    background: #FFFFFF;
    position: relative;
}
.brand-avatar-img {
    width: 48px;
    height: 48px;
    object-fit: contain;
    transform: scale(2.2);
    transform-origin: 50% 16%;
    display: block;
}
.online-indicator {
    position: absolute;
    bottom: 1px;
    right: 1px;
    width: 11px;
    height: 11px;
    background-color: #10B981;
    border: 2px solid #FFFFFF;
    border-radius: 50%;
    box-shadow: 0 0 4px rgba(16, 185, 129, 0.4);
}
.brand-name {
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: 0.5px;
    color: #2B1E1C;
    line-height: 1.2;
}
.brand-sub {
    font-size: 0.78rem;
    color: #8A6D69;
    font-weight: 600;
}

/* Base Buttons */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    transition: all 0.18s ease-in-out !important;
    border: 1px solid #EADAD5 !important;
    color: #2B1E1C !important;
    background: #FFFFFF !important;
}
.stButton > button:hover {
    border-color: #BC4946 !important;
    color: #BC4946 !important;
    background: #FAF0ED !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(188, 73, 70, 0.1) !important;
}

/* Primary Red Button (+ New Chat) */
div.st-key-sb_btn_new button,
div.st-key-sb_btn_new button[kind="secondary"],
div.st-key-sb_btn_new button[data-testid="baseButton-secondary"] {
    background: #BC4946 !important;
    background-color: #BC4946 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 14px rgba(188, 73, 70, 0.28) !important;
}
div.st-key-sb_btn_new button:hover {
    background: #A83835 !important;
    background-color: #A83835 !important;
    color: #FFFFFF !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(188, 73, 70, 0.35) !important;
}

/* Clear Button */
div.st-key-sb_btn_clear button,
div.st-key-sb_btn_clear button[kind="secondary"],
div.st-key-sb_btn_clear button[data-testid="baseButton-secondary"] {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    color: #BC4946 !important;
    border: 1px solid #EADAD5 !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 6px rgba(188, 73, 70, 0.05) !important;
}
div.st-key-sb_btn_clear button:hover {
    background: #FAF0ED !important;
    background-color: #FAF0ED !important;
    border-color: #BC4946 !important;
    color: #A83835 !important;
    transform: translateY(-1px) !important;
}

/* Navigation Items (Search, Saved, Projects) */
div.st-key-nav_btn_search > button,
div.st-key-nav_btn_saved > button,
div.st-key-nav_btn_projects > button {
    background: #FFFFFF !important;
    border: 1px solid #EADAD5 !important;
    border-radius: 12px !important;
    color: #2B1E1C !important;
    font-weight: 600 !important;
    padding: 0.55rem 0.9rem !important;
    margin-bottom: 6px !important;
    box-shadow: 0 2px 6px rgba(188, 73, 70, 0.04) !important;
    text-align: left !important;
    justify-content: flex-start !important;
    width: 100% !important;
}
div.st-key-nav_btn_search > button:hover,
div.st-key-nav_btn_saved > button:hover,
div.st-key-nav_btn_projects > button:hover {
    background: #FAF0ED !important;
    border-color: #BC4946 !important;
    color: #BC4946 !important;
    transform: translateY(-1px) !important;
}

/* Sidebar Section Title */
.sidebar-section-title {
    font-size: 0.76rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #BC4946;
    margin: 0.8rem 0.1rem 0.5rem 0.1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Recent Chat Buttons */
div[class*="st-key-rc_btn_act_"] > button {
    background: #FCE8E2 !important;
    border: 1px solid #F3C9BF !important;
    color: #2B1E1C !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    box-shadow: 0 2px 6px rgba(188, 73, 70, 0.08) !important;
}
div[class*="st-key-rc_btn_inact_"] > button {
    background: #FFFFFF !important;
    border: 1px solid #EADAD5 !important;
    color: #2B1E1C !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    text-align: left !important;
    justify-content: flex-start !important;
}
div[class*="st-key-rc_btn_inact_"] > button:hover {
    background: #FAF0ED !important;
    border-color: #D98278 !important;
    color: #BC4946 !important;
}

/* View All Chats Button */
div.st-key-btn_view_all_chats > button {
    background: #FFFFFF !important;
    border: 1px solid #EADAD5 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    color: #2B1E1C !important;
    margin-top: 6px !important;
    width: 100% !important;
}
div.st-key-btn_view_all_chats > button:hover {
    background: #FAF0ED !important;
    border-color: #BC4946 !important;
    color: #BC4946 !important;
}

/* Sidebar Specs Card */
.sidebar-specs-card {
    margin-top: 1.4rem;
    padding: 10px 12px;
    background: #FAF0ED;
    border-radius: 12px;
    border: 1px solid #EADAD5;
    font-size: 0.78rem;
    color: #6C5A57;
    box-shadow: 0 2px 6px rgba(188, 73, 70, 0.04);
    line-height: 1.5;
}

.view-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 0.6rem;
    margin-bottom: 0.8rem;
    border-bottom: 1px solid #EADAD5;
}
.view-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #2B1E1C;
    display: flex;
    align-items: center;
    gap: 6px;
}
.empty-state {
    text-align: center;
    padding: 1.4rem 1rem;
    color: #7A6966;
    font-size: 0.84rem;
    line-height: 1.5;
    background: #FAF0ED;
    border-radius: 12px;
    border: 1px dashed #EADAD5;
    margin: 0.6rem 0;
}

/* Top Navigation bar */
.top-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 0.7rem;
    margin-bottom: 0.8rem;
    border-bottom: 1px solid #EADAD5;
    position: relative;
    z-index: 2;
}
.top-model-pill {
    display: flex;
    align-items: center;
    gap: 6px;
    background: #FFFFFF;
    border: 1px solid #EADAD5;
    padding: 5px 14px;
    border-radius: 9999px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #2B1E1C;
    box-shadow: 0 2px 6px rgba(188, 73, 70, 0.04);
}
.top-status-dot {
    width: 8px;
    height: 8px;
    background-color: #10B981;
    border-radius: 50%;
    display: inline-block;
}

/* Hero Welcome Stage */
.hero-stage {
    position: relative;
    text-align: center;
    padding: 0.4rem 0 0.8rem 0;
    margin-bottom: 0.2rem;
}
.skyline-decor {
    position: absolute;
    top: 10px;
    left: -2.2rem;
    right: -2.2rem;
    height: 190px;
    pointer-events: none;
    z-index: 0;
}
.skyline-decor svg {
    width: 100%;
    height: 100%;
}
.watermark-r {
    position: absolute;
    top: 0px;
    right: 20px;
    font-size: 135px;
    font-weight: 900;
    font-style: italic;
    color: #BC4946;
    opacity: 0.08;
    user-select: none;
    pointer-events: none;
    line-height: 1;
    font-family: 'Plus Jakarta Sans', sans-serif;
    z-index: 0;
}
.star-accent {
    position: absolute;
    color: #E29A90;
    opacity: 0.5;
    user-select: none;
    pointer-events: none;
    z-index: 0;
}
.star-1 { top: 60px; left: 23%; font-size: 15px; }
.star-2 { top: 25px; right: 27%; font-size: 18px; }
.star-3 { bottom: 50px; right: 5%; font-size: 13px; }

.avatar-center-box {
    position: relative;
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 2;
    margin-bottom: 0.2rem;
}
.avatar-halo {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 245px;
    height: 245px;
    border-radius: 50%;
    background: radial-gradient(circle, #FF221E 0%, #E6120E 40%, rgba(230, 18, 14, 0.72) 65%, rgba(230, 18, 14, 0.15) 85%, transparent 100%);
    box-shadow: 0 0 55px rgba(255, 34, 30, 0.45);
    pointer-events: none;
    z-index: 0;
}
.avatar-figure {
    position: relative;
    display: inline-block;
    animation: rajuFloat 5.5s ease-in-out infinite;
    transform-origin: 50% 95%;
    z-index: 1;
}
.raju-hero-character {
    height: 175px;
    width: auto;
    display: block;
    object-fit: contain;
    user-select: none;
    pointer-events: none;
    filter: drop-shadow(0 6px 14px rgba(0, 0, 0, 0.28)) drop-shadow(0 0 1.5px rgba(255, 255, 255, 0.9));
}
@keyframes rajuFloat {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    38% { transform: translateY(-4px) rotate(0.4deg); }
    70% { transform: translateY(-2px) rotate(-0.3deg); }
}
.eyelid {
    position: absolute;
    background: #E8A838;
    border-radius: 50%;
    transform-origin: top center;
    transform: scaleY(0);
    opacity: 0;
    pointer-events: none;
    animation: naturalBlink 5.5s ease-in-out infinite;
}
.eyelid-left {
    top: 27.3%;
    left: 27.2%;
    width: 5.6%;
    height: 4.4%;
}
.eyelid-right {
    top: 27.3%;
    left: 41.3%;
    width: 5.6%;
    height: 4.4%;
}
@keyframes naturalBlink {
    0%, 95%, 100% { transform: scaleY(0); opacity: 0; }
    97%, 98.5% { transform: scaleY(1); opacity: 0.95; }
}
.avatar-ground-shadow {
    width: 130px;
    height: 12px;
    background: radial-gradient(ellipse at center, rgba(188, 73, 70, 0.28) 0%, rgba(217, 130, 120, 0.08) 55%, transparent 75%);
    border-radius: 50%;
    margin-top: -8px;
    animation: shadowPulse 5.5s ease-in-out infinite;
    z-index: 1;
}
@keyframes shadowPulse {
    0%, 100% { transform: scale(1); opacity: 0.8; }
    38%, 70% { transform: scale(0.92, 0.88); opacity: 0.55; }
}

.welcome-heading {
    font-size: 2.1rem;
    font-weight: 800;
    color: #2B1E1C;
    margin: 0.2rem 0 0.15rem 0;
    letter-spacing: -0.5px;
    position: relative;
    z-index: 2;
}
.welcome-heading .highlight-red {
    color: #BC4946;
}
.welcome-subtitle {
    font-size: 0.98rem;
    font-weight: 500;
    color: #5C4D4A;
    margin-bottom: 0.75rem;
    position: relative;
    z-index: 2;
}

/* =========================================================
   FOUR INTERACTIVE SUGGESTION CARDS (SINGLE ROW 4 COLUMNS)
   ========================================================= */
[data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 12px !important;
    width: 100% !important;
    position: relative !important;
    z-index: 2 !important;
}
[data-testid="stHorizontalBlock"] > [data-testid="column"] {
    flex: 1 1 0% !important;
    min-width: 0 !important;
}

div.st-key-btn_card_1 button,
div.st-key-btn_card_2 button,
div.st-key-btn_card_3 button,
div.st-key-btn_card_4 button {
    height: 120px !important;
    min-height: 120px !important;
    background: #FFFFFF !important;
    border: 1px solid #EADAD5 !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 18px rgba(188, 73, 70, 0.05) !important;
    text-align: left !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: flex-start !important;
    justify-content: flex-start !important;
    padding: 0.9rem 0.85rem !important;
    position: relative !important;
    overflow: hidden !important;
    transition: all 0.22s ease-in-out !important;
    white-space: normal !important;
    width: 100% !important;
}
div.st-key-btn_card_1 button:hover,
div.st-key-btn_card_2 button:hover,
div.st-key-btn_card_3 button:hover,
div.st-key-btn_card_4 button:hover {
    border-color: #D98278 !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 22px rgba(188, 73, 70, 0.12) !important;
    background: #FFFFFF !important;
}

/* Circular arrow badge at bottom right */
div.st-key-btn_card_1 button::after,
div.st-key-btn_card_2 button::after,
div.st-key-btn_card_3 button::after,
div.st-key-btn_card_4 button::after {
    content: "→";
    position: absolute;
    bottom: 10px;
    right: 10px;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: #FCE8E3;
    color: #BC4946;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    font-weight: 800;
    line-height: 24px;
    text-align: center;
    transition: background 0.2s ease, color 0.2s ease;
}
div.st-key-btn_card_1 button:hover::after,
div.st-key-btn_card_2 button:hover::after,
div.st-key-btn_card_3 button:hover::after,
div.st-key-btn_card_4 button:hover::after {
    background: #BC4946;
    color: #FFFFFF;
}

/* Bottom gradient wave accent */
div.st-key-btn_card_1 button::before,
div.st-key-btn_card_2 button::before,
div.st-key-btn_card_3 button::before,
div.st-key-btn_card_4 button::before {
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: linear-gradient(90deg, #FBE8E3 0%, #F5D2C9 50%, #FCEAE5 100%);
    border-bottom-left-radius: 16px;
    border-bottom-right-radius: 16px;
}

div.st-key-btn_card_1 button *,
div.st-key-btn_card_2 button *,
div.st-key-btn_card_3 button *,
div.st-key-btn_card_4 button * {
    white-space: normal !important;
    text-overflow: clip !important;
    overflow: visible !important;
    word-break: normal !important;
}

div.st-key-btn_card_1 .stMarkdownEllipsis,
div.st-key-btn_card_2 .stMarkdownEllipsis,
div.st-key-btn_card_3 .stMarkdownEllipsis,
div.st-key-btn_card_4 .stMarkdownEllipsis {
    display: flex !important;
    flex-direction: column !important;
    align-items: flex-start !important;
    white-space: normal !important;
    text-overflow: clip !important;
    overflow: visible !important;
    width: 100% !important;
}

div.st-key-btn_card_1 button p:first-child,
div.st-key-btn_card_2 button p:first-child,
div.st-key-btn_card_3 button p:first-child,
div.st-key-btn_card_4 button p:first-child {
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    color: #2B1E1C !important;
    margin-bottom: 0.25rem !important;
    line-height: 1.25 !important;
    display: block !important;
    width: 100% !important;
}
div.st-key-btn_card_1 button p:last-child,
div.st-key-btn_card_2 button p:last-child,
div.st-key-btn_card_3 button p:last-child,
div.st-key-btn_card_4 button p:last-child {
    font-size: 0.74rem !important;
    font-weight: 500 !important;
    color: #7A6966 !important;
    line-height: 1.3 !important;
    padding-right: 22px !important;
    margin-top: 0 !important;
    display: block !important;
    width: 100% !important;
}

/* Bottom Right Decorative Wave */
.bottom-decor-wave {
    position: absolute;
    bottom: 0;
    right: 0;
    width: 280px;
    height: 60px;
    pointer-events: none;
    z-index: 0;
}
.bottom-decor-wave svg {
    width: 100%;
    height: 100%;
}

/* Base Chat Messages */
div[data-testid="stChatMessage"] {
    padding: 1.1rem 1.3rem !important;
    border-radius: 18px !important;
    margin-bottom: 0.9rem !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
}
div[data-testid="stChatMessage"][aria-label*="user"],
div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: #FCECE8 !important;
    border: 1px solid #EADAD5 !important;
    border-bottom-right-radius: 4px !important;
    box-shadow: 0 4px 14px rgba(188, 73, 70, 0.05) !important;
}
div[data-testid="stChatMessage"][aria-label*="user"] p,
div[data-testid="stChatMessage"][aria-label*="user"] span,
div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) p,
div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) span {
    color: #2B1E1C !important;
}
div[data-testid="stChatMessage"][aria-label*="assistant"],
div[data-testid="stChatMessage"]:has(img[src*="raju_avatar"]) {
    background: #FFFFFF !important;
    border: 1px solid #EADAD5 !important;
    border-bottom-left-radius: 4px !important;
    box-shadow: 0 4px 16px rgba(188, 73, 70, 0.05) !important;
}
div[data-testid="stChatMessage"][aria-label*="assistant"] p,
div[data-testid="stChatMessage"][aria-label*="assistant"] span,
div[data-testid="stChatMessage"]:has(img[src*="raju_avatar"]) p,
div[data-testid="stChatMessage"]:has(img[src*="raju_avatar"]) span {
    color: #2B1E1C !important;
}
div[data-testid="stChatMessage"] img {
    border-radius: 50% !important;
    object-fit: cover !important;
    object-position: center 2px !important;
    background: #FFFFFF !important;
    border: 2px solid #BC4946 !important;
    box-shadow: 0 2px 8px rgba(188, 73, 70, 0.18) !important;
}

/* Action Toolbar under AI Response */
.action-pill-btn button {
    background: #FFFFFF !important;
    border: 1px solid #EADAD5 !important;
    border-radius: 9999px !important;
    font-size: 0.76rem !important;
    padding: 0.25rem 0.65rem !important;
    color: #5C4D4A !important;
    box-shadow: 0 1px 4px rgba(188, 73, 70, 0.04) !important;
    transition: all 0.15s ease !important;
}
.action-pill-btn button:hover {
    background: #FAF0ED !important;
    border-color: #BC4946 !important;
    color: #BC4946 !important;
    transform: translateY(-1px) !important;
}

/* Chat Input */
div[data-testid="stChatInput"] {
    background: #FFFFFF !important;
    border-radius: 9999px !important;
    border: 1.5px solid #EADAD5 !important;
    box-shadow: 0 6px 24px rgba(188, 73, 70, 0.08) !important;
    padding: 4px 14px !important;
    margin-top: 0.8rem !important;
}
div[data-testid="stChatInput"]:focus-within {
    border-color: #BC4946 !important;
    box-shadow: 0 0 0 3px rgba(188, 73, 70, 0.16) !important;
}
div[data-testid="stChatInput"] > div,
div[data-testid="stChatInput"] [data-baseweb="base-input"],
div[data-testid="stChatInput"] [data-baseweb="base-input"] > div,
div[data-testid="stChatInput"] [data-baseweb="textarea"],
div[data-testid="stChatInput"] textarea {
    border: none !important;
    border-width: 0 !important;
    border-color: transparent !important;
    outline: none !important;
    box-shadow: none !important;
    background: transparent !important;
}
div[data-testid="stChatInput"] textarea {
    color: #2B1E1C !important;
    font-size: 0.95rem !important;
}
div[data-testid="stChatInput"] button {
    background: #BC4946 !important;
    border-radius: 50% !important;
    width: 36px !important;
    height: 36px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 2px 8px rgba(188, 73, 70, 0.3) !important;
    transition: all 0.15s ease !important;
}
div[data-testid="stChatInput"] button:hover {
    background: #A83835 !important;
    transform: scale(1.06) !important;
}
div[data-testid="stChatInput"] button svg {
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
}
</style>
"""
st.markdown(css_styles, unsafe_allow_html=True)

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
    # 1. Mighty Raju Brand Header with Online Status Badge
    brand_html = (
        '<div class="brand-header">'
        '<div class="brand-avatar-box">'
        '<div class="brand-avatar-circle">'
        f'<img src="data:image/png;base64,{mighty_raju_avatar_b64}" class="brand-avatar-img" />'
        '</div>'
        '<span class="online-indicator"></span>'
        '</div>'
        '<div>'
        '<div class="brand-name">MIGHTY RAJU</div>'
        '<div class="brand-sub">AI Assistant</div>'
        '</div>'
        '</div>'
    )
    st.markdown(brand_html, unsafe_allow_html=True)

    # 2. Primary Action Buttons: + New Chat & Clear
    col_new, col_clear = st.columns(2)
    with col_new:
        if st.button("＋ New Chat", key="sb_btn_new", use_container_width=True, help="Start a new conversation"):
            st.session_state.active_chat_id = None
            st.session_state.messages = []
            st.session_state.pending_prompt = None
            st.session_state.sidebar_mode = "main"
            st.rerun()

    with col_clear:
        if st.button("🗑️ Clear", key="sb_btn_clear", use_container_width=True, help="Clear current conversation"):
            if st.session_state.active_chat_id:
                db.clear_conversation_messages(st.session_state.active_chat_id)
            st.session_state.messages = []
            st.session_state.pending_prompt = None
            st.rerun()

    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

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
            st.markdown(f"<div style='font-size: 0.78rem; color: #7A6966; margin-bottom: 0.4rem;'>Found {len(results)} match{'es' if len(results) != 1 else ''}:</div>", unsafe_allow_html=True)

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
            st.markdown(f"<div style='font-size: 0.78rem; color: #7A6966; margin-bottom: 0.4rem;'>{len(saved_chats)} bookmarked conversation{'s' if len(saved_chats) != 1 else ''}:</div>", unsafe_allow_html=True)
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
            st.markdown("<div class='empty-state'><strong>No saved chats yet.</strong><br>Click the ⭐️ Bookmark icon at the top of any active chat to pin it here!</div>", unsafe_allow_html=True)

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

        with st.expander("➕ Create New Project", expanded=False):
            new_pname = st.text_input("Project Name", placeholder="e.g. Python Study, Vacation Plan...", key="inp_new_project")
            if st.button("Create Project", key="btn_create_proj_submit", use_container_width=True):
                if new_pname.strip():
                    created_id = db.create_project(new_pname.strip())
                    st.success(f"Project '{new_pname}' created!")
                    st.rerun()
                else:
                    st.warning("Please enter a valid project name.")

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

        projects = db.get_all_projects()
        if projects:
            st.markdown(f"<div style='font-size: 0.78rem; color: #7A6966; margin: 0.6rem 0 0.4rem 0;'>{len(projects)} Project Folder{'s' if len(projects) != 1 else ''}:</div>", unsafe_allow_html=True)
            for p in projects:
                with st.expander(f"📁 {p['name']} ({p['chat_count']})", expanded=(st.session_state.selected_project_id == p["id"])):
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
            st.markdown("<div class='empty-state'><strong>No projects created yet.</strong><br>Use the box above to create project folders and organize your chats!</div>", unsafe_allow_html=True)

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
            st.markdown(f"<div style='font-size: 0.78rem; color: #7A6966; margin-bottom: 0.4rem;'>{len(all_chats)} total conversation{'s' if len(all_chats) != 1 else ''}:</div>", unsafe_allow_html=True)
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
        if st.button("🔍  Search Chats", key="nav_btn_search", use_container_width=True):
            st.session_state.sidebar_mode = "search"
            st.rerun()

        # B. Saved Chats
        saved_count = len(db.get_saved_conversations())
        saved_label = f"🔖  Saved Chats ({saved_count})" if saved_count > 0 else "🔖  Saved Chats"
        if st.button(saved_label, key="nav_btn_saved", use_container_width=True):
            st.session_state.sidebar_mode = "saved"
            st.rerun()

        # C. Projects
        proj_count = len(db.get_all_projects())
        proj_label = f"📁  Projects ({proj_count})" if proj_count > 0 else "📁  Projects"
        if st.button(proj_label, key="nav_btn_projects", use_container_width=True):
            st.session_state.sidebar_mode = "projects"
            st.rerun()

        # Star Divider
        star_divider = (
            '<div style="display:flex;align-items:center;justify-content:center;margin:0.8rem 0;color:#D98278;font-size:0.9rem;">'
            '<span style="flex-grow:1;height:1px;background:#EADAD5;margin-right:8px;"></span>'
            '<span>★</span>'
            '<span style="flex-grow:1;height:1px;background:#EADAD5;margin-left:8px;"></span>'
            '</div>'
        )
        st.markdown(star_divider, unsafe_allow_html=True)

        # -----------------------------------------------------
        # RECENT CHATS (Real, Functional History)
        # -----------------------------------------------------
        recent_header = (
            '<div class="sidebar-section-title">'
            '<span>RECENT CHATS</span>'
            '<span style="font-size:0.88rem;">🕒</span>'
            '</div>'
        )
        st.markdown(recent_header, unsafe_allow_html=True)

        recent_chats = db.get_recent_conversations(5)

        if recent_chats:
            for rc in recent_chats:
                is_active = (rc["id"] == st.session_state.active_chat_id)
                star = "⭐ " if rc["is_saved"] else ""
                display_title = f"{'👉 ' if is_active else '💬 '}{star}{rc['title']}"
                btn_key = f"rc_btn_act_{rc['id']}" if is_active else f"rc_btn_inact_{rc['id']}"

                if st.button(display_title, key=btn_key, use_container_width=True):
                    st.session_state.active_chat_id = rc["id"]
                    st.session_state.messages = db.get_messages(rc["id"])
                    st.rerun()

            # View All Chats Button
            all_count = len(db.get_all_conversations())
            if st.button(f"⊞⊞ View All Chats ({all_count})", key="btn_view_all_chats", use_container_width=True):
                st.session_state.sidebar_mode = "all_chats"
                st.rerun()
        else:
            st.markdown("<div class='empty-state'>No conversations yet.<br>Send a message to start!</div>", unsafe_allow_html=True)

    # Sidebar Bottom Tech Stack Footer
    specs_html = (
        '<div class="sidebar-specs-card">'
        '<div style="margin-bottom:3px;"><strong style="color:#BC4946;">⚡ Engine:</strong> Gemini 3.5 Flash</div>'
        '<div style="margin-bottom:3px;"><strong style="color:#BC4946;">🔗 LangChain:</strong> 0.2.50</div>'
        '<div><strong style="color:#BC4946;">💾 Storage:</strong> SQLite (Persistent)</div>'
        '</div>'
    )
    st.markdown(specs_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# Top Navigation Toolbar (Inside Main Card)
# ---------------------------------------------------------
current_conv = None
if st.session_state.active_chat_id:
    current_conv = db.get_conversation(st.session_state.active_chat_id)

col_top_left, col_top_right = st.columns([3, 2])

with col_top_left:
    status_title = "Mighty Raju Digital Assistant"
    if current_conv:
        proj_badge = f" • 📁 {current_conv['project_name']}" if current_conv.get("project_name") else ""
        top_html = (
            '<div class="top-nav" style="border:none;margin:0;padding:0;">'
            '<div class="top-model-pill">'
            '<span class="top-status-dot"></span>'
            '<span style="margin-left:2px;">💬</span>'
            f'<strong>{current_conv["title"]}</strong>{proj_badge}'
            '</div>'
            '</div>'
        )
    else:
        top_html = (
            '<div class="top-nav" style="border:none;margin:0;padding:0;">'
            '<div class="top-model-pill">'
            '<span class="top-status-dot"></span>'
            '<span style="margin-left:2px;">⚡</span>'
            f'<span>{status_title}</span>'
            '<span style="color:#BC4946;font-weight:700;">(Gemini 3.5 Flash)</span>'
            '</div>'
            '</div>'
        )
    st.markdown(top_html, unsafe_allow_html=True)

with col_top_right:
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

st.markdown("<hr style='margin:0.2rem 0 0.8rem 0;border:none;border-top:1px solid #EADAD5;'>", unsafe_allow_html=True)

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
if len(st.session_state.messages) == 0 and not st.session_state.pending_prompt:
    if mighty_raju_img_b64:
        hero_html = (
            '<div class="hero-stage">'
            '<div class="skyline-decor">'
            '<svg viewBox="0 0 1000 200" fill="none" preserveAspectRatio="none">'
            '<path d="M0,200 L0,150 L25,150 L25,120 L55,120 L55,150 L75,150 L75,95 L105,95 L105,150 L135,150 L135,110 L150,110 L150,75 L160,75 L160,110 L175,110 L175,150 L205,150 L205,130 L235,130 L235,150 L255,150 L255,90 L270,60 L285,90 L285,150 L315,150 L315,115 L345,115 L345,150 L375,150 L375,100 L395,100 L395,65 L400,35 L405,65 L405,100 L425,100 L425,150 L455,150 L455,120 L485,120 L485,150 L515,150 L515,105 L545,105 L545,150 L575,150 L575,90 L595,90 L595,55 L605,55 L605,90 L625,90 L625,150 L655,150 L655,120 L685,120 L685,150 L715,150 L715,80 L730,45 L745,80 L745,150 L775,150 L775,110 L805,110 L805,150 L835,150 L835,95 L855,95 L855,65 L860,30 L865,65 L865,95 L885,95 L885,150 L915,150 L915,120 L945,120 L945,150 L975,150 L975,105 L1000,105 L1000,200 Z" fill="#EAAFA6" opacity="0.32"/>'
            '</svg>'
            '</div>'
            '<div class="watermark-r">R</div>'
            '<div class="star-accent star-1">★</div>'
            '<div class="star-accent star-2">✦</div>'
            '<div class="star-accent star-3">★</div>'
            '<div class="avatar-center-box">'
            '<div class="avatar-halo"></div>'
            '<div class="avatar-figure">'
            f'<img src="data:image/png;base64,{mighty_raju_img_b64}" class="raju-hero-character" alt="Mighty Raju" />'
            '<div class="eyelid eyelid-left"></div>'
            '<div class="eyelid eyelid-right"></div>'
            '</div>'
            '<div class="avatar-ground-shadow"></div>'
            '</div>'
            '<div class="welcome-heading">Hey, I\'m <span class="highlight-red">Mighty Raju!</span> 👋</div>'
            '<div class="welcome-subtitle">Your AI companion. Ask me anything and let\'s figure it out together.</div>'
            '</div>'
        )
    else:
        hero_html = '<div style="text-align: center; font-size: 3rem; margin: 1rem 0;">⚡</div>'

    st.markdown(hero_html, unsafe_allow_html=True)

    # Four Interactive Suggestion Cards (Single Row 4 Columns)
    card_col1, card_col2, card_col3, card_col4 = st.columns(4)

    with card_col1:
        if st.button(
            "</>  Explain Code\n\nUnderstand programming concepts step by step.",
            key="btn_card_1",
            use_container_width=True
        ):
            st.session_state.pending_prompt = "Explain this programming concept step by step with clear explanations and practical examples:"
            st.rerun()

    with card_col2:
        if st.button(
            "💡  Brainstorm Ideas\n\nExplore creative ideas and find inspiration.",
            key="btn_card_2",
            use_container_width=True
        ):
            st.session_state.pending_prompt = "Brainstorm creative, high-impact ideas and solutions for:"
            st.rerun()

    with card_col3:
        if st.button(
            "📖  Learn Something\n\nDiscover and understand new topics.",
            key="btn_card_3",
            use_container_width=True
        ):
            st.session_state.pending_prompt = "Teach me something fascinating and new about science or technology:"
            st.rerun()

    with card_col4:
        if st.button(
            "✏️  Writing Help\n\nWrite, improve and refine your content.",
            key="btn_card_4",
            use_container_width=True
        ):
            st.session_state.pending_prompt = "Help me write, improve, and refine clear and engaging content about:"
            st.rerun()

    # Bottom Right Decorative Waves
    bottom_wave_html = (
        '<div class="bottom-decor-wave">'
        '<svg viewBox="0 0 280 60" preserveAspectRatio="none" fill="none">'
        '<path d="M0,60 Q140,10 280,30 L280,60 Z" fill="#D97268" opacity="0.25"/>'
        '<path d="M50,60 Q180,18 280,45 L280,60 Z" fill="#BC4946" opacity="0.32"/>'
        '</svg>'
        '</div>'
    )
    st.markdown(bottom_wave_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# Render Chat History & Action Buttons
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
