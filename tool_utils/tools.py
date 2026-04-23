import streamlit as st

st.set_page_config(page_title="Tools", layout="wide")

with open("assets/style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
.stDeployButton {display:none;}
[data-testid="stToolbar"] {display:none !important;}
section[data-testid="stSidebarNav"] {display:none !important;}
.block-container {padding-top: 0rem !important;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="top-strip">
    <div class="top-strip-inner">
        <span>🔐 Stay ahead of cyber threats — Scan every link before you click.</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="custom-navbar">
    <div class="nav-left">
        <div class="brand-box">
            <div class="brand-logo">LS</div>
            <div class="brand-name">LinkShield AI</div>
        </div>
    </div>
    <div class="nav-right">
        <span>Scanner</span>
        <span>Tools</span>
        <span>Login</span>
        <span>Register</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="tools-page-header">
    <h1>Tools</h1>
    <p>Choose a phishing analysis tool below.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="tool-card">
        <h3>SSL Checker</h3>
        <p>
        Analyze the SSL certificate of any website to verify its security,
        encryption strength, validity period, and issuing authority.
        This helps you detect insecure or fake websites before sharing sensitive information.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open SSL Checker", key="ssl_btn"):
        st.switch_page("pages/ssl_checker.py")

    st.markdown("""
    <div class="tool-card">
        <h3>QR Tools</h3>
        <p>
        Generate secure QR codes for URLs or text instantly.
        Useful for sharing links safely while avoiding phishing risks hidden behind unknown or malicious QR codes.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open QR Tools", key="qr_btn"):
        st.switch_page("pages/qr_tools.py")

with col2:
    st.markdown("""
    <div class="tool-card">
        <h3>DNS Lookup</h3>
        <p>
        Analyze domain DNS records like A, MX, NS, TXT, and CNAME
        to inspect infrastructure and detect suspicious domain behavior.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open DNS Lookup", key="dns_btn"):
        st.switch_page("pages/dns_lookup.py")

    st.markdown("""
    <div class="tool-card">
        <h3>Website Age</h3>
        <p>
        Check the domain’s registration date, last update, and expiry details
        to determine how long a website has existed.
        Newly created domains are often linked to phishing or scam activities.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Website Age", key="age_btn"):
        st.switch_page("pages/website.py")