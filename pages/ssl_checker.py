import os
import streamlit as st
from tool_utils.ssl_checker import check_ssl

st.set_page_config(page_title="SSL Checker", layout="wide")

css_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "assets",
    "style.css"
)

with open(css_path, "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="ssl-top-strip">
    IN PhishGuard — Free Cybersecurity Tool for India. Cybercrime Helpline: 1930 &nbsp; Security Guide →
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="ssl-navbar">
    <div class="ssl-nav-left">
        <div class="ssl-logo-box">LS</div>
        <div class="ssl-logo-text">LinkShield AI</div>
    </div>
   
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="ssl-hero-wrap">
    <div class="ssl-hero-left">
        <div class="ssl-badge">🔒 SSL CERTIFICATE CHECKER</div>
        <div class="ssl-big-title">
            Free SSL Certificate Checker India —
            <span>Verify HTTPS Safety</span>
        </div>
        <div class="ssl-big-desc">
            Verify HTTPS certificates — check validity, expiry, self-signed status, and certificate
            authority. Fake banking sites often use suspicious SSL.
        </div>
    </div>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="ssl-info-section">
    <div class="ssl-info-title">Free SSL Certificate Checker India — What It Does</div>
    <div class="ssl-info-text">
        PhishGuard's <b>free SSL certificate checker</b> lets you instantly <b>check SSL certificate website</b>
        validity for any domain. Enter any URL to verify HTTPS certificate status, expiry date, issuer (CA), and
        self-signed detection. Our <b>SSL checker India</b> is trusted by thousands of users who want to
        <b>check if a website HTTPS is safe in India</b> before entering passwords, OTPs, or banking details.
        Phishing sites increasingly use free SSL — so HTTPS alone does not mean a site is safe.
        Always check the certificate issuer, domain age, and registration date together.
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class="ssl-check-title">🔒 Check SSL Certificate</div>
""", unsafe_allow_html=True)

input_col, button_col = st.columns([5, 1])

with input_col:
    url = st.text_input(
        "",
        placeholder="e.g. google.com or https://example.com",
        key="ssl_input"
    )

with button_col:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    check_clicked = st.button("🛡 Check SSL", use_container_width=True)


st.markdown("</div>", unsafe_allow_html=True)

if check_clicked:
    if not url.strip():
        st.warning("Please enter a URL.")
    else:
        result = check_ssl(url)
if check_clicked:
    if not url.strip():
        st.warning("Please enter a URL.")
    else:
        result = check_ssl(url)
        # temporary debug

        if "issuer" in result:
            st.markdown(f"""
            <div class="ssl-status-box">
                {result["status"]}
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="ssl-result-card">', unsafe_allow_html=True)
            st.markdown('<div class="ssl-result-card-title">Issuer Details</div>', unsafe_allow_html=True)

            for key, value in result["issuer"].items():
                col1, col2 = st.columns([1.2, 2.2])
                with col1:
                    st.markdown(f'<div class="ssl-result-key">{key}</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div class="ssl-result-value">{value}</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)


            
            st.markdown('<div class="ssl-section-right">', unsafe_allow_html=True)
            st.markdown('<div class="ssl-result-card">', unsafe_allow_html=True)
            st.markdown('<div class="ssl-result-card-title">Subject Details</div>', unsafe_allow_html=True)

            for key, value in result["subject"].items():
                col1, col2 = st.columns([1.2, 2.2])
                with col1:
                    st.markdown(f'<div class="ssl-result-key">{key}</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div class="ssl-result-value">{value}</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.error(result["status"])