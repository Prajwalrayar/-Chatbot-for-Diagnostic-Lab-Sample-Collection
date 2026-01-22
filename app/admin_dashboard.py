import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd
from db.database import fetch_all_bookings


def render_admin_dashboard():
    # Professional Admin Dashboard Styling - Matching Main Theme
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        .admin-header {
            background: rgba(30, 30, 60, 0.6);
            backdrop-filter: blur(20px);
            padding: 2rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            text-align: center;
            border: 1px solid rgba(99, 102, 241, 0.2);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.25);
        }
        .admin-header h1 {
            font-family: 'Inter', sans-serif !important;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0;
            font-size: 1.75rem;
            font-weight: 800;
            letter-spacing: -0.03em;
        }
        .stats-container {
            display: flex;
            gap: 1.25rem;
            margin: 1.5rem 0;
        }
        .stats-card {
            font-family: 'Inter', sans-serif;
            background: rgba(30, 30, 60, 0.5);
            backdrop-filter: blur(10px);
            padding: 1.75rem;
            border-radius: 16px;
            color: #f1f5f9;
            text-align: center;
            border: 1px solid rgba(99, 102, 241, 0.2);
            flex: 1;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .stats-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 20px 40px rgba(99, 102, 241, 0.2);
            border-color: rgba(99, 102, 241, 0.4);
        }
        .stats-icon {
            font-size: 2.25rem;
            margin-bottom: 0.75rem;
        }
        .stats-number {
            font-size: 2.75rem;
            font-weight: 800;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .stats-label {
            font-size: 0.8rem;
            color: #94a3b8;
            font-weight: 600;
            margin-top: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .stats-card.pink .stats-number {
            background: linear-gradient(135deg, #ec4899 0%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .stats-card.teal .stats-number {
            background: linear-gradient(135deg, #06b6d4 0%, #22d3ee 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="admin-header"><h1>🔐 Admin Dashboard</h1></div>', unsafe_allow_html=True)

    password = st.text_input("Enter Admin Password", type="password", placeholder="Enter password...")

    if password != "admin123":
        if password:
            st.error("❌ Unauthorized access - Invalid password")
        else:
            st.info("🔑 Please enter the admin password to access the dashboard")
        return

    st.success("✅ Access granted - Welcome Admin!")
    
    st.divider()

    bookings = fetch_all_bookings()
    
    # Stats Cards - Professional Design
    total_bookings = len(bookings) if bookings else 0
    unique_tests = len(set([b[4] for b in bookings])) if bookings else 0
    unique_centers = len(set([b[5] for b in bookings])) if bookings else 0
    
    st.markdown(f'''
    <div class="stats-container">
        <div class="stats-card">
            <div class="stats-icon">📊</div>
            <div class="stats-number">{total_bookings}</div>
            <div class="stats-label">Total Bookings</div>
        </div>
        <div class="stats-card pink">
            <div class="stats-icon">🧪</div>
            <div class="stats-number">{unique_tests}</div>
            <div class="stats-label">Test Types</div>
        </div>
        <div class="stats-card teal">
            <div class="stats-icon">🏥</div>
            <div class="stats-number">{unique_centers}</div>
            <div class="stats-label">Centers Used</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.divider()
    
    st.subheader("📋 All Bookings")

    if not bookings:
        st.info("📭 No bookings found.")
        return

    # 🔹 UPDATED: 8 columns (including Test Center)
    columns = [
        "ID",
        "Name",
        "Phone",
        "Email",
        "Test",
        "Test Center",
        "Date",
        "Time"
    ]

    df = pd.DataFrame(bookings, columns=columns)
    df.reset_index(drop=True, inplace=True)

    st.dataframe(df, use_container_width=True)

    st.divider()

    # ---------------- DOWNLOAD CSV ----------------
    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download All Bookings (CSV)",
        data=csv_data,
        file_name="lab_bookings.csv",
        mime="text/csv"
    )
