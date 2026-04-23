import streamlit as st
import qrcode
from io import BytesIO

st.set_page_config(page_title="LinkShield AI - QR Tools", layout="wide")

# ---------- LOAD CSS ----------
with open("assets/style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------- HIDE DEFAULT STREAMLIT ----------
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "qr_mode" not in st.session_state:
    st.session_state.qr_mode = "scan"

if "nav_page" not in st.session_state:
    st.session_state.nav_page = "QR Tools"

# ---------- TOP STRIP ----------
st.markdown("""
<div class="top-strip">
    <div class="top-strip-text">
        IN <span>LinkShield AI</span> — Free cybersecurity tool for India. Cybercrime Helpline: <b>1930</b>
        <span class="guide-link">Security Guide →</span>
    </div>
</div>
""", unsafe_allow_html=True)



st.markdown("""
<div class="brand-row">
    <div class="brand-logo-box">LS</div>
    <div class="brand-name-text">LinkShield AI</div>
</div>
""", unsafe_allow_html=True)

# ---------- HERO ----------
st.markdown("""
<div class="qr-hero">
    <div class="qr-hero-label">QR CODE SECURITY TOOL</div>
    <div class="qr-hero-title">
        Free QR Code Safety Scanner India —
        <span>Detect Fake UPI QR Codes</span>
    </div>
    <div class="qr-hero-subtitle">
        Decode any QR code and instantly check the embedded URL for phishing
        threats before you visit it. Detect fake UPI payment QR codes and
        malicious QRishing attacks.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- TAB BUTTONS ----------
st.markdown('<div class="qr-main-wrap">', unsafe_allow_html=True)

tab1, tab2 = st.columns(2)

with tab1:
    if st.button("◫ Scan QR Code", key="scan_tab", use_container_width=True):
        st.session_state.qr_mode = "scan"

with tab2:
    if st.button("✎ Generate QR Code", key="generate_tab", use_container_width=True):
        st.session_state.qr_mode = "generate"

# ---------- SCAN MODE ----------
if st.session_state.qr_mode == "scan":
    st.markdown("""
    <div class="qr-upload-box">
        <div class="qr-upload-icon">📷</div>
        <div class="qr-upload-title">Upload or drag a QR code image</div>
        <div class="qr-upload-sub">PNG, JPG, GIF, WebP · Max 5MB</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload QR image",
        type=["png", "jpg", "jpeg", "gif", "webp"],
        label_visibility="collapsed",
        key="qr_upload"
    )

    if uploaded_file is not None:
        st.success("QR image uploaded successfully.")

        st.markdown("""
        <div class="qr-result-card">
            <div class="qr-result-title">QR Scan Result</div>
            <div class="qr-safe-chip">Image uploaded</div>
            <div class="qr-result-text">
                Your QR image has been uploaded successfully. Next, you can connect
                your backend to decode the QR content, extract URL/UPI data, and
                classify it as legitimate, suspicious, or phishing.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------- GENERATE MODE ----------
elif st.session_state.qr_mode == "generate":
    st.markdown("""
    <div class="qr-generate-box">
        <div class="qr-generate-title">Generate QR Code</div>
        <div class="qr-generate-subtitle">
            Enter text, URL, or UPI link to generate a QR code.
        </div>
    </div>
    """, unsafe_allow_html=True)

    qr_text = st.text_input("Enter text or URL", placeholder="Enter URL, text, or UPI link", key="qr_text_input")

    if st.button("Generate Now", key="generate_now_btn"):
        if qr_text.strip():
            qr = qrcode.make(qr_text)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            buffer.seek(0)

            st.markdown("""
            <div class="qr-result-card">
                <div class="qr-result-title">Generated QR Code</div>
                <div class="qr-safe-chip">Generated successfully</div>
            </div>
            """, unsafe_allow_html=True)

            st.image(buffer, width=250)

            st.download_button(
                label="Download QR Code",
                data=buffer,
                file_name="generated_qr.png",
                mime="image/png",
                key="download_qr_btn"
            )
        else:
            st.warning("Please enter text or URL first.")

# ---------- INFO CARDS ----------
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="qr-info-card">
        <div class="qr-info-title">⚠️ QRishing Attacks</div>
        <div class="qr-info-text">
            QRishing is phishing via malicious QR codes. Attackers place fake QR
            codes on payment terminals, posters, or messages claiming to be UPI
            refunds or cashback. Always decode and check the QR before scanning.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="qr-info-card">
        <div class="qr-info-title">🛡️ India QR Safety Tips</div>
        <div class="qr-info-text">
            Never scan QR codes claiming you will receive money instantly.
            In UPI, to receive money you usually do not need to scan a QR.
            Always verify the merchant or receiver name before payment.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- OPTIONAL PAGE OUTPUT ----------
if st.session_state.nav_page != "QR Tools":
    st.info(f"You clicked: {st.session_state.nav_page}")