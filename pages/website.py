import streamlit as st

st.set_page_config(page_title="Website Age Checker", layout="wide")

# ---------- LOAD CSS ----------
with open("assets/style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------- HIDE STREAMLIT DEFAULT ----------
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
.stDeployButton {display:none;}

[data-testid="stToolbar"] {
    display: none !important;
}

section[data-testid="stSidebarNav"] {
    display: none !important;
}

.block-container {
    padding-top: 0rem !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- SAMPLE AGE FUNCTION ----------
def get_domain_age(domain):
    domain = domain.replace("https://", "").replace("http://", "").replace("www.", "").strip("/").strip()

    if domain.lower() == "paypal.com":
        return {
            "domain": "paypal.com",
            "created": "13 October 1999",
            "updated": "10 September 2024",
            "expiry": "13 October 2026",
            "registrar": "MarkMonitor Inc.",
            "country": "US",
            "age": "24 years",
            "risk": "Old Domain - Lower Risk"
        }
    elif domain.lower() == "sbi.co.in":
        return {
            "domain": "sbi.co.in",
            "created": "24 July 2003",
            "updated": "12 July 2024",
            "expiry": "24 July 2027",
            "registrar": "INRegistry",
            "country": "IN",
            "age": "20+ years",
            "risk": "Old Domain - Lower Risk"
        }
    elif domain.lower() == "google.com":
        return {
            "domain": "google.com",
            "created": "15 September 1997",
            "updated": "21 January 2025",
            "expiry": "14 September 2028",
            "registrar": "MarkMonitor Inc.",
            "country": "US",
            "age": "27+ years",
            "risk": "Old Domain - Lower Risk"
        }
    else:
        return {
            "domain": domain,
            "created": "02 December 2024",
            "updated": "15 January 2025",
            "expiry": "02 December 2026",
            "registrar": "GoDaddy Inc.",
            "country": "IN",
            "age": "4 months",
            "risk": "Newer Domain - Check Carefully"
        }

# ---------- TOP INFO BAR ----------
st.markdown("""
<div class="top-strip">
    <div class="top-strip-inner">
        <span>LinkShield AI – Free cybersecurity tool for India</span>
        <span>Cybercrime Helpline: <b>1930</b></span>
        <span>Security Guide</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- NAVBAR ----------
st.markdown("""
<div class="custom-navbar">
    <div class="nav-left">
        <div class="brand-box">
            <div class="brand-logo">AI</div>
            <div class="brand-name">LinkShield AI</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- HERO ----------
st.markdown("""
<div class="age-hero">
    <div class="hero-badge">WEBSITE AGE CHECKER</div>
    <h1>
        Free Website Age Checker India —
        <span>When Was This Domain Registered?</span>
    </h1>
    <p>
        Check registration date, expiry date, and domain age using WHOIS.
        A newly registered website can be a strong fraud signal.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------- INFO SECTION ----------
st.markdown("""
<div class="age-info">
    <h2>Website Age Checker India — Find Out When Any Domain Was Registered</h2>
    <p>
        Use LinkShield AI's <b>free domain age checker</b> to find out when a domain was registered,
        when it expires, who registered it, and other important WHOIS details.
        Newly created domains can sometimes be risky, especially for phishing websites.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------- SEARCH CARD ----------
if "age_input" not in st.session_state:
    st.session_state.age_input = ""

st.markdown('<div class="search-card">', unsafe_allow_html=True)
st.markdown('<div class="search-title">🔎 Check Domain Age</div>', unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])

with col1:
    domain = st.text_input(
        "",
        value=st.session_state.age_input,
        placeholder="e.g. google.com or https://example.com",
        key="domain_age_input",
        label_visibility="collapsed"
    )

with col2:
    check_btn = st.button("📅 Check Age", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- RESULT ----------
# ---------- RESULT ----------
if check_btn and domain.strip():
    data = get_domain_age(domain)

    st.markdown("""
    <style>
    .result-title {
        font-size: 40px;
        font-weight: 800;
        color: #163b77;
        margin-top: 25px;
        margin-bottom: 20px;
        margin-left :20px;
    }
    .mini-card {
        background: #ffffff;
        border: 1px solid #dbe6f5;
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 8px 20px rgba(26, 68, 135, 0.08);
    }
    .mini-label {
        font-size: 13px;
        color: #6c85aa;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .mini-value {
        font-size: 20px;
        color: #1a3f78;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="result-title">Website Age Result</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f'''
        <div class="mini-card">
            <div class="mini-label">Domain</div>
            <div class="mini-value">{data["domain"]}</div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown(f'''
        <div class="mini-card">
            <div class="mini-label">Created On</div>
            <div class="mini-value">{data["created"]}</div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown(f'''
        <div class="mini-card">
            <div class="mini-label">Updated On</div>
            <div class="mini-value">{data["updated"]}</div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown(f'''
        <div class="mini-card">
            <div class="mini-label">Expiry Date</div>
            <div class="mini-value">{data["expiry"]}</div>
        </div>
        ''', unsafe_allow_html=True)

    with c2:
        st.markdown(f'''
        <div class="mini-card">
            <div class="mini-label">Registrar</div>
            <div class="mini-value">{data["registrar"]}</div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown(f'''
        <div class="mini-card">
            <div class="mini-label">Country</div>
            <div class="mini-value">{data["country"]}</div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown(f'''
        <div class="mini-card">
            <div class="mini-label">Domain Age</div>
            <div class="mini-value">{data["age"]}</div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown(f'''
        <div class="mini-card">
            <div class="mini-label">Risk Note</div>
            <div class="mini-value">{data["risk"]}</div>
        </div>
        ''', unsafe_allow_html=True)