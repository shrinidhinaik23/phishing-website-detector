import streamlit as st
import dns.resolver

st.set_page_config(page_title="PhishGuard - DNS Lookup", layout="wide")

# ---------- LOAD CSS ----------
with open("assets/style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    

# ---------- HIDE STREAMLIT ----------
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ---------- DNS FUNCTION ----------
def get_dns_records(domain):
    record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]
    results = {}

    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            values = []

            for rdata in answers:
                if rtype == "MX":
                    values.append(f"{str(rdata.exchange).rstrip('.')} (Priority: {rdata.preference})")
                else:
                    values.append(str(rdata).replace('"', ''))

            results[rtype] = values if values else ["No record found"]

        except Exception:
            results[rtype] = ["No record found"]

    return results

# ---------- TOP BAR ----------
st.markdown("""
<div class="top-strip">
    <div class="top-strip-text">
        IN <span>LinkShield AI</span> — Free cybersecurity tool for India. Cybercrime Helpline: <b>1930</b>
        <span class="guide-link">Security Guide →</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- NAVBAR ----------
st.markdown("""
<div class="main-navbar">
    <div class="nav-left">
        <div class="brand-box">
            <div class="brand-logo">LS</div>
            <div class="brand-name">LinkShield Ai</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- HERO ----------
hero_left, hero_right = st.columns([4.5, 1.5], gap="large")

with hero_left:
    st.markdown("""
    <div class="hero-section">
        <div class="dns-chip">DNS LOOKUP</div>
        <div class="hero-title">
            Free DNS Lookup Tool India —
            <span>Check All DNS Records</span>
        </div>
        <div class="hero-subtitle">
            Query A, AAAA, MX, NS, TXT, CNAME records — plus SPF and DMARC email
            authentication. Detect misconfigured and suspicious domains.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------- INFO SECTION ----------
st.markdown("""
<div class="info-wrapper">
    <div class="info-heading">
        DNS Lookup Tool India — Check A, MX, NS, TXT, SPF &amp; DMARC Records Free
    </div>
    <div class="info-text">
        Use PhishGuard’s <b>free DNS lookup tool</b> to check MX record domain configuration,
        verify SPF and DMARC email authentication, and query A, AAAA, NS, CNAME, and TXT
        records instantly. Our <b>DNS records checker online</b> is built for Indian security
        researchers, developers, and everyday users who want to verify domain configurations.
        Phishing domains often have missing DMARC records and suspicious NS configurations —
        use our <b>DNS lookup India</b> tool to spot anomalies before they affect you.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- LOOKUP CARD ----------
st.markdown('<div class="lookup-outer-card">', unsafe_allow_html=True)
st.markdown('<div class="lookup-heading">🔎 DNS Lookup</div>', unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])

with col1:
    domain = st.text_input(
        "",
        placeholder="e.g. google.com or paypal.com",
        label_visibility="collapsed"
    )

with col2:
    search_clicked = st.button("Look Up DNS")

st.markdown('</div>', unsafe_allow_html=True)

# ---------- RESULT ----------
if search_clicked:
    if domain.strip():
        clean_domain = (
            domain.strip()
            .replace("https://", "")
            .replace("http://", "")
            .split("/")[0]
        )

        records = get_dns_records(clean_domain)

        st.markdown(
            f'<div class="results-card"><div class="results-title">DNS Records for {clean_domain}</div></div>',
            unsafe_allow_html=True
        )

        for rtype, values in records.items():
            card_html = f'<div class="record-card"><div class="record-type">{rtype} Record</div>'

            for value in values:
                if value == "No record found":
                    card_html += '<div class="record-value empty">No record found</div>'
                else:
                    card_html += f'<div class="record-value">• {value}</div>'

            card_html += '</div>'

            st.markdown(card_html, unsafe_allow_html=True)

    else:
        st.warning("Please enter a domain name.")