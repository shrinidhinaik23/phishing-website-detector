import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import pandas as pd
import requests

st.set_page_config(page_title="LinkShield AI", layout="wide")

with open("assets/style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* ---------- AUTH PAGES ---------- */
.auth-wrapper {
    display: flex;
    justify-content: center;
    margin-top: 24px;
    margin-bottom: 30px;
}
.auth-card {
    width: 100%;
    max-width: 640px;
    background: #ffffff;
    border: 1px solid #dbe7fb;
    border-radius: 28px;
    padding: 38px 34px;
    box-shadow: 0 20px 45px rgba(30, 67, 135, 0.10);
}
.auth-icon {
    width: 64px;
    height: 64px;
    border-radius: 18px;
    background: linear-gradient(135deg, #2f6fdd, #5a8df0);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    color: white;
    margin-bottom: 18px;
}
.auth-title {
    font-size: 34px;
    font-weight: 800;
    color: #163b77;
    margin-bottom: 8px;
}
.auth-subtitle {
    font-size: 17px;
    color: #6e84a3;
    margin-bottom: 28px;
    line-height: 1.5;
}
.auth-links {
    display: flex;
    justify-content: space-between;
    margin-top: 16px;
    margin-bottom: 10px;
    font-size: 15px;
}
.auth-links span {
    color: #2f6fdd;
    font-weight: 600;
    cursor: pointer;
}
.auth-divider {
    text-align: center;
    color: #94a7c3;
    font-size: 14px;
    margin: 18px 0 10px 0;
}
.auth-footer {
    text-align: center;
    margin-top: 18px;
    font-size: 15px;
    color: #6e84a3;
}
.auth-footer b {
    color: #2f6fdd;
}

/* Better button style */
.stButton > button {
    height: 50px;
    border-radius: 14px;
    font-size: 17px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="top-banner">
    <b>🔐 Stay ahead of cyber threats — Scan every link before you click.</b>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# SESSION STATE
# ----------------------------
if "scan_result" not in st.session_state:
    st.session_state.scan_result = None

if "nav_page" not in st.session_state:
    st.session_state.nav_page = "Scanner"

if "scan_history" not in st.session_state:
    st.session_state.scan_history = []

# ----------------------------
# FUNCTION TO SAVE SCAN
# ----------------------------
def save_scan(url, status):
    st.session_state.scan_history.append({
        "url": url,
        "status": status,
        "time": datetime.now()
    })

# ----------------------------
# FUNCTION TO CALCULATE STATS
# ----------------------------
def get_scan_stats():
    history = st.session_state.scan_history

    total_scans = len(history)
    high_risk_count = sum(1 for item in history if item["status"] == "High Risk")
    suspicious_count = sum(1 for item in history if item["status"] == "Suspicious")
    safe_count = sum(1 for item in history if item["status"] == "Safe")

    today_date = datetime.now().date()
    today_scans = sum(1 for item in history if item["time"].date() == today_date)

    high_risk_urls = [item["url"] for item in history if item["status"] == "High Risk"]
    suspicious_urls = [item["url"] for item in history if item["status"] == "Suspicious"]
    safe_urls = [item["url"] for item in history if item["status"] == "Safe"]

    return {
        "total_scans": total_scans,
        "high_risk_count": high_risk_count,
        "suspicious_count": suspicious_count,
        "safe_count": safe_count,
        "today_scans": today_scans,
        "high_risk_urls": high_risk_urls,
        "suspicious_urls": suspicious_urls,
        "safe_urls": safe_urls
    }



def predict_url(url):
    try:
        res = requests.post(
            "http://127.0.0.1:5000/predict",
            json={"url": url},
            timeout=15
        )

        if res.status_code == 200:
            data = res.json()
            return {
                "status": data.get("status", "Suspicious"),
                "high_risk": data.get("high_risk", 30),
                "suspicious": data.get("suspicious", 60),
                "safe_score": data.get("safe_score", 20)
            }
        else:
            return {
                "status": "Suspicious",
                "high_risk": 30,
                "suspicious": 60,
                "safe_score": 20
            }

    except Exception as e:
        st.error(f"Backend connection failed: {e}")
        return {
            "status": "Suspicious",
            "high_risk": 30,
            "suspicious": 60,
            "safe_score": 20
        }

# ----------------------------
# NAVBAR
# ----------------------------
nav1, nav2 = st.columns([7, 3])

with nav1:
    st.markdown("""
    <div class="logo-area">
        <div class="logo-box">LS</div>
        <div class="brand">LinkShield AI</div>
    </div>
    """, unsafe_allow_html=True)

with nav2:
    st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
    n1, n2, n3, n4, n5 = st.columns([1.2,1.2,1.2,1.2,1.2])

    with n1:
        if st.button("Scanner", key="nav_scanner", use_container_width=True):
            st.session_state.nav_page = "Scanner"

    with n2:
        if st.button("Tools", key="nav_tools", use_container_width=True):
            st.session_state.nav_page = "Tools"

    with n3:
        if st.button("Login", key="nav_login", use_container_width=True):
            st.session_state.nav_page = "Login"

    with n4:
        if st.button("Register", key="nav_register", use_container_width=True):
            st.session_state.nav_page = "Register"

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

# ----------------------------
# NAVIGATION PAGES
# ----------------------------

if st.session_state.nav_page == "Tools":
  

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
    

            

elif st.session_state.nav_page == "Login":
    st.markdown("""
    <div class="auth-wrapper">
        <div class="auth-card">
            <div class="auth-icon">🔐</div>
            <div class="auth-title">Welcome Back</div>
            <div class="auth-subtitle">
                Login to continue scanning URLs, track history, and manage your phishing protection dashboard.
            </div>
    """, unsafe_allow_html=True)

    left_space, center_col, right_space = st.columns([1.2, 2.2, 1.2])

    with center_col:
        username = st.text_input(
            "Username or Email",
            key="login_username",
            placeholder="Enter your username or email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password",
            placeholder="Enter your password"
        )

        remember = st.checkbox("Remember me", key="remember_me")

        login_click = st.button("Login Now", key="login_now", use_container_width=True)

        action_col1, action_col2, action_col3 = st.columns([1, 2.2, 1])

        with action_col1:
            if st.button("Forgot Password?", key="forgot_password_btn", use_container_width=True):
                st.info("Forgot password page not added yet.")

        with action_col3:
            if st.button("Create Account", key="create_account_btn", use_container_width=True):
                st.session_state.nav_page = "Register"
                st.rerun()

        st.markdown("""
            <div class="auth-divider">Secure login protected by PhishGuard</div>
        """, unsafe_allow_html=True)

        st.markdown(
            "<div class='auth-footer'>New here?</div>",
            unsafe_allow_html=True
        )

        footer_left, footer_center, footer_right = st.columns([1.4, 1.2, 1.4])

        with footer_center:
            if st.button("Register to get started", key="register_get_started_btn", use_container_width=True):
                st.session_state.nav_page = "Register"
                st.rerun()

        if login_click:
            if not username.strip() or not password.strip():
                st.warning("Please enter both username and password.")
            else:
                st.success("Login successful UI created. Connect backend authentication next.")

    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.nav_page == "Register":
    st.markdown("""
    <div class="auth-wrapper">
        <div class="auth-card">
            <div class="auth-icon">📝</div>
            <div class="auth-title">Create Account</div>
            <div class="auth-subtitle">
                Join PhishGuard to scan links, save history, and stay protected from phishing attacks.
            </div>
    """, unsafe_allow_html=True)

    left_space, center_col, right_space = st.columns([1.1, 2.4, 1.1])

    with center_col:
        fullname = st.text_input(
            "Full Name",
            key="register_name",
            placeholder="Enter your full name"
        )
        email = st.text_input(
            "Email",
            key="register_email",
            placeholder="Enter your email"
        )
        password = st.text_input(
            "Create Password",
            type="password",
            key="register_password",
            placeholder="Create password"
        )
        confirm = st.text_input(
            "Confirm Password",
            type="password",
            key="register_confirm_password",
            placeholder="Confirm password"
        )
        agree = st.checkbox("I agree to the Terms & Conditions", key="register_terms")
        register_click = st.button("Create Account", key="register_now", use_container_width=True)

        st.markdown("""
            <div class="auth-divider">Your account helps you save scans and manage protection smarter</div>
            <div class="auth-footer">
                Already have an account?
            </div>
        """, unsafe_allow_html=True)

        footer_left, footer_center, footer_right = st.columns([1.4, 1.2, 1.4])

        with footer_center:
            if st.button("Login here", key="login_here_btn", use_container_width=True):
                st.session_state.nav_page = "Login"
                st.rerun()

        if register_click:
            if not fullname.strip() or not email.strip() or not password.strip() or not confirm.strip():
                st.warning("Please fill all fields.")
            elif password != confirm:
                st.error("Passwords do not match.")
            elif not agree:
                st.warning("Please accept the terms and conditions.")
            else:
                st.success("Register UI created successfully. Connect backend registration next.")

    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.nav_page == "Scanner":
    left, right = st.columns([1.6, 1])

    with left:
        st.markdown("""
        <div class="info-pill">
            • AI POWERED • REAL-TIME SCANNING • SECURE LINKS
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="title">
            Is that link <span class="safe">safe</span> — or a
            <span class="trap">trap?</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="desc">
        <p class="hero-subtext">
           Analyze any suspicious URL instantly using advanced AI-powered detection, real-time scanning, and comprehensive threat analysis to identify phishing, malware, and deceptive websites before they can cause harm.
        """, unsafe_allow_html=True)
        url = st.text_input("", placeholder="Paste suspicious URL here...", key="url_input")
        check = st.button("Check Safety", key="check_btn")

        if check:
            if not url.strip():
                st.session_state.scan_result = "empty"
            else:
                prediction = predict_url(url)

                st.session_state.scan_result = {
                    "url": url,
                    "status": prediction["status"],
                    "high_risk": prediction["high_risk"],
                    "suspicious": prediction["suspicious"],
                    "safe_score": prediction["safe_score"]
                }

                save_scan(url, prediction["status"])

        if st.session_state.scan_result == "empty":
            st.markdown("""
            <div class="yellow-box">
                ⚠️ Please enter a URL first.
            </div>
            """, unsafe_allow_html=True)

        elif isinstance(st.session_state.scan_result, dict):
            result = st.session_state.scan_result

            if result["status"] == "Safe":
                icon = "✔"
                subtext = "This URL appears safe based on current checks"
            elif result["status"] == "Suspicious":
                icon = "⚠"
                subtext = "This URL looks suspicious and should be reviewed"
            else:
                icon = "🚨"
                subtext = "This URL appears highly risky or phishing-like"

            result_html = f"""
            <html>
            <head>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background: transparent;
                    font-family: Arial, sans-serif;
                }}

                .scan-result-card {{
                    margin-top: 10px;
                    width: 100%;
                    max-width: 650px;
                    background: #ffffff;
                    border: 1px solid #dbe7fb;
                    border-radius: 24px;
                    padding: 26px;
                    box-shadow: 0 20px 45px rgba(30, 67, 135, 0.10);
                    box-sizing: border-box;
                }}

                .scan-result-title {{
                    font-size: 18px;
                    font-weight: 700;
                    letter-spacing: 1px;
                    color: #8aa0bc;
                    margin-bottom: 24px;
                }}

                .score-row {{
                    display: grid;
                    grid-template-columns: 120px 1fr 50px;
                    align-items: center;
                    gap: 14px;
                    margin-bottom: 18px;
                }}

                .score-label {{
                    font-size: 18px;
                    color: #355277;
                    font-weight: 500;
                }}

                .score-bar {{
                    width: 100%;
                    height: 12px;
                    background: #edf3fb;
                    border-radius: 999px;
                    overflow: hidden;
                }}

                .score-fill {{
                    height: 100%;
                    border-radius: 999px;
                }}

                .red-fill {{ background: #e33434; }}
                .orange-fill {{ background: #e58a0a; }}
                .green-fill {{ background: #16a56b; }}

                .score-number {{
                    font-size: 24px;
                    font-weight: 800;
                    text-align: right;
                }}

                .red-text {{ color: #e33434; }}
                .orange-text {{ color: #e58a0a; }}
                .green-text {{ color: #16a56b; }}

                .safe-site-box {{
                    margin-top: 20px;
                    background: #eaf8f0;
                    border: 1px solid #bdebd2;
                    border-radius: 18px;
                    padding: 18px;
                    display: flex;
                    align-items: center;
                    gap: 14px;
                }}

                .safe-icon {{
                    width: 34px;
                    height: 34px;
                    border-radius: 50%;
                    background: #16a56b;
                    color: white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: 700;
                    flex-shrink: 0;
                }}

                .safe-domain {{
                    font-size: 18px;
                    font-weight: 700;
                    color: #173b74;
                    word-break: break-word;
                }}

                .safe-subtext {{
                    font-size: 15px;
                    color: #6b83a3;
                    margin-top: 4px;
                }}
            </style>
            </head>
            <body>
                <div class="scan-result-card">
                    <div class="scan-result-title">SCAN RESULT</div>

                    <div class="score-row">
                        <div class="score-label">High Risk</div>
                        <div class="score-bar">
                            <div class="score-fill red-fill" style="width:{result['high_risk']}%;"></div>
                        </div>
                        <div class="score-number red-text">{result['high_risk']}</div>
                    </div>

                    <div class="score-row">
                        <div class="score-label">Suspicious</div>
                        <div class="score-bar">
                            <div class="score-fill orange-fill" style="width:{result['suspicious']}%;"></div>
                        </div>
                        <div class="score-number orange-text">{result['suspicious']}</div>
                    </div>

                    <div class="score-row">
                        <div class="score-label">Safe</div>
                        <div class="score-bar">
                            <div class="score-fill green-fill" style="width:{result['safe_score']}%;"></div>
                        </div>
                        <div class="score-number green-text">{result['safe_score']}</div>
                    </div>

                    <div class="safe-site-box">
                        <div class="safe-icon">{icon}</div>
                        <div>
                            <div class="safe-domain">{result['url']}</div>
                            <div class="safe-subtext">{subtext}</div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """

            components.html(result_html, height=340, scrolling=False)

    with right:
        st.markdown("""
        <div class="hero-animation">
            <div class="pulse-ring ring1"></div>
            <div class="pulse-ring ring2"></div>
            <div class="pulse-ring ring3"></div>
            <div class="shield-core">🛡️</div>
        </div>
        """, unsafe_allow_html=True)

    # ----------------------------
    # CUSTOM CSS FOR STATS
    # ----------------------------
    st.markdown("""
    <style>
    .metric-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0;
        margin-top: 25px;
        margin-bottom: 25px;
        border-radius: 18px;
        overflow: hidden;
    }
    .metric-card {
        background: #16386b;
        color: white;
        text-align: center;
        padding: 30px 20px;
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    .metric-card:last-child {
        border-right: none;
    }
    .metric-number {
        font-size: 52px;
        font-weight: 800;
        margin-bottom: 8px;
    }
    .metric-title {
        font-size: 20px;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .metric-sub {
        font-size: 16px;
        color: #c9d8f2;
    }
    .blue-num { color: #7db8ff; }
    .red-num { color: #ff9c9c; }
    .yellow-num { color: #ffd84d; }
    .green-num { color: #78f0c6; }

    .url-list-box {
        background: #ffffff;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.06);
        margin-top: 18px;
        margin-bottom: 18px;
    }
    .url-list-title {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 12px;
        color: #16386b;
    }
    </style>
    """, unsafe_allow_html=True)

    # ----------------------------
    # STATS
    # ----------------------------
    stats = get_scan_stats()

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="metric-number blue-num">{stats['total_scans']}</div>
            <div class="metric-title">Total Scans</div>
            <div class="metric-sub">All-time analyses</div>
        </div>
        <div class="metric-card">
            <div class="metric-number red-num">{stats['high_risk_count']}</div>
            <div class="metric-title">High Risk</div>
            <div class="metric-sub">Detected phishing URLs</div>
        </div>
        <div class="metric-card">
            <div class="metric-number yellow-num">{stats['suspicious_count']}</div>
            <div class="metric-title">Suspicious</div>
            <div class="metric-sub">Flagged for review</div>
        </div>
        <div class="metric-card">
            <div class="metric-number green-num">{stats['today_scans']}</div>
            <div class="metric-title">Today</div>
            <div class="metric-sub">Scans performed today</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

     # ----------------------------
    # FULL HISTORY TABLE - CUSTOM UI
    # ----------------------------
    st.markdown("""
    <style>
    .scan-history-wrap{
        margin-top: 28px;
    }
    .scan-history-title{
        font-size: 34px;
        font-weight: 800;
        color: #163b77;
        margin-bottom: 18px;
    }
    .scan-history-card{
        background: #ffffff;
        border: 1px solid #dbe7fb;
        border-radius: 22px;
        overflow: hidden;
        box-shadow: 0 14px 35px rgba(30, 67, 135, 0.08);
    }
    .scan-history-head{
        display: grid;
        grid-template-columns: 2.6fr 1fr 1.2fr;
        background: linear-gradient(90deg, #163b77, #2455a6);
        color: white;
        font-weight: 700;
        font-size: 17px;
        padding: 16px 20px;
    }
    .scan-history-row{
        display: grid;
        grid-template-columns: 2.6fr 1fr 1.2fr;
        padding: 16px 20px;
        border-top: 1px solid #edf3fb;
        align-items: center;
        background: #ffffff;
    }
    .scan-history-row:nth-child(even){
        background: #f8fbff;
    }
    .scan-url{
        color: #163b77;
        font-size: 15px;
        font-weight: 600;
        word-break: break-word;
    }
    .scan-time{
        color: #6b83a3;
        font-size: 14px;
        font-weight: 500;
    }
    .status-pill{
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        font-size: 14px;
        font-weight: 700;
        text-align: center;
    }
    .status-safe{
        background: #eaf8f0;
        color: #159a63;
        border: 1px solid #bdebd2;
    }
    .status-suspicious{
        background: #fff6e7;
        color: #d88a00;
        border: 1px solid #ffd98a;
    }
    .status-highrisk{
        background: #fff0f0;
        color: #d63b3b;
        border: 1px solid #f3b5b5;
    }
    .empty-history{
        background: #ffffff;
        border: 1px dashed #c9d8f2;
        border-radius: 18px;
        padding: 30px;
        text-align: center;
        color: #6b83a3;
        font-size: 17px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='scan-history-wrap'>", unsafe_allow_html=True)
    st.markdown("<div class='scan-history-title'>Scan History</div>", unsafe_allow_html=True)

    if st.session_state.scan_history:
        st.markdown("""
        <div class="scan-history-card">
            <div class="scan-history-head">
                <div>URL</div>
                <div>Status</div>
                <div>Scanned On</div>
            </div>
        """, unsafe_allow_html=True)

        for item in reversed(st.session_state.scan_history):
            if item["status"] == "Safe":
                status_class = "status-pill status-safe"
            elif item["status"] == "Suspicious":
                status_class = "status-pill status-suspicious"
            else:
                status_class = "status-pill status-highrisk"

            formatted_time = item["time"].strftime("%d %b %Y, %I:%M %p")

            st.markdown(f"""
            <div class="scan-history-row">
                <div class="scan-url">{item['url']}</div>
                <div><span class="{status_class}">{item['status']}</span></div>
                <div class="scan-time">{formatted_time}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="empty-history">
            No scan history available yet. Start scanning URLs to see results here.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)