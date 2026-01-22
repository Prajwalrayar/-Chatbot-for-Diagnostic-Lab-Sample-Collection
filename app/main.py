import streamlit as st
import datetime
import sys
from pathlib import Path
from pypdf import PdfReader
import re

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------------------------
# Path setup
# -------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from admin_dashboard import render_admin_dashboard
from db.database import create_table, insert_booking, count_bookings_for_slot

create_table()

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Diagnostic Lab Assistant",
    page_icon="🧪",
    layout="wide"
)

# -------------------------------------------------
# � PROFESSIONAL FLOWING GRADIENT THEME (SDE-2)
# -------------------------------------------------
st.markdown("""
<style>
    /* ============================================
       🔥 MASTER FIX - ALL TEXT WHITE
    ============================================ */
    .stApp *:not([data-baseweb="popover"] *):not([data-baseweb="menu"] *):not([role="option"] *):not([role="listbox"] *) {
        color: #ffffff !important;
    }
    
    /* Dropdown menus - dark text on white */
    [data-baseweb="popover"], [data-baseweb="popover"] *,
    [data-baseweb="menu"], [data-baseweb="menu"] *,
    [role="listbox"], [role="listbox"] *,
    [role="option"], [role="option"] * {
        color: #1a1a2e !important;
        background-color: #ffffff !important;
    }
    
    [role="option"]:hover, [role="option"]:hover *,
    [role="option"][aria-selected="true"], [role="option"][aria-selected="true"] * {
        color: #ffffff !important;
        background: #6366f1 !important;
    }
    
    /* ============================================
       GOOGLE FONTS - Inter for Professional Look
    ============================================ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    /* ============================================
       PROFESSIONAL KEYFRAME ANIMATIONS
    ============================================ */
    @keyframes meshGradient {
        0%, 100% {
            background-position: 0% 0%;
        }
        25% {
            background-position: 100% 0%;
        }
        50% {
            background-position: 100% 100%;
        }
        75% {
            background-position: 0% 100%;
        }
    }
    
    @keyframes subtleGlow {
        0%, 100% {
            box-shadow: 0 4px 60px rgba(99, 102, 241, 0.15);
        }
        50% {
            box-shadow: 0 4px 80px rgba(168, 85, 247, 0.2);
        }
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes colorFlow {
        0%, 100% { border-color: #6366f1; }
        33% { border-color: #8b5cf6; }
        66% { border-color: #06b6d4; }
    }

    /* ============================================
       MAIN APP - PROFESSIONAL MESH GRADIENT
    ============================================ */
    .stApp {
        background: 
            radial-gradient(ellipse at 0% 0%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
            radial-gradient(ellipse at 100% 0%, rgba(168, 85, 247, 0.12) 0%, transparent 50%),
            radial-gradient(ellipse at 100% 100%, rgba(6, 182, 212, 0.1) 0%, transparent 50%),
            radial-gradient(ellipse at 0% 100%, rgba(236, 72, 153, 0.08) 0%, transparent 50%),
            linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #1a1a2e 75%, #0f0f23 100%) !important;
        background-size: 200% 200% !important;
        animation: meshGradient 20s ease-in-out infinite !important;
        min-height: 100vh;
    }

    /* ============================================
       MAIN CONTAINER - Glass Morphism
    ============================================ */
    .main .block-container {
        background: rgba(15, 15, 35, 0.85) !important;
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: 24px !important;
        padding: 2.5rem !important;
        margin: 2rem auto !important;
        max-width: 920px;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        box-shadow: 
            0 4px 60px rgba(99, 102, 241, 0.1),
            0 0 0 1px rgba(255, 255, 255, 0.05),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        animation: subtleGlow 8s ease-in-out infinite, fadeUp 0.6s ease-out;
    }

    /* ============================================
       TITLE - Gradient Text Professional
    ============================================ */
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        font-size: 2.25rem !important;
        text-align: center;
        letter-spacing: -0.03em;
        margin-bottom: 1.5rem !important;
        padding: 0.75rem 0;
        background: linear-gradient(135deg, 
            #6366f1 0%, #8b5cf6 25%, #a855f7 50%, 
            #06b6d4 75%, #6366f1 100%) !important;
        background-size: 200% auto;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        animation: shimmer 4s linear infinite;
    }
    
    /* ============================================
       TEXT STYLES - High Contrast
    ============================================ */
    h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    
    p, span, label, div, li {
        color: #f1f5f9 !important;
    }
    
    .stMarkdown, .stMarkdown p, .stMarkdown span {
        color: #f1f5f9 !important;
        font-size: 1rem;
        line-height: 1.75;
    }
    
    /* Ensure all main content text is visible */
    .main p, .main span, .main label, .main div {
        color: #f1f5f9 !important;
    }

    /* ============================================
       SIDEBAR - Professional Gradient
    ============================================ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, 
            rgba(15, 15, 35, 0.98) 0%, 
            rgba(26, 26, 46, 0.98) 50%,
            rgba(22, 33, 62, 0.98) 100%) !important;
        border-right: 1px solid rgba(99, 102, 241, 0.15);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        color: #e2e8f0 !important;
        font-size: 0.85rem;
    }
    
    [data-testid="stSidebar"] .stRadio label span {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #ffffff !important;
    }

    /* ============================================
       BUTTONS - Professional with Hover Effects
    ============================================ */
    .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.875rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.35);
        min-width: 160px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.6s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%) !important;
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(139, 92, 246, 0.45);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    .stButton > button p, 
    .stButton > button span,
    .stButton > button div {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* ============================================
       INPUT FIELDS - Clean Professional
    ============================================ */
    .stTextInput > div > div > input {
        background: rgba(30, 30, 60, 0.6) !important;
        border: 2px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
        padding: 0.875rem 1.125rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15), 0 4px 20px rgba(99, 102, 241, 0.2) !important;
        background: rgba(30, 30, 60, 0.8) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #64748b !important;
    }
    
    .stTextInput > label,
    .stSelectbox > label,
    .stDateInput > label {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* ============================================
       SELECTBOX - Professional Dropdown
    ============================================ */
    .stSelectbox > div > div {
        background: rgba(30, 30, 60, 0.8) !important;
        border: 2px solid rgba(99, 102, 241, 0.4) !important;
        border-radius: 12px !important;
    }
    
    .stSelectbox > div > div > div {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    .stSelectbox > div > div > div span {
        color: #ffffff !important;
    }
    
    .stSelectbox svg {
        fill: #a5b4fc !important;
    }
    
    /* Fix dropdown value display */
    [data-baseweb="select"] > div {
        color: #ffffff !important;
    }
    
    [data-baseweb="select"] span {
        color: #ffffff !important;
    }
    
    [data-baseweb="popover"] {
        background: #ffffff !important;
        border: 2px solid #6366f1 !important;
        border-radius: 12px !important;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3) !important;
    }
    
    [data-baseweb="menu"] {
        background: #ffffff !important;
    }
    
    [data-baseweb="menu"] ul {
        background: #ffffff !important;
    }
    
    [role="listbox"] {
        background: #ffffff !important;
    }
    
    [role="option"] {
        color: #1e1e3c !important;
        background: #ffffff !important;
        transition: all 0.2s ease;
        border-radius: 8px;
        margin: 2px 4px;
        font-weight: 500 !important;
    }
    
    [role="option"]:hover,
    [role="option"][aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: #ffffff !important;
    }
    
    [role="option"] * {
        color: inherit !important;
    }

    /* ============================================
       DATE INPUT
    ============================================ */
    .stDateInput > div > div > input {
        background: rgba(30, 30, 60, 0.8) !important;
        border: 2px solid rgba(99, 102, 241, 0.4) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    /* Date picker calendar */
    [data-baseweb="calendar"] {
        background: #ffffff !important;
        border-radius: 12px !important;
    }
    
    [data-baseweb="calendar"] * {
        color: #1e1e3c !important;
    }
    
    [data-baseweb="calendar"] button[aria-selected="true"] {
        background: #6366f1 !important;
        color: #ffffff !important;
    }
    
    [data-baseweb="calendar"] button[aria-selected="true"] * {
        color: #ffffff !important;
    }

    /* ============================================
       CHAT MESSAGES - Professional Cards
    ============================================ */
    [data-testid="stChatMessage"] {
        background: rgba(30, 30, 60, 0.5) !important;
        border: 1px solid rgba(99, 102, 241, 0.15) !important;
        border-radius: 16px !important;
        padding: 1.25rem !important;
        margin: 0.875rem 0 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stChatMessage"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.15);
        border-color: rgba(99, 102, 241, 0.3) !important;
    }
    
    [data-testid="stChatMessage"] * {
        color: #e2e8f0 !important;
    }

    /* ============================================
       CHAT INPUT - Clean Design
    ============================================ */
    [data-testid="stChatInput"] {
        background: rgba(30, 30, 60, 0.6) !important;
        border: 2px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 16px !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="stChatInput"]:focus-within {
        border-color: #6366f1 !important;
        animation: colorFlow 4s linear infinite;
    }
    
    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: #f1f5f9 !important;
    }
    
    [data-testid="stChatInput"] textarea::placeholder {
        color: #64748b !important;
    }

    /* ============================================
       ALERTS - Professional Notifications
    ============================================ */
    [data-testid="stAlert"],
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        padding: 1rem 1.25rem !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stAlert"] * {
        color: #f1f5f9 !important;
    }
    
    [data-baseweb="notification"] {
        background: rgba(99, 102, 241, 0.15) !important;
        border-left: 4px solid #6366f1 !important;
    }
    
    .stSuccess, div[data-testid="stAlert"][data-baseweb*="positive"] {
        background: rgba(34, 197, 94, 0.15) !important;
        border-left: 4px solid #22c55e !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.15) !important;
        border-left: 4px solid #ef4444 !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.15) !important;
        border-left: 4px solid #f59e0b !important;
    }

    /* ============================================
       FILE UPLOADER - Clean Professional
    ============================================ */
    [data-testid="stFileUploader"] > div {
        background: rgba(30, 30, 60, 0.8) !important;
        border: 2px dashed #8b5cf6 !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"] > div:hover {
        background: rgba(99, 102, 241, 0.2) !important;
        border-color: #a855f7 !important;
    }
    
    [data-testid="stFileUploader"] *,
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] div,
    [data-testid="stFileUploader"] section,
    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploaderDropzone"] *,
    [data-testid="stFileUploaderDropzoneInstructions"] *,
    [data-testid="stFileUploaderDropzoneInstructions"] span,
    [data-testid="stFileUploaderDropzoneInstructions"] div {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
    }
    
    [data-testid="stFileUploader"] button * {
        color: #ffffff !important;
    }

    /* ============================================
       DIVIDER - Subtle Gradient Line
    ============================================ */
    hr {
        height: 2px !important;
        border: none !important;
        border-radius: 1px !important;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(99, 102, 241, 0.5) 20%,
            rgba(139, 92, 246, 0.6) 50%,
            rgba(99, 102, 241, 0.5) 80%,
            transparent 100%) !important;
        margin: 2rem 0 !important;
    }

    /* ============================================
       DATAFRAME - Professional Table
    ============================================ */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    .stDataFrame,
    .stDataFrame > div,
    [data-testid="stDataFrame"] {
        background: #ffffff !important;
    }
    
    .stDataFrame th,
    .stDataFrame td,
    .stDataFrame * {
        color: #1e1e3c !important;
        background: #ffffff !important;
    }
    
    .stDataFrame th {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: #ffffff !important;
    }

    /* ============================================
       SUBHEADERS - Professional Accent
    ============================================ */
    .stSubheader, h3 {
        color: #f1f5f9 !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        padding-bottom: 0.75rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid transparent;
        border-image: linear-gradient(90deg, #6366f1, #8b5cf6, #06b6d4) 1;
    }

    /* ============================================
       EXPANDER
    ============================================ */
    .streamlit-expanderHeader {
        background: rgba(30, 30, 60, 0.5) !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
    }

    /* ============================================
       RESPONSIVE DESIGN
    ============================================ */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1.5rem !important;
            margin: 1rem !important;
            border-radius: 16px !important;
        }
        
        h1 {
            font-size: 1.75rem !important;
        }
        
        .stButton > button {
            width: 100%;
            min-width: unset;
        }
    }

    /* ============================================
       SCROLLBAR - Minimal Professional
    ============================================ */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    /* ============================================
       SCROLLBAR - Minimal Professional
    ============================================ */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 15, 35, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #6366f1, #8b5cf6);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #8b5cf6, #a855f7);
    }
    
    /* ============================================
       SPINNER / LOADER
    ============================================ */
    .stSpinner > div {
        border-top-color: #6366f1 !important;
    }
    
    /* ============================================
       🔥 FORCE ALL TEXT VISIBLE - NUCLEAR OPTION
    ============================================ */
    /* All text white on dark backgrounds */
    .stApp, .main, .block-container,
    .stMarkdown, .stText, .stWrite,
    [data-testid="stMarkdownContainer"],
    [data-testid="stText"],
    [data-testid="stChatMessage"],
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"],
    .element-container {
        color: #ffffff !important;
    }
    
    .stApp p, .stApp span, .stApp div, .stApp label, .stApp li,
    .main p, .main span, .main div, .main label, .main li,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] div {
        color: #ffffff !important;
    }
    
    /* Radio buttons and checkbox labels */
    .stRadio label, .stCheckbox label,
    .stRadio span, .stCheckbox span,
    .stRadio p, .stCheckbox p,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] span {
        color: #ffffff !important;
    }
    
    /* Selectbox displayed value */
    [data-baseweb="select"] > div,
    [data-baseweb="select"] span,
    [data-baseweb="select"] div[aria-selected],
    .stSelectbox [data-baseweb="select"] * {
        color: #ffffff !important;
    }
    
    /* Dropdown menu items - WHITE BG, DARK TEXT */
    [data-baseweb="popover"],
    [data-baseweb="popover"] > div,
    [data-baseweb="menu"],
    [data-baseweb="menu"] ul,
    [role="listbox"],
    [role="listbox"] ul {
        background: #ffffff !important;
        color: #1a1a2e !important;
    }
    
    [role="option"],
    [role="option"] span,
    [role="option"] div,
    [data-baseweb="menu"] li,
    [data-baseweb="menu"] li span {
        color: #1a1a2e !important;
        background: #ffffff !important;
    }
    
    [role="option"]:hover,
    [role="option"]:hover span,
    [role="option"][aria-selected="true"],
    [role="option"][aria-selected="true"] span {
        background: #6366f1 !important;
        color: #ffffff !important;
    }
    
    /* File uploader text */
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] label {
        color: #ffffff !important;
    }
    
    /* Alert boxes - dark text */
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span,
    [data-testid="stAlert"] div,
    .stAlert p, .stAlert span {
        color: #1a1a2e !important;
    }
    
    /* Success/Info/Warning boxes */
    [data-baseweb="notification"] p,
    [data-baseweb="notification"] span {
        color: #1a1a2e !important;
    }
    
    /* Input placeholder */
    input::placeholder, textarea::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }
    
    /* Input text */
    input, textarea {
        color: #ffffff !important;
    }
    
    /* Strong emphasis */
    strong, b, em, i {
        color: inherit !important;
    }
    
    /* Headers force white */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Session state (ALL REQUIRED FLAGS)
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "step" not in st.session_state:
    st.session_state.step = 0

if "booking" not in st.session_state:
    st.session_state.booking = {}

if "query_mode" not in st.session_state:
    st.session_state.query_mode = None  # None | "lab"

if "booking_active" not in st.session_state:
    st.session_state.booking_active = False

if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False

if "doc_chunks" not in st.session_state:
    st.session_state.doc_chunks = []

if "doc_embeddings" not in st.session_state:
    st.session_state.doc_embeddings = None

if "embedder" not in st.session_state:
    st.session_state.embedder = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
menu = st.sidebar.radio("Menu", ["Chatbot", "Admin"])

uploaded_files = st.sidebar.file_uploader(
    "Upload Lab PDF(s)",
    type=["pdf"],
    accept_multiple_files=True,
    disabled=st.session_state.booking_active
)

# -------------------------------------------------
# Read PDFs (SAFE + STABLE)
# -------------------------------------------------
if uploaded_files:
    full_text = ""
    for f in uploaded_files:
        reader = PdfReader(f)
        for page in reader.pages:
            full_text += page.extract_text() or ""

    chunks = [
        p.strip()
        for p in full_text.replace("\n", " ").split(". ")
        if len(p.strip()) > 80
    ]

    if len(chunks) > 0:
        st.session_state.doc_chunks = chunks
        st.session_state.doc_embeddings = st.session_state.embedder.encode(chunks)
        
        # Auto-explain document on first upload
        if not st.session_state.pdf_uploaded:
            st.session_state.pdf_uploaded = True
            # Generate automatic explanation using semantic embeddings
            doc_summary_query = "explain document summary overview main content"
            q_emb = st.session_state.embedder.encode([doc_summary_query])
            sims = cosine_similarity(q_emb, st.session_state.doc_embeddings)[0]
            top_k = min(10, len(chunks))
            idx = sims.argsort()[-top_k:][::-1]
            top_chunks = [chunks[i] for i in idx if sims[i] > 0.05]
            
            if top_chunks:
                explanation = "📄 **Document Uploaded Successfully!**\n\n"
                explanation += "**Here's what this document contains:**\n\n"
                explanation += " ".join(top_chunks)
                st.session_state.messages.append({"role": "assistant", "content": explanation})
        else:
            st.session_state.pdf_uploaded = True
    else:
        st.session_state.doc_chunks = []
        st.session_state.doc_embeddings = None
        st.session_state.pdf_uploaded = False

# -------------------------------------------------
# Admin
# -------------------------------------------------
if menu == "Admin":
    render_admin_dashboard()
    st.stop()

# -------------------------------------------------
# Title
# -------------------------------------------------
st.title("🧪 Diagnostic Lab Sample Collection Assistant")

# -------------------------------------------------
# Static data
# -------------------------------------------------
LAB_TESTS = [
    "Complete Blood Count (CBC)",
    "Blood Sugar (Fasting)",
    "Blood Sugar (PP)",
    "HbA1c",
    "Lipid Profile",
    "Liver Function Test (LFT)",
    "Kidney Function Test (KFT)",
    "Thyroid Profile (T3, T4, TSH)",
    "Vitamin D",
    "Vitamin B12",
    "Urine Routine",
    "COVID-19 RT-PCR",
    "Complete Health Checkup"
]

TEST_CENTERS = [
    "Apollo Diagnostics (Jayanagar)",
    "Apollo Diagnostics (BTM Layout)",
    "Manipal TRUtest (Yeshwanthpur)",
    "Manipal TRUtest (Whitefield)",
    "Dr Lal PathLabs (Indiranagar)",
    "Dr Lal PathLabs (BTM Layout)",
    "Metropolis Healthcare (Jayanagar)",
    "Metropolis Healthcare (Malleshwaram)",
    "Aster Labs (Whitefield)",
    "Aster Labs (Hebbal)",
    "Neuberg Anand Reference Laboratory (Koramangala)",
    "Orange Health Labs (HSR Layout)",
    "Orange Health Labs (Indiranagar)",
    "SRL Diagnostics (Rajajinagar)",
    "Fortis Diagnostic Center (Bannerghatta Road)"
]

steps = [
    "entry", "name", "phone", "email",
    "test", "test_center", "date", "time", "confirm"
]

current_step = steps[st.session_state.step]
st.session_state.booking_active = current_step != "entry"

# -------------------------------------------------
# Chat history
# -------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# =================================================
# ENTRY (HOME)
# =================================================
if current_step == "entry" and st.session_state.query_mode is None:

    if not st.session_state.messages:
        st.session_state.messages.append(
            {"role": "assistant", "content": "How can I help you today?"}
        )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📅 Book Appointment"):
            st.session_state.messages.append(
                {"role": "user", "content": "Book Appointment"}
            )
            st.session_state.step = 1
            st.session_state.query_mode = None
            st.rerun()

    with col2:
        if st.button("❓ Queries"):
            st.session_state.query_mode = "lab"
            st.session_state.messages.append(
                {"role": "assistant", "content": "Here are some common laboratory questions:"}
            )
            st.rerun()

# =================================================
# LAB QUERIES
# =================================================
elif current_step == "entry" and st.session_state.query_mode == "lab":

    st.subheader("🔬 Laboratory Information")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🕘 Working hours of lab"):
            st.session_state.messages.append(
                {"role": "assistant", "content": "The lab operates from 9:00 AM to 6:00 PM."}
            )
            st.rerun()

        if st.button("📅 Is Sunday available?"):
            st.session_state.messages.append(
                {"role": "assistant", "content": "Yes, the lab is open on Sundays."}
            )
            st.rerun()

    with col2:
        if st.button("⏰ Last slot of the day"):
            st.session_state.messages.append(
                {"role": "assistant", "content": "The last slot is from 5:00 PM to 6:00 PM."}
            )
            st.rerun()

        if st.button("📆 Advance booking required?"):
            st.session_state.messages.append(
                {"role": "assistant", "content": "You must book at least 2 days in advance."}
            )
            st.rerun()

    st.divider()

    if st.button("⬅ Back to Main Menu"):
        st.session_state.query_mode = None
        st.session_state.messages.append(
            {"role": "assistant", "content": "Back to main menu."}
        )
        st.rerun()

# =================================================
# DOCUMENT Q&A HELPER FUNCTIONS
# =================================================

def detect_query_intent(query):
    """Detect if user wants detailed explanation, short summary, or specific answer"""
    query_lower = query.lower().strip()
    
    # Short/concise summary patterns
    short_patterns = [
        "explain in short", "short explanation", "brief", "briefly", 
        "summarize", "summary", "in short", "quick summary", "tldr",
        "concise", "shortly", "give me short", "short version"
    ]
    
    # Detailed explanation patterns
    detail_patterns = [
        "explain in detail", "detailed explanation", "explain thoroughly",
        "full explanation", "elaborate", "in depth", "comprehensive",
        "explain everything", "tell me everything", "complete explanation"
    ]
    
    # General explain (thorough by default)
    explain_patterns = ["explain", "what is this about", "what does it say"]
    
    for pattern in short_patterns:
        if pattern in query_lower:
            return "short"
    
    for pattern in detail_patterns:
        if pattern in query_lower:
            return "detailed"
    
    for pattern in explain_patterns:
        if pattern in query_lower and not any(p in query_lower for p in short_patterns):
            return "detailed"
    
    return "question"

def get_relevant_chunks(query, chunks, embeddings, embedder, mode="question"):
    """Get relevant chunks based on query intent using semantic similarity"""
    q_emb = embedder.encode([query])
    sims = cosine_similarity(q_emb, embeddings)[0]
    
    if mode == "detailed":
        # Get more chunks for detailed explanation (top 10-15)
        threshold = 0.10
        top_k = min(15, len(chunks))
    elif mode == "short":
        # Get fewer but most relevant chunks for summary (top 3-5)
        threshold = 0.20
        top_k = min(5, len(chunks))
    else:
        # Question mode - get semantically relevant chunks
        threshold = 0.12
        top_k = min(10, len(chunks))
    
    idx = sims.argsort()[-top_k:][::-1]
    relevant = [(chunks[i], sims[i]) for i in idx if sims[i] > threshold]
    
    return relevant

def format_response(relevant_chunks, mode, query):
    """Format response based on query intent - returns paragraph format"""
    if not relevant_chunks:
        return "❌ The document does not contain information related to your query."
    
    if mode == "detailed":
        # Thorough explanation - combine all chunks into flowing paragraphs
        response = "📚 **Detailed Explanation from Document:**\n\n"
        paragraphs = []
        for chunk, score in relevant_chunks:
            paragraphs.append(chunk.strip())
        response += " ".join(paragraphs)
        
    elif mode == "short":
        # Concise summary - combine top chunks into a brief paragraph
        response = "📝 **Quick Summary:**\n\n"
        summary_sentences = []
        for chunk, score in relevant_chunks[:3]:
            # Extract first meaningful sentence from each chunk
            sentences = chunk.split('.')
            for sent in sentences[:2]:
                sent = sent.strip()
                if sent and len(sent) > 20:
                    summary_sentences.append(sent)
        
        if summary_sentences:
            response += ". ".join(summary_sentences) + "."
        else:
            response += relevant_chunks[0][0][:300]
        response += "\n\n*For more details, ask me to 'explain' or 'explain in detail'.*"
        
    else:
        # Question mode - provide direct answer as paragraph
        response = "📘 **Answer from Document:**\n\n"
        
        # Combine most relevant chunks into flowing text
        seen_content = set()
        answer_parts = []
        
        for chunk, score in relevant_chunks:
            # Avoid duplicate content
            chunk_key = chunk[:50]
            if chunk_key not in seen_content:
                seen_content.add(chunk_key)
                answer_parts.append(chunk.strip())
        
        response += " ".join(answer_parts)
    
    return response

# =================================================
# DOCUMENT Q&A (TEXTBOX ALWAYS ENABLED)
# =================================================
if current_step == "entry":
    if st.session_state.pdf_uploaded:
        st.divider()
        st.info(" PDF uploaded!")

    q = st.chat_input("Ask anything..." if st.session_state.pdf_uploaded else "Upload a PDF to ask questions...")

    if q and st.session_state.pdf_uploaded:
        st.session_state.messages.append({"role": "user", "content": q})

        if (
            st.session_state.doc_embeddings is None
            or len(st.session_state.doc_embeddings) == 0
        ):
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": "I couldn't extract readable content from the uploaded document."
                }
            )
            st.rerun()

        # Detect query intent
        intent = detect_query_intent(q)
        
        # Get relevant chunks based on intent
        relevant_chunks = get_relevant_chunks(
            q, 
            st.session_state.doc_chunks,
            st.session_state.doc_embeddings,
            st.session_state.embedder,
            mode=intent
        )
        
        # Format response based on intent
        answer = format_response(relevant_chunks, intent, q)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
        st.rerun()

# =================================================
# BOOKING FLOW
# =================================================
if current_step == "name":
    st.subheader("📝 Step 1: Enter Your Name")
    name_input = st.text_input("Full Name", key="name_input")
    if st.button("Next", key="name_btn"):
        if name_input and len(name_input.strip()) > 1:
            st.session_state.booking["name"] = name_input.strip()
            st.session_state.messages.append({"role": "user", "content": f"Name: {name_input}"})
            st.session_state.step += 1
            st.rerun()
        else:
            st.error("Please enter a valid name.")

elif current_step == "phone":
    st.subheader("📞 Step 2: Enter Phone Number")
    phone_input = st.text_input("Phone (10 digits)", key="phone_input")
    if st.button("Next", key="phone_btn"):
        if phone_input and phone_input.isdigit() and len(phone_input) == 10:
            st.session_state.booking["phone"] = phone_input
            st.session_state.messages.append({"role": "user", "content": f"Phone: {phone_input}"})
            st.session_state.step += 1
            st.rerun()
        else:
            st.error("Phone number must be exactly 10 digits.")

elif current_step == "email":
    st.subheader("📧 Step 3: Enter Email")
    email_input = st.text_input("Gmail Address", key="email_input")
    if st.button("Next", key="email_btn"):
        if email_input and re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email_input):
            st.session_state.booking["email"] = email_input
            st.session_state.messages.append({"role": "user", "content": f"Email: {email_input}"})
            st.session_state.step += 1
            st.rerun()
        else:
            st.error("Please enter a valid Gmail address.")

elif current_step == "test":
    st.subheader("🧪 Step 4: Select Test")
    test_selected = st.selectbox("Choose a Test", LAB_TESTS, key="test_select")
    if st.button("Next", key="test_btn"):
        st.session_state.booking["test"] = test_selected
        st.session_state.messages.append({"role": "user", "content": f"Test: {test_selected}"})
        st.session_state.step += 1
        st.rerun()

elif current_step == "test_center":
    st.subheader("🏥 Step 5: Select Test Center")
    center_selected = st.selectbox("Choose a Center", TEST_CENTERS, key="center_select")
    if st.button("Next", key="center_btn"):
        st.session_state.booking["test_center"] = center_selected
        st.session_state.messages.append({"role": "user", "content": f"Center: {center_selected}"})
        st.session_state.step += 1
        st.rerun()

elif current_step == "date":
    st.subheader("📅 Step 6: Select Date")
    date_selected = st.date_input(
        "Appointment Date",
        min_value=datetime.date.today() + datetime.timedelta(days=2),
        key="date_input"
    )
    if st.button("Next", key="date_btn"):
        st.session_state.booking["date"] = str(date_selected)
        st.session_state.messages.append({"role": "user", "content": f"Date: {date_selected}"})
        st.session_state.step += 1
        st.rerun()

elif current_step == "time":
    st.subheader("⏰ Step 7: Select Time Slot")
    slots = []
    for h in range(9, 18):
        t = f"{h:02d}:00"
        b = count_bookings_for_slot(
            st.session_state.booking["test"],
            st.session_state.booking["test_center"],
            st.session_state.booking["date"],
            t
        )
        if b < 2:
            slots.append((t, f"{t} ({2-b} slots left)"))
    
    if slots:
        slot_selected = st.selectbox("Choose Time", slots, format_func=lambda x: x[1], key="time_select")
        if st.button("Next", key="time_btn"):
            st.session_state.booking["time"] = slot_selected[0]
            st.session_state.messages.append({"role": "user", "content": f"Time: {slot_selected[0]}"})
            st.session_state.step += 1
            st.rerun()
    else:
        st.warning("No slots available for this date. Please go back and select another date.")

elif current_step == "confirm":
    st.subheader("✅ Step 8: Confirm Your Booking")
    st.write("**Please review your booking details:**")
    st.write(f"- **Name:** {st.session_state.booking.get('name', '')}")
    st.write(f"- **Phone:** {st.session_state.booking.get('phone', '')}")
    st.write(f"- **Email:** {st.session_state.booking.get('email', '')}")
    st.write(f"- **Test:** {st.session_state.booking.get('test', '')}")
    st.write(f"- **Center:** {st.session_state.booking.get('test_center', '')}")
    st.write(f"- **Date:** {st.session_state.booking.get('date', '')}")
    st.write(f"- **Time:** {st.session_state.booking.get('time', '')}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Confirm Booking", key="confirm_btn"):
            insert_booking(st.session_state.booking)
            st.session_state.messages.append(
                {"role": "assistant", "content": "✅ Appointment booked successfully!"}
            )
            st.session_state.booking = {}
            st.session_state.step = 0
            st.session_state.query_mode = None
            st.rerun()
    with col2:
        if st.button("❌ Cancel", key="cancel_btn"):
            st.session_state.booking = {}
            st.session_state.step = 0
            st.session_state.query_mode = None
            st.session_state.messages.append(
                {"role": "assistant", "content": "Booking cancelled. How can I help you?"}
            )
            st.rerun()
