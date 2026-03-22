import streamlit as st
import pandas as pd
import math
import plotly.graph_objects as go
import plotly.express as px
import json, hashlib, os
from datetime import datetime

st.set_page_config(page_title="🥭 Mango Profit Navigator", page_icon="🥭",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700;800;900&family=Noto+Sans+Devanagari:wght@400;600;700&family=Noto+Sans+Telugu:wght@400;600;700&family=Noto+Sans+Tamil:wght@400;600;700&family=Noto+Sans+Gujarati:wght@400;600;700&family=Noto+Sans+Kannada:wght@400;600;700&display=swap');

html, body, [class*="css"] {
  font-family: 'Baloo 2', 'Noto Sans Devanagari', 'Noto Sans Telugu', 'Noto Sans Tamil', 'Noto Sans Gujarati', 'Noto Sans Kannada', sans-serif !important;
}

/* === GLOBAL BACKGROUND === */
.stApp {
  background: linear-gradient(160deg, #0a1f12 0%, #0d2e1a 40%, #0a1f12 100%) !important;
  background-attachment: fixed !important;
}
.main .block-container {
  background: transparent !important;
  padding-top: 12px !important;
}

/* === SIDEBAR === */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #061209 0%, #0d2e1a 50%, #061209 100%) !important;
  border-right: 1px solid rgba(82,183,136,0.2) !important;
}
[data-testid="stSidebar"] * { color: #c8f0d0 !important; }
[data-testid="stSidebar"] h3 { color: #52b788 !important; font-size: 1.1rem !important; }
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stNumberInput input {
  background: rgba(82,183,136,0.1) !important;
  color: #e8fdf0 !important;
  border: 1px solid rgba(82,183,136,0.35) !important;
  border-radius: 10px !important;
  font-family: inherit !important;
}
[data-testid="stSidebar"] label { color: #74c89b !important; font-weight: 600 !important; }

/* === ANIMATIONS === */
@keyframes fadeSlideDown {
  from { opacity: 0; transform: translateY(-24px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes cardPop {
  0%   { opacity: 0; transform: scale(0.85) translateY(16px); }
  70%  { transform: scale(1.03) translateY(-2px); }
  100% { opacity: 1; transform: scale(1) translateY(0); }
}
@keyframes gradientShift {
  0%,100% { background-position: 0% 50%; }
  50%      { background-position: 100% 50%; }
}
@keyframes floatMango {
  0%,100% { transform: translateY(0) rotate(-4deg); }
  50%      { transform: translateY(-14px) rotate(4deg); }
}
@keyframes pulse {
  0%,100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(82,183,136,0.4); }
  50%      { transform: scale(1.015); box-shadow: 0 0 0 10px rgba(82,183,136,0); }
}
@keyframes ticker {
  0%   { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
@keyframes rankPop {
  0%   { opacity: 0; transform: translateX(-30px) scale(0.8); }
  60%  { transform: translateX(4px) scale(1.04); }
  100% { opacity: 1; transform: translateX(0) scale(1); }
}
@keyframes shimmer {
  0%   { background-position: -200% center; }
  100% { background-position: 200% center; }
}
@keyframes glowPulse {
  0%,100% { box-shadow: 0 0 16px rgba(82,183,136,0.3); }
  50%      { box-shadow: 0 0 32px rgba(82,183,136,0.7), 0 0 60px rgba(82,183,136,0.2); }
}

/* === HERO === */
.hero-banner {
  background: linear-gradient(270deg, #061209, #0d3320, #1a5c38, #0d3320, #061209);
  background-size: 400% 400%;
  animation: gradientShift 8s ease infinite, fadeSlideDown 0.7s ease;
  border-radius: 24px;
  border: 1px solid rgba(82,183,136,0.25);
  padding: 38px 44px 30px;
  margin-bottom: 18px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 40px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.05);
}
.hero-banner::before {
  content: '';
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at 30% 50%, rgba(82,183,136,0.12) 0%, transparent 60%),
              radial-gradient(ellipse at 80% 20%, rgba(255,209,102,0.06) 0%, transparent 50%);
  pointer-events: none;
}
.hero-title {
  font-size: 2.5rem; font-weight: 900; margin: 0;
  background: linear-gradient(135deg, #ffffff 0%, #a7f3d0 50%, #ffd166 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: none;
  line-height: 1.2;
}
.hero-sub {
  font-size: 1.05rem; color: #74c89b; margin-top: 10px;
  font-weight: 500; letter-spacing: 0.2px;
}
.float-mango {
  animation: floatMango 3.5s ease-in-out infinite;
  display: inline-block; font-size: 36px;
}
.float-mango2 {
  animation: floatMango 4s ease-in-out infinite 0.8s;
  display: inline-block; font-size: 28px;
}

/* === TICKER === */
.ticker-wrap {
  background: linear-gradient(90deg, #04100a, #061c10, #04100a);
  border: 1px solid rgba(82,183,136,0.2);
  border-radius: 12px; padding: 11px 0;
  margin-bottom: 16px; overflow: hidden;
  position: relative;
  box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}
.ticker-label-fixed {
  position: absolute; left: 0; top: 0; height: 100%;
  background: linear-gradient(90deg, #04100a 65%, transparent);
  padding: 0 18px; display: flex; align-items: center;
  color: #52b788; font-size: 11px; font-weight: 800;
  text-transform: uppercase; letter-spacing: 2px; z-index: 2;
  white-space: nowrap;
}
.ticker-inner { display: flex; animation: ticker 30s linear infinite; }
.ticker-item {
  display: inline-flex; align-items: center; gap: 8px;
  margin-right: 40px; white-space: nowrap;
}
.ticker-place { color: #74c89b; font-size: 12px; font-weight: 600; }
.ticker-price { color: #ffd166; font-size: 14px; font-weight: 800; }
.ticker-up { color: #4ade80; font-weight: 700; }
.ticker-down { color: #f87171; font-weight: 700; }

/* === METRIC CARDS === */
.metric-card {
  background: linear-gradient(145deg, rgba(13,46,26,0.9), rgba(6,18,9,0.95));
  border: 1px solid rgba(82,183,136,0.25);
  border-radius: 18px; padding: 22px 18px;
  text-align: center;
  animation: cardPop 0.5s cubic-bezier(.34,1.56,.64,1) both;
  transition: transform 0.25s, box-shadow 0.25s;
  box-shadow: 0 4px 24px rgba(0,0,0,0.4);
  backdrop-filter: blur(10px);
}
.metric-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 36px rgba(0,0,0,0.5), 0 0 0 1px rgba(82,183,136,0.4);
}
.metric-card.best {
  background: linear-gradient(135deg, #0d4a26, #1a6b3c);
  border: 1px solid rgba(82,183,136,0.6);
  animation: cardPop 0.5s cubic-bezier(.34,1.56,.64,1) both, glowPulse 3s ease-in-out infinite;
}
.metric-card .lbl {
  font-size: 10px; font-weight: 800; text-transform: uppercase;
  letter-spacing: 1px; color: #52b788; margin-bottom: 8px;
}
.metric-card .val {
  font-size: 28px; font-weight: 900;
  background: linear-gradient(135deg, #a7f3d0, #ffd166);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.metric-card.best .val { font-size: 30px; }
.metric-card .sub { font-size: 11px; color: #5a9a72; margin-top: 5px; font-weight: 600; }

/* === TOP 3 PODIUM === */
.podium-wrap {
  display: flex; gap: 16px; margin-bottom: 24px;
  animation: fadeSlideUp 0.6s ease;
}
.podium-card {
  flex: 1; border-radius: 20px; padding: 22px 18px;
  position: relative; overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: default;
}
.podium-card:hover { transform: translateY(-6px) scale(1.01); }
.podium-card.gold {
  background: linear-gradient(145deg, #3a2200, #6b4000);
  border: 1px solid rgba(255,215,0,0.5);
  box-shadow: 0 8px 32px rgba(255,165,0,0.25), 0 0 0 1px rgba(255,215,0,0.2);
  animation: cardPop 0.5s cubic-bezier(.34,1.56,.64,1) 0.1s both;
}
.podium-card.silver {
  background: linear-gradient(145deg, #1a1a2e, #2a2a3e);
  border: 1px solid rgba(192,192,192,0.4);
  box-shadow: 0 6px 24px rgba(192,192,192,0.15);
  animation: cardPop 0.5s cubic-bezier(.34,1.56,.64,1) 0.2s both;
}
.podium-card.bronze {
  background: linear-gradient(145deg, #2d1a0a, #4a2c10);
  border: 1px solid rgba(205,127,50,0.4);
  box-shadow: 0 6px 24px rgba(205,127,50,0.15);
  animation: cardPop 0.5s cubic-bezier(.34,1.56,.64,1) 0.3s both;
}
.podium-medal { font-size: 42px; display: block; margin-bottom: 6px; }
.podium-rank { font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; opacity: 0.7; margin-bottom: 4px; }
.podium-name { font-size: 15px; font-weight: 800; color: white; margin-bottom: 6px; line-height: 1.3; }
.podium-profit { font-size: 26px; font-weight: 900; }
.gold .podium-profit { color: #ffd700; }
.silver .podium-profit { color: #c0c0c0; }
.bronze .podium-profit { color: #cd7f32; }
.podium-detail { font-size: 11px; opacity: 0.65; margin-top: 4px; color: #ccc; }
.podium-cat { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 10px; font-weight: 700; margin-top: 6px; }
.gold .podium-cat { background: rgba(255,215,0,0.2); color: #ffd700; border: 1px solid rgba(255,215,0,0.3); }
.silver .podium-cat { background: rgba(192,192,192,0.2); color: #c0c0c0; border: 1px solid rgba(192,192,192,0.3); }
.bronze .podium-cat { background: rgba(205,127,50,0.2); color: #cd7f32; border: 1px solid rgba(205,127,50,0.3); }

/* === RESULT TABLE === */
.result-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.result-table th {
  background: linear-gradient(90deg, #061209, #0d2e1a);
  color: #74c89b; font-weight: 800; font-size: 10px;
  text-transform: uppercase; letter-spacing: 1px;
  padding: 14px 14px; text-align: left;
  border-bottom: 1px solid rgba(82,183,136,0.2);
}
.result-table td {
  padding: 12px 14px; border-bottom: 1px solid rgba(82,183,136,0.08);
  color: #c8f0d0; vertical-align: middle;
}
.result-table tr:hover td { background: rgba(82,183,136,0.06); }
.result-table tr:last-child td { border-bottom: none; }
.rt-wrap {
  background: linear-gradient(145deg, rgba(6,18,9,0.95), rgba(13,46,26,0.9));
  border: 1px solid rgba(82,183,136,0.2);
  border-radius: 16px; overflow: hidden;
  box-shadow: 0 4px 24px rgba(0,0,0,0.4);
  animation: fadeSlideUp 0.5s ease;
}

/* === RANK BADGES === */
.rank-badge {
  width: 32px; height: 32px; border-radius: 50%;
  display: inline-flex; align-items: center; justify-content: center;
  font-weight: 900; font-size: 13px;
  animation: rankPop 0.4s cubic-bezier(.34,1.56,.64,1) both;
}
.r1 { background: linear-gradient(135deg, #FFD700, #FF8C00); color: #3a1800; box-shadow: 0 2px 12px rgba(255,165,0,0.5); }
.r2 { background: linear-gradient(135deg, #E8E8E8, #B0B0B0); color: #222; }
.r3 { background: linear-gradient(135deg, #CD7F32, #8B4513); color: #fff; }
.rn { background: rgba(82,183,136,0.2); color: #74c89b; border: 1px solid rgba(82,183,136,0.3); }

/* === PROFIT BAR === */
.profit-bar-wrap { display: flex; align-items: center; gap: 8px; }
.profit-bar-bg { height: 6px; background: rgba(82,183,136,0.15); border-radius: 3px; flex: 1; overflow: hidden; }
.profit-bar-fill { height: 6px; border-radius: 3px; background: linear-gradient(90deg, #52b788, #ffd166); transition: width 1s ease; }

/* === CATEGORY TAGS === */
.cat-tag { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 10px; font-weight: 800; white-space: nowrap; }
.Mandi { background: rgba(52,152,219,0.2); color: #74b9ff; border: 1px solid rgba(52,152,219,0.3); }
.Processing { background: rgba(155,89,182,0.2); color: #c8a0f0; border: 1px solid rgba(155,89,182,0.3); }
.Pulp { background: rgba(243,156,18,0.2); color: #ffd18a; border: 1px solid rgba(243,156,18,0.3); }
.Pickle { background: rgba(231,76,60,0.2); color: #ff8f85; border: 1px solid rgba(231,76,60,0.3); }
.LocalExport { background: rgba(82,183,136,0.2); color: #74c89b; border: 1px solid rgba(82,183,136,0.3); }
.AbroadExport { background: rgba(26,188,156,0.2); color: #7fffd4; border: 1px solid rgba(26,188,156,0.3); }

/* === ADVICE CARDS === */
.advice-card {
  background: linear-gradient(145deg, rgba(13,46,26,0.9), rgba(6,18,9,0.95));
  border: 1px solid rgba(82,183,136,0.25);
  border-radius: 16px; padding: 22px;
  margin-bottom: 14px;
  transition: transform 0.25s, box-shadow 0.25s;
  animation: cardPop 0.5s cubic-bezier(.34,1.56,.64,1) both;
}
.advice-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.5), 0 0 0 1px rgba(82,183,136,0.3);
}
.advice-icon { font-size: 32px; margin-bottom: 10px; display: block; }
.advice-title { font-weight: 800; color: #a7f3d0; font-size: 15px; margin-bottom: 6px; }
.advice-body { font-size: 13px; color: #74c89b; line-height: 1.7; }

/* === AUTH === */
.auth-card {
  background: linear-gradient(145deg, rgba(13,46,26,0.95), rgba(6,18,9,0.98));
  border: 1px solid rgba(82,183,136,0.3);
  border-radius: 24px; padding: 40px 44px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.7);
  animation: cardPop 0.6s cubic-bezier(.34,1.56,.64,1);
}
.auth-title {
  font-size: 1.9rem; font-weight: 900;
  background: linear-gradient(135deg, #a7f3d0, #ffd166);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; text-align: center; margin-bottom: 8px;
}

/* === NAMASTE BAR === */
.namaste-bar {
  background: linear-gradient(90deg, #061209, #0d3320, #061209);
  border: 1px solid rgba(82,183,136,0.3);
  color: #a7f3d0; border-radius: 14px; padding: 16px 24px;
  margin-bottom: 20px; font-size: 15px; font-weight: 700;
  display: flex; align-items: center; gap: 10px;
  animation: fadeSlideDown 0.5s ease;
  box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}

/* === TIP BOX === */
.tip-box {
  background: linear-gradient(135deg, rgba(255,209,102,0.1), rgba(243,156,18,0.08));
  border: 1px solid rgba(255,209,102,0.3);
  border-radius: 12px; padding: 13px 16px;
  font-size: 12.5px; color: #ffd166; line-height: 1.6;
  margin-top: 14px; animation: pulse 4s ease-in-out infinite;
}

/* === WELCOME FEATURES === */
.wc-feature {
  background: linear-gradient(145deg, rgba(13,46,26,0.85), rgba(6,18,9,0.9));
  border: 1px solid rgba(82,183,136,0.2);
  border-radius: 18px; padding: 24px 18px; text-align: center;
  transition: transform 0.25s, box-shadow 0.25s;
  animation: cardPop 0.5s cubic-bezier(.34,1.56,.64,1) both;
}
.wc-feature:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 32px rgba(0,0,0,0.5), 0 0 0 1px rgba(82,183,136,0.35);
}
.wc-feat-icon { font-size: 40px; margin-bottom: 12px; display: block; }

/* === SECTION DIVIDER === */
.section-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(82,183,136,0.4), transparent);
  border: none; margin: 24px 0;
}

/* === VOICE BUTTON === */
.voice-btn {
  display: inline-flex; align-items: center; gap: 8px;
  background: linear-gradient(135deg, #0d3320, #1a5c38);
  border: 1px solid rgba(82,183,136,0.4);
  border-radius: 50px; padding: 10px 20px;
  color: #a7f3d0; font-weight: 700; font-size: 13px;
  cursor: pointer; transition: all 0.2s;
  box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}
.voice-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(82,183,136,0.3); }

/* === BUTTONS === */
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #0d3320, #1a5c38) !important;
  border: 1px solid rgba(82,183,136,0.4) !important;
  border-radius: 12px !important; font-weight: 800 !important;
  font-size: 14px !important; color: #a7f3d0 !important;
  transition: all 0.2s !important;
  box-shadow: 0 4px 16px rgba(0,0,0,0.3) !important;
  font-family: inherit !important;
}
.stButton > button[kind="primary"]:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px rgba(82,183,136,0.3) !important;
  border-color: rgba(82,183,136,0.7) !important;
}
.stButton > button[kind="secondary"] {
  background: rgba(82,183,136,0.08) !important;
  border: 1px solid rgba(82,183,136,0.25) !important;
  border-radius: 12px !important; color: #74c89b !important;
  font-family: inherit !important;
}
.stTabs [data-baseweb="tab-list"] { background: rgba(6,18,9,0.8) !important; border-radius: 12px !important; gap: 4px !important; }
.stTabs [data-baseweb="tab"] { color: #74c89b !important; font-weight: 700 !important; border-radius: 10px !important; font-family: inherit !important; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, #0d3320, #1a5c38) !important; color: #a7f3d0 !important; }

/* Streamlit elements dark */
.stDownloadButton > button {
  background: linear-gradient(135deg, #1a5c38, #2d6a4f) !important;
  border: 1px solid rgba(82,183,136,0.4) !important;
  color: #a7f3d0 !important; border-radius: 12px !important;
  font-family: inherit !important;
}
div[data-testid="stMarkdownContainer"] p { color: #c8f0d0; }
.stSelectbox label, .stNumberInput label, .stTextInput label { color: #74c89b !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)

USERS_FILE = "users.json"
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE) as f: return json.load(f)
    return {}
def save_users(u):
    with open(USERS_FILE,"w") as f: json.dump(u,f,indent=2)
def hp(p): return hashlib.sha256(p.encode()).hexdigest()
def register_user(un,pw,fn,ph=""):
    u=load_users()
    if un in u: return False,"Username already exists!"
    u[un]={"password":hp(pw),"full_name":fn,"phone":ph,"created":str(datetime.now())}
    save_users(u); return True,"Registered! Please login."
def login_user(un,pw):
    u=load_users()
    if un not in u: return False,"Username not found!"
    if u[un]["password"]!=hp(pw): return False,"Incorrect password!"
    return True,u[un]["full_name"]

T={
"en":{
 "title":"🥭 Farmer's Mango Profit Navigator","subtitle":"Find the Best Market. Earn the Highest Return.",
 "ticker_label":"LIVE PRICES","lname":"👤 Farmer Name","lvillage":"🏘️ Village","lvar":"🥭 Mango Variety",
 "lqty":"📦 Quantity (Quintals)","run_btn":"🚀 Find Best Market",
 "tip":"💡 Sell with nearby farmers to cut transport costs and boost profit!",
 "wctitle":"Welcome, Mango Farmer!","wcsub":"Select your village, variety, quantity — then click Find Best Market.",
 "namaste":"Namaste","base_price":"Today's Market Price","best_profit":"Best Net Profit",
 "best_market":"Best Market","your_village":"Your Village",
 "tab1":"🥭 Top 3 Podium","tab2":"📊 All Options","tab3":"📈 Profit Charts","tab4":"🗺️ Map","tab5":"💡 Smart Advice",
 "rank":"Rank","market":"Market / Buyer","cat":"Type","dist":"Dist (km)",
 "rev":"Revenue (₹)","trans":"Transport (₹)","profit":"Net Profit (₹)",
 "chart_title":"Profit Comparison — Top 10","pie_title":"Profit Share by Category",
 "adv_title":"Smart Selling Advice for","prices_title":"📈 Nearby Market Prices",
 "today_price":"Today","yesterday_price":"Yesterday",
 "lang_full":"English",
 "voice_btn":"🔊 Listen to Top 3 Results","voice_reading":"Reading results aloud...",
 "login":"Login","register":"Register","logout":"Logout",
 "login_title":"👤 Login to Continue","reg_title":"📝 Create Account",
 "username":"Username","password":"Password","full_name":"Full Name","phone":"Phone (optional)",
 "login_btn":"Login →","reg_btn":"Register →",
 "have_account":"Already have account? Login","no_account":"New user? Create account",
 "mandal_ph":"Select Mandal","village_ph":"Select Village","name_ph":"Enter your name","qty_label":"quintals",
 "variety_advice":{
   "Banganapalli": [
     ("🌟","Premium Export Grade","Banganapalli is India's top export mango. Always approach export packhouses first — they pay 15-25% more than local mandis."),
     ("📦","Proper Grading is Key","Separate A/B/C grades before selling. Export buyers only take Grade A (>250g, blemish-free). Lower grades go to processing."),
     ("🌡️","Temperature Management","Harvest slightly early (mature but not ripe) for export. Keep in shade and deliver within 6 hours of harvest for best prices."),
     ("🤝","Negotiate in Groups","Form a Farmer Producer Group (FPG) — export buyers prefer bulk lots of 5+ tonnes. Together you get better rates."),
   ],
   "Totapuri": [
     ("🏭","Target Processing Units","Totapuri is a processing king — pulp factories, juice units, and pickles all want it. Processing pays 8-12% more than mandi."),
     ("⚡","Speed Matters","Totapuri oxidizes fast. Deliver to processing units within 12 hours of harvest for maximum price and no deductions."),
     ("🧪","Brix Level Selling","Ask buyers to check Brix (sugar level). Brix 14+ fetches ₹3-5/kg premium in pulp factories."),
     ("📅","Advance Contracts","Sign advance contracts with PLR Foods or Srini Food Park before harvest — guaranteed price protects you from market dips."),
   ],
   "Neelam": [
     ("🏪","Mandi is Your Best Friend","Neelam thrives in local mandis — consumers love the taste and aroma. Arrive before 8am for peak bidding prices."),
     ("🎁","Retail Packing Premium","Pack 6-12 fruits in gift boxes. Local urban buyers (Tirupati, Chennai) pay ₹80-120/kg retail vs ₹25-35/kg mandi."),
     ("🌿","Organic Premium","If you avoid chemicals, get organic certification — Neelam organic sells at 40-60% premium in city markets."),
     ("📱","Sell Direct Online","WhatsApp groups in Tirupati & Hyderabad buy farm-fresh Neelam directly. Eliminate middlemen entirely."),
   ],
   "Rasalu": [
     ("🥒","Pickle Factories Pay More","Rasalu is the #1 pickle mango. Rayachoti and Tirupati pickle factories pay a 10-15% premium over mandi rates."),
     ("🕐","Harvest at Right Stage","For pickles, harvest firm-mature (not ripe). Overly ripe Rasalu gets heavy price cuts from pickle buyers."),
     ("💰","Premium for Small Fruits","Pickle makers prefer smaller fruits (150-200g). Don't discard small fruits — they may fetch more than large ones!"),
     ("🔄","Dual Market Strategy","Send firm fruits to pickle units, ripe/soft fruits to mandi. Don't mix — keeps quality high for both buyers."),
   ],
 },
 "var_labels":{"Banganapalli":"Banganapalli\n⭐ Export","Totapuri":"Totapuri\n⭐ Processing","Neelam":"Neelam\n⭐ Mandi","Rasalu":"Rasalu\n⭐ Pickle"},
},
"te":{
 "title":"🥭 రైతు మామిడి లాభాల నావిగేటర్","subtitle":"అత్యుత్తమ మార్కెట్ కనుగొనండి. అధిక లాభం సంపాదించండి.",
 "ticker_label":"నేటి ధరలు","lname":"👤 రైతు పేరు","lvillage":"🏘️ మీ గ్రామం","lvar":"🥭 మామిడి రకం",
 "lqty":"📦 పరిమాణం (క్వింటాల్లు)","run_btn":"🚀 అత్యుత్తమ మార్కెట్ కనుగొనండి",
 "tip":"💡 పొరుగు రైతులతో కలిసి అమ్మండి — రవాణా ఖర్చు తక్కువ!",
 "wctitle":"స్వాగతం, మామిడి రైతు!","wcsub":"మీ గ్రామం, రకం, పరిమాణం ఎంచుకుని క్లిక్ చేయండి.",
 "namaste":"నమస్తే","base_price":"నేటి మార్కెట్ ధర","best_profit":"అత్యధిక నికర లాభం",
 "best_market":"అత్యుత్తమ మార్కెట్","your_village":"మీ గ్రామం",
 "tab1":"🥭 టాప్ 3 పోడియం","tab2":"📊 అన్ని ఎంపికలు","tab3":"📈 లాభాల పోలిక","tab4":"🗺️ మ్యాప్","tab5":"💡 తెలివైన సలహా",
 "rank":"వరుస","market":"మార్కెట్","cat":"రకం","dist":"దూరం (కి.మీ)",
 "rev":"ఆదాయం (₹)","trans":"రవాణా (₹)","profit":"నికర లాభం (₹)",
 "chart_title":"లాభాల పోలిక — టాప్ 10","pie_title":"వర్గం వారీ లాభం",
 "adv_title":"తెలివైన అమ్మకపు సలహా","prices_title":"📈 సమీప మార్కెట్ ధరలు",
 "today_price":"నేడు","yesterday_price":"నిన్న",
 "lang_full":"తెలుగు",
 "voice_btn":"🔊 ఫలితాలు వినండి","voice_reading":"ఫలితాలు చదువుతున్నాం...",
 "login":"లాగిన్","register":"రిజిస్టర్","logout":"లాగ్ అవుట్",
 "login_title":"👤 కొనసాగించడానికి లాగిన్","reg_title":"📝 ఖాతా సృష్టించండి",
 "username":"వినియోగదారు పేరు","password":"పాస్వర్డ్","full_name":"పూర్తి పేరు","phone":"ఫోన్ (ఐచ్ఛికం)",
 "login_btn":"లాగిన్ →","reg_btn":"రిజిస్టర్ →",
 "have_account":"ఖాతా ఉందా? లాగిన్","no_account":"కొత్తగా? ఖాతా సృష్టించండి",
 "mandal_ph":"మండల్ ఎంచుకోండి","village_ph":"గ్రామం ఎంచుకోండి","name_ph":"మీ పేరు","qty_label":"క్వింటాల్లు",
 "variety_advice":{
   "Banganapalli": [
     ("🌟","ప్రీమియం ఎగుమతి రకం","బంగినపల్లి భారతదేశంలో అత్యుత్తమ ఎగుమతి మామిడి. ఎగుమతి ప్యాక్‌హౌస్‌లు మొదటగా సంప్రదించండి — మండీ కంటే 15-25% ఎక్కువ ధర పొందుతారు."),
     ("📦","సరైన గ్రేడింగ్ అవసరం","A/B/C గ్రేడ్‌లు వేరు చేయండి. ఎగుమతి కొనుగోలుదారులు గ్రేడ్ A మాత్రమే తీసుకుంటారు."),
     ("🌡️","ఉష్ణోగ్రత నిర్వహణ","ఎగుమతి కోసం కొంచెం ముందు కోయండి. నీడలో ఉంచి 6 గంటల్లో డెలివరీ చేయండి."),
     ("🤝","గ్రూపులో అమ్మండి","రైతు ఉత్పత్తి సంఘం ఏర్పాటు చేయండి — 5+ టన్నుల లాట్‌కు మెరుగైన ధర పొందుతారు."),
   ],
   "Totapuri": [
     ("🏭","ప్రాసెసింగ్ యూనిట్లు లక్ష్యంగా చేసుకోండి","తోటపురి ప్రాసెసింగ్ రాజు — పల్ప్ కర్మాగారాలు, జ్యూస్ యూనిట్లు ఎక్కువ ధర ఇస్తాయి."),
     ("⚡","వేగం ముఖ్యం","తోటపురి వేగంగా పాడవుతుంది. కోసిన 12 గంటల్లో డెలివరీ చేయండి."),
     ("🧪","బ్రిక్స్ స్థాయి పరీక్ష","Brix 14+ అయితే పల్ప్ కర్మాగారాలు ₹3-5/kg అదనంగా ఇస్తాయి."),
     ("📅","ముందే ఒప్పందం చేసుకోండి","పంట ముందే PLR Foods లేదా Srini Food Park తో ఒప్పందం చేసుకోండి."),
   ],
   "Neelam": [
     ("🏪","మండీలో బెస్ట్ ధర","నీలం మండీలో చాలా మంది ఇష్టపడతారు. ఉదయం 8 గంటల ముందు చేరుకోండి."),
     ("🎁","రిటైల్ ప్యాకింగ్ ప్రీమియం","6-12 పండ్లు గిఫ్ట్ బాక్స్‌లో ప్యాక్ చేస్తే ₹80-120/kg వస్తుంది."),
     ("🌿","ఆర్గానిక్ ప్రీమియం","రసాయనాలు వాడకపోతే ఆర్గానిక్ సర్టిఫికేషన్ తీసుకోండి — 40-60% అధిక ధర."),
     ("📱","ఆన్‌లైన్‌లో నేరుగా అమ్మండి","WhatsApp గ్రూపుల ద్వారా తిరుపతి, హైదరాబాద్ కొనుగోలుదారులకు నేరుగా అమ్మండి."),
   ],
   "Rasalu": [
     ("🥒","ఊరగాయ కర్మాగారాలు ఎక్కువ ఇస్తాయి","రసాలు #1 ఊరగాయ మామిడి. మండీ కంటే 10-15% అధిక ధర పొందుతారు."),
     ("🕐","సరైన దశలో కోయండి","ఊరగాయ కోసం గట్టిగా ఉన్నప్పుడు కోయండి. పండిన రసాలుకు ధర తక్కువ."),
     ("💰","చిన్న పండ్లకు అధిక ధర","ఊరగాయ తయారీదారులు చిన్న పండ్లు (150-200g) ఇష్టపడతారు."),
     ("🔄","రెండు మార్కెట్ వ్యూహం","గట్టి పండ్లు ఊరగాయ యూనిట్లకు, పండిన పండ్లు మండీకి పంపండి."),
   ],
 },
 "var_labels":{"Banganapalli":"బంగినపల్లి\n⭐ ఎగుమతి","Totapuri":"తోటపురి\n⭐ ప్రాసెసింగ్","Neelam":"నీలం\n⭐ మండీ","Rasalu":"రసాలు\n⭐ ఊరగాయ"},
},
"hi":{
 "title":"🥭 किसान का आम लाभ नेविगेटर","subtitle":"सबसे अच्छा बाजार खोजें। सबसे ज्यादा मुनाफा कमाएं।",
 "ticker_label":"आज के भाव","lname":"👤 किसान का नाम","lvillage":"🏘️ आपका गांव","lvar":"🥭 आम की किस्म",
 "lqty":"📦 मात्रा (क्विंटल)","run_btn":"🚀 सबसे अच्छा बाजार खोजें",
 "tip":"💡 पड़ोसी किसानों के साथ मिलकर बेचें — परिवहन लागत कम होगी!",
 "wctitle":"स्वागत है, आम किसान!","wcsub":"अपना गांव, किस्म और मात्रा चुनें — फिर क्लिक करें।",
 "namaste":"नमस्ते","base_price":"आज का बाजार भाव","best_profit":"सर्वाधिक शुद्ध लाभ",
 "best_market":"सबसे अच्छा बाजार","your_village":"आपका गांव",
 "tab1":"🥭 टॉप 3 पोडियम","tab2":"📊 सभी विकल्प","tab3":"📈 लाभ तुलना","tab4":"🗺️ मानचित्र","tab5":"💡 स्मार्ट सलाह",
 "rank":"क्रम","market":"बाजार","cat":"प्रकार","dist":"दूरी (कि.मी.)",
 "rev":"आय (₹)","trans":"परिवहन (₹)","profit":"शुद्ध लाभ (₹)",
 "chart_title":"लाभ तुलना — टॉप 10","pie_title":"श्रेणी अनुसार लाभ",
 "adv_title":"स्मार्ट बिक्री सलाह","prices_title":"📈 पास के बाजार के भाव",
 "today_price":"आज","yesterday_price":"कल",
 "lang_full":"हिंदी",
 "voice_btn":"🔊 परिणाम सुनें","voice_reading":"परिणाम पढ़े जा रहे हैं...",
 "login":"लॉगिन","register":"रजिस्टर","logout":"लॉगआउट",
 "login_title":"👤 लॉगिन करें","reg_title":"📝 खाता बनाएं",
 "username":"यूज़रनेम","password":"पासवर्ड","full_name":"पूरा नाम","phone":"फोन (वैकल्पिक)",
 "login_btn":"लॉगिन →","reg_btn":"रजिस्टर →",
 "have_account":"खाता है? लॉगिन करें","no_account":"नए हैं? खाता बनाएं",
 "mandal_ph":"मंडल चुनें","village_ph":"गांव चुनें","name_ph":"अपना नाम","qty_label":"क्विंटल",
 "variety_advice":{
   "Banganapalli": [
     ("🌟","प्रीमियम एक्सपोर्ट किस्म","बंगनपल्ली भारत का सर्वश्रेष्ठ निर्यात आम है। एक्सपोर्ट पैकहाउस पहले संपर्क करें — मंडी से 15-25% अधिक मिलेगा।"),
     ("📦","ग्रेडिंग जरूरी है","A/B/C ग्रेड अलग करें। एक्सपोर्ट खरीदार केवल ग्रेड A लेते हैं।"),
     ("🌡️","तापमान प्रबंधन","थोड़ा पहले काटें और 6 घंटे में डिलीवरी करें।"),
     ("🤝","समूह में बेचें","किसान उत्पादक समूह बनाएं — 5+ टन लॉट पर बेहतर दाम मिलता है।"),
   ],
   "Totapuri": [
     ("🏭","प्रसंस्करण इकाइयां टारगेट करें","तोतापुरी प्रसंस्करण का राजा है — पल्प फैक्ट्रियां 8-12% अधिक देती हैं।"),
     ("⚡","जल्दी डिलीवरी करें","तोतापुरी जल्दी खराब होता है। 12 घंटे में डिलीवरी करें।"),
     ("🧪","Brix स्तर जांचें","Brix 14+ होने पर ₹3-5/kg अतिरिक्त मिलता है।"),
     ("📅","अग्रिम अनुबंध करें","फसल से पहले PLR Foods से अनुबंध करें।"),
   ],
   "Neelam": [
     ("🏪","मंडी में सर्वोत्तम भाव","नीलम मंडी में लोकप्रिय है। सुबह 8 बजे से पहले पहुंचें।"),
     ("🎁","रिटेल पैकिंग प्रीमियम","गिफ्ट बॉक्स में पैक करके ₹80-120/kg मिलता है।"),
     ("🌿","जैविक प्रीमियम","रसायन न डालें तो जैविक प्रमाण लें — 40-60% अधिक भाव।"),
     ("📱","ऑनलाइन सीधे बेचें","WhatsApp ग्रुप से सीधे शहरी खरीदारों को बेचें।"),
   ],
   "Rasalu": [
     ("🥒","अचार कारखाने अधिक देते हैं","रसालु #1 अचार आम है। मंडी से 10-15% अधिक मिलेगा।"),
     ("🕐","सही समय पर काटें","अचार के लिए कच्चा-पका काटें। पका आम सस्ता होता है।"),
     ("💰","छोटे फलों पर अधिक दाम","150-200g के छोटे फल अचार बनाने वालों को पसंद हैं।"),
     ("🔄","दोहरी बाजार रणनीति","कड़े फल अचार इकाइयों को, पके फल मंडी को भेजें।"),
   ],
 },
 "var_labels":{"Banganapalli":"बंगनपल्ली\n⭐ निर्यात","Totapuri":"तोतापुरी\n⭐ प्रसंस्करण","Neelam":"नीलम\n⭐ मंडी","Rasalu":"रसालु\n⭐ अचार"},
},
"ta":{
 "title":"🥭 விவசாயியின் மாம்பழ லாப வழிகாட்டி","subtitle":"சிறந்த சந்தையைக் கண்டறியுங்கள். அதிக வருமானம் ஈட்டுங்கள்.",
 "ticker_label":"இன்றைய விலைகள்","lname":"👤 விவசாயி பெயர்","lvillage":"🏘️ கிராமம்","lvar":"🥭 மாம்பழ வகை",
 "lqty":"📦 அளவு (குவிண்டால்)","run_btn":"🚀 சிறந்த சந்தையைக் கண்டறி",
 "tip":"💡 அண்டை விவசாயிகளுடன் சேர்ந்து விற்கவும்!",
 "wctitle":"வரவேற்கிறோம், மாம்பழ விவசாயி!","wcsub":"கிராமம், வகை, அளவை தேர்ந்தெடுத்து கிளிக் செய்யுங்கள்.",
 "namaste":"வணக்கம்","base_price":"இன்றைய விலை","best_profit":"அதிகபட்ச லாபம்",
 "best_market":"சிறந்த சந்தை","your_village":"கிராமம்",
 "tab1":"🥭 சிறந்த 3","tab2":"📊 அனைத்தும்","tab3":"📈 லாப ஒப்பீடு","tab4":"🗺️ வரைபடம்","tab5":"💡 ஆலோசனை",
 "rank":"வரிசை","market":"சந்தை","cat":"வகை","dist":"தூரம்",
 "rev":"வருவாய் (₹)","trans":"போக்குவரத்து (₹)","profit":"நிகர லாபம் (₹)",
 "chart_title":"லாப ஒப்பீடு","pie_title":"வகை வாரியான லாபம்",
 "adv_title":"விற்பனை ஆலோசனை","prices_title":"📈 சந்தை விலைகள்",
 "today_price":"இன்று","yesterday_price":"நேற்று",
 "lang_full":"தமிழ்",
 "voice_btn":"🔊 முடிவுகளை கேளுங்கள்","voice_reading":"முடிவுகள் படிக்கப்படுகின்றன...",
 "login":"உள்நுழைவு","register":"பதிவு","logout":"வெளியேறு",
 "login_title":"👤 உள்நுழைக","reg_title":"📝 கணக்கு உருவாக்கு",
 "username":"பயனர்பெயர்","password":"கடவுச்சொல்","full_name":"முழு பெயர்","phone":"தொலைபேசி (விருப்பம்)",
 "login_btn":"உள்நுழைவு →","reg_btn":"பதிவு →",
 "have_account":"கணக்கு உள்ளதா? உள்நுழைக","no_account":"புதியவரா? கணக்கு உருவாக்கு",
 "mandal_ph":"மண்டலம் தேர்ந்தெடு","village_ph":"கிராமம் தேர்ந்தெடு","name_ph":"உங்கள் பெயர்","qty_label":"குவிண்டால்",
 "variety_advice":{
   "Banganapalli": [
     ("🌟","ஏற்றுமதி தரம்","பங்கனபல்லி இந்தியாவின் சிறந்த ஏற்றுமதி மாம்பழம். ஏற்றுமதி நிலையங்களை முதலில் தொடர்பு கொள்ளுங்கள்."),
     ("📦","தரம் பிரிக்கவும்","A/B/C தரங்களை பிரிக்கவும். ஏற்றுமதி வாங்குபவர்கள் தரம் A மட்டுமே எடுப்பார்கள்."),
     ("🌡️","வெப்பநிலை மேலாண்மை","ஏற்றுமதிக்கு கொஞ்சம் முன்பே அறுவடை செய்யுங்கள். 6 மணி நேரத்தில் விநியோகிக்கவும்."),
     ("🤝","குழுவாக விற்கவும்","விவசாயி உற்பத்தி குழுவை உருவாக்கவும் — 5+ டன் தொகுதிக்கு சிறந்த விலை கிடைக்கும்."),
   ],
   "Totapuri": [
     ("🏭","பதப்படுத்தல் நிலையங்கள்","தொதாபுரி பதப்படுத்தல் ராஜா — பழச்சாறு தொழிற்சாலைகள் 8-12% அதிகமாக தருகின்றன."),
     ("⚡","விரைந்து விநியோகிக்கவும்","12 மணி நேரத்திற்குள் விநியோகிக்கவும்."),
     ("🧪","Brix அளவை சரிபார்க்கவும்","Brix 14+ இருந்தால் ₹3-5/kg கூடுதலாக கிடைக்கும்."),
     ("📅","முன்கூட்டிய ஒப்பந்தம்","அறுவடைக்கு முன் PLR Foods உடன் ஒப்பந்தம் செய்யுங்கள்."),
   ],
   "Neelam": [
     ("🏪","மண்டி சிறந்தது","நீலம் மண்டியில் மிகவும் பிரபலம். காலை 8 மணிக்கு முன் வந்தடையுங்கள்."),
     ("🎁","சில்லறை பேக்கிங்","பரிசு பெட்டிகளில் பேக்கிங் செய்தால் ₹80-120/kg கிடைக்கும்."),
     ("🌿","இயற்கை சான்றிதழ்","இயற்கை விவசாயம் செய்தால் 40-60% அதிக விலை கிடைக்கும்."),
     ("📱","நேரடியாக விற்கவும்","WhatsApp வழியாக நேரடியாக நகர வாங்குபவர்களுக்கு விற்கவும்."),
   ],
   "Rasalu": [
     ("🥒","ஊறுகாய் தொழிற்சாலைகள்","ரசாலு #1 ஊறுகாய் மாம்பழம். மண்டியை விட 10-15% அதிகம்."),
     ("🕐","சரியான நேரத்தில் அறுவடை","ஊறுகாய்க்கு உறுதியான நிலையில் அறுவடை செய்யுங்கள்."),
     ("💰","சிறிய பழங்களுக்கு அதிக விலை","150-200g பழங்கள் ஊறுகாய் தயாரிப்பாளர்களுக்கு விரும்பப்படுகின்றன."),
     ("🔄","இரட்டை சந்தை உத்தி","உறுதியான பழங்களை ஊறுகாய் நிலையங்களுக்கும், பழுத்தவற்றை மண்டிக்கும் அனுப்புங்கள்."),
   ],
 },
 "var_labels":{"Banganapalli":"பங்கனபல்லி\n⭐ ஏற்றுமதி","Totapuri":"தொதாபுரி\n⭐ பதப்படுத்தல்","Neelam":"நீலம்\n⭐ மண்டி","Rasalu":"ரசாலு\n⭐ ஊறுகாய்"},
},
"gu":{
 "title":"🥭 ખેડૂતનો કેરી નફો નેવિગેટર","subtitle":"શ્રેષ્ઠ બજાર શોધો. સૌથી વધુ નફો કમાઓ.",
 "ticker_label":"આજના ભાવ","lname":"👤 ખેડૂતનું નામ","lvillage":"🏘️ ગામ","lvar":"🥭 કેરીની જાત",
 "lqty":"📦 જથ્થો (ક્વિન્ટલ)","run_btn":"🚀 શ્રેષ્ઠ બજાર શોધો",
 "tip":"💡 પડોશી ખેડૂતો સાથે મળીને વેચો — પરિવહન ખર્ચ ઘટશે!",
 "wctitle":"સ્વાગત છે, કેરી ખેડૂત!","wcsub":"ગામ, જાત અને જથ્થો પસંદ કરો — પછી ક્લિક કરો.",
 "namaste":"નમસ્તે","base_price":"આજનો બજાર ભાવ","best_profit":"સૌથી વધુ ચોખ્ખો નફો",
 "best_market":"શ્રેષ્ઠ બજાર","your_village":"તમારું ગામ",
 "tab1":"🥭 ટોપ 3 પોડિયમ","tab2":"📊 બધા વિકલ્પ","tab3":"📈 નફો સરખામણી","tab4":"🗺️ નકશો","tab5":"💡 સ્માર્ટ સલાહ",
 "rank":"ક્રમ","market":"બજાર","cat":"પ્રકાર","dist":"અંતર (કિ.મી.)",
 "rev":"આવક (₹)","trans":"પરિવહન (₹)","profit":"ચોખ્ખો નફો (₹)",
 "chart_title":"નફો સરખામણી","pie_title":"શ્રેણી મુજબ નફો",
 "adv_title":"વેચાણ સલાહ","prices_title":"📈 નજીકના બજારના ભાવ",
 "today_price":"આજ","yesterday_price":"ગઈ કાલ",
 "lang_full":"ગુજરાતી",
 "voice_btn":"🔊 પરિણામ સાંભળો","voice_reading":"પરિણામ વાંચવામાં આવી રહ્યા છે...",
 "login":"લૉગઇન","register":"નોંધણી","logout":"લૉગ આઉટ",
 "login_title":"👤 લૉગઇન કરો","reg_title":"📝 ખાતું બનાવો",
 "username":"વપરાશકર્તા નામ","password":"પાસવર્ડ","full_name":"પૂરું નામ","phone":"ફોન (વૈકલ્પિક)",
 "login_btn":"લૉગઇન →","reg_btn":"નોંધણી →",
 "have_account":"ખાતું છે? લૉગઇન","no_account":"નવા છો? ખાતું બનાવો",
 "mandal_ph":"મંડળ પસંદ કરો","village_ph":"ગામ પસંદ કરો","name_ph":"તમારું નામ","qty_label":"ક્વિન્ટલ",
 "variety_advice":{
   "Banganapalli": [
     ("🌟","પ્રીમિયમ નિકાસ જાત","બંગનપલ્લી ભારતની સૌથી સારી નિકાસ કેરી છે. નિકાસ પૅકહાઉસ પ્રથમ સંપર્ક કરો."),
     ("📦","ગ્રેડિંગ જરૂરી","A/B/C ગ્રેડ અલગ કરો. નિકાસ ખરીદદારો ગ્રેડ A જ લે છે."),
     ("🌡️","તાપમાન વ્યવસ્થાપન","6 કલાકમાં ડિલિવરી કરો."),
     ("🤝","જૂથમાં વેચો","5+ ટન માટે ખેડૂત ઉત્પાદક જૂથ બનાવો."),
   ],
   "Totapuri": [
     ("🏭","પ્રૉસેસિંગ એકમોને ટાર્ગેટ કરો","તોતાપુરી પ્રૉસેસિંગ રાજા છે — 8-12% વધુ ભાવ મળે."),
     ("⚡","ઝડપી ડિલિવરી","12 કલાકમાં ડિલિવરી કરો."),
     ("🧪","Brix સ્તર","Brix 14+ હોય તો ₹3-5/kg વધુ."),
     ("📅","અગ્રિમ કરાર","PLR Foods સાથે પહેલેથી કરાર કરો."),
   ],
   "Neelam": [
     ("🏪","મંડીમાં શ્રેષ્ઠ ભાવ","સવારે 8 વાગ્યા પહેલા પહોંચો."),
     ("🎁","રિટેલ પૅકિંગ","ગિફ્ટ બૉક્સ ₹80-120/kg."),
     ("🌿","ઓર્ગેનિક પ્રીમિયમ","40-60% વધુ ભાવ."),
     ("📱","ઑનલાઇન સીધું વેચો","WhatsApp ગ્રૂપ દ્વારા."),
   ],
   "Rasalu": [
     ("🥒","અથાણું ફૅક્ટરી","10-15% વધુ ભાવ."),
     ("🕐","સાચા સ્તરે કાપો","અથાણા માટે સખત-પાકું."),
     ("💰","નાના ફળ","150-200g ફળ વધુ ભાવ."),
     ("🔄","બેવડી બજાર વ્યૂહ","સખત અથાણા, પાકેલ મંડી."),
   ],
 },
 "var_labels":{"Banganapalli":"બંગનપલ્લી\n⭐ નિકાસ","Totapuri":"તોતાપુરી\n⭐ પ્રૉસેસિંગ","Neelam":"નીલમ\n⭐ મંડી","Rasalu":"રસાળુ\n⭐ અથાણું"},
},
"kn":{
 "title":"🥭 ರೈತನ ಮಾವಿನ ಲಾಭ ನ್ಯಾವಿಗೇಟರ್","subtitle":"ಅತ್ಯುತ್ತಮ ಮಾರುಕಟ್ಟೆ ಹುಡುಕಿ. ಹೆಚ್ಚು ಲಾಭ ಗಳಿಸಿ.",
 "ticker_label":"ಇಂದಿನ ಬೆಲೆಗಳು","lname":"👤 ರೈತರ ಹೆಸರು","lvillage":"🏘️ ಹಳ್ಳಿ","lvar":"🥭 ಮಾವಿನ ತಳಿ",
 "lqty":"📦 ಪ್ರಮಾಣ (ಕ್ವಿಂಟಾಲ್)","run_btn":"🚀 ಅತ್ಯುತ್ತಮ ಮಾರುಕಟ್ಟೆ ಹುಡುಕಿ",
 "tip":"💡 ನೆರೆಯ ರೈತರೊಂದಿಗೆ ಒಟ್ಟಾಗಿ ಮಾರಾಟ ಮಾಡಿ!",
 "wctitle":"ಸ್ವಾಗತ, ಮಾವಿನ ರೈತ!","wcsub":"ಹಳ್ಳಿ, ತಳಿ, ಪ್ರಮಾಣ ಆರಿಸಿ — ನಂತರ ಕ್ಲಿಕ್ ಮಾಡಿ.",
 "namaste":"ನಮಸ್ಕಾರ","base_price":"ಇಂದಿನ ಮಾರುಕಟ್ಟೆ ಬೆಲೆ","best_profit":"ಅತ್ಯಧಿಕ ನಿವ್ವಳ ಲಾಭ",
 "best_market":"ಅತ್ಯುತ್ತಮ ಮಾರುಕಟ್ಟೆ","your_village":"ನಿಮ್ಮ ಹಳ್ಳಿ",
 "tab1":"🥭 ಟಾಪ್ 3 ಪೋಡಿಯಂ","tab2":"📊 ಎಲ್ಲಾ ಆಯ್ಕೆಗಳು","tab3":"📈 ಲಾಭ ಹೋಲಿಕೆ","tab4":"🗺️ ನಕ್ಷೆ","tab5":"💡 ಸ್ಮಾರ್ಟ್ ಸಲಹೆ",
 "rank":"ಶ್ರೇಣಿ","market":"ಮಾರುಕಟ್ಟೆ","cat":"ಪ್ರಕಾರ","dist":"ದೂರ (ಕಿ.ಮೀ.)",
 "rev":"ಆದಾಯ (₹)","trans":"ಸಾರಿಗೆ (₹)","profit":"ನಿವ್ವಳ ಲಾಭ (₹)",
 "chart_title":"ಲಾಭ ಹೋಲಿಕೆ","pie_title":"ವರ್ಗ ಪ್ರಕಾರ ಲಾಭ",
 "adv_title":"ಮಾರಾಟ ಸಲಹೆ","prices_title":"📈 ಹತ್ತಿರದ ಮಾರುಕಟ್ಟೆ ಬೆಲೆ",
 "today_price":"ಇಂದು","yesterday_price":"ನಿನ್ನೆ",
 "lang_full":"ಕನ್ನಡ",
 "voice_btn":"🔊 ಫಲಿತಾಂಶ ಕೇಳಿ","voice_reading":"ಫಲಿತಾಂಶಗಳನ್ನು ಓದಲಾಗುತ್ತಿದೆ...",
 "login":"ಲಾಗಿನ್","register":"ನೋಂದಣಿ","logout":"ಲಾಗ್ ಔಟ್",
 "login_title":"👤 ಲಾಗಿನ್ ಮಾಡಿ","reg_title":"📝 ಖಾತೆ ರಚಿಸಿ",
 "username":"ಬಳಕೆದಾರ ಹೆಸರು","password":"ಪಾಸ್ವರ್ಡ್","full_name":"ಪೂರ್ಣ ಹೆಸರು","phone":"ಫೋನ್ (ಐಚ್ಛಿಕ)",
 "login_btn":"ಲಾಗಿನ್ →","reg_btn":"ನೋಂದಣಿ →",
 "have_account":"ಖಾತೆ ಇದೆಯೇ? ಲಾಗಿನ್","no_account":"ಹೊಸಬರೇ? ಖಾತೆ ರಚಿಸಿ",
 "mandal_ph":"ಮಂಡಲ ಆಯ್ಕೆ","village_ph":"ಹಳ್ಳಿ ಆಯ್ಕೆ","name_ph":"ನಿಮ್ಮ ಹೆಸರು","qty_label":"ಕ್ವಿಂಟಾಲ್",
 "variety_advice":{
   "Banganapalli": [
     ("🌟","ರಫ್ತು ತಳಿ","ಬಂಗನಪಲ್ಲಿ ಭಾರತದ ಅತ್ಯುತ್ತಮ ರಫ್ತು ಮಾವು. ರಫ್ತು ಪ್ಯಾಕ್‌ಹೌಸ್ ಮೊದಲು ಸಂಪರ್ಕಿಸಿ."),
     ("📦","ದರ್ಜೆ ವಿಂಗಡಣೆ","A/B/C ದರ್ಜೆಗಳನ್ನು ಪ್ರತ್ಯೇಕಿಸಿ."),
     ("🌡️","ತಾಪಮಾನ ನಿರ್ವಹಣೆ","6 ಗಂಟೆಯಲ್ಲಿ ವಿತರಿಸಿ."),
     ("🤝","ಗುಂಪಾಗಿ ಮಾರಾಟ","5+ ಟನ್ ಲಾಟ್‌ಗೆ ಉತ್ತಮ ಬೆಲೆ."),
   ],
   "Totapuri": [
     ("🏭","ಸಂಸ್ಕರಣ ಘಟಕಗಳು","ತೋತಾಪುರಿ ಸಂಸ್ಕರಣದ ರಾಜ — 8-12% ಹೆಚ್ಚು."),
     ("⚡","ತ್ವರಿತ ವಿತರಣೆ","12 ಗಂಟೆಯಲ್ಲಿ ವಿತರಿಸಿ."),
     ("🧪","Brix ಮಟ್ಟ","Brix 14+ ಆದರೆ ₹3-5/kg ಹೆಚ್ಚು."),
     ("📅","ಮುಂಗಡ ಒಪ್ಪಂದ","PLR Foods ಜೊತೆ ಮುಂಚೆ ಒಪ್ಪಂದ ಮಾಡಿ."),
   ],
   "Neelam": [
     ("🏪","ಮಂಡಿ ಅತ್ಯುತ್ತಮ","ಬೆಳಿಗ್ಗೆ 8 ಗಂಟೆ ಮೊದಲು ತಲುಪಿ."),
     ("🎁","ರಿಟೇಲ್ ಪ್ಯಾಕಿಂಗ್","ಗಿಫ್ಟ್ ಬಾಕ್ಸ್‌ನಲ್ಲಿ ₹80-120/kg."),
     ("🌿","ಸಾವಯವ ಪ್ರೀಮಿಯಂ","40-60% ಹೆಚ್ಚು ಬೆಲೆ."),
     ("📱","ಆನ್‌ಲೈನ್ ಮಾರಾಟ","WhatsApp ಮೂಲಕ ನೇರ ಮಾರಾಟ."),
   ],
   "Rasalu": [
     ("🥒","ಉಪ್ಪಿನಕಾಯಿ ಕಾರ್ಖಾನೆ","ಮಂಡಿಗಿಂತ 10-15% ಹೆಚ್ಚು."),
     ("🕐","ಸರಿಯಾದ ಹಂತದಲ್ಲಿ ಕಟಾವು","ಉಪ್ಪಿನಕಾಯಿಗೆ ಗಟ್ಟಿ-ಹಣ್ಣು."),
     ("💰","ಚಿಕ್ಕ ಹಣ್ಣುಗಳಿಗೆ ಹೆಚ್ಚು","150-200g ಹಣ್ಣು ಹೆಚ್ಚು ಬೆಲೆ."),
     ("🔄","ದ್ವಿ ಮಾರುಕಟ್ಟೆ ತಂತ್ರ","ಗಟ್ಟಿ → ಉಪ್ಪಿನಕಾಯಿ, ಹಣ್ಣು → ಮಂಡಿ."),
   ],
 },
 "var_labels":{"Banganapalli":"ಬಂಗನಪಲ್ಲಿ\n⭐ ರಫ್ತು","Totapuri":"ತೋತಾಪುರಿ\n⭐ ಸಂಸ್ಕರಣ","Neelam":"ನೀಲಂ\n⭐ ಮಂಡಿ","Rasalu":"ರಸಾಲು\n⭐ ಉಪ್ಪಿನಕಾಯಿ"},
},
}

VTR={
"te":{"BALAYAPALLI":"బాలయపల్లి","ALIMILI":"అలిమిలి","BHYRAVARAM":"భైరవారం","CHILAMANURU":"చిలమనూరు",
 "GOTTIKADU":"గొట్టికాడు","HASTHAKAVERI":"హస్తకావేరి","JAYAMPU":"జయంపు","KADAGUNTA":"కాదగుంట",
 "KALAGANDA":"కళగండ","KAMAKURU":"కామకూరు","KATRAGUNTA":"కాట్రగుంట","KAYYURU":"కయ్యూరు",
 "KOTAMBEDU":"కొటంబేడు","MANNURU":"మన్నూరు","NIDIGALLU":"నిడిగళ్ళు","CHANDRAGIRI":"చంద్రగిరి",
 "AGARALA":"అగరాల","THONDAWADA":"తొండవాడ","MITTAPALEM":"మిట్టపాలెం","GADANKI":"గాడంకి",
 "PAKALA":"పాకల","DAMALCHERUVU":"దామలచెరువు","RENIGUNTA":"రేణిగుంట","KARAKAMBADI":"కారకంబాడి",
 "ATHURU":"ఆతూరు","AVILALA":"అవిలాల","TIRUCHANUR":"తిరుచానూరు","THUMMALAGUNTA":"తుమ్మలగుంట",
 "MANGALAM":"మంగళం","RANADHEERPURAM":"రానాధీర్పురం","SRIKALAHASTHI":"శ్రీకాళహస్తి",
 "AMMAPALEM":"అమ్మపాలెం","EMPEDU":"ఎంపేడు","YERPEDU":"యేర్పేడు","GUDIMALLAM":"గుడిమళ్ళం",
 "PAPANAIDUPET":"పాపనాయుడుపేట","NAIDUPET":"నాయుడుపేట","ANNAMEDU":"అన్నమేడు",
 "NAGALAPURAM":"నాగలాపురం","KRISHNAPURAM":"కృష్ణపురం","SULLURPET":"సుళ్ళూరుపేట",
 "ABAKA":"అబాక","TADA":"తాడ","MAMBATTU":"మంబట్టు","VAKADU":"వకాడు","KALLURU":"కళ్ళూరు",
 "VENKATAGIRI":"వెంకటగిరి","PUTTUR":"పుత్తూరు","NESANUR":"నేసనూరు","OZILI":"ఓజిలి",
 "GURRAMKONDA":"గుర్రంకొండ","DAKKILI":"దక్కిలి","AMUDURU":"అముదూరు","SATYAVEDU":"సత్యవేడు",
 "AROOR":"అరూర్","NARAYANAVANAM":"నారాయణవనం","BHEEMUNICHERUVU":"భీమునిచెరువు",
 "PELLAKUR":"పెళ్ళకూరు","ANAKAVOLU":"అనకవోలు","VARADAIAHPALEM":"వరదయ్యపాలెం",
 "AMBUR":"అంబూరు","THOTTAMBEDU":"తొట్టంబేడు","BONUPALLE":"బొన్నుపల్లె",
 "TIRUPATI (RURAL)":"తిరుపతి (గ్రామీణ)","TIRUPATI (URBAN)":"తిరుపతి (పట్టణ)"},
"hi":{"CHANDRAGIRI":"चंद्रगिरि","GADANKI":"गाडंकी","PAKALA":"पाकला","RENIGUNTA":"रेनिगुंटा",
 "TIRUPATI (RURAL)":"तिरुपति (ग्रामीण)","TIRUPATI (URBAN)":"तिरुपति (शहरी)","SRIKALAHASTHI":"श्रीकालहस्ती",
 "YERPEDU":"येरपेडु","NAIDUPET":"नायडुपेट","NAGALAPURAM":"नागलापुरम","SULLURPET":"सुल्लूरपेट",
 "TADA":"ताडा","VENKATAGIRI":"वेंकटगिरि","PUTTUR":"पुत्तूर","SATYAVEDU":"सत्यवेडु",
 "ALIMILI":"अलिमिलि","BHYRAVARAM":"भैरवारम","PAKALA":"पाकला"},
"ta":{"TIRUPATI (RURAL)":"திருப்பதி","CHANDRAGIRI":"சந்திரகிரி","PAKALA":"பாக்கல",
 "SRIKALAHASTHI":"ஸ்ரீகாளஹஸ்தி","RENIGUNTA":"ரேணிகுண்டா","SULLURPET":"சுல்லூர்பேட்",
 "VENKATAGIRI":"வெங்கடகிரி","PUTTUR":"புத்தூர்","SATYAVEDU":"சத்யவேடு"},
"gu":{"TIRUPATI (RURAL)":"તિરુપતિ","CHANDRAGIRI":"ચંદ્રગિરિ","PAKALA":"પાકાલ",
 "SRIKALAHASTHI":"શ્રીકાળહસ્તી","RENIGUNTA":"રેણિગુંટા","SULLURPET":"સુળ્ળૂરપેટ",
 "VENKATAGIRI":"વેંકટગિરિ","PUTTUR":"પુત્તૂર"},
"kn":{"TIRUPATI (RURAL)":"ತಿರುಪತಿ","CHANDRAGIRI":"ಚಂದ್ರಗಿರಿ","PAKALA":"ಪಾಕಲ",
 "SRIKALAHASTHI":"ಶ್ರೀಕಾಳಹಸ್ತಿ","RENIGUNTA":"ರೇಣಿಗುಂಟ","SULLURPET":"ಸುಳ್ಳೂರ್‌ಪೇಟ",
 "VENKATAGIRI":"ವೆಂಕಟಗಿರಿ","PUTTUR":"ಪುತ್ತೂರು"},
}

# Market name translations for all languages
MTR = {
"te": {
    "Tirupati APMC (RC Road)": "తిరుపతి APMC (RC రోడ్)",
    "Pakala Main Mango APMC": "పాకల మాంగో APMC",
    "Puttur Mango Market Yard": "పుత్తూరు మాంగో మార్కెట్",
    "Chandragiri APMC": "చంద్రగిరి APMC",
    "Srikalahasti APMC": "శ్రీకాళహస్తి APMC",
    "Venkatagiri APMC": "వెంకటగిరి APMC",
    "Naidupeta APMC": "నాయుడుపేట APMC",
    "Satyavedu APMC": "సత్యవేడు APMC",
    "Galla Foods Rayachoti": "గళ్ళ ఫుడ్స్ రాయచోటి",
    "Sri Varsha Food Products": "శ్రీ వర్ష ఫుడ్ ప్రొడక్ట్స్",
    "Hayath Foods": "హయాత్ ఫుడ్స్",
    "Tirupati Pickle Works": "తిరుపతి పికల్ వర్క్స్",
    "Padmavathi Pickles": "పద్మావతి పికల్స్",
    "Tirupati APMC Export": "తిరుపతి APMC ఎగుమతి",
    "Renigunta Packhouse": "రేణిగుంట ప్యాక్‌హౌస్",
    "Tirupati APMC Int Export": "తిరుపతి APMC అంతర్జాతీయ",
    "Renigunta Cold Room Export": "రేణిగుంట కోల్డ్ రూమ్",
},
"hi": {
    "Tirupati APMC (RC Road)": "तिरुपति APMC (RC रोड)",
    "Pakala Main Mango APMC": "पाकला मैन मैंगो APMC",
    "Puttur Mango Market Yard": "पुत्तूर मैंगो मार्केट",
    "Chandragiri APMC": "चंद्रगिरि APMC",
    "Tirupati Pickle Works": "तिरुपति अचार वर्क्स",
    "Tirupati APMC Export": "तिरुपति APMC निर्यात",
    "Renigunta Packhouse": "रेनिगुंटा पैकहाउस",
    "Tirupati APMC Int Export": "तिरुपति APMC अंतर्राष्ट्रीय",
},
"ta": {
    "Tirupati APMC (RC Road)": "திருப்பதி APMC",
    "Pakala Main Mango APMC": "பாக்கல் மாம்பழ APMC",
    "Tirupati Pickle Works": "திருப்பதி ஊறுகாய் தொழிற்சாலை",
    "Tirupati APMC Export": "திருப்பதி APMC ஏற்றுமதி",
},
"gu": {},
"kn": {},
}

CTR={
"te":{"Mandi":"మండీ","Processing":"ప్రాసెసింగ్","Pulp":"పల్ప్","Pickle":"ఊరగాయ",
     "Local Export":"స్థానిక ఎగుమతి","Abroad Export":"విదేశీ ఎగుమతి"},
"hi":{"Mandi":"मंडी","Processing":"प्रसंस्करण","Pulp":"पल्प","Pickle":"अचार",
     "Local Export":"स्थानीय निर्यात","Abroad Export":"विदेश निर्यात"},
"ta":{"Mandi":"மண்டி","Processing":"பதப்படுத்தல்","Pulp":"பழச்சாறு","Pickle":"ஊறுகாய்",
     "Local Export":"உள்நாட்டு ஏற்றுமதி","Abroad Export":"வெளிநாட்டு ஏற்றுமதி"},
"gu":{"Mandi":"મંડી","Processing":"પ્રૉસેસિંગ","Pulp":"પલ્પ","Pickle":"અથાણું",
     "Local Export":"સ્થાનિક નિકાસ","Abroad Export":"વિદેશ નિકાસ"},
"kn":{"Mandi":"ಮಂಡಿ","Processing":"ಸಂಸ್ಕರಣ","Pulp":"ಪಲ್ಪ್","Pickle":"ಉಪ್ಪಿನಕಾಯಿ",
     "Local Export":"ಸ್ಥಳೀಯ ರಫ್ತು","Abroad Export":"ವಿದೇಶ ರಫ್ತು"},
"en":{"Mandi":"Mandi","Processing":"Processing","Pulp":"Pulp","Pickle":"Pickle",
     "Local Export":"Local Export","Abroad Export":"Abroad Export"},
}

def tv(n, l):
    if l == "en": return n
    return VTR.get(l, {}).get(n.upper(), n)

def tc(c, l): return CTR.get(l, CTR["en"]).get(c, c)

def tm(name, l):
    if l == "en": return name
    return MTR.get(l, {}).get(name, name)

VILLAGES=[
{"Mandal":"BALAYAPALLI","GP":"ALIMILI","Lat":14.0152,"Lon":79.6124},
{"Mandal":"BALAYAPALLI","GP":"BALAYAPALLI","Lat":13.9856,"Lon":79.6452},
{"Mandal":"BALAYAPALLI","GP":"BHYRAVARAM","Lat":14.0221,"Lon":79.6845},
{"Mandal":"BALAYAPALLI","GP":"CHILAMANURU","Lat":14.0512,"Lon":79.6231},
{"Mandal":"BALAYAPALLI","GP":"GOTTIKADU","Lat":13.9621,"Lon":79.6712},
{"Mandal":"BALAYAPALLI","GP":"HASTHAKAVERI","Lat":13.9455,"Lon":79.6322},
{"Mandal":"BALAYAPALLI","GP":"JAYAMPU","Lat":13.9922,"Lon":79.7011},
{"Mandal":"BALAYAPALLI","GP":"KADAGUNTA","Lat":14.0312,"Lon":79.5912},
{"Mandal":"BALAYAPALLI","GP":"KALAGANDA","Lat":13.9112,"Lon":79.6241},
{"Mandal":"BALAYAPALLI","GP":"KAMAKURU","Lat":13.9521,"Lon":79.5844},
{"Mandal":"BALAYAPALLI","GP":"KATRAGUNTA","Lat":14.0012,"Lon":79.6543},
{"Mandal":"BALAYAPALLI","GP":"KAYYURU","Lat":13.8821,"Lon":79.6912},
{"Mandal":"BALAYAPALLI","GP":"KOTAMBEDU","Lat":13.9244,"Lon":79.7121},
{"Mandal":"BALAYAPALLI","GP":"MANNURU","Lat":13.9712,"Lon":79.7342},
{"Mandal":"BALAYAPALLI","GP":"NIDIGALLU","Lat":14.0421,"Lon":79.6921},
{"Mandal":"CHANDRAGIRI","GP":"CHANDRAGIRI","Lat":13.5834,"Lon":79.3214},
{"Mandal":"CHANDRAGIRI","GP":"AGARALA","Lat":13.6012,"Lon":79.3145},
{"Mandal":"CHANDRAGIRI","GP":"THONDAWADA","Lat":13.6122,"Lon":79.3712},
{"Mandal":"CHANDRAGIRI","GP":"MITTAPALEM","Lat":13.5822,"Lon":79.3611},
{"Mandal":"PAKALA","GP":"GADANKI","Lat":13.5321,"Lon":79.2112},
{"Mandal":"PAKALA","GP":"PAKALA","Lat":13.4512,"Lon":79.1121},
{"Mandal":"PAKALA","GP":"DAMALCHERUVU","Lat":13.5112,"Lon":79.1011},
{"Mandal":"RENIGUNTA","GP":"RENIGUNTA","Lat":13.6345,"Lon":79.5124},
{"Mandal":"RENIGUNTA","GP":"KARAKAMBADI","Lat":13.6645,"Lon":79.4712},
{"Mandal":"RENIGUNTA","GP":"ATHURU","Lat":13.6812,"Lon":79.5122},
{"Mandal":"TIRUPATI (RURAL)","GP":"AVILALA","Lat":13.6012,"Lon":79.4121},
{"Mandal":"TIRUPATI (RURAL)","GP":"TIRUCHANUR","Lat":13.6111,"Lon":79.4512},
{"Mandal":"TIRUPATI (RURAL)","GP":"THUMMALAGUNTA","Lat":13.6044,"Lon":79.4011},
{"Mandal":"TIRUPATI (URBAN)","GP":"MANGALAM","Lat":13.6545,"Lon":79.4512},
{"Mandal":"TIRUPATI (URBAN)","GP":"RANADHEERPURAM","Lat":13.6411,"Lon":79.4311},
{"Mandal":"SRIKALAHASTHI","GP":"SRIKALAHASTHI","Lat":13.7498,"Lon":79.7034},
{"Mandal":"SRIKALAHASTHI","GP":"AMMAPALEM","Lat":13.7411,"Lon":79.6212},
{"Mandal":"SRIKALAHASTHI","GP":"EMPEDU","Lat":13.8112,"Lon":79.7122},
{"Mandal":"YERPEDU","GP":"YERPEDU","Lat":13.6845,"Lon":79.5945},
{"Mandal":"YERPEDU","GP":"GUDIMALLAM","Lat":13.6421,"Lon":79.5511},
{"Mandal":"YERPEDU","GP":"PAPANAIDUPET","Lat":13.6645,"Lon":79.5823},
{"Mandal":"NAIDUPET","GP":"NAIDUPET","Lat":13.9142,"Lon":79.8944},
{"Mandal":"NAIDUPET","GP":"ANNAMEDU","Lat":13.8812,"Lon":79.9111},
{"Mandal":"NAGALAPURAM","GP":"NAGALAPURAM","Lat":13.4022,"Lon":79.9214},
{"Mandal":"NAGALAPURAM","GP":"KRISHNAPURAM","Lat":13.3812,"Lon":79.9411},
{"Mandal":"SULLURPET","GP":"SULLURPET","Lat":13.7008,"Lon":80.0211},
{"Mandal":"SULLURPET","GP":"ABAKA","Lat":13.7012,"Lon":80.0112},
{"Mandal":"TADA","GP":"TADA","Lat":13.5845,"Lon":80.0312},
{"Mandal":"TADA","GP":"MAMBATTU","Lat":13.5611,"Lon":80.0211},
{"Mandal":"VAKADU","GP":"VAKADU","Lat":14.0124,"Lon":80.1012},
{"Mandal":"VAKADU","GP":"KALLURU","Lat":14.0512,"Lon":80.0911},
{"Mandal":"VENKATAGIRI","GP":"VENKATAGIRI","Lat":13.9575,"Lon":79.5847},
{"Mandal":"VENKATAGIRI","GP":"AMMAPALEM","Lat":13.9812,"Lon":79.5412},
{"Mandal":"PUTTUR","GP":"PUTTUR","Lat":13.4419,"Lon":79.553},
{"Mandal":"PUTTUR","GP":"NESANUR","Lat":13.4722,"Lon":79.5911},
{"Mandal":"OZILI","GP":"OZILI","Lat":13.9845,"Lon":79.9124},
{"Mandal":"OZILI","GP":"GURRAMKONDA","Lat":13.9512,"Lon":79.8412},
{"Mandal":"DAKKILI","GP":"DAKKILI","Lat":14.1345,"Lon":79.6122},
{"Mandal":"DAKKILI","GP":"AMUDURU","Lat":14.1211,"Lon":79.6012},
{"Mandal":"SATYAVEDU","GP":"SATYAVEDU","Lat":13.5045,"Lon":79.9712},
{"Mandal":"SATYAVEDU","GP":"AROOR","Lat":13.5112,"Lon":79.9011},
{"Mandal":"NARAYANAVANAM","GP":"NARAYANAVANAM","Lat":13.4211,"Lon":79.5822},
{"Mandal":"NARAYANAVANAM","GP":"BHEEMUNICHERUVU","Lat":13.4111,"Lon":79.5512},
{"Mandal":"PELLAKUR","GP":"PELLAKUR","Lat":13.8345,"Lon":79.8544},
{"Mandal":"PELLAKUR","GP":"ANAKAVOLU","Lat":13.8412,"Lon":79.8512},
{"Mandal":"VARADAIAHPALEM","GP":"VARADAIAHPALEM","Lat":13.5945,"Lon":79.9221},
{"Mandal":"VARADAIAHPALEM","GP":"AMBUR","Lat":13.5612,"Lon":79.9112},
{"Mandal":"THOTTAMBEDU","GP":"THOTTAMBEDU","Lat":13.8445,"Lon":79.7543},
{"Mandal":"THOTTAMBEDU","GP":"BONUPALLE","Lat":13.8212,"Lon":79.7211},
]

PRICES=[
{"place":"Tirupati APMC (RC Road)","lat":13.6231,"lon":79.4125,"today":29,"yesterday":34},
{"place":"Pakala Main Mango APMC","lat":13.4568,"lon":79.1174,"today":27,"yesterday":32},
{"place":"Railway Kodur APMC Yard","lat":13.9515,"lon":79.3514,"today":28,"yesterday":33},
{"place":"Puttur Mango Market Yard","lat":13.4428,"lon":79.5531,"today":41,"yesterday":44},
{"place":"Chandragiri APMC","lat":13.5828,"lon":79.3142,"today":25,"yesterday":30},
{"place":"Srikalahasti APMC","lat":13.7498,"lon":79.7034,"today":30,"yesterday":35},
{"place":"Venkatagiri APMC","lat":13.9575,"lon":79.5847,"today":28,"yesterday":33},
{"place":"Nagalapuram APMC","lat":13.3985,"lon":79.7915,"today":27,"yesterday":32},
{"place":"Naidupeta APMC","lat":13.9142,"lon":79.8944,"today":29,"yesterday":34},
{"place":"Satyavedu APMC","lat":13.5076,"lon":79.9715,"today":26,"yesterday":31},
{"place":"Sullurpeta APMC","lat":13.7008,"lon":80.0211,"today":25,"yesterday":30},
{"place":"Bangarupalem","lat":13.2,"lon":78.9333,"today":34,"yesterday":42},
{"place":"Chittoor","lat":13.2172,"lon":79.1003,"today":36,"yesterday":39},
{"place":"Punganur","lat":13.3667,"lon":78.5667,"today":29,"yesterday":36},
{"place":"Pakala","lat":13.4667,"lon":79.1167,"today":37,"yesterday":41},
{"place":"Pileru","lat":13.65,"lon":78.95,"today":34,"yesterday":39},
{"place":"Madanapalle AMC","lat":13.6114,"lon":78.4716,"today":33,"yesterday":40},
{"place":"Gurramkonda e-NAM","lat":13.782,"lon":78.584,"today":39,"yesterday":45},
{"place":"Galiveedu Market Yard","lat":14.1035,"lon":78.5142,"today":36,"yesterday":43},
{"place":"Jamiya Mango Yard","lat":14.0562,"lon":78.751,"today":38,"yesterday":45},
{"place":"Nimmanapalle Yard","lat":13.5932,"lon":78.6011,"today":38,"yesterday":44},
{"place":"Burakayalakota Hub","lat":13.801,"lon":78.354,"today":39,"yesterday":41},
{"place":"Nandini Private Mandi","lat":13.5824,"lon":78.5025,"today":37,"yesterday":39},
{"place":"Chowdepalle Yard","lat":13.4116,"lon":78.6148,"today":36,"yesterday":45},
]
PROCESSING=[
{"name":"Galla Foods Rayachoti","lat":14.0585,"lon":78.749},{"name":"Roshan Fruits India","lat":13.6517,"lon":78.9415},
{"name":"Sri Varsha Food Products","lat":13.6275,"lon":79.4312},{"name":"Hayath Foods","lat":13.6212,"lon":79.468},
{"name":"Grofresh Agrofoods","lat":14.1825,"lon":79.171},{"name":"Srini Food Park","lat":13.185,"lon":78.961},
{"name":"Sree Sannidhi Foods","lat":14.2015,"lon":79.145},{"name":"Ohms Food Products","lat":14.061,"lon":78.7425},
{"name":"Navya Foods Pvt Ltd","lat":14.085,"lon":78.7315},{"name":"Bright Mangoes","lat":13.935,"lon":79.365},
{"name":"PLR Foods Pvt Ltd","lat":13.0639,"lon":78.8248},{"name":"Vijay Food Processing","lat":13.2092,"lon":79.1326},
]
PULP=[
{"name":"PLR Foods Pvt Ltd","lat":13.0639,"lon":78.8248},{"name":"Vijay Food Processing","lat":13.2092,"lon":79.1326},
{"name":"Galla Foods Ltd","lat":13.2092,"lon":79.1326},{"name":"Srini Food Park","lat":13.2106,"lon":79.1161},
{"name":"Sree Sannidhi Foods","lat":13.2148,"lon":79.0982},{"name":"Hayath Foods","lat":13.3091,"lon":79.0774},
{"name":"Navya Foods Pvt Ltd","lat":14.1952,"lon":79.1573},{"name":"Grofresh Agrofoods","lat":13.6541,"lon":78.9489},
{"name":"B M Fruits","lat":13.6425,"lon":79.5033},{"name":"Paiyur Group Mango Pulp","lat":14.042,"lon":78.761},
]
PICKLE=[
{"name":"Rayachoti Pickles","lat":14.0585,"lon":78.749},{"name":"Tirupati Pickle Works","lat":13.629,"lon":79.4285},
{"name":"Padmavathi Pickles","lat":13.6025,"lon":79.441},{"name":"Puttur Pickle Makers","lat":13.4415,"lon":79.553},
{"name":"Srikalahasti Pickle Industries","lat":13.755,"lon":79.7045},
{"name":"Pileru Pickle Works","lat":13.6515,"lon":78.941},
{"name":"Punganur Mango Pickle","lat":13.364,"lon":78.5825},{"name":"Kalikiri Pickle","lat":13.645,"lon":78.782},
{"name":"Chittoor Pack Pickle","lat":13.2215,"lon":79.112},{"name":"Madanapalle Pickle","lat":13.551,"lon":78.5215},
]
LOCAL_EXPORT=[
{"name":"Rayachoti APMC Export","lat":14.062,"lon":78.742},{"name":"Rajampet APMC","lat":14.1885,"lon":79.156},
{"name":"Tirupati APMC Export","lat":13.6285,"lon":79.4192},{"name":"Renigunta Packhouse","lat":13.6385,"lon":79.5068},
{"name":"Srikalahasti Cold Room","lat":13.751,"lon":79.702},{"name":"Puttur Export Yard","lat":13.445,"lon":79.548},
{"name":"Bangarupalem APMC","lat":13.212,"lon":78.968},{"name":"Chittoor APMC","lat":13.2115,"lon":79.112},
{"name":"Punganur Market Yard","lat":13.362,"lon":78.5805},{"name":"Pileru Packhouse","lat":13.6515,"lon":78.941},
]
ABROAD_EXPORT=[
{"name":"Tirupati APMC Int Export","lat":13.6288,"lon":79.4192},
{"name":"Renigunta Cold Room Export","lat":13.6519,"lon":79.5126},
{"name":"Rayachoti APMC Int","lat":14.0532,"lon":78.7516},
{"name":"Rajampet APMC Int","lat":14.195,"lon":79.1585},
{"name":"Srikalahasti Int Collection","lat":13.749,"lon":79.702},
{"name":"Chandragiri Packhouse","lat":13.566,"lon":79.317},
{"name":"Grofresh Export Pack","lat":13.215,"lon":79.055},
{"name":"Roshan Fruits Export","lat":14.06,"lon":78.755},
{"name":"Navya Foods Export","lat":13.21,"lon":78.745},
{"name":"Bright Mangoes Export","lat":13.205,"lon":78.76},
]

ROUTE_COLORS=["#FFD700","#C0C0C0","#CD7F32","#52b788","#3498db","#9b59b6","#f39c12","#e74c3c","#1abc9c","#e91e63"]

def hav(la1,lo1,la2,lo2):
    R=6371
    a=math.sin(math.radians((la2-la1)/2))**2+math.cos(math.radians(la1))*math.cos(math.radians(la2))*math.sin(math.radians((lo2-lo1)/2))**2
    return R*2*math.asin(math.sqrt(a))

def get_base_price(vla,vlo):
    best,price=float("inf"),29
    for p in PRICES:
        d=hav(vla,vlo,p["lat"],p["lon"])
        if d<best: best=d; price=p["today"]
    return price

def compute_top10(vla,vlo,bp,qty,var):
    accept={"Mandi":["Banganapalli","Totapuri","Neelam","Rasalu"],
            "Processing":["Totapuri","Neelam"],"Pulp":["Totapuri"],
            "Pickle":["Totapuri","Rasalu"],"Local Export":["Banganapalli"],
            "Abroad Export":["Banganapalli"]}
    margin={"Mandi":0,"Processing":0.03,"Pulp":0.04,"Pickle":0.025,"Local Export":0.05,"Abroad Export":0.07}
    datasets={"Mandi":[(p["place"],p["lat"],p["lon"]) for p in PRICES],
              "Processing":[(r["name"],r["lat"],r["lon"]) for r in PROCESSING],
              "Pulp":[(r["name"],r["lat"],r["lon"]) for r in PULP],
              "Pickle":[(r["name"],r["lat"],r["lon"]) for r in PICKLE],
              "Local Export":[(r["name"],r["lat"],r["lon"]) for r in LOCAL_EXPORT],
              "Abroad Export":[(r["name"],r["lat"],r["lon"]) for r in ABROAD_EXPORT]}
    res,seen=[],set()
    for cat,rows in datasets.items():
        if var not in accept[cat]: continue
        for nm,lat,lon in rows:
            k=f"{nm}|{cat}"
            if k in seen: continue
            seen.add(k)
            dist=hav(vla,vlo,lat,lon)
            rev=bp*(1+margin[cat])*100*qty
            tran=dist*12*qty
            res.append({"Category":cat,"Name":nm,"Distance_km":round(dist,1),
                        "Revenue":int(rev),"Transport":int(tran),"NetProfit":int(rev-tran),
                        "Lat":lat,"Lon":lon})
    res.sort(key=lambda x:-x["NetProfit"])
    return res[:10]

# SESSION STATE
for k,v in [("lang","en"),("logged_in",False),("username",""),("full_name",""),
             ("auth_mode","login"),("variety","Banganapalli"),("results",None)]:
    if k not in st.session_state: st.session_state[k]=v

lang=st.session_state.lang; tr=T[lang]

# ── LANGUAGE SELECTOR ──
def lang_bar():
    cols = st.columns([1,1,1,1,1,1,4,1] if st.session_state.logged_in else [1,1,1,1,1,1,5])
    lang_opts = [("en","🇬🇧 English"),("te","తె తెలుగు"),("hi","हि हिंदी"),("ta","த தமிழ்"),("gu","ગુ ગુજરાતી"),("kn","ಕ ಕನ್ನಡ")]
    for i,(col,(lc,lbl)) in enumerate(zip(cols[:6], lang_opts)):
        with col:
            if st.button(lbl, key=f"lang_{lc}", use_container_width=True,
                         type="primary" if st.session_state.lang==lc else "secondary"):
                st.session_state.lang=lc; st.rerun()
    if st.session_state.logged_in:
        with cols[7]:
            if st.button(f"🔴 {tr['logout']}", use_container_width=True):
                st.session_state.logged_in=False; st.session_state.results=None; st.rerun()

# ── AUTH SCREEN ──
if not st.session_state.logged_in:
    lang_bar()
    tr=T[st.session_state.lang]
    st.markdown(f"""<div class="hero-banner">
      <div style="margin-bottom:14px">
        <span class="float-mango">🥭</span>&nbsp;
        <span class="float-mango2">🌿</span>&nbsp;
        <span class="float-mango">🌾</span>&nbsp;
        <span class="float-mango2">💚</span>&nbsp;
        <span class="float-mango">🥭</span>
      </div>
      <h1 class="hero-title">{tr["title"]}</h1>
      <p class="hero-sub">{tr["subtitle"]}</p>
    </div>""", unsafe_allow_html=True)

    _,ca,_=st.columns([1,2,1])
    with ca:
        mode=st.session_state.auth_mode
        if mode=="login":
            st.markdown(f'<div class="auth-card"><div class="auth-title">{tr["login_title"]}</div>',unsafe_allow_html=True)
            with st.form("lf"):
                un=st.text_input(tr["username"],placeholder="Enter username")
                pw=st.text_input(tr["password"],type="password",placeholder="Enter password")
                if st.form_submit_button(tr["login_btn"],use_container_width=True,type="primary"):
                    if not un or not pw: st.error("Please fill all fields")
                    else:
                        ok,msg=login_user(un,pw)
                        if ok:
                            st.session_state.logged_in=True; st.session_state.username=un
                            st.session_state.full_name=msg; st.success(f"Welcome {msg}! 🥭"); st.rerun()
                        else: st.error(f"❌ {msg}")
            st.markdown("</div>",unsafe_allow_html=True)
            if st.button(f"📝 {tr['no_account']}",use_container_width=True):
                st.session_state.auth_mode="register"; st.rerun()
        else:
            st.markdown(f'<div class="auth-card"><div class="auth-title">{tr["reg_title"]}</div>',unsafe_allow_html=True)
            with st.form("rf"):
                fn=st.text_input(tr["full_name"],placeholder="Your full name")
                un=st.text_input(tr["username"],placeholder="Choose a username")
                ph=st.text_input(tr["phone"],placeholder="9XXXXXXXXX")
                pw=st.text_input(tr["password"],type="password",placeholder="Create password")
                pw2=st.text_input("Confirm Password",type="password",placeholder="Re-enter password")
                if st.form_submit_button(tr["reg_btn"],use_container_width=True,type="primary"):
                    if not fn or not un or not pw: st.error("Fill all required fields")
                    elif pw!=pw2: st.error("Passwords do not match!")
                    elif len(pw)<6: st.error("Password min 6 characters")
                    else:
                        ok,msg=register_user(un,pw,fn,ph)
                        if ok: st.success(f"✅ {msg}"); st.session_state.auth_mode="login"; st.rerun()
                        else: st.error(f"❌ {msg}")
            st.markdown("</div>",unsafe_allow_html=True)
            if st.button(f"👤 {tr['have_account']}",use_container_width=True):
                st.session_state.auth_mode="login"; st.rerun()
    st.stop()

# ── MAIN APP ──
lang=st.session_state.lang; tr=T[lang]
lang_bar()
tr=T[st.session_state.lang]; lang=st.session_state.lang

st.markdown(f"""<div class="hero-banner">
  <div style="margin-bottom:14px">
    <span class="float-mango">🥭</span>&nbsp;
    <span class="float-mango2">🌿</span>&nbsp;
    <span class="float-mango">🌾</span>&nbsp;
    <span class="float-mango2">💚</span>&nbsp;
    <span class="float-mango">🥭</span>
  </div>
  <h1 class="hero-title">{tr["title"]}</h1>
  <p class="hero-sub">{tr["subtitle"]}</p>
</div>""", unsafe_allow_html=True)

# TICKER
thtml=""
for p in PRICES:
    d=p["today"]-p["yesterday"]; ar="▲" if d>=0 else "▼"; cl="ticker-up" if d>=0 else "ticker-down"
    thtml+=f'<span class="ticker-item"><span class="ticker-place">{p["place"]}</span> <span class="ticker-price">₹{p["today"]}/kg</span> <span class="{cl}">{ar}{abs(d)}</span></span>'
dbl=thtml+thtml
st.markdown(f'''<div class="ticker-wrap"><div class="ticker-label-fixed">📈 {tr["ticker_label"]}</div><div style="padding-left:160px"><div class="ticker-inner">{dbl}</div></div></div>''',unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown(f"### 👋 {tr['namaste']}, **{st.session_state.full_name}**!")
    st.markdown("---")
    farmer_name=st.text_input(tr["lname"],value=st.session_state.full_name,placeholder=tr["name_ph"])
    mandals=sorted(set(v["Mandal"] for v in VILLAGES))
    mdmap={tv(m,lang):m for m in mandals}
    selmd=st.selectbox("📍 Mandal",["— "+tr["mandal_ph"]+" —"]+sorted(mdmap.keys()))
    village_val=None
    if selmd and not selmd.startswith("—"):
        men=mdmap[selmd]
        vills=[v["GP"] for v in VILLAGES if v["Mandal"]==men]
        vmap={tv(v,lang):v for v in vills}
        selvd=st.selectbox(tr["lvillage"],["— "+tr["village_ph"]+" —"]+sorted(vmap.keys()))
        if selvd and not selvd.startswith("—"): village_val=vmap[selvd]
    else:
        st.selectbox(tr["lvillage"],["— "+tr["village_ph"]+" —"],disabled=True)
    st.markdown(f"**{tr['lvar']}**")
    vc=st.columns(2)
    for i,v in enumerate(["Banganapalli","Totapuri","Neelam","Rasalu"]):
        lbl=tr["var_labels"][v]
        with vc[i%2]:
            if st.button(lbl,key=f"v_{v}",use_container_width=True,type="primary" if v==st.session_state.variety else "secondary"):
                st.session_state.variety=v; st.rerun()
    qty=st.number_input(tr["lqty"],min_value=1,max_value=500,value=10)
    st.markdown("<br>",unsafe_allow_html=True)
    run_clicked=st.button(tr["run_btn"],use_container_width=True,type="primary")
    st.markdown(f'<div class="tip-box">{tr["tip"]}</div>',unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"**{tr['prices_title']}**")
    show_prices=PRICES
    if village_val:
        vr=next((v for v in VILLAGES if v["GP"]==village_val),None)
        if vr: show_prices=sorted(PRICES,key=lambda p:hav(vr["Lat"],vr["Lon"],p["lat"],p["lon"]))[:8]
    for p in show_prices[:8]:
        d=p["today"]-p["yesterday"]; ic="🟢" if d>=0 else "🔴"; chg=f"+{d}" if d>=0 else str(d)
        pname = tm(p['place'], lang)
        st.markdown(f"{ic} **{pname[:22]}**  \n₹{p['today']}/kg ({chg})")

if run_clicked:
    if not village_val: st.error("⚠️ Please select your village first!")
    else:
        vr=next((v for v in VILLAGES if v["GP"]==village_val),None)
        if vr:
            bp=get_base_price(vr["Lat"],vr["Lon"])
            with st.spinner("🔄 Analyzing markets..."): top10=compute_top10(vr["Lat"],vr["Lon"],bp,qty,st.session_state.variety)
            if top10:
                st.session_state.results={"data":top10,"farmer_name":farmer_name or st.session_state.full_name,
                    "village":village_val,"base_price":bp,"qty":qty,
                    "v_lat":vr["Lat"],"v_lon":vr["Lon"],"variety":st.session_state.variety}
            else: st.warning("No results. Try Banganapalli or Totapuri.")

if st.session_state.results:
    R=st.session_state.results; top10=R["data"]; best=top10[0]; vd=tv(R["village"],lang)
    
    st.markdown(f'''<div class="namaste-bar">
      🥭 {tr["namaste"]}, <span style="color:#ffd166;margin:0 6px;font-size:17px">{R["farmer_name"]}</span>
      &nbsp;|&nbsp; 🏘️ {vd}
      &nbsp;|&nbsp; 🥭 {R["variety"]}
      &nbsp;|&nbsp; 📦 {R["qty"]} {tr["qty_label"]}
    </div>''',unsafe_allow_html=True)
    
    m1,m2,m3,m4=st.columns(4)
    for delay,col,content in [
        ("0.1s",m1,f'<div class="lbl">📈 {tr["base_price"]}</div><div class="val">₹{R["base_price"]}/kg</div><div class="sub">{vd}</div>'),
        ("0.2s",m2,f'<div class="lbl">📦 Quantity</div><div class="val">{R["qty"]} qtl</div><div class="sub">{R["qty"]*100} kg</div>'),
        ("0.3s",m3,f'<div class="lbl">🏆 {tr["best_profit"]}</div><div class="val">₹{best["NetProfit"]:,}</div><div class="sub">{tm(best["Name"],lang)[:26]}</div>'),
        ("0.4s",m4,f'<div class="lbl">🥭 {tr["best_market"]}</div><div class="val" style="font-size:16px;line-height:1.3">{tm(best["Name"],lang)[:24]}</div><div class="sub">{best["Distance_km"]} km · {tc(best["Category"],lang)}</div>'),
    ]:
        with col:
            cls = "best" if delay=="0.3s" else ""
            st.markdown(f'<div class="metric-card {cls}" style="animation-delay:{delay}">{content}</div>',unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>",unsafe_allow_html=True)

    # VOICE READ BUTTON
    top3_text = f"{tr['namaste']} {R['farmer_name']}. "
    for i, r in enumerate(top10[:3]):
        medal = ["First", "Second", "Third"][i]
        top3_text += f"{medal} option: {tm(r['Name'], lang)}, {tc(r['Category'], lang)}, {r['Distance_km']} km away, net profit rupees {r['NetProfit']:,}. "
    
    lang_voice_map = {"en":"en-IN","te":"te-IN","hi":"hi-IN","ta":"ta-IN","gu":"gu-IN","kn":"kn-IN"}
    voice_lang = lang_voice_map.get(lang, "en-IN")
    safe_text = top3_text.replace("`", "'").replace("\\", "")
    voice_js = f"""
    <script>
    function speakResults() {{
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            var text = `{safe_text}`;
            var utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = '{voice_lang}';
            utterance.rate = 0.9;
            utterance.pitch = 1.0;
            window.speechSynthesis.speak(utterance);
        }} else {{
            alert('Voice not supported in this browser');
        }}
    }}
    </script>
    <button class="voice-btn" onclick="speakResults()">
      {tr["voice_btn"]}
    </button>
    """
    st.markdown(voice_js, unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)

    tab1,tab2,tab3,tab4,tab5=st.tabs([tr["tab1"],tr["tab2"],tr["tab3"],tr["tab4"],tr["tab5"]])

    # ── TAB 1: TOP 3 PODIUM ──
    with tab1:
        st.markdown("<br>",unsafe_allow_html=True)
        medal_classes=["gold","silver","bronze"]
        medal_emojis=["🥇","🥈","🥉"]
        medal_labels=["#1 BEST","#2","#3"]
        
        cols_pod = st.columns(3)
        for i in range(min(3, len(top10))):
            r = top10[i]
            translated_name = tm(r["Name"], lang)
            cat_translated = tc(r["Category"], lang)
            with cols_pod[i]:
                st.markdown(f'''
                <div class="podium-card {medal_classes[i]}">
                  <span class="podium-medal">{medal_emojis[i]}</span>
                  <div class="podium-rank" style="color:{'#ffd700' if i==0 else '#c0c0c0' if i==1 else '#cd7f32'}">{medal_labels[i]}</div>
                  <div class="podium-name">{translated_name}</div>
                  <div class="podium-profit">₹{r["NetProfit"]:,}</div>
                  <div class="podium-detail">{tr["dist"]}: {r["Distance_km"]} km</div>
                  <div class="podium-detail">{tr["rev"]}: ₹{r["Revenue"]:,}</div>
                  <div class="podium-detail">{tr["trans"]}: ₹{r["Transport"]:,}</div>
                  <span class="podium-cat">{cat_translated}</span>
                </div>''', unsafe_allow_html=True)
        
        # Comparison bar chart for top 3
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown(f"#### 📊 Top 3 Breakdown")
        top3 = top10[:3]
        names3 = [tm(r["Name"],lang)[:22] for r in top3]
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            name=tr["profit"], x=names3, y=[r["NetProfit"] for r in top3],
            marker_color=["#FFD700","#C0C0C0","#CD7F32"],
            text=[f"₹{r['NetProfit']:,}" for r in top3], textposition="auto",
            textfont=dict(color="black", size=13, family="Baloo 2"),
        ))
        fig3.add_trace(go.Bar(
            name=tr["trans"], x=names3, y=[r["Transport"] for r in top3],
            marker_color=["rgba(255,150,50,0.6)","rgba(180,180,180,0.6)","rgba(160,100,50,0.6)"],
            text=[f"₹{r['Transport']:,}" for r in top3], textposition="auto",
        ))
        fig3.update_layout(
            barmode="group", height=320,
            plot_bgcolor="rgba(6,18,9,0.8)",
            paper_bgcolor="rgba(0,0,0,0)",
            yaxis_title="₹ Amount",
            font=dict(family="Baloo 2", color="#a7f3d0"),
            xaxis=dict(gridcolor="rgba(82,183,136,0.1)"),
            yaxis=dict(gridcolor="rgba(82,183,136,0.1)"),
            legend=dict(orientation="h", y=1.08, bgcolor="rgba(0,0,0,0)", font=dict(color="#a7f3d0")),
            margin=dict(l=10,r=10,t=40,b=10)
        )
        st.plotly_chart(fig3, use_container_width=True)

    # ── TAB 2: ALL OPTIONS TABLE ──
    with tab2:
        mp=best["NetProfit"]; rows_html=""
        for i,r in enumerate(top10):
            pct=int(r["NetProfit"]/mp*100) if mp>0 else 0
            medal="🥇" if i==0 else "🥈" if i==1 else "🥉" if i==2 else f"#{i+1}"
            rc="r1" if i==0 else "r2" if i==1 else "r3" if i==2 else "rn"
            ck=r["Category"].replace(" ","")
            ct=tc(r["Category"],lang)
            translated_name = tm(r["Name"],lang)
            bar=f'<div class="profit-bar-wrap"><div class="profit-bar-bg"><div class="profit-bar-fill" style="width:{pct}%"></div></div><span style="font-size:11px;color:#74c89b">{pct}%</span></div>'
            rows_html+=f'<tr><td><span class="rank-badge {rc}">{medal}</span></td><td><b style="color:#e8fdf0">{translated_name}</b></td><td><span class="cat-tag {ck}">{ct}</span></td><td style="color:#74c89b">{r["Distance_km"]} km</td><td style="color:#a7f3d0">₹{r["Revenue"]:,}</td><td style="color:#ffd166">₹{r["Transport"]:,}</td><td><b style="color:#52b788;font-size:15px">₹{r["NetProfit"]:,}</b></td><td>{bar}</td></tr>'
        st.markdown(f'''<div class="rt-wrap"><table class="result-table"><thead><tr><th>{tr["rank"]}</th><th>{tr["market"]}</th><th>{tr["cat"]}</th><th>{tr["dist"]}</th><th>{tr["rev"]}</th><th>{tr["trans"]}</th><th>{tr["profit"]}</th><th>% Best</th></tr></thead><tbody>{rows_html}</tbody></table></div>''',unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        
        # Better CSV with all columns and translated names
        csv_rows = []
        for i,r in enumerate(top10):
            csv_rows.append({
                "Rank": i+1,
                "Market Name (English)": r["Name"],
                "Market Name (Local)": tm(r["Name"],lang),
                "Category (English)": r["Category"],
                "Category (Local)": tc(r["Category"],lang),
                "Distance (km)": r["Distance_km"],
                "Base Price (₹/kg)": R["base_price"],
                "Quantity (Quintals)": R["qty"],
                "Quantity (kg)": R["qty"]*100,
                "Revenue (₹)": r["Revenue"],
                "Transport Cost (₹)": r["Transport"],
                "Net Profit (₹)": r["NetProfit"],
                "Farmer": R["farmer_name"],
                "Village": R["village"],
                "Variety": R["variety"],
                "Date": datetime.now().strftime("%Y-%m-%d"),
            })
        df=pd.DataFrame(csv_rows)
        st.download_button(
            "📥 Download Full Report (CSV)",
            df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig'),
            f"mango_profit_report_{R['village']}_{R['variety']}_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv",
            use_container_width=True
        )

    # ── TAB 3: CHARTS ──
    with tab3:
        ca,cb=st.columns(2)
        with ca:
            st.markdown(f"#### {tr['chart_title']}")
            names=[tm(r["Name"],lang)[:20]+"…" if len(tm(r["Name"],lang))>20 else tm(r["Name"],lang) for r in top10]
            fig=go.Figure()
            fig.add_trace(go.Bar(name=tr["profit"],y=names,x=[r["NetProfit"] for r in top10],orientation="h",
                marker=dict(color=ROUTE_COLORS[:len(top10)]),
                text=[f"₹{r['NetProfit']:,}" for r in top10],textposition="auto"))
            fig.add_trace(go.Bar(name=tr["trans"],y=names,x=[r["Transport"] for r in top10],orientation="h",
                marker_color="rgba(255,209,102,0.5)",
                text=[f"₹{r['Transport']:,}" for r in top10],textposition="auto"))
            fig.update_layout(
                barmode="group",height=440,
                plot_bgcolor="rgba(6,18,9,0.8)",paper_bgcolor="rgba(0,0,0,0)",
                xaxis_title="₹ Amount",
                font=dict(family="Baloo 2",color="#a7f3d0"),
                xaxis=dict(gridcolor="rgba(82,183,136,0.1)"),
                yaxis=dict(gridcolor="rgba(82,183,136,0.1)"),
                legend=dict(orientation="h",y=1.08,bgcolor="rgba(0,0,0,0)"),
                margin=dict(l=10,r=10,t=40,b=10)
            )
            st.plotly_chart(fig,use_container_width=True)
        with cb:
            st.markdown(f"#### {tr['pie_title']}")
            cs={}
            for r in top10: k=tc(r["Category"],lang); cs[k]=cs.get(k,0)+r["NetProfit"]
            fp=px.pie(names=list(cs.keys()),values=list(cs.values()),
                color_discrete_sequence=["#52b788","#ffd166","#e74c3c","#3498db","#9b59b6","#1abc9c"],hole=0.45)
            fp.update_traces(textposition="inside",textinfo="percent+label",
                marker=dict(line=dict(color="rgba(0,0,0,0.5)",width=2)))
            fp.update_layout(
                height=440,font=dict(family="Baloo 2",color="#a7f3d0"),
                paper_bgcolor="rgba(0,0,0,0)",showlegend=True,
                legend=dict(orientation="h",y=-0.15,bgcolor="rgba(0,0,0,0)"),
                margin=dict(l=10,r=10,t=10,b=10)
            )
            st.plotly_chart(fp,use_container_width=True)
        
        st.markdown("---")
        st.markdown(f"#### {tr['prices_title']}")
        np2=sorted(PRICES,key=lambda p:hav(R["v_lat"],R["v_lon"],p["lat"],p["lon"]))[:12]
        fp2=go.Figure()
        fp2.add_trace(go.Bar(name=tr["today_price"],x=[p["place"][:18] for p in np2],y=[p["today"] for p in np2],
            marker_color=["#52b788" if p["today"]>=p["yesterday"] else "#e74c3c" for p in np2],
            text=[f"₹{p['today']}" for p in np2],textposition="auto"))
        fp2.add_trace(go.Bar(name=tr["yesterday_price"],x=[p["place"][:18] for p in np2],y=[p["yesterday"] for p in np2],
            marker_color="rgba(120,120,120,0.5)",text=[f"₹{p['yesterday']}" for p in np2],textposition="auto"))
        fp2.update_layout(
            barmode="group",height=380,
            plot_bgcolor="rgba(6,18,9,0.8)",paper_bgcolor="rgba(0,0,0,0)",
            yaxis_title="₹ per kg",xaxis_tickangle=-45,
            font=dict(family="Baloo 2",color="#a7f3d0"),
            xaxis=dict(gridcolor="rgba(82,183,136,0.1)"),
            yaxis=dict(gridcolor="rgba(82,183,136,0.1)"),
            legend=dict(orientation="h",y=1.08,bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=10,r=10,t=40,b=80)
        )
        st.plotly_chart(fp2,use_container_width=True)

    # ── TAB 4: MAP ──
    with tab4:
        st.markdown("#### 🗺️ Market Map — Top 10 Options")
        fm=go.Figure()
        fm.add_trace(go.Scattermapbox(lat=[R["v_lat"]],lon=[R["v_lon"]],mode="markers+text",
            marker=dict(size=24,color="#ffd166",symbol="star"),text=[f"🏘️ {vd}"],textposition="top right",
            name=f"🏘️ {vd}",hovertemplate=f"<b>Your Village</b><br>{vd}<extra></extra>"))
        for i,r in enumerate(top10):
            col=ROUTE_COLORS[i%len(ROUTE_COLORS)]; medal="🥇" if i==0 else "🥈" if i==1 else "🥉" if i==2 else f"#{i+1}"
            translated_name = tm(r["Name"],lang)
            fm.add_trace(go.Scattermapbox(lat=[R["v_lat"],r["Lat"]],lon=[R["v_lon"],r["Lon"]],mode="lines",
                line=dict(width=3 if i==0 else 2,color=col),opacity=0.9 if i==0 else 0.6,showlegend=False,hoverinfo="skip"))
            fm.add_trace(go.Scattermapbox(lat=[r["Lat"]],lon=[r["Lon"]],mode="markers+text",
                marker=dict(size=18 if i<3 else 14,color=col),text=[medal],textposition="top center",
                name=f"{medal} {translated_name[:28]}",
                hovertemplate=f"<b>{medal} {translated_name}</b><br>Type: {tc(r['Category'],lang)}<br>Distance: {r['Distance_km']} km<br>Revenue: ₹{r['Revenue']:,}<br>Transport: ₹{r['Transport']:,}<br><b>Net Profit: ₹{r['NetProfit']:,}</b><extra></extra>"))
        fm.update_layout(
            mapbox=dict(style="carto-darkmatter",center=dict(lat=R["v_lat"],lon=R["v_lon"]),zoom=8),
            height=580,margin=dict(l=0,r=0,t=0,b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="v",x=0.01,y=0.99,bgcolor="rgba(6,18,9,0.9)",
                       bordercolor="rgba(82,183,136,0.3)",borderwidth=1,font=dict(size=11,color="#a7f3d0")),
            font=dict(family="Baloo 2"))
        st.plotly_chart(fm,use_container_width=True)

    # ── TAB 5: SMART ADVICE (VARIETY-SPECIFIC) ──
    with tab5:
        variety = R["variety"]
        adv_list = tr["variety_advice"].get(variety, [])
        vl = tr["var_labels"].get(variety, variety).split("\n")[0]
        st.markdown(f"#### {tr['adv_title']}: **{vl}**")
        st.markdown("<br>",unsafe_allow_html=True)
        ac1,ac2=st.columns(2)
        for i,(icon,title,body) in enumerate(adv_list):
            with [ac1,ac2][i%2]:
                st.markdown(f'''<div class="advice-card" style="animation-delay:{0.1+i*0.1}s">
                  <div class="advice-icon">{icon}</div>
                  <div class="advice-title">{title}</div>
                  <div class="advice-body">{body}</div>
                </div>''',unsafe_allow_html=True)
        st.markdown('''<div style="background:linear-gradient(135deg,rgba(13,46,26,0.9),rgba(6,18,9,0.95));border:1px solid rgba(82,183,136,0.25);border-radius:16px;padding:22px;text-align:center;margin-top:20px"><div style="font-size:36px;margin-bottom:10px">🌾 &nbsp; 🥭 &nbsp; 💚 &nbsp; 🌿 &nbsp; 🏡 &nbsp; 🚛 &nbsp; 💰</div><p style="color:#74c89b;font-size:14px;margin:0;font-weight:600">Empowering Indian Farmers with Market Intelligence 🇮🇳</p></div>''',unsafe_allow_html=True)

else:
    st.markdown(f'''<div style="text-align:center;padding:60px 20px">
      <div class="float-mango" style="font-size:80px">🥭</div>
      <h2 style="color:#a7f3d0;margin:20px 0 10px;font-size:2rem;font-weight:900">{tr["wctitle"]}</h2>
      <p style="color:#52b788;max-width:480px;margin:0 auto;line-height:1.8;font-size:15px">{tr["wcsub"]}</p>
    </div>''',unsafe_allow_html=True)
    w1,w2,w3=st.columns(3)
    for col,(icon,title,sub) in zip([w1,w2,w3],[
        ("📍","Pick Your Village","Find all nearby markets within 200km"),
        ("🥭","Choose Your Variety","Matched to the right buyers for your mango"),
        ("💰","See Top 3 Profits","Compare all options and pick the best deal")
    ]):
        with col:
            st.markdown(f'''<div class="wc-feature">
              <div class="wc-feat-icon">{icon}</div>
              <div style="font-weight:800;color:#a7f3d0;font-size:15px;margin-bottom:6px">{title}</div>
              <div style="font-size:13px;color:#52b788">{sub}</div>
            </div>''',unsafe_allow_html=True)

st.markdown('''<div style="text-align:center;color:#2d6a4f;font-size:12px;padding:20px 0;margin-top:24px;border-top:1px solid rgba(82,183,136,0.15)">
  🥭 Farmer\'s Mango Profit Navigator &nbsp;·&nbsp; Empowering farmers across Andhra Pradesh &nbsp;·&nbsp; 🇮🇳 Made in India
</div>''',unsafe_allow_html=True)
