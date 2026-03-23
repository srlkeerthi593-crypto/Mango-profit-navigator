import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import math
import plotly.graph_objects as go
import plotly.express as px
import json, hashlib, os, re
from datetime import datetime

st.set_page_config(page_title="🥭 Mango Profit Navigator", page_icon="🥭",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700;800;900&family=Noto+Sans+Devanagari:wght@400;500;600;700;800&family=Noto+Sans+Telugu:wght@400;500;600;700;800&family=Noto+Sans+Tamil:wght@400;500;600;700;800&family=Noto+Sans+Gujarati:wght@400;500;600;700;800&family=Noto+Sans+Kannada:wght@400;500;600;700;800&display=swap');

*, *::before, *::after,
html, body, div, span, p, h1, h2, h3, h4, h5, h6,
button, input, select, textarea, label, a,
[class*='css'], [data-testid], [data-baseweb],
.stApp, .stMarkdown, .stButton, .stTabs,
.stSelectbox, .stTextInput, .stNumberInput {
  font-family: 'Baloo 2','Noto Sans Telugu','Noto Sans Devanagari','Noto Sans Tamil','Noto Sans Gujarati','Noto Sans Kannada',system-ui,sans-serif !important;
}

/* ── MANGO VILLAGE BACKGROUND ── */
.stApp {
  background:
    radial-gradient(ellipse at 10% 20%, rgba(255,140,0,0.12) 0%, transparent 40%),
    radial-gradient(ellipse at 90% 80%, rgba(34,139,34,0.15) 0%, transparent 40%),
    radial-gradient(ellipse at 50% 50%, rgba(255,209,0,0.06) 0%, transparent 60%),
    radial-gradient(ellipse at 20% 80%, rgba(82,183,136,0.1) 0%, transparent 35%),
    radial-gradient(ellipse at 80% 10%, rgba(255,165,0,0.09) 0%, transparent 35%),
    linear-gradient(160deg, #030e05 0%, #061a09 25%, #041208 50%, #071e0c 75%, #030e05 100%) !important;
  background-attachment: fixed !important;
}

/* Animated mango pattern overlay */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  background-image:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Ctext x='10' y='40' font-size='24' opacity='0.04' fill='%23ffd700'%3E🥭%3C/text%3E%3Ctext x='80' y='100' font-size='18' opacity='0.03' fill='%2352b788'%3E🌿%3C/text%3E%3Ctext x='140' y='60' font-size='20' opacity='0.04' fill='%23ffa500'%3E🥭%3C/text%3E%3Ctext x='30' y='160' font-size='16' opacity='0.03' fill='%2352b788'%3E🌾%3C/text%3E%3Ctext x='110' y='180' font-size='22' opacity='0.04' fill='%23ffd700'%3E🥭%3C/text%3E%3Ctext x='170' y='140' font-size='14' opacity='0.03' fill='%2352b788'%3E🌿%3C/text%3E%3C/svg%3E");
  background-size: 200px 200px;
  animation: bgScroll 60s linear infinite;
}

@keyframes bgScroll { from { background-position: 0 0; } to { background-position: 200px 200px; } }

.main .block-container { background: transparent !important; padding-top: 10px !important; max-width: 1400px !important; position: relative; z-index: 1; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg,
    rgba(2,8,4,0.97) 0%,
    rgba(8,25,12,0.98) 30%,
    rgba(12,35,18,0.97) 60%,
    rgba(2,8,4,0.97) 100%) !important;
  border-right: 2px solid rgba(255,165,0,0.3) !important;
  box-shadow: 4px 0 30px rgba(0,0,0,0.6), inset -1px 0 0 rgba(82,183,136,0.1) !important;
}
[data-testid="stSidebar"]::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 40px,
    rgba(82,183,136,0.02) 40px,
    rgba(82,183,136,0.02) 41px
  );
  pointer-events: none;
}
[data-testid="stSidebar"] * { color: #b8e8c8 !important; }
[data-testid="stSidebar"] h3 { color: #ffd166 !important; font-size:1.05rem !important; letter-spacing:.4px !important; text-shadow: 0 0 20px rgba(255,209,102,0.4); }
[data-testid="stSidebar"] label { color: #74d4a0 !important; font-weight:700 !important; font-size:12px !important; text-transform:uppercase !important; letter-spacing:.8px !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,165,0,0.25) !important; }

[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stNumberInput input {
  background: #e8faf0 !important;
  color: #030a05 !important;
  -webkit-text-fill-color: #030a05 !important;
  border: 2px solid #ffa500 !important;
  border-radius: 10px !important;
  font-weight: 700 !important; font-size: 14px !important;
  caret-color: #030a05 !important;
}
[data-testid="stSidebar"] .stTextInput input:focus,
[data-testid="stSidebar"] .stNumberInput input:focus {
  background: #fffef0 !important; border-color: #ff8c00 !important;
  box-shadow: 0 0 0 3px rgba(255,165,0,0.25) !important;
}
[data-testid="stSidebar"] .stTextInput input::placeholder { color: #5a9a72 !important; -webkit-text-fill-color: #5a9a72 !important; }
[data-testid="stSidebar"] .stNumberInput button { background: #a7f3d0 !important; color: #030a05 !important; border-radius:6px !important; }
[data-testid="stSidebar"] .stSelectbox > div > div {
  background: #e8faf0 !important; color: #030a05 !important;
  -webkit-text-fill-color: #030a05 !important;
  border: 2px solid #ffa500 !important; border-radius:10px !important; font-weight:600 !important;
}
[data-testid="stSidebar"] .stSelectbox svg { fill: #030a05 !important; }

/* ── ANIMATIONS ── */
@keyframes fadeDown { from{opacity:0;transform:translateY(-20px)} to{opacity:1;transform:translateY(0)} }
@keyframes fadeUp   { from{opacity:0;transform:translateY(16px)}  to{opacity:1;transform:translateY(0)} }
@keyframes pop {
  0%{opacity:0;transform:scale(.82) translateY(14px)}
  65%{transform:scale(1.04) translateY(-2px)}
  100%{opacity:1;transform:scale(1) translateY(0)}
}
@keyframes gradShift { 0%,100%{background-position:0% 50%} 50%{background-position:100% 50%} }
@keyframes floatA { 0%,100%{transform:translateY(0) rotate(-5deg)} 50%{transform:translateY(-18px) rotate(5deg)} }
@keyframes floatB { 0%,100%{transform:translateY(0) rotate(3deg)} 50%{transform:translateY(-13px) rotate(-3deg)} }
@keyframes ticker { 0%{transform:translateX(0)} 100%{transform:translateX(-50%)} }
@keyframes shimmerText { 0%{background-position:-200% center} 100%{background-position:200% center} }
@keyframes glowGold { 0%,100%{box-shadow:0 0 14px rgba(255,165,0,.3),0 4px 20px rgba(0,0,0,.5)} 50%{box-shadow:0 0 35px rgba(255,165,0,.7),0 0 60px rgba(255,165,0,.2),0 4px 20px rgba(0,0,0,.5)} }
@keyframes glowGreen { 0%,100%{box-shadow:0 0 14px rgba(82,183,136,.25)} 50%{box-shadow:0 0 30px rgba(82,183,136,.6),0 0 50px rgba(82,183,136,.15)} }
@keyframes rankSlide { 0%{opacity:0;transform:translateX(-24px) scale(.8)} 60%{transform:translateX(3px) scale(1.04)} 100%{opacity:1;transform:none} }
@keyframes pulseTip { 0%,100%{transform:scale(1)} 50%{transform:scale(1.012)} }
@keyframes waveBar { 0%,100%{height:3px} 50%{height:14px} }
@keyframes speakGlow { 0%,100%{box-shadow:0 4px 20px rgba(255,165,0,.4)} 50%{box-shadow:0 4px 35px rgba(255,165,0,.8),0 0 0 10px rgba(255,165,0,0)} }
@keyframes mangoFloat { 0%{transform:translateY(0) rotate(-3deg)} 50%{transform:translateY(-10px) rotate(3deg)} 100%{transform:translateY(0) rotate(-3deg)} }
@keyframes rainbowBorder {
  0%{border-color:rgba(255,165,0,0.6)}
  25%{border-color:rgba(82,183,136,0.6)}
  50%{border-color:rgba(255,209,102,0.6)}
  75%{border-color:rgba(52,152,219,0.6)}
  100%{border-color:rgba(255,165,0,0.6)}
}

/* ── HERO BANNER ── */
.hero-banner {
  background: linear-gradient(270deg,#020d05,#0e2d10,#1a4a12,#0e2d10,#020d05);
  background-size:400% 400%; animation: gradShift 9s ease infinite, fadeDown .7s ease;
  border-radius:28px;
  border:2px solid rgba(255,165,0,0.4);
  padding:44px 52px 36px;
  margin-bottom:18px; position:relative; overflow:hidden;
  box-shadow:0 12px 60px rgba(0,0,0,.8),
             inset 0 1px 0 rgba(255,255,255,.05),
             0 0 0 1px rgba(255,165,0,0.1);
}
.hero-banner::before {
  content:''; position:absolute; inset:0; pointer-events:none;
  background:
    radial-gradient(ellipse at 15% 50%, rgba(255,165,0,.18) 0%, transparent 45%),
    radial-gradient(ellipse at 85% 20%, rgba(82,183,136,.14) 0%, transparent 45%),
    radial-gradient(ellipse at 50% 90%, rgba(255,209,102,.1) 0%, transparent 40%);
}
.hero-banner::after {
  content:''; position:absolute; inset:0; pointer-events:none; opacity:.3;
  background-image:
    radial-gradient(circle, rgba(255,165,0,.15) 1px, transparent 1px),
    radial-gradient(circle, rgba(82,183,136,.1) 1px, transparent 1px);
  background-size:30px 30px, 50px 50px;
  background-position: 0 0, 15px 15px;
}

/* Floating mango decorations inside hero */
.hero-deco {
  position:absolute; right:30px; top:50%; transform:translateY(-50%);
  display:flex; flex-direction:column; gap:8px; opacity:0.6; z-index:1;
}
.hero-deco span { font-size:28px; animation:mangoFloat 3s ease-in-out infinite; }
.hero-deco span:nth-child(2){ animation-delay:.7s; font-size:22px; }
.hero-deco span:nth-child(3){ animation-delay:1.4s; font-size:18px; }

.hero-title {
  font-size:2.7rem; font-weight:900; margin:0; line-height:1.2;
  background: linear-gradient(120deg,#fff5e0 0%,#ffd166 30%,#a7f3d0 60%,#52ff9a 80%,#ffd166 100%);
  background-size:200% auto;
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
  animation: shimmerText 4s linear infinite; position:relative; z-index:1;
  text-shadow: none;
}
.hero-sub {
  font-size:1.1rem; color:#ffd166; margin-top:12px; font-weight:700;
  position:relative; z-index:1;
  text-shadow: 0 2px 10px rgba(255,209,102,0.3);
}
.fm1 { display:inline-block; font-size:40px; animation:floatA 3.2s ease-in-out infinite; filter:drop-shadow(0 4px 12px rgba(255,165,0,.6)); position:relative; z-index:1; }
.fm2 { display:inline-block; font-size:32px; animation:floatB 4s ease-in-out infinite .6s; filter:drop-shadow(0 3px 8px rgba(82,183,136,.4)); position:relative; z-index:1; }

/* ── TICKER ── */
.ticker-wrap {
  background: linear-gradient(90deg, #030a04, #0a1f08, #030a04);
  border: 1px solid rgba(255,165,0,.35);
  border-radius:13px; padding:11px 0;
  margin-bottom:16px; overflow:hidden; position:relative;
  box-shadow: 0 4px 20px rgba(0,0,0,.5), inset 0 1px 0 rgba(255,165,0,0.1);
}
.ticker-label-fixed {
  position:absolute; left:0; top:0; height:100%;
  background:linear-gradient(90deg,#030a04 60%,transparent);
  padding:0 18px; display:flex; align-items:center;
  color:#ffd166; font-size:10px; font-weight:900; text-transform:uppercase; letter-spacing:2px; z-index:2; white-space:nowrap;
}
.ticker-inner { display:flex; animation:ticker 32s linear infinite; }
.ticker-item { display:inline-flex; align-items:center; gap:7px; margin-right:36px; white-space:nowrap; }
.ticker-place { color:#74c89b; font-size:12px; font-weight:600; }
.ticker-price { color:#ffd166; font-size:14px; font-weight:900; }
.ticker-up { color:#4ade80; font-weight:800; }
.ticker-down { color:#f87171; font-weight:800; }

/* ── METRIC CARDS ── */
.metric-card {
  background: linear-gradient(145deg,rgba(15,40,20,0.95),rgba(6,15,8,0.98));
  border:1px solid rgba(82,183,136,.3);
  border-radius:20px; padding:22px 18px;
  text-align:center; animation:pop .5s cubic-bezier(.34,1.56,.64,1) both;
  transition:transform .25s,box-shadow .25s;
  box-shadow:0 6px 28px rgba(0,0,0,.5);
}
.metric-card:hover { transform:translateY(-6px); box-shadow:0 16px 40px rgba(0,0,0,.6),0 0 0 1px rgba(255,165,0,.4); }
.metric-card.best {
  background: linear-gradient(135deg,#1a3d10,#2d5e18,#1a3d10);
  border:2px solid rgba(255,165,0,.7);
  animation:pop .5s cubic-bezier(.34,1.56,.64,1) both, glowGold 2.5s ease-in-out infinite;
}
.metric-card .lbl {
  font-size:10px; font-weight:900; text-transform:uppercase;
  letter-spacing:1.4px; color:#ffa500; margin-bottom:8px;
}
.metric-card .val {
  font-size:28px; font-weight:900;
  background:linear-gradient(135deg,#ffd166,#a7f3d0,#ffd166);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.metric-card.best .val { font-size:30px; }
.metric-card .sub { font-size:11px; color:#52b788; margin-top:6px; font-weight:600; }

/* ── PODIUM ── */
.podium-wrap { display:flex; gap:16px; margin-top:10px; }
.podium-card { flex:1; border-radius:22px; padding:26px 20px; position:relative; overflow:hidden; transition:transform .3s,box-shadow .3s; }
.podium-card:hover { transform:translateY(-8px) scale(1.01); }
.podium-card.gold  { background:linear-gradient(145deg,#3d2200,#6b3a00,#3d2200); border:2px solid rgba(255,215,0,.6); box-shadow:0 10px 40px rgba(255,165,0,.4),inset 0 1px 0 rgba(255,255,255,.1); animation:pop .5s cubic-bezier(.34,1.56,.64,1) .1s both; }
.podium-card.silver{ background:linear-gradient(145deg,#1a1a28,#2d2d45,#1a1a28); border:1px solid rgba(192,192,192,.5); box-shadow:0 8px 30px rgba(180,180,180,.2); animation:pop .5s cubic-bezier(.34,1.56,.64,1) .2s both; }
.podium-card.bronze{ background:linear-gradient(145deg,#321a08,#5a2e0a,#321a08); border:1px solid rgba(205,127,50,.5); box-shadow:0 8px 30px rgba(205,127,50,.25); animation:pop .5s cubic-bezier(.34,1.56,.64,1) .3s both; }
.podium-medal { font-size:48px; display:block; margin-bottom:10px; filter:drop-shadow(0 4px 8px rgba(0,0,0,.5)); }
.podium-rank { font-size:10px; font-weight:900; text-transform:uppercase; letter-spacing:3px; margin-bottom:8px; }
.podium-name { font-size:14px; font-weight:800; color:#fff; margin-bottom:10px; line-height:1.4; }
.podium-profit { font-size:30px; font-weight:900; }
.gold  .podium-profit, .gold  .podium-rank { color:#ffd700; }
.silver .podium-profit, .silver .podium-rank { color:#d0d0d0; }
.bronze .podium-profit, .bronze .podium-rank { color:#cd7f32; }
.podium-detail { font-size:11px; opacity:.65; margin-top:5px; color:#ddd; }
.podium-cat { display:inline-block; padding:4px 12px; border-radius:20px; font-size:10px; font-weight:800; margin-top:10px; }
.gold   .podium-cat { background:rgba(255,215,0,.2); color:#ffd700; border:1px solid rgba(255,215,0,.4); }
.silver .podium-cat { background:rgba(192,192,192,.2); color:#ccc; border:1px solid rgba(192,192,192,.4); }
.bronze .podium-cat { background:rgba(205,127,50,.2); color:#cd7f32; border:1px solid rgba(205,127,50,.4); }

/* ── RESULTS TABLE ── */
.rt-wrap {
  background:linear-gradient(145deg,rgba(4,12,7,.97),rgba(12,35,18,.94));
  border:1px solid rgba(255,165,0,.25); border-radius:18px; overflow:hidden;
  box-shadow:0 6px 30px rgba(0,0,0,.5); animation:fadeUp .5s ease;
}
.result-table { width:100%; border-collapse:collapse; font-size:13px; }
.result-table th {
  background:linear-gradient(90deg,#020d05,#0d2a10);
  color:#ffa500; font-weight:900; font-size:10px; text-transform:uppercase;
  letter-spacing:1.2px; padding:15px; text-align:left;
  border-bottom:1px solid rgba(255,165,0,.25);
}
.result-table td { padding:13px 15px; border-bottom:1px solid rgba(82,183,136,.08); color:#b8e8c8; vertical-align:middle; }
.result-table tr:hover td { background:rgba(255,165,0,.05); }
.result-table tr:last-child td { border-bottom:none; }
.rank-badge { width:34px; height:34px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-weight:900; font-size:13px; animation:rankSlide .4s cubic-bezier(.34,1.56,.64,1) both; }
.r1 { background:linear-gradient(135deg,#FFD700,#FF8C00); color:#2a1200; box-shadow:0 3px 14px rgba(255,165,0,.6); }
.r2 { background:linear-gradient(135deg,#E8E8E8,#A8A8A8); color:#111; }
.r3 { background:linear-gradient(135deg,#CD7F32,#8B4513); color:#fff; }
.rn { background:rgba(82,183,136,.2); color:#74c89b; border:1px solid rgba(82,183,136,.4); }
.profit-bar-wrap { display:flex; align-items:center; gap:8px; }
.profit-bar-bg { height:7px; background:rgba(82,183,136,.12); border-radius:4px; flex:1; overflow:hidden; }
.profit-bar-fill { height:7px; border-radius:4px; background:linear-gradient(90deg,#ff8c00,#ffd166,#52b788); }

/* ── CATEGORY TAGS ── */
.cat-tag { display:inline-block; padding:4px 11px; border-radius:20px; font-size:10px; font-weight:900; white-space:nowrap; }
.Mandi        { background:rgba(52,152,219,.2); color:#82c4ff; border:1px solid rgba(52,152,219,.4); }
.Processing   { background:rgba(155,89,182,.2); color:#c8a0f0; border:1px solid rgba(155,89,182,.4); }
.Pulp         { background:rgba(243,156,18,.2); color:#ffd18a; border:1px solid rgba(243,156,18,.4); }
.Pickle       { background:rgba(231,76,60,.2);  color:#ff9f9a; border:1px solid rgba(231,76,60,.4); }
.LocalExport  { background:rgba(82,183,136,.2); color:#74c89b; border:1px solid rgba(82,183,136,.4); }
.AbroadExport { background:rgba(26,188,156,.2); color:#7fffd4; border:1px solid rgba(26,188,156,.4); }

/* ── ADVICE CARDS ── */
.advice-card {
  background:linear-gradient(145deg,rgba(15,40,20,.94),rgba(6,15,8,.98));
  border:1px solid rgba(255,165,0,.28); border-radius:18px; padding:24px;
  margin-bottom:16px; transition:transform .25s,box-shadow .25s;
  animation:pop .5s cubic-bezier(.34,1.56,.64,1) both;
  box-shadow: 0 4px 20px rgba(0,0,0,.4);
}
.advice-card:hover { transform:translateY(-5px); box-shadow:0 12px 32px rgba(0,0,0,.55),0 0 0 1px rgba(255,165,0,.4); }
.advice-icon { font-size:34px; margin-bottom:12px; display:block; }
.advice-title { font-weight:800; color:#ffd166; font-size:15px; margin-bottom:8px; }
.advice-body { font-size:13px; color:#74c89b; line-height:1.75; }

/* ── AUTH CARD ── */
.auth-card {
  background:linear-gradient(145deg,rgba(10,34,18,.98),rgba(4,12,7,.99));
  border:2px solid rgba(255,165,0,.4); border-radius:26px; padding:42px 46px;
  box-shadow:0 20px 70px rgba(0,0,0,.8),0 0 0 1px rgba(255,165,0,.1);
  animation:pop .6s cubic-bezier(.34,1.56,.64,1);
}
.auth-title {
  font-size:1.9rem; font-weight:900;
  background:linear-gradient(135deg,#ffd166,#a7f3d0,#ffd166);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
  text-align:center; margin-bottom:10px;
  background-size: 200% auto; animation: shimmerText 4s linear infinite;
}

/* ── NAMASTE BAR ── */
.namaste-bar {
  background:linear-gradient(90deg,#030a04,#0e2812,#030a04);
  border:1px solid rgba(255,165,0,.4); color:#ffd166;
  border-radius:16px; padding:16px 24px; margin-bottom:22px;
  font-size:14px; font-weight:700; display:flex; align-items:center;
  gap:12px; flex-wrap:wrap; animation:fadeDown .5s ease;
  box-shadow:0 4px 22px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,165,0,.1);
}

/* ── TIP BOX ── */
.tip-box {
  background:linear-gradient(135deg,rgba(255,165,0,.15),rgba(255,209,102,.08));
  border:1px solid rgba(255,165,0,.4); border-radius:13px;
  padding:13px 16px; font-size:12px; color:#ffd166; line-height:1.65;
  margin-top:14px; animation:pulseTip 4s ease-in-out infinite;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.05);
}

/* ── WELCOME FEATURES ── */
.wc-feature {
  background:linear-gradient(145deg,rgba(15,40,20,.9),rgba(6,15,8,.95));
  border:1px solid rgba(255,165,0,.3); border-radius:20px; padding:26px 20px;
  text-align:center; transition:transform .25s,box-shadow .25s;
  animation:pop .5s cubic-bezier(.34,1.56,.64,1) both;
  box-shadow: 0 4px 20px rgba(0,0,0,.4);
}
.wc-feature:hover { transform:translateY(-7px); box-shadow:0 16px 36px rgba(0,0,0,.6),0 0 0 1px rgba(255,165,0,.5); }
.wc-feat-icon { font-size:46px; margin-bottom:14px; display:block; }
.wc-title { font-weight:800; color:#ffd166; font-size:16px; margin-bottom:8px; }
.wc-sub { font-size:13px; color:#52b788; }

/* ── SECTION DIVIDER ── */
.section-divider {
  height:2px;
  background:linear-gradient(90deg,transparent,rgba(255,165,0,.5),rgba(82,183,136,.5),transparent);
  border:none; margin:24px 0;
}

/* ── STREAMLIT BUTTONS ── */
.stButton > button {
  font-family:inherit !important;
  border-radius:13px !important;
  font-weight:800 !important;
  font-size:13px !important;
  transition:all .2s !important;
  white-space:normal !important;
  line-height:1.3 !important;
}
.stButton > button[kind="primary"] {
  background:linear-gradient(135deg,#1a4a10,#2d7a20) !important;
  border:2px solid rgba(255,165,0,.5) !important;
  color:#ffd166 !important;
  box-shadow:0 4px 16px rgba(0,0,0,.4) !important;
}
.stButton > button[kind="primary"]:hover {
  transform:translateY(-2px) !important;
  box-shadow:0 10px 28px rgba(255,165,0,.35) !important;
  border-color:rgba(255,165,0,.9) !important;
}
.stButton > button[kind="secondary"] {
  background:rgba(255,165,0,.08) !important;
  border:1px solid rgba(255,165,0,.3) !important;
  color:#ffa500 !important;
}
.stButton > button[kind="secondary"]:hover {
  background:rgba(255,165,0,.16) !important; transform:translateY(-1px) !important;
}
.stTabs [data-baseweb="tab-list"] {
  background:rgba(2,8,4,.92) !important; border-radius:16px !important;
  gap:4px !important; padding:5px !important;
  border:1px solid rgba(255,165,0,.2) !important;
}
.stTabs [data-baseweb="tab"] { color:#ffa500 !important; font-weight:700 !important; border-radius:12px !important; font-size:13px !important; }
.stTabs [aria-selected="true"] {
  background:linear-gradient(135deg,#1a4a10,#2d7a20) !important;
  color:#ffd166 !important;
  box-shadow:0 3px 14px rgba(0,0,0,.4) !important;
}
.stDownloadButton > button {
  background:linear-gradient(135deg,#1a5c38,#2d6a4f) !important;
  border:2px solid rgba(255,165,0,.4) !important; color:#ffd166 !important;
  border-radius:13px !important; font-family:inherit !important; font-weight:800 !important;
}
div[data-testid="stMarkdownContainer"] p { color:#b8e8c8 !important; }

/* ── LANGUAGE BAR BUTTONS ── */
.lang-active-btn button { background:linear-gradient(135deg,#ff8c00,#ffd166) !important; color:#1a0a00 !important; border:none !important; }
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
    if un in u: return False, T[st.session_state.get("lang","en")]["err_user_exists"]
    u[un]={"password":hp(pw),"full_name":fn,"phone":ph,"created":str(datetime.now())}
    save_users(u); return True, T[st.session_state.get("lang","en")]["reg_success"]
def login_user(un,pw):
    u=load_users()
    if un not in u: return False, T[st.session_state.get("lang","en")]["err_no_user"]
    if u[un]["password"]!=hp(pw): return False, T[st.session_state.get("lang","en")]["err_wrong_pass"]
    return True,u[un]["full_name"]

T={
"en":{
 "title":"🥭 Farmer's Mango Profit Navigator","subtitle":"Find the Best Market. Earn the Highest Return.",
 "ticker_label":"LIVE PRICES",
 "lname":"👤 Farmer Name","lvillage":"🏘️ Village","lvar":"🥭 Mango Variety",
 "lqty":"📦 Quantity (Quintals)","run_btn":"🚀 Find Best Market",
 "tip":"💡 Sell with nearby farmers to cut transport costs and boost profit!",
 "wctitle":"Welcome, Mango Farmer!","wcsub":"Select your village, variety, quantity — then click Find Best Market.",
 "wc1_title":"Pick Your Village","wc1_sub":"Find all nearby markets within 200km",
 "wc2_title":"Choose Your Variety","wc2_sub":"Matched to the right buyers for your mango",
 "wc3_title":"See Top 3 Profits","wc3_sub":"Compare all options and pick the best deal",
 "namaste":"Namaste","base_price":"Today's Market Price","best_profit":"Best Net Profit",
 "best_market":"Best Market","your_village":"Your Village",
 "tab1":"🥭 Top 3 Podium","tab2":"📊 All Options","tab3":"📈 Profit Charts","tab4":"🗺️ Map","tab5":"💡 Smart Advice",
 "rank":"Rank","market":"Market / Buyer","cat":"Type","dist":"Dist (km)",
 "rev":"Revenue (₹)","trans":"Transport (₹)","profit":"Net Profit (₹)",
 "chart_title":"Profit Comparison — Top 10","pie_title":"Profit Share by Category",
 "adv_title":"Smart Selling Advice for",
 "prices_title":"📈 Nearby Market Prices","today_price":"Today","yesterday_price":"Yesterday",
 "lang_full":"English",
 "voice_btn":"🔊 Listen to Top 3 Results","voice_stop":"⏹ Stop Reading",
 "login":"Login","register":"Register","logout":"🔴 Logout",
 "login_title":"👤 Login to Continue","reg_title":"📝 Create Account",
 "username":"Username","password":"Password","full_name":"Full Name","phone":"Phone (optional)",
 "login_btn":"Login →","reg_btn":"Register →",
 "have_account":"Already have account? Login","no_account":"New user? Create account",
 "mandal_ph":"Select Mandal","village_ph":"Select Village",
 "name_ph":"Enter your name","qty_label":"quintals",
 "err_fill":"Please fill all fields","err_pw_match":"Passwords do not match!",
 "err_pw_len":"Password min 6 characters","err_user_exists":"Username already exists!",
 "reg_success":"Registered! Please login.","err_no_user":"Username not found!",
 "err_wrong_pass":"Incorrect password!","err_village":"⚠️ Please select your village first!",
 "err_no_results":"No results. Try Banganapalli or Totapuri.",
 "analyzing":"🔄 Analyzing markets...",
 "map_title":"🗺️ Real Road Map — Powered by OpenStreetMap",
 "map_cap":"🛣️ Routes shown are real road distances via OSRM routing engine",
 "download_btn":"📥 Download Full Report (CSV)",
 "top3_breakdown":"📊 Top 3 Breakdown",
 "footer":"🥭 Farmer's Mango Profit Navigator · Empowering farmers across Andhra Pradesh · 🇮🇳 Made in India",
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
 "ticker_label":"నేటి ధరలు",
 "lname":"👤 రైతు పేరు","lvillage":"🏘️ మీ గ్రామం","lvar":"🥭 మామిడి రకం",
 "lqty":"📦 పరిమాణం (క్వింటాల్లు)","run_btn":"🚀 అత్యుత్తమ మార్కెట్ కనుగొనండి",
 "tip":"💡 పొరుగు రైతులతో కలిసి అమ్మండి — రవాణా ఖర్చు తక్కువ!",
 "wctitle":"స్వాగతం, మామిడి రైతు!","wcsub":"మీ గ్రామం, రకం, పరిమాణం ఎంచుకుని క్లిక్ చేయండి.",
 "wc1_title":"మీ గ్రామం ఎంచుకోండి","wc1_sub":"200కి.మీ. పరిధిలోని అన్ని మార్కెట్లు",
 "wc2_title":"మీ రకం ఎంచుకోండి","wc2_sub":"సరైన కొనుగోలుదారులకు మ్యాచ్",
 "wc3_title":"టాప్ 3 లాభాలు చూడండి","wc3_sub":"పోల్చి అత్యుత్తమ డీల్ ఎంచుకోండి",
 "namaste":"నమస్తే","base_price":"నేటి మార్కెట్ ధర","best_profit":"అత్యధిక నికర లాభం",
 "best_market":"అత్యుత్తమ మార్కెట్","your_village":"మీ గ్రామం",
 "tab1":"🥭 టాప్ 3 పోడియం","tab2":"📊 అన్ని ఎంపికలు","tab3":"📈 లాభాల పోలిక","tab4":"🗺️ మ్యాప్","tab5":"💡 తెలివైన సలహా",
 "rank":"వరుస","market":"మార్కెట్","cat":"రకం","dist":"దూరం (కి.మీ)",
 "rev":"ఆదాయం (₹)","trans":"రవాణా (₹)","profit":"నికర లాభం (₹)",
 "chart_title":"లాభాల పోలిక — టాప్ 10","pie_title":"వర్గం వారీ లాభం",
 "adv_title":"తెలివైన అమ్మకపు సలహా",
 "prices_title":"📈 సమీప మార్కెట్ ధరలు","today_price":"నేడు","yesterday_price":"నిన్న",
 "lang_full":"తెలుగు",
 "voice_btn":"🔊 ఫలితాలు వినండి","voice_stop":"⏹ ఆపండి",
 "login":"లాగిన్","register":"రిజిస్టర్","logout":"🔴 లాగ్ అవుట్",
 "login_title":"👤 కొనసాగించడానికి లాగిన్","reg_title":"📝 ఖాతా సృష్టించండి",
 "username":"వినియోగదారు పేరు","password":"పాస్వర్డ్","full_name":"పూర్తి పేరు","phone":"ఫోన్ (ఐచ్ఛికం)",
 "login_btn":"లాగిన్ →","reg_btn":"రిజిస్టర్ →",
 "have_account":"ఖాతా ఉందా? లాగిన్","no_account":"కొత్తగా? ఖాతా సృష్టించండి",
 "mandal_ph":"మండల్ ఎంచుకోండి","village_ph":"గ్రామం ఎంచుకోండి",
 "name_ph":"మీ పేరు","qty_label":"క్వింటాల్లు",
 "err_fill":"దయచేసి అన్ని ఫీల్డ్స్ పూరించండి","err_pw_match":"పాస్వర్డ్లు సరిపోలడం లేదు!",
 "err_pw_len":"పాస్వర్డ్ కనీసం 6 అక్షరాలు","err_user_exists":"వినియోగదారు పేరు ఇప్పటికే ఉంది!",
 "reg_success":"నమోదు అయింది! లాగిన్ చేయండి.","err_no_user":"వినియోగదారు పేరు కనుగొనబడలేదు!",
 "err_wrong_pass":"తప్పు పాస్వర్డ్!","err_village":"⚠️ దయచేసి మీ గ్రామం ఎంచుకోండి!",
 "err_no_results":"ఫలితాలు లేవు. బంగినపల్లి లేదా తోటపురి ప్రయత్నించండి.",
 "analyzing":"🔄 మార్కెట్లు విశ్లేషిస్తున్నాం...",
 "map_title":"🗺️ నిజమైన రోడ్ మ్యాప్ — OpenStreetMap",
 "map_cap":"🛣️ OSRM ద్వారా నిజమైన రోడ్ దూరాలు చూపబడ్డాయి",
 "download_btn":"📥 పూర్తి నివేదిక డౌన్‌లోడ్ (CSV)",
 "top3_breakdown":"📊 టాప్ 3 వివరాలు",
 "footer":"🥭 రైతు మామిడి లాభాల నావిగేటర్ · ఆంధ్రప్రదేశ్ రైతులకు సేవ · 🇮🇳 భారత్ లో తయారైంది",
 "variety_advice":{
   "Banganapalli": [
     ("🌟","ప్రీమియం ఎగుమతి రకం","బంగినపల్లి భారతదేశంలో అత్యుత్తమ ఎగుమతి మామిడి. ఎగుమతి ప్యాక్‌హౌస్‌లు మొదటగా సంప్రదించండి — మండీ కంటే 15-25% ఎక్కువ ధర పొందుతారు."),
     ("📦","సరైన గ్రేడింగ్ అవసరం","A/B/C గ్రేడ్‌లు వేరు చేయండి. ఎగుమతి కొనుగోలుదారులు గ్రేడ్ A మాత్రమే తీసుకుంటారు (250g+, మచ్చలు లేకుండా)."),
     ("🌡️","ఉష్ణోగ్రత నిర్వహణ","ఎగుమతి కోసం కొంచెం ముందు కోయండి. నీడలో ఉంచి 6 గంటల్లో డెలివరీ చేయండి."),
     ("🤝","గ్రూపులో అమ్మండి","రైతు ఉత్పత్తి సంఘం ఏర్పాటు చేయండి — 5+ టన్నుల లాట్‌కు మెరుగైన ధర పొందుతారు."),
   ],
   "Totapuri": [
     ("🏭","ప్రాసెసింగ్ యూనిట్లు లక్ష్యంగా చేసుకోండి","తోటపురి ప్రాసెసింగ్ రాజు — పల్ప్ కర్మాగారాలు, జ్యూస్ యూనిట్లు మండీ కంటే 8-12% ఎక్కువ ఇస్తాయి."),
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
 "ticker_label":"आज के भाव",
 "lname":"👤 किसान का नाम","lvillage":"🏘️ आपका गांव","lvar":"🥭 आम की किस्म",
 "lqty":"📦 मात्रा (क्विंटल)","run_btn":"🚀 सबसे अच्छा बाजार खोजें",
 "tip":"💡 पड़ोसी किसानों के साथ मिलकर बेचें — परिवहन लागत कम होगी!",
 "wctitle":"स्वागत है, आम किसान!","wcsub":"अपना गांव, किस्म और मात्रा चुनें — फिर क्लिक करें।",
 "wc1_title":"अपना गांव चुनें","wc1_sub":"200 किमी के भीतर सभी बाजार",
 "wc2_title":"अपनी किस्म चुनें","wc2_sub":"सही खरीदारों से मिलाएं",
 "wc3_title":"टॉप 3 मुनाफे देखें","wc3_sub":"तुलना करें और सबसे अच्छा सौदा चुनें",
 "namaste":"नमस्ते","base_price":"आज का बाजार भाव","best_profit":"सर्वाधिक शुद्ध लाभ",
 "best_market":"सबसे अच्छा बाजार","your_village":"आपका गांव",
 "tab1":"🥭 टॉप 3 पोडियम","tab2":"📊 सभी विकल्प","tab3":"📈 लाभ तुलना","tab4":"🗺️ मानचित्र","tab5":"💡 स्मार्ट सलाह",
 "rank":"क्रम","market":"बाजार","cat":"प्रकार","dist":"दूरी (किमी)",
 "rev":"आय (₹)","trans":"परिवहन (₹)","profit":"शुद्ध लाभ (₹)",
 "chart_title":"लाभ तुलना — टॉप 10","pie_title":"श्रेणी अनुसार लाभ",
 "adv_title":"स्मार्ट बिक्री सलाह",
 "prices_title":"📈 पास के बाजार के भाव","today_price":"आज","yesterday_price":"कल",
 "lang_full":"हिंदी",
 "voice_btn":"🔊 परिणाम सुनें","voice_stop":"⏹ रोकें",
 "login":"लॉगिन","register":"रजिस्टर","logout":"🔴 लॉगआउट",
 "login_title":"👤 लॉगिन करें","reg_title":"📝 खाता बनाएं",
 "username":"यूज़रनेम","password":"पासवर्ड","full_name":"पूरा नाम","phone":"फोन (वैकल्पिक)",
 "login_btn":"लॉगिन →","reg_btn":"रजिस्टर →",
 "have_account":"खाता है? लॉगिन करें","no_account":"नए हैं? खाता बनाएं",
 "mandal_ph":"मंडल चुनें","village_ph":"गांव चुनें",
 "name_ph":"अपना नाम","qty_label":"क्विंटल",
 "err_fill":"कृपया सभी फ़ील्ड भरें","err_pw_match":"पासवर्ड मेल नहीं खाते!",
 "err_pw_len":"पासवर्ड न्यूनतम 6 अक्षर","err_user_exists":"यूज़रनेम पहले से मौजूद है!",
 "reg_success":"पंजीकरण हुआ! लॉगिन करें.","err_no_user":"यूज़रनेम नहीं मिला!",
 "err_wrong_pass":"गलत पासवर्ड!","err_village":"⚠️ कृपया पहले अपना गांव चुनें!",
 "err_no_results":"कोई परिणाम नहीं। बंगनपल्ली या तोतापुरी आज़माएं।",
 "analyzing":"🔄 बाजारों का विश्लेषण हो रहा है...",
 "map_title":"🗺️ वास्तविक सड़क मानचित्र — OpenStreetMap",
 "map_cap":"🛣️ OSRM से वास्तविक सड़क दूरियां",
 "download_btn":"📥 पूरी रिपोर्ट डाउनलोड (CSV)",
 "top3_breakdown":"📊 टॉप 3 विवरण",
 "footer":"🥭 किसान का आम लाभ नेविगेटर · आंध्र प्रदेश के किसानों की सेवा · 🇮🇳 भारत में बना",
 "variety_advice":{
   "Banganapalli": [
     ("🌟","प्रीमियम एक्सपोर्ट किस्म","बंगनपल्ली भारत का सर्वश्रेष्ठ निर्यात आम है। एक्सपोर्ट पैकहाउस पहले संपर्क करें — मंडी से 15-25% अधिक मिलेगा।"),
     ("📦","ग्रेडिंग जरूरी है","A/B/C ग्रेड अलग करें। एक्सपोर्ट खरीदार केवल ग्रेड A (250g+) लेते हैं।"),
     ("🌡️","तापमान प्रबंधन","थोड़ा पहले काटें और 6 घंटे में डिलीवरी करें।"),
     ("🤝","समूह में बेचें","किसान उत्पादक समूह बनाएं — 5+ टन लॉट पर बेहतर दाम मिलता है।"),
   ],
   "Totapuri": [
     ("🏭","प्रसंस्करण इकाइयां टारगेट करें","तोतापुरी प्रसंस्करण का राजा है — पल्प फैक्ट्रियां मंडी से 8-12% अधिक देती हैं।"),
     ("⚡","जल्दी डिलीवरी करें","तोतापुरी जल्दी खराब होता है। कटाई के 12 घंटे में डिलीवरी करें।"),
     ("🧪","Brix स्तर जांचें","Brix 14+ होने पर ₹3-5/kg अतिरिक्त मिलता है।"),
     ("📅","अग्रिम अनुबंध करें","फसल से पहले PLR Foods के साथ अनुबंध करें।"),
   ],
   "Neelam": [
     ("🏪","मंडी में सर्वोत्तम भाव","नीलम मंडी में बहुत लोकप्रिय है। सुबह 8 बजे से पहले पहुंचें।"),
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
 "ticker_label":"இன்றைய விலைகள்",
 "lname":"👤 விவசாயி பெயர்","lvillage":"🏘️ கிராமம்","lvar":"🥭 மாம்பழ வகை",
 "lqty":"📦 அளவு (குவிண்டால்)","run_btn":"🚀 சிறந்த சந்தையைக் கண்டறி",
 "tip":"💡 அண்டை விவசாயிகளுடன் சேர்ந்து விற்கவும் — போக்குவரத்து செலவு குறையும்!",
 "wctitle":"வரவேற்கிறோம், மாம்பழ விவசாயி!","wcsub":"கிராமம், வகை, அளவை தேர்ந்தெடுத்து கிளிக் செய்யுங்கள்.",
 "wc1_title":"உங்கள் கிராமம் தேர்ந்தெடுங்கள்","wc1_sub":"200 கி.மீ. தொலைவிலுள்ள சந்தைகள்",
 "wc2_title":"உங்கள் வகை தேர்ந்தெடுங்கள்","wc2_sub":"சரியான வாங்குபவர்களுடன் பொருத்தம்",
 "wc3_title":"சிறந்த 3 லாபங்கள் பாருங்கள்","wc3_sub":"ஒப்பிட்டு சிறந்த ஒப்பந்தம் தேர்ந்தெடுங்கள்",
 "namaste":"வணக்கம்","base_price":"இன்றைய விலை","best_profit":"அதிகபட்ச லாபம்",
 "best_market":"சிறந்த சந்தை","your_village":"கிராமம்",
 "tab1":"🥭 சிறந்த 3","tab2":"📊 அனைத்தும்","tab3":"📈 லாப ஒப்பீடு","tab4":"🗺️ வரைபடம்","tab5":"💡 ஆலோசனை",
 "rank":"வரிசை","market":"சந்தை","cat":"வகை","dist":"தூரம் (கி.மீ.)",
 "rev":"வருவாய் (₹)","trans":"போக்குவரத்து (₹)","profit":"நிகர லாபம் (₹)",
 "chart_title":"லாப ஒப்பீடு — சிறந்த 10","pie_title":"வகை வாரியான லாபம்",
 "adv_title":"விற்பனை ஆலோசனை",
 "prices_title":"📈 சந்தை விலைகள்","today_price":"இன்று","yesterday_price":"நேற்று",
 "lang_full":"தமிழ்",
 "voice_btn":"🔊 முடிவுகளை கேளுங்கள்","voice_stop":"⏹ நிறுத்து",
 "login":"உள்நுழைவு","register":"பதிவு","logout":"🔴 வெளியேறு",
 "login_title":"👤 உள்நுழைக","reg_title":"📝 கணக்கு உருவாக்கு",
 "username":"பயனர்பெயர்","password":"கடவுச்சொல்","full_name":"முழு பெயர்","phone":"தொலைபேசி (விருப்பம்)",
 "login_btn":"உள்நுழைவு →","reg_btn":"பதிவு →",
 "have_account":"கணக்கு உள்ளதா? உள்நுழைக","no_account":"புதியவரா? கணக்கு உருவாக்கு",
 "mandal_ph":"மண்டலம் தேர்ந்தெடு","village_ph":"கிராமம் தேர்ந்தெடு",
 "name_ph":"உங்கள் பெயர்","qty_label":"குவிண்டால்",
 "err_fill":"அனைத்து புலங்களையும் நிரப்பவும்","err_pw_match":"கடவுச்சொற்கள் பொருந்தவில்லை!",
 "err_pw_len":"கடவுச்சொல் குறைந்தது 6 எழுத்துகள்","err_user_exists":"பயனர்பெயர் ஏற்கெனவே உள்ளது!",
 "reg_success":"பதிவு ஆனது! உள்நுழைக.","err_no_user":"பயனர்பெயர் கிடைக்கவில்லை!",
 "err_wrong_pass":"தவறான கடவுச்சொல்!","err_village":"⚠️ முதலில் உங்கள் கிராமத்தை தேர்ந்தெடுங்கள்!",
 "err_no_results":"முடிவுகள் இல்லை. பங்கனபல்லி அல்லது தொதாபுரி முயற்சிக்கவும்.",
 "analyzing":"🔄 சந்தைகளை பகுப்பாய்வு செய்கிறோம்...",
 "map_title":"🗺️ உண்மையான சாலை வரைபடம் — OpenStreetMap",
 "map_cap":"🛣️ OSRM வழியாக உண்மையான சாலை தூரங்கள்",
 "download_btn":"📥 முழு அறிக்கை பதிவிறக்கம் (CSV)",
 "top3_breakdown":"📊 சிறந்த 3 விவரம்",
 "footer":"🥭 மாம்பழ லாப வழிகாட்டி · ஆந்திரப் பிரதேச விவசாயிகளுக்கு · 🇮🇳 இந்தியாவில் தயாரிக்கப்பட்டது",
 "variety_advice":{
   "Banganapalli": [
     ("🌟","ஏற்றுமதி தரம்","பங்கனபல்லி இந்தியாவின் சிறந்த ஏற்றுமதி மாம்பழம். ஏற்றுமதி நிலையங்களை முதலில் தொடர்பு கொள்ளுங்கள் — மண்டியை விட 15-25% அதிகம்."),
     ("📦","தரம் பிரிக்கவும்","A/B/C தரங்களை பிரிக்கவும். ஏற்றுமதி வாங்குபவர்கள் தரம் A (250g+) மட்டுமே எடுப்பார்கள்."),
     ("🌡️","வெப்பநிலை மேலாண்மை","ஏற்றுமதிக்கு கொஞ்சம் முன்பே அறுவடை. 6 மணி நேரத்தில் விநியோகிக்கவும்."),
     ("🤝","குழுவாக விற்கவும்","விவசாயி உற்பத்தி குழு உருவாக்கவும் — 5+ டன் தொகுதிக்கு சிறந்த விலை."),
   ],
   "Totapuri": [
     ("🏭","பதப்படுத்தல் நிலையங்கள்","தொதாபுரி பதப்படுத்தல் ராஜா — பழச்சாறு தொழிற்சாலைகள் 8-12% அதிகமாக தருகின்றன."),
     ("⚡","விரைந்து விநியோகிக்கவும்","12 மணி நேரத்திற்குள் விநியோகிக்கவும்."),
     ("🧪","Brix அளவை சரிபார்க்கவும்","Brix 14+ இருந்தால் ₹3-5/kg கூடுதலாக கிடைக்கும்."),
     ("📅","முன்கூட்டிய ஒப்பந்தம்","அறுவடைக்கு முன் PLR Foods உடன் ஒப்பந்தம்."),
   ],
   "Neelam": [
     ("🏪","மண்டி சிறந்தது","நீலம் மண்டியில் மிகவும் பிரபலம். காலை 8 மணிக்கு முன் வந்தடையுங்கள்."),
     ("🎁","சில்லறை பேக்கிங்","பரிசு பெட்டிகளில் பேக்கிங் செய்தால் ₹80-120/kg கிடைக்கும்."),
     ("🌿","இயற்கை சான்றிதழ்","இயற்கை விவசாயம் செய்தால் 40-60% அதிக விலை."),
     ("📱","நேரடியாக விற்கவும்","WhatsApp வழியாக நேரடியாக நகர வாங்குபவர்களுக்கு விற்கவும்."),
   ],
   "Rasalu": [
     ("🥒","ஊறுகாய் தொழிற்சாலைகள்","ரசாலு #1 ஊறுகாய் மாம்பழம். மண்டியை விட 10-15% அதிகம்."),
     ("🕐","சரியான நேரத்தில் அறுவடை","ஊறுகாய்க்கு உறுதியான நிலையில் அறுவடை செய்யுங்கள்."),
     ("💰","சிறிய பழங்களுக்கு அதிக விலை","150-200g பழங்கள் ஊறுகாய் தயாரிப்பாளர்களுக்கு விரும்பப்படுகின்றன."),
     ("🔄","இரட்டை சந்தை உத்தி","உறுதியான → ஊறுகாய் நிலையங்கள், பழுத்த → மண்டி."),
   ],
 },
 "var_labels":{"Banganapalli":"பங்கனபல்லி\n⭐ ஏற்றுமதி","Totapuri":"தொதாபுரி\n⭐ பதப்படுத்தல்","Neelam":"நீலம்\n⭐ மண்டி","Rasalu":"ரசாலு\n⭐ ஊறுகாய்"},
},

"gu":{
 "title":"🥭 ખેડૂતનો કેરી નફો નેવિગેટર","subtitle":"શ્રેષ્ઠ બજાર શોધો. સૌથી વધુ નફો કમાઓ.",
 "ticker_label":"આજના ભાવ",
 "lname":"👤 ખેડૂતનું નામ","lvillage":"🏘️ ગામ","lvar":"🥭 કેરીની જાત",
 "lqty":"📦 જથ્થો (ક્વિન્ટલ)","run_btn":"🚀 શ્રેષ્ઠ બજાર શોધો",
 "tip":"💡 પડોશી ખેડૂતો સાથે મળીને વેચો — પરિવહન ખર્ચ ઘટશે!",
 "wctitle":"સ્વાગત છે, કેરી ખેડૂત!","wcsub":"ગામ, જાત અને જથ્થો પસંદ કરો — પછી ક્લિક કરો.",
 "wc1_title":"તમારું ગામ પસંદ કરો","wc1_sub":"200 કિ.મી. ત્રિજ્યામાં બધા બજારો",
 "wc2_title":"તમારી જાત પસંદ કરો","wc2_sub":"યોગ્ય ખરીદારો સાથે મેળ",
 "wc3_title":"ટોપ 3 નફો જુઓ","wc3_sub":"સરખામણી કરો અને શ્રેષ્ઠ સોદો પસંદ કરો",
 "namaste":"નમસ્તે","base_price":"આજનો બજાર ભાવ","best_profit":"સૌથી વધુ ચોખ્ખો નફો",
 "best_market":"શ્રેષ્ઠ બજાર","your_village":"તમારું ગામ",
 "tab1":"🥭 ટોપ 3 પોડિયમ","tab2":"📊 બધા વિકલ્પ","tab3":"📈 નફો સરખામણી","tab4":"🗺️ નકશો","tab5":"💡 સ્માર્ટ સલાહ",
 "rank":"ક્રમ","market":"બજાર","cat":"પ્રકાર","dist":"અંતર (કિ.મી.)",
 "rev":"આવક (₹)","trans":"પરિવહન (₹)","profit":"ચોખ્ખો નફો (₹)",
 "chart_title":"નફો સરખામણી — ટોપ 10","pie_title":"શ્રેણી મુજબ નફો",
 "adv_title":"વેચાણ સલાહ",
 "prices_title":"📈 નજીકના બજારના ભાવ","today_price":"આજ","yesterday_price":"ગઈ કાલ",
 "lang_full":"ગુજરાતી",
 "voice_btn":"🔊 પરિણામ સાંભળો","voice_stop":"⏹ રોકો",
 "login":"લૉગઇન","register":"નોંધણી","logout":"🔴 લૉગ આઉટ",
 "login_title":"👤 લૉગઇન કરો","reg_title":"📝 ખાતું બનાવો",
 "username":"વપરાશકર્તા નામ","password":"પાસવર્ડ","full_name":"પૂરું નામ","phone":"ફોન (વૈકલ્પિક)",
 "login_btn":"લૉગઇન →","reg_btn":"નોંધણી →",
 "have_account":"ખાતું છે? લૉગઇન","no_account":"નવા છો? ખાતું બનાવો",
 "mandal_ph":"મંડળ પસંદ કરો","village_ph":"ગામ પસંદ કરો",
 "name_ph":"તમારું નામ","qty_label":"ક્વિન્ટલ",
 "err_fill":"કૃપા કરીને બધા ક્ષેત્રો ભરો","err_pw_match":"પાસવર્ડ મળતા નથી!",
 "err_pw_len":"પાસવર્ડ ઓછામાં ઓછા 6 અક્ષર","err_user_exists":"વપરાશકર્તા નામ પહેલેથી અસ્તિત્વ ધરાવે છે!",
 "reg_success":"નોંધણી થઈ! કૃપા કરીને લૉગઇન કરો.","err_no_user":"વપરાશકર્તા નામ મળ્યું નહીં!",
 "err_wrong_pass":"ખોટો પાસવર્ડ!","err_village":"⚠️ કૃપા કરીને પ્રથમ તમારું ગામ પસંદ કરો!",
 "err_no_results":"કોઈ પરિણામ નહીં. બંગનપલ્લી અથવા તોતાપુરી અજમાવો.",
 "analyzing":"🔄 બજારોનું વિશ્લેષણ...",
 "map_title":"🗺️ વાસ્તવિક સડક નકશો — OpenStreetMap",
 "map_cap":"🛣️ OSRM દ્વારા વાસ્તવિક સડક અંતર",
 "download_btn":"📥 સંપૂર્ણ અહેવાલ ડાઉનલોડ (CSV)",
 "top3_breakdown":"📊 ટોપ 3 વિવરણ",
 "footer":"🥭 કેરી નફો નેવિગેટર · ગુજરાત અને આંધ્ર પ્રદેશ ખેડૂતો · 🇮🇳 ભારતમાં બનેલું",
 "variety_advice":{
   "Banganapalli": [
     ("🌟","પ્રીમિયમ નિકાસ જાત","બંગનપલ્લી ભારતની સૌથી સારી નિકાસ કેરી. નિકાસ પૅકહાઉસ પ્રથમ સંપર્ક — 15-25% વધુ ભાવ."),
     ("📦","ગ્રેડિંગ જરૂરી","A/B/C ગ્રેડ અલગ કરો. નિકાસ ખરીદદારો ગ્રેડ A (250g+) જ લે છે."),
     ("🌡️","તાપમાન વ્યવસ્થાપન","નિકાસ માટે થોડું વહેલું કાપો. 6 કલાકમાં ડિલિવરી."),
     ("🤝","જૂથમાં વેચો","5+ ટન માટે ખેડૂત ઉત્પાદક જૂથ — વધુ સારા ભાવ."),
   ],
   "Totapuri": [
     ("🏭","પ્રૉસેસિંગ એકમો ટાર્ગેટ","તોતાપુરી પ્રૉસેસિંગ રાજા — 8-12% વધુ ભાવ."),
     ("⚡","ઝડપી ડિલિવરી","12 કલાકમાં ડિલિવરી."),
     ("🧪","Brix 14+ = ₹3-5/kg વધુ","Brix સ્તર તપાસો."),
     ("📅","અગ્રિમ કરાર","PLR Foods સાથે પહેલેથી કરાર."),
   ],
   "Neelam": [
     ("🏪","મંડીમાં શ્રેષ્ઠ ભાવ","સવારે 8 વાગ્યા પહેલા પહોંચો."),
     ("🎁","રિટેલ પૅકિંગ","ગિફ્ટ બૉક્સ ₹80-120/kg."),
     ("🌿","ઓર્ગેનિક = 40-60% વધુ","ઓર્ગેનિક સર્ટિફિકેશન."),
     ("📱","WhatsApp ઑનલાઇન","સીધા શહેરી ખરીદારોને વેચો."),
   ],
   "Rasalu": [
     ("🥒","અથાણાં ફૅક્ટરી","10-15% વધુ ભાવ."),
     ("🕐","સાચા સ્તરે કાપો","અથાણા માટે સખત-પાકું."),
     ("💰","નાના ફળ = વધુ ભાવ","150-200g ફળ."),
     ("🔄","બેવડી બજાર વ્યૂહ","સખત → અથાણાં, પાકેલ → મંડી."),
   ],
 },
 "var_labels":{"Banganapalli":"બંગનપલ્લી\n⭐ નિકાસ","Totapuri":"તોતાપુરી\n⭐ પ્રૉસેસિંગ","Neelam":"નીલમ\n⭐ મંડી","Rasalu":"રસાળુ\n⭐ અથાણું"},
},

"kn":{
 "title":"🥭 ರೈತನ ಮಾವಿನ ಲಾಭ ನ್ಯಾವಿಗೇಟರ್","subtitle":"ಅತ್ಯುತ್ತಮ ಮಾರುಕಟ್ಟೆ ಹುಡುಕಿ. ಹೆಚ್ಚು ಲಾಭ ಗಳಿಸಿ.",
 "ticker_label":"ಇಂದಿನ ಬೆಲೆಗಳು",
 "lname":"👤 ರೈತರ ಹೆಸರು","lvillage":"🏘️ ಹಳ್ಳಿ","lvar":"🥭 ಮಾವಿನ ತಳಿ",
 "lqty":"📦 ಪ್ರಮಾಣ (ಕ್ವಿಂಟಾಲ್)","run_btn":"🚀 ಅತ್ಯುತ್ತಮ ಮಾರುಕಟ್ಟೆ ಹುಡುಕಿ",
 "tip":"💡 ನೆರೆಯ ರೈತರೊಂದಿಗೆ ಒಟ್ಟಾಗಿ ಮಾರಾಟ ಮಾಡಿ — ಸಾರಿಗೆ ವೆಚ್ಚ ಕಡಿಮೆ!",
 "wctitle":"ಸ್ವಾಗತ, ಮಾವಿನ ರೈತ!","wcsub":"ಹಳ್ಳಿ, ತಳಿ, ಪ್ರಮಾಣ ಆರಿಸಿ — ನಂತರ ಕ್ಲಿಕ್ ಮಾಡಿ.",
 "wc1_title":"ನಿಮ್ಮ ಹಳ್ಳಿ ಆರಿಸಿ","wc1_sub":"200 ಕಿ.ಮೀ. ತ್ರಿಜ್ಯದಲ್ಲಿ ಎಲ್ಲಾ ಮಾರುಕಟ್ಟೆಗಳು",
 "wc2_title":"ನಿಮ್ಮ ತಳಿ ಆರಿಸಿ","wc2_sub":"ಸರಿಯಾದ ಖರೀದಿದಾರರಿಗೆ ಹೊಂದಿಸಿ",
 "wc3_title":"ಟಾಪ್ 3 ಲಾಭ ನೋಡಿ","wc3_sub":"ಹೋಲಿಸಿ ಅತ್ಯುತ್ತಮ ಒಪ್ಪಂದ ಆರಿಸಿ",
 "namaste":"ನಮಸ್ಕಾರ","base_price":"ಇಂದಿನ ಮಾರುಕಟ್ಟೆ ಬೆಲೆ","best_profit":"ಅತ್ಯಧಿಕ ನಿವ್ವಳ ಲಾಭ",
 "best_market":"ಅತ್ಯುತ್ತಮ ಮಾರುಕಟ್ಟೆ","your_village":"ನಿಮ್ಮ ಹಳ್ಳಿ",
 "tab1":"🥭 ಟಾಪ್ 3 ಪೋಡಿಯಂ","tab2":"📊 ಎಲ್ಲಾ ಆಯ್ಕೆಗಳು","tab3":"📈 ಲಾಭ ಹೋಲಿಕೆ","tab4":"🗺️ ನಕ್ಷೆ","tab5":"💡 ಸ್ಮಾರ್ಟ್ ಸಲಹೆ",
 "rank":"ಶ್ರೇಣಿ","market":"ಮಾರುಕಟ್ಟೆ","cat":"ಪ್ರಕಾರ","dist":"ದೂರ (ಕಿ.ಮೀ.)",
 "rev":"ಆದಾಯ (₹)","trans":"ಸಾರಿಗೆ (₹)","profit":"ನಿವ್ವಳ ಲಾಭ (₹)",
 "chart_title":"ಲಾಭ ಹೋಲಿಕೆ — ಟಾಪ್ 10","pie_title":"ವರ್ಗ ಪ್ರಕಾರ ಲಾಭ",
 "adv_title":"ಮಾರಾಟ ಸಲಹೆ",
 "prices_title":"📈 ಹತ್ತಿರದ ಮಾರುಕಟ್ಟೆ ಬೆಲೆ","today_price":"ಇಂದು","yesterday_price":"ನಿನ್ನೆ",
 "lang_full":"ಕನ್ನಡ",
 "voice_btn":"🔊 ಫಲಿತಾಂಶ ಕೇಳಿ","voice_stop":"⏹ ನಿಲ್ಲಿಸಿ",
 "login":"ಲಾಗಿನ್","register":"ನೋಂದಣಿ","logout":"🔴 ಲಾಗ್ ಔಟ್",
 "login_title":"👤 ಲಾಗಿನ್ ಮಾಡಿ","reg_title":"📝 ಖಾತೆ ರಚಿಸಿ",
 "username":"ಬಳಕೆದಾರ ಹೆಸರು","password":"ಪಾಸ್ವರ್ಡ್","full_name":"ಪೂರ್ಣ ಹೆಸರು","phone":"ಫೋನ್ (ಐಚ್ಛಿಕ)",
 "login_btn":"ಲಾಗಿನ್ →","reg_btn":"ನೋಂದಣಿ →",
 "have_account":"ಖಾತೆ ಇದೆಯೇ? ಲಾಗಿನ್","no_account":"ಹೊಸಬರೇ? ಖಾತೆ ರಚಿಸಿ",
 "mandal_ph":"ಮಂಡಲ ಆಯ್ಕೆ","village_ph":"ಹಳ್ಳಿ ಆಯ್ಕೆ",
 "name_ph":"ನಿಮ್ಮ ಹೆಸರು","qty_label":"ಕ್ವಿಂಟಾಲ್",
 "err_fill":"ದಯವಿಟ್ಟು ಎಲ್ಲಾ ಕ್ಷೇತ್ರಗಳನ್ನು ಭರ್ತಿ ಮಾಡಿ","err_pw_match":"ಪಾಸ್ವರ್ಡ್‌ಗಳು ಹೊಂದಾಣಿಕೆಯಾಗುತ್ತಿಲ್ಲ!",
 "err_pw_len":"ಪಾಸ್ವರ್ಡ್ ಕನಿಷ್ಠ 6 ಅಕ್ಷರ","err_user_exists":"ಬಳಕೆದಾರ ಹೆಸರು ಈಗಾಗಲೇ ಅಸ್ತಿತ್ವದಲ್ಲಿದೆ!",
 "reg_success":"ನೋಂದಣಿ ಆಗಿದೆ! ದಯವಿಟ್ಟು ಲಾಗಿನ್ ಮಾಡಿ.","err_no_user":"ಬಳಕೆದಾರ ಹೆಸರು ಕಂಡುಬಂದಿಲ್ಲ!",
 "err_wrong_pass":"ತಪ್ಪಾದ ಪಾಸ್ವರ್ಡ್!","err_village":"⚠️ ದಯವಿಟ್ಟು ಮೊದಲು ನಿಮ್ಮ ಹಳ್ಳಿ ಆರಿಸಿ!",
 "err_no_results":"ಫಲಿತಾಂಶಗಳಿಲ್ಲ. ಬಂಗನಪಲ್ಲಿ ಅಥವಾ ತೋತಾಪುರಿ ಪ್ರಯತ್ನಿಸಿ.",
 "analyzing":"🔄 ಮಾರುಕಟ್ಟೆಗಳನ್ನು ವಿಶ್ಲೇಷಿಸುತ್ತಿದ್ದೇವೆ...",
 "map_title":"🗺️ ನಿಜವಾದ ರಸ್ತೆ ನಕ್ಷೆ — OpenStreetMap",
 "map_cap":"🛣️ OSRM ಮೂಲಕ ನಿಜವಾದ ರಸ್ತೆ ದೂರಗಳು",
 "download_btn":"📥 ಸಂಪೂರ್ಣ ವರದಿ ಡೌನ್‌ಲೋಡ್ (CSV)",
 "top3_breakdown":"📊 ಟಾಪ್ 3 ವಿವರ",
 "footer":"🥭 ಮಾವಿನ ಲಾಭ ನ್ಯಾವಿಗೇಟರ್ · ಆಂಧ್ರ ಪ್ರದೇಶ ರೈತರ ಸೇವೆ · 🇮🇳 ಭಾರತದಲ್ಲಿ ತಯಾರಿಸಲಾಗಿದೆ",
 "variety_advice":{
   "Banganapalli": [
     ("🌟","ರಫ್ತು ತಳಿ","ಬಂಗನಪಲ್ಲಿ ಭಾರತದ ಅತ್ಯುತ್ತಮ ರಫ್ತು ಮಾವು. ರಫ್ತು ಪ್ಯಾಕ್‌ಹೌಸ್ ಮೊದಲು ಸಂಪರ್ಕಿಸಿ — 15-25% ಹೆಚ್ಚು ಬೆಲೆ."),
     ("📦","ದರ್ಜೆ ವಿಂಗಡಣೆ","A/B/C ದರ್ಜೆ ಪ್ರತ್ಯೇಕಿಸಿ. ರಫ್ತು ಖರೀದಿದಾರರು ದರ್ಜೆ A (250g+) ಮಾತ್ರ."),
     ("🌡️","ತಾಪಮಾನ ನಿರ್ವಹಣೆ","6 ಗಂಟೆಯಲ್ಲಿ ವಿತರಿಸಿ."),
     ("🤝","ಗುಂಪಾಗಿ ಮಾರಾಟ","5+ ಟನ್ — ಉತ್ತಮ ಬೆಲೆ."),
   ],
   "Totapuri": [
     ("🏭","ಸಂಸ್ಕರಣ ಘಟಕಗಳು","ತೋತಾಪುರಿ ಸಂಸ್ಕರಣದ ರಾಜ — 8-12% ಹೆಚ್ಚು."),
     ("⚡","ತ್ವರಿತ ವಿತರಣೆ","12 ಗಂಟೆಯಲ್ಲಿ ವಿತರಿಸಿ."),
     ("🧪","Brix 14+ = ₹3-5/kg ಹೆಚ್ಚು","Brix ಮಟ್ಟ ಪರೀಕ್ಷಿಸಿ."),
     ("📅","ಮುಂಗಡ ಒಪ್ಪಂದ","PLR Foods ಜೊತೆ ಮುಂಚೆ."),
   ],
   "Neelam": [
     ("🏪","ಮಂಡಿ ಅತ್ಯುತ್ತಮ","ಬೆಳಿಗ್ಗೆ 8 ಗಂಟೆ ಮೊದಲು ತಲುಪಿ."),
     ("🎁","ರಿಟೇಲ್ ಪ್ಯಾಕಿಂಗ್","ಗಿಫ್ಟ್ ಬಾಕ್ಸ್ ₹80-120/kg."),
     ("🌿","ಸಾವಯವ = 40-60% ಹೆಚ್ಚು","ಸಾವಯವ ಪ್ರಮಾಣಪತ್ರ ಪಡೆಯಿರಿ."),
     ("📱","WhatsApp ಮಾರಾಟ","ನೇರ ಮಾರಾಟ."),
   ],
   "Rasalu": [
     ("🥒","ಉಪ್ಪಿನಕಾಯಿ ಕಾರ್ಖಾನೆ","10-15% ಹೆಚ್ಚು."),
     ("🕐","ಸರಿಯಾದ ಹಂತದಲ್ಲಿ ಕಟಾವು","ಗಟ್ಟಿ-ಹಣ್ಣು."),
     ("💰","ಚಿಕ್ಕ ಹಣ್ಣು = ಹೆಚ್ಚು ಬೆಲೆ","150-200g."),
     ("🔄","ದ್ವಿ ಮಾರುಕಟ್ಟೆ","ಗಟ್ಟಿ → ಉಪ್ಪಿನಕಾಯಿ, ಹಣ್ಣು → ಮಂಡಿ."),
   ],
 },
 "var_labels":{"Banganapalli":"ಬಂಗನಪಲ್ಲಿ\n⭐ ರಫ್ತು","Totapuri":"ತೋತಾಪುರಿ\n⭐ ಸಂಸ್ಕರಣ","Neelam":"ನೀಲಂ\n⭐ ಮಂಡಿ","Rasalu":"ರಸಾಲು\n⭐ ಉಪ್ಪಿನಕಾಯಿ"},
},
}

# ─── Village/Mandal translations ───
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
 "ALIMILI":"अलिमिलि","BHYRAVARAM":"भैरवारम","BALAYAPALLI":"बालयपल्ली","AGARALA":"अगराला",
 "RENIGUNTA":"रेनिगुंटा","KARAKAMBADI":"काराकंबाडि","AVILALA":"अविलाला","TIRUCHANUR":"तिरुचानूर",
 "THUMMALAGUNTA":"थुम्मलगुंटा","MANGALAM":"मंगलम","RANADHEERPURAM":"राणाधीरपुरम"},
"ta":{"TIRUPATI (RURAL)":"திருப்பதி (கிராமம்)","CHANDRAGIRI":"சந்திரகிரி","PAKALA":"பாக்கல",
 "SRIKALAHASTHI":"ஸ்ரீகாளஹஸ்தி","RENIGUNTA":"ரேணிகுண்டா","SULLURPET":"சுல்லூர்பேட்",
 "VENKATAGIRI":"வெங்கடகிரி","PUTTUR":"புத்தூர்","SATYAVEDU":"சத்யவேடு",
 "TIRUPATI (URBAN)":"திருப்பதி (நகரம்)","NAIDUPET":"நாயுடுபேட்","NAGALAPURAM":"நாகலாபுரம்"},
"gu":{"TIRUPATI (RURAL)":"તિરુપતિ (ગ્રામ)","CHANDRAGIRI":"ચંદ્રગિરિ","PAKALA":"પાકાલ",
 "SRIKALAHASTHI":"શ્રીકાળહસ્તી","RENIGUNTA":"રેણિગુંટા","SULLURPET":"સુળ્ળૂરપેટ",
 "VENKATAGIRI":"વેંકટગિરિ","PUTTUR":"પુત્તૂર","TIRUPATI (URBAN)":"તિરુપતિ (શહેર)"},
"kn":{"TIRUPATI (RURAL)":"ತಿರುಪತಿ (ಗ್ರಾಮ)","CHANDRAGIRI":"ಚಂದ್ರಗಿರಿ","PAKALA":"ಪಾಕಲ",
 "SRIKALAHASTHI":"ಶ್ರೀಕಾಳಹಸ್ತಿ","RENIGUNTA":"ರೇಣಿಗುಂಟ","SULLURPET":"ಸುಳ್ಳೂರ್‌ಪೇಟ",
 "VENKATAGIRI":"ವೆಂಕಟಗಿರಿ","PUTTUR":"ಪುತ್ತೂರು","TIRUPATI (URBAN)":"ತಿರುಪತಿ (ನಗರ)"},
}

MTR = {
"te": {
    "Tirupati APMC (RC Road)":"తిరుపతి APMC (RC రోడ్)","Pakala Main Mango APMC":"పాకల మాంగో APMC",
    "Railway Kodur APMC Yard":"రైల్వే కోడూరు APMC","Puttur Mango Market Yard":"పుత్తూరు మాంగో మార్కెట్",
    "Chandragiri APMC":"చంద్రగిరి APMC","Srikalahasti APMC":"శ్రీకాళహస్తి APMC",
    "Venkatagiri APMC":"వెంకటగిరి APMC","Nagalapuram APMC":"నాగలాపురం APMC",
    "Naidupeta APMC":"నాయుడుపేట APMC","Satyavedu APMC":"సత్యవేడు APMC",
    "Sullurpeta APMC":"సుళ్ళూరుపేట APMC","Bangarupalem":"బంగారుపాలెం",
    "Chittoor":"చిత్తూరు","Punganur":"పుంగనూరు","Pakala":"పాకల","Pileru":"పిలేరు",
    "Madanapalle AMC":"మదనపల్లె AMC","Gurramkonda e-NAM":"గుర్రంకొండ e-NAM",
    "Galiveedu Market Yard":"గాలివీడు మార్కెట్","Jamiya Mango Yard":"జమియా మాంగో యార్డ్",
    "Nimmanapalle Yard":"నిమ్మనపల్లె యార్డ్","Burakayalakota Hub":"బురకాయలకోట",
    "Nandini Private Mandi":"నందిని ప్రైవేట్ మండీ","Chowdepalle Yard":"చౌడేపల్లె యార్డ్",
    "Galla Foods Rayachoti":"గళ్ళ ఫుడ్స్ రాయచోటి","Roshan Fruits India":"రోషన్ ఫ్రూట్స్",
    "Sri Varsha Food Products":"శ్రీ వర్ష ఫుడ్ ప్రొడక్ట్స్","Hayath Foods":"హయాత్ ఫుడ్స్",
    "Grofresh Agrofoods":"గ్రోఫ్రెష్ అగ్రోఫుడ్స్","Srini Food Park":"శ్రీని ఫుడ్ పార్క్",
    "Sree Sannidhi Foods":"శ్రీ సన్నిధి ఫుడ్స్","Ohms Food Products":"ఓమ్స్ ఫుడ్ ప్రొడక్ట్స్",
    "Navya Foods Pvt Ltd":"నవ్య ఫుడ్స్ ప్రై.లి.","Bright Mangoes":"బ్రైట్ మాంగోస్",
    "PLR Foods Pvt Ltd":"PLR ఫుడ్స్ ప్రై.లి.","Vijay Food Processing":"విజయ్ ఫుడ్ ప్రాసెసింగ్",
    "Galla Foods Ltd":"గళ్ళ ఫుడ్స్ లిమిటెడ్","B M Fruits":"B M ఫ్రూట్స్",
    "Paiyur Group Mango Pulp":"పైయూర్ గ్రూప్ మాంగో పల్ప్",
    "Rayachoti Pickles":"రాయచోటి పికల్స్","Tirupati Pickle Works":"తిరుపతి పికల్ వర్క్స్",
    "Padmavathi Pickles":"పద్మావతి పికల్స్","Puttur Pickle Makers":"పుత్తూరు పికల్ మేకర్స్",
    "Srikalahasti Pickle Industries":"శ్రీకాళహస్తి పికల్ ఇండస్ట్రీస్","Pileru Pickle Works":"పిలేరు పికల్ వర్క్స్",
    "Punganur Mango Pickle":"పుంగనూరు మాంగో పికల్","Kalikiri Pickle":"కాళికిరి పికల్",
    "Chittoor Pack Pickle":"చిత్తూరు పికల్","Madanapalle Pickle":"మదనపల్లె పికల్",
    "Rayachoti APMC Export":"రాయచోటి APMC ఎగుమతి","Rajampet APMC":"రాజంపేట APMC",
    "Tirupati APMC Export":"తిరుపతి APMC ఎగుమతి","Renigunta Packhouse":"రేణిగుంట ప్యాక్‌హౌస్",
    "Srikalahasti Cold Room":"శ్రీకాళహస్తి కోల్డ్ రూమ్","Puttur Export Yard":"పుత్తూరు ఎగుమతి యార్డ్",
    "Bangarupalem APMC":"బంగారుపాలెం APMC","Chittoor APMC":"చిత్తూరు APMC",
    "Punganur Market Yard":"పుంగనూరు మార్కెట్ యార్డ్","Pileru Packhouse":"పిలేరు ప్యాక్‌హౌస్",
    "Tirupati APMC Int Export":"తిరుపతి APMC అంతర్జాతీయ","Renigunta Cold Room Export":"రేణిగుంట కోల్డ్ రూమ్",
    "Rayachoti APMC Int":"రాయచోటి APMC అంతర్జాతీయ","Rajampet APMC Int":"రాజంపేట APMC అంతర్జాతీయ",
    "Srikalahasti Int Collection":"శ్రీకాళహస్తి అంతర్జాతీయ","Chandragiri Packhouse":"చంద్రగిరి ప్యాక్‌హౌస్",
    "Grofresh Export Pack":"గ్రోఫ్రెష్ ఎగుమతి","Roshan Fruits Export":"రోషన్ ఫ్రూట్స్ ఎగుమతి",
    "Navya Foods Export":"నవ్య ఫుడ్స్ ఎగుమతి","Bright Mangoes Export":"బ్రైట్ మాంగోస్ ఎగుమతి",
},
"hi": {
    "Tirupati APMC (RC Road)":"तिरुपति APMC","Pakala Main Mango APMC":"पाकला मैंगो APMC",
    "Railway Kodur APMC Yard":"रेलवे कोडूर APMC","Puttur Mango Market Yard":"पुत्तूर मैंगो मार्केट",
    "Chandragiri APMC":"चंद्रगिरि APMC","Srikalahasti APMC":"श्रीकालहस्ती APMC",
    "Venkatagiri APMC":"वेंकटगिरि APMC","Nagalapuram APMC":"नागलापुरम APMC",
    "Naidupeta APMC":"नायडुपेट APMC","Satyavedu APMC":"सत्यवेडु APMC",
    "Sullurpeta APMC":"सुल्लूरपेट APMC","Bangarupalem":"बंगारुपालेम",
    "Chittoor":"चित्तूर","Punganur":"पुंगनूर","Pakala":"पाकला","Pileru":"पिलेरु",
    "Madanapalle AMC":"मदनपल्ले AMC","Gurramkonda e-NAM":"गुर्रमकोंडा e-NAM",
    "Galiveedu Market Yard":"गलिवीडु मार्केट","Jamiya Mango Yard":"जमिया मैंगो यार्ड",
    "Galla Foods Rayachoti":"गल्ला फूड्स रायचोटी","Roshan Fruits India":"रोशन फ्रूट्स",
    "Sri Varsha Food Products":"श्री वर्षा फूड","Hayath Foods":"हयात फूड्स",
    "Grofresh Agrofoods":"ग्रोफ्रेश","Srini Food Park":"श्रीनी फूड पार्क",
    "Sree Sannidhi Foods":"श्री सन्निधि फूड्स","Navya Foods Pvt Ltd":"नव्या फूड्स",
    "Bright Mangoes":"ब्राइट मैंगोज","PLR Foods Pvt Ltd":"PLR फूड्स","Vijay Food Processing":"विजय फूड",
    "Galla Foods Ltd":"गल्ला फूड्स","B M Fruits":"B M फ्रूट्स","Paiyur Group Mango Pulp":"पैयूर मैंगो पल्प",
    "Rayachoti Pickles":"रायचोटी अचार","Tirupati Pickle Works":"तिरुपति अचार",
    "Padmavathi Pickles":"पद्मावती अचार","Puttur Pickle Makers":"पुत्तूर अचार",
    "Srikalahasti Pickle Industries":"श्रीकालहस्ती अचार","Pileru Pickle Works":"पिलेरु अचार",
    "Punganur Mango Pickle":"पुंगनूर आम अचार","Kalikiri Pickle":"कालिकिरि अचार",
    "Chittoor Pack Pickle":"चित्तूर अचार","Madanapalle Pickle":"मदनपल्ले अचार",
    "Rayachoti APMC Export":"रायचोटी APMC निर्यात","Rajampet APMC":"राजंपेट APMC",
    "Tirupati APMC Export":"तिरुपति APMC निर्यात","Renigunta Packhouse":"रेनिगुंटा पैकहाउस",
    "Srikalahasti Cold Room":"श्रीकालहस्ती कोल्ड रूम","Puttur Export Yard":"पुत्तूर निर्यात यार्ड",
    "Chittoor APMC":"चित्तूर APMC","Tirupati APMC Int Export":"तिरुपति APMC अंतर्राष्ट्रीय",
    "Renigunta Cold Room Export":"रेनिगुंटा कोल्ड रूम","Srikalahasti Int Collection":"श्रीकाल. अंतर्राष्ट्रीय",
    "Chandragiri Packhouse":"चंद्रगिरि पैकहाउस","Navya Foods Export":"नव्या फूड्स निर्यात",
    "Bright Mangoes Export":"ब्राइट मैंगोज निर्यात",
},
"ta": {
    "Tirupati APMC (RC Road)":"திருப்பதி APMC","Pakala Main Mango APMC":"பாக்கல் APMC",
    "Chandragiri APMC":"சந்திரகிரி APMC","Srikalahasti APMC":"ஸ்ரீகாளஹஸ்தி APMC",
    "Venkatagiri APMC":"வெங்கடகிரி APMC","Sullurpeta APMC":"சுல்லூர்பேட் APMC",
    "Galla Foods Rayachoti":"கல்லா ஃபுட்ஸ்","Srini Food Park":"ஸ்ரீனி ஃபுட் பார்க்",
    "PLR Foods Pvt Ltd":"PLR ஃபுட்ஸ்","Vijay Food Processing":"விஜய் ஃபுட்",
    "Rayachoti Pickles":"ராயசோட்டி ஊறுகாய்","Tirupati Pickle Works":"திருப்பதி ஊறுகாய்",
    "Padmavathi Pickles":"பத்மாவதி ஊறுகாய்","Tirupati APMC Export":"திருப்பதி APMC ஏற்றுமதி",
    "Renigunta Packhouse":"ரேணிகுண்டா பேக்ஹவுஸ்","Tirupati APMC Int Export":"திருப்பதி APMC சர்வதேச",
    "Chandragiri Packhouse":"சந்திரகிரி பேக்ஹவுஸ்",
},
"gu": {
    "Tirupati APMC (RC Road)":"તિરુપતિ APMC","Chandragiri APMC":"ચંદ્રગિરિ APMC",
    "Srikalahasti APMC":"શ્રીકાળહસ્તી APMC","Srini Food Park":"શ્રીની ફૂડ પાર્ક",
    "PLR Foods Pvt Ltd":"PLR ફૂડ્સ","Rayachoti Pickles":"રાયચોટી અથાણું",
    "Tirupati Pickle Works":"તિરુપતિ અથાણું","Tirupati APMC Export":"તિરુપતિ APMC નિકાસ",
    "Tirupati APMC Int Export":"તિરુ. APMC આંતરરાષ્ટ્રીય",
},
"kn": {
    "Tirupati APMC (RC Road)":"ತಿರುಪತಿ APMC","Chandragiri APMC":"ಚಂದ್ರಗಿರಿ APMC",
    "Srikalahasti APMC":"ಶ್ರೀಕಾಳಹಸ್ತಿ APMC","Srini Food Park":"ಶ್ರೀನಿ ಫುಡ್ ಪಾರ್ಕ್",
    "PLR Foods Pvt Ltd":"PLR ಫುಡ್ಸ್","Rayachoti Pickles":"ರಾಯಚೋಟಿ ಉಪ್ಪಿನಕಾಯಿ",
    "Tirupati Pickle Works":"ತಿರುಪತಿ ಉಪ್ಪಿನಕಾಯಿ","Tirupati APMC Export":"ತಿರುಪತಿ APMC ರಫ್ತು",
    "Tirupati APMC Int Export":"ತಿರು. APMC ಅಂತರ್ರಾಷ್ಟ್ರೀಯ","Chandragiri Packhouse":"ಚಂದ್ರಗಿರಿ ಪ್ಯಾಕ್‌ಹೌಸ್",
},
}

CTR={
"te":{"Mandi":"మండీ","Processing":"ప్రాసెసింగ్","Pulp":"పల్ప్","Pickle":"ఊరగాయ","Local Export":"స్థానిక ఎగుమతి","Abroad Export":"విదేశీ ఎగుమతి"},
"hi":{"Mandi":"मंडी","Processing":"प्रसंस्करण","Pulp":"पल्प","Pickle":"अचार","Local Export":"स्थानीय निर्यात","Abroad Export":"विदेश निर्यात"},
"ta":{"Mandi":"மண்டி","Processing":"பதப்படுத்தல்","Pulp":"பழச்சாறு","Pickle":"ஊறுகாய்","Local Export":"உள்நாட்டு ஏற்றுமதி","Abroad Export":"வெளிநாட்டு ஏற்றுமதி"},
"gu":{"Mandi":"મંડી","Processing":"પ્રૉસેસિંગ","Pulp":"પલ્પ","Pickle":"અથાણું","Local Export":"સ્થાનિક નિકાસ","Abroad Export":"વિદેશ નિકાસ"},
"kn":{"Mandi":"ಮಂಡಿ","Processing":"ಸಂಸ್ಕರಣ","Pulp":"ಪಲ್ಪ್","Pickle":"ಉಪ್ಪಿನಕಾಯಿ","Local Export":"ಸ್ಥಳೀಯ ರಫ್ತು","Abroad Export":"ವಿದೇಶ ರಫ್ತು"},
"en":{"Mandi":"Mandi","Processing":"Processing","Pulp":"Pulp","Pickle":"Pickle","Local Export":"Local Export","Abroad Export":"Abroad Export"},
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
{"place":"Tirupati APMC (RC Road)","lat":13.6231,"lon":79.4125,"today":36,"yesterday":31},
{"place":"Pakala Main Mango APMC","lat":13.4568,"lon":79.1174,"today":34,"yesterday":30},
{"place":"Railway Kodur APMC Yard","lat":13.9515,"lon":79.3514,"today":28,"yesterday":33},
{"place":"Puttur Mango Market Yard","lat":13.4428,"lon":79.5531,"today":45,"yesterday":41},
{"place":"Chandragiri APMC","lat":13.5828,"lon":79.3142,"today":32,"yesterday":28},
{"place":"Srikalahasti APMC","lat":13.7498,"lon":79.7034,"today":38,"yesterday":35},
{"place":"Venkatagiri APMC","lat":13.9575,"lon":79.5847,"today":29,"yesterday":33},
{"place":"Nagalapuram APMC","lat":13.3985,"lon":79.7915,"today":31,"yesterday":27},
{"place":"Naidupeta APMC","lat":13.9142,"lon":79.8944,"today":27,"yesterday":31},
{"place":"Satyavedu APMC","lat":13.5076,"lon":79.9715,"today":33,"yesterday":29},
{"place":"Sullurpeta APMC","lat":13.7008,"lon":80.0211,"today":30,"yesterday":25},
{"place":"Bangarupalem","lat":13.2,"lon":78.9333,"today":42,"yesterday":38},
{"place":"Chittoor","lat":13.2172,"lon":79.1003,"today":37,"yesterday":41},
{"place":"Punganur","lat":13.3667,"lon":78.5667,"today":40,"yesterday":35},
{"place":"Pakala","lat":13.4667,"lon":79.1167,"today":39,"yesterday":43},
{"place":"Pileru","lat":13.65,"lon":78.95,"today":43,"yesterday":38},
{"place":"Madanapalle AMC","lat":13.6114,"lon":78.4716,"today":38,"yesterday":34},
{"place":"Gurramkonda e-NAM","lat":13.782,"lon":78.584,"today":44,"yesterday":48},
{"place":"Galiveedu Market Yard","lat":14.1035,"lon":78.5142,"today":41,"yesterday":37},
{"place":"Jamiya Mango Yard","lat":14.0562,"lon":78.751,"today":46,"yesterday":42},
{"place":"Nimmanapalle Yard","lat":13.5932,"lon":78.6011,"today":35,"yesterday":40},
{"place":"Burakayalakota Hub","lat":13.801,"lon":78.354,"today":47,"yesterday":43},
{"place":"Nandini Private Mandi","lat":13.5824,"lon":78.5025,"today":33,"yesterday":38},
{"place":"Chowdepalle Yard","lat":13.4116,"lon":78.6148,"today":42,"yesterday":38},
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

# ── SESSION STATE ──
for k,v in [("lang","en"),("logged_in",False),("username",""),("full_name",""),
             ("auth_mode","login"),("variety","Banganapalli"),("results",None)]:
    if k not in st.session_state: st.session_state[k]=v

lang=st.session_state.lang; tr=T[lang]

# ── LANGUAGE BAR ──
def lang_bar():
    lang_opts = [
        ("en", "🇬🇧 English"),
        ("te", "🌿 తెలుగు"),
        ("hi", "🇮🇳 हिंदी"),
        ("ta", "🌺 தமிழ்"),
        ("gu", "🦁 ગુજરાતી"),
        ("kn", "🐘 ಕನ್ನಡ"),
    ]
    tr_cur = T[st.session_state.lang]
    if st.session_state.logged_in:
        cols = st.columns([1.2,1.2,1.2,1.2,1.2,1.2,2.5,1.2])
    else:
        cols = st.columns([1.2,1.2,1.2,1.2,1.2,1.2,4])
    for i,(lc,lbl) in enumerate(lang_opts):
        with cols[i]:
            active = st.session_state.lang == lc
            if st.button(lbl, key=f"lang_{lc}", use_container_width=True,
                         type="primary" if active else "secondary"):
                st.session_state.lang=lc; st.rerun()
    if st.session_state.logged_in:
        with cols[7]:
            if st.button(tr_cur["logout"], use_container_width=True, type="secondary"):
                st.session_state.logged_in=False; st.session_state.results=None; st.rerun()

# ── AUTH SCREEN ──
if not st.session_state.logged_in:
    lang_bar()
    tr=T[st.session_state.lang]
    st.markdown(f"""<div class="hero-banner">
      <div class="hero-deco"><span>🥭</span><span>🌿</span><span>🌾</span></div>
      <div style="margin-bottom:14px">
        <span class="fm1">🥭</span>&nbsp;
        <span class="fm2">🌿</span>&nbsp;
        <span class="fm1" style="animation-delay:.6s">🌾</span>&nbsp;
        <span class="fm2" style="animation-delay:1s">💛</span>&nbsp;
        <span class="fm1" style="animation-delay:1.4s">🥭</span>
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
                un=st.text_input(tr["username"],placeholder=tr["name_ph"])
                pw=st.text_input(tr["password"],type="password",placeholder="••••••")
                if st.form_submit_button(tr["login_btn"],use_container_width=True,type="primary"):
                    if not un or not pw: st.error(tr["err_fill"])
                    else:
                        ok,msg=login_user(un,pw)
                        if ok:
                            st.session_state.logged_in=True; st.session_state.username=un
                            st.session_state.full_name=msg; st.success(f"🥭 {tr['namaste']} {msg}!"); st.rerun()
                        else: st.error(f"❌ {msg}")
            st.markdown("</div>",unsafe_allow_html=True)
            if st.button(f"📝 {tr['no_account']}",use_container_width=True):
                st.session_state.auth_mode="register"; st.rerun()
        else:
            st.markdown(f'<div class="auth-card"><div class="auth-title">{tr["reg_title"]}</div>',unsafe_allow_html=True)
            with st.form("rf"):
                fn=st.text_input(tr["full_name"],placeholder=tr["name_ph"])
                un=st.text_input(tr["username"],placeholder="username")
                ph=st.text_input(tr["phone"],placeholder="9XXXXXXXXX")
                pw=st.text_input(tr["password"],type="password",placeholder="••••••")
                pw2=st.text_input(tr["password"]+" ✓",type="password",placeholder="••••••")
                if st.form_submit_button(tr["reg_btn"],use_container_width=True,type="primary"):
                    if not fn or not un or not pw: st.error(tr["err_fill"])
                    elif pw!=pw2: st.error(tr["err_pw_match"])
                    elif len(pw)<6: st.error(tr["err_pw_len"])
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
lang=st.session_state.lang; tr=T[lang]

st.markdown(f"""<div class="hero-banner">
  <div class="hero-deco"><span>🥭</span><span>🌿</span><span>🌾</span></div>
  <div style="margin-bottom:14px">
    <span class="fm1">🥭</span>&nbsp;
    <span class="fm2">🌿</span>&nbsp;
    <span class="fm1" style="animation-delay:.6s">🌾</span>&nbsp;
    <span class="fm2" style="animation-delay:1s">💛</span>&nbsp;
    <span class="fm1" style="animation-delay:1.4s">🥭</span>
  </div>
  <h1 class="hero-title">{tr["title"]}</h1>
  <p class="hero-sub">{tr["subtitle"]}</p>
</div>""", unsafe_allow_html=True)

# PRICE TICKER — translated place names
thtml=""
for p in PRICES:
    d=p["today"]-p["yesterday"]; ar="▲" if d>=0 else "▼"; cl="ticker-up" if d>=0 else "ticker-down"
    pname = tm(p["place"], lang)
    thtml+=f'<span class="ticker-item"><span class="ticker-place">{pname}</span> <span class="ticker-price">₹{p["today"]}/kg</span> <span class="{cl}">{ar}{abs(d)}</span></span>'
dbl=thtml+thtml
st.markdown(f'''<div class="ticker-wrap"><div class="ticker-label-fixed">📈 {tr["ticker_label"]}</div><div style="padding-left:160px"><div class="ticker-inner">{dbl}</div></div></div>''',unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown(f"### 👋 {tr['namaste']}, **{st.session_state.full_name}**! 🥭")
    st.markdown("---")
    farmer_name=st.text_input(tr["lname"],value=st.session_state.full_name,placeholder=tr["name_ph"])

    # Mandal selector - fully translated
    mandals=sorted(set(v["Mandal"] for v in VILLAGES))
    mdmap={tv(m,lang):m for m in mandals}
    selmd=st.selectbox("📍 "+ tr["mandal_ph"],["— "+tr["mandal_ph"]+" —"]+sorted(mdmap.keys()))

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
    vcols = st.columns(2)
    for i,(v,_,_) in enumerate([("Banganapalli","banga","🥭"),("Totapuri","tota","🟣"),("Neelam","neel","🔵"),("Rasalu","rasa","🔴")]):
        lbl_raw = tr["var_labels"][v]
        with vcols[i%2]:
            selected = v == st.session_state.variety
            if st.button(lbl_raw, key=f"v_{v}", use_container_width=True,
                        type="primary" if selected else "secondary"):
                st.session_state.variety = v; st.rerun()

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
    if not village_val: st.error(tr["err_village"])
    else:
        vr=next((v for v in VILLAGES if v["GP"]==village_val),None)
        if vr:
            bp=get_base_price(vr["Lat"],vr["Lon"])
            with st.spinner(tr["analyzing"]): top10=compute_top10(vr["Lat"],vr["Lon"],bp,qty,st.session_state.variety)
            if top10:
                st.session_state.results={"data":top10,"farmer_name":farmer_name or st.session_state.full_name,
                    "village":village_val,"base_price":bp,"qty":qty,
                    "v_lat":vr["Lat"],"v_lon":vr["Lon"],"variety":st.session_state.variety}
            else: st.warning(tr["err_no_results"])

if st.session_state.results:
    R=st.session_state.results; top10=R["data"]; best=top10[0]; vd=tv(R["village"],lang)

    st.markdown(f'''<div class="namaste-bar">
      🥭 {tr["namaste"]}, <span style="color:#a7f3d0;margin:0 6px;font-size:17px">{R["farmer_name"]}</span>
      &nbsp;|&nbsp; 🏘️ {vd}
      &nbsp;|&nbsp; 🥭 {R["variety"]}
      &nbsp;|&nbsp; 📦 {R["qty"]} {tr["qty_label"]}
    </div>''',unsafe_allow_html=True)

    m1,m2,m3,m4=st.columns(4)
    for delay,col,content in [
        ("0.1s",m1,f'<div class="lbl">📈 {tr["base_price"]}</div><div class="val">₹{R["base_price"]}/kg</div><div class="sub">{vd}</div>'),
        ("0.2s",m2,f'<div class="lbl">📦 {tr["lqty"]}</div><div class="val">{R["qty"]} {tr["qty_label"]}</div><div class="sub">{R["qty"]*100} kg</div>'),
        ("0.3s",m3,f'<div class="lbl">🏆 {tr["best_profit"]}</div><div class="val">₹{best["NetProfit"]:,}</div><div class="sub">{tm(best["Name"],lang)[:26]}</div>'),
        ("0.4s",m4,f'<div class="lbl">🎯 {tr["best_market"]}</div><div class="val" style="font-size:16px;line-height:1.3">{tm(best["Name"],lang)[:22]}</div><div class="sub">{best["Distance_km"]} km · {tc(best["Category"],lang)}</div>'),
    ]:
        with col:
            cls = "best" if delay=="0.3s" else ""
            st.markdown(f'<div class="metric-card {cls}" style="animation-delay:{delay}">{content}</div>',unsafe_allow_html=True)

    st.markdown("<hr class='section-divider'>",unsafe_allow_html=True)

    # ── VOICE BUTTON — speaks in selected language ──
    lang_voice_map = {"en":"en-IN","te":"te-IN","hi":"hi-IN","ta":"ta-IN","gu":"gu-IN","kn":"kn-IN"}
    voice_lang = lang_voice_map.get(lang, "en-IN")

    voice_templates = {
        "en": {
            "greeting": f"Namaste {R['farmer_name']}. Here are your top 3 market options for {R['variety']} mangoes.",
            "item": lambda i,r: f"Option {i+1}: {r['Name']}, {r['Category']}, {r['Distance_km']} kilometres away. Net profit: {r['NetProfit']:,} rupees.",
        },
        "te": {
            "greeting": f"నమస్తే {R['farmer_name']}. {R['variety']} మామిడికి మీ టాప్ 3 మార్కెట్ ఎంపికలు.",
            "item": lambda i,r: f"{['మొదటి','రెండవ','మూడవ'][i]} ఎంపిక: {tm(r['Name'],'te')}, {tc(r['Category'],'te')}, {r['Distance_km']} కిలోమీటర్లు. నికర లాభం: {r['NetProfit']:,} రూపాయలు.",
        },
        "hi": {
            "greeting": f"नमस्ते {R['farmer_name']}। {R['variety']} आम के लिए आपके शीर्ष 3 बाजार विकल्प।",
            "item": lambda i,r: f"{['पहला','दूसरा','तीसरा'][i]} विकल्प: {tm(r['Name'],'hi')}, {tc(r['Category'],'hi')}, {r['Distance_km']} किलोमीटर दूर। शुद्ध लाभ: {r['NetProfit']:,} रुपये।",
        },
        "ta": {
            "greeting": f"வணக்கம் {R['farmer_name']}. {R['variety']} மாம்பழத்திற்கான உங்கள் சிறந்த 3 சந்தைகள்.",
            "item": lambda i,r: f"{['முதல்','இரண்டாம்','மூன்றாம்'][i]} தேர்வு: {tm(r['Name'],'ta')}, {tc(r['Category'],'ta')}, {r['Distance_km']} கிலோமீட்டர். நிகர லாபம்: {r['NetProfit']:,} ரூபாய்.",
        },
        "gu": {
            "greeting": f"નમસ્તે {R['farmer_name']}. {R['variety']} કેરી માટે તમારા ટોપ ૩ બજાર વિકલ્પો.",
            "item": lambda i,r: f"{['પ્રથમ','બીજો','ત્રીજો'][i]} વિકલ્પ: {tm(r['Name'],'gu')}, {tc(r['Category'],'gu')}, {r['Distance_km']} કિલોમીટર. ચોખ્ખો નફો: {r['NetProfit']:,} રૂપિયા.",
        },
        "kn": {
            "greeting": f"ನಮಸ್ಕಾರ {R['farmer_name']}. {R['variety']} ಮಾವಿನ ಅಗ್ರ 3 ಮಾರುಕಟ್ಟೆಗಳು.",
            "item": lambda i,r: f"{['ಮೊದಲ','ಎರಡನೇ','ಮೂರನೇ'][i]} ಆಯ್ಕೆ: {tm(r['Name'],'kn')}, {tc(r['Category'],'kn')}, {r['Distance_km']} ಕಿಲೋಮೀಟರ್. ನಿವ್ವಳ ಲಾಭ: {r['NetProfit']:,} ರೂಪಾಯಿ.",
        },
    }
    vt = voice_templates.get(lang, voice_templates["en"])
    parts = [vt["greeting"]]
    for i, r in enumerate(top10[:3]):
        parts.append(vt["item"](i, r))
    safe_text = " ".join(parts).replace("'","").replace('"',"").replace("\\","").replace("\n"," ")
    vbtn_label = tr["voice_btn"].replace("🔊 ","")
    vstop_label = tr["voice_stop"].replace("⏹ ","")

    # Split text into sentences for chunked Google TTS (max 200 chars per chunk)
    def split_chunks(text, maxlen=180):
        sentences = re.split(r'(?<=[।.।!?])\s+', text)
        chunks, cur = [], ""
        for s in sentences:
            if len(cur) + len(s) + 1 <= maxlen:
                cur = (cur + " " + s).strip()
            else:
                if cur: chunks.append(cur)
                cur = s[:maxlen]
        if cur: chunks.append(cur)
        return chunks

    # Google Translate TTS — works for all Indian languages, high quality
    gtts_lang_map = {"te":"te","ta":"ta","kn":"kn","gu":"gu","hi":"hi","en":"en"}
    gtts_lang = gtts_lang_map.get(lang, "en")

    # For regional langs without reliable browser TTS, use Google TTS audio approach
    # We pass chunks as JS array and play them sequentially via Audio objects
    use_gtts = lang in ["te","ta","kn","gu"]  # these lack browser voices

    chunks = split_chunks(safe_text)
    chunks_js = json.dumps(chunks)

    voice_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;900&family=Noto+Sans+Telugu:wght@700&family=Noto+Sans+Devanagari:wght@700&family=Noto+Sans+Tamil:wght@700&family=Noto+Sans+Gujarati:wght@700&family=Noto+Sans+Kannada:wght@700&display=swap" rel="stylesheet">
<style>
body{{margin:0;padding:4px 0;background:transparent;}}
.vfab{{
    display:inline-flex;align-items:center;gap:10px;
    background:linear-gradient(135deg,#2d1a00,#6b3a00);
    border:2px solid rgba(255,165,0,0.7);border-radius:50px;
    padding:14px 30px;color:#ffd166;font-weight:900;font-size:15px;
    cursor:pointer;letter-spacing:.3px;
    font-family:'Baloo 2','Noto Sans Telugu','Noto Sans Devanagari','Noto Sans Tamil','Noto Sans Gujarati','Noto Sans Kannada',sans-serif;
    box-shadow:0 6px 24px rgba(0,0,0,.5);transition:all .25s;
    animation:spk 2.5s ease-in-out infinite;
}}
.vfab:hover{{transform:translateY(-3px);box-shadow:0 12px 32px rgba(255,165,0,.5);}}
.vfab.on{{background:linear-gradient(135deg,#6b1010,#9e1c1c);border-color:rgba(231,76,60,.7);color:#ffd0d0;animation:none;}}
.status{{font-size:11px;color:#74c89b;margin-top:4px;display:none;font-family:inherit;}}
.wb{{display:inline-block;width:4px;border-radius:3px;background:currentColor;margin:0 2px;vertical-align:middle;height:4px;animation:wba .55s ease-in-out infinite;}}
.wb:nth-child(2){{animation-delay:.11s}}.wb:nth-child(3){{animation-delay:.22s}}.wb:nth-child(4){{animation-delay:.33s}}
@keyframes wba{{0%,100%{{height:3px}}50%{{height:16px}}}}
@keyframes spk{{0%,100%{{box-shadow:0 6px 24px rgba(0,0,0,.5),0 0 0 0 rgba(255,165,0,.5)}}50%{{box-shadow:0 6px 24px rgba(0,0,0,.5),0 0 0 12px rgba(255,165,0,0)}}}}
</style></head>
<body>
<button class="vfab" id="btn" onclick="toggle()">
  🔊 <span id="lbl">{vbtn_label}</span>
  <span id="bars" style="display:none">
    <span class="wb"></span><span class="wb"></span><span class="wb"></span><span class="wb"></span>
  </span>
</button>
<div class="status" id="status"></div>
<script>
var speaking = false;
var synth = window.speechSynthesis;
var fullText = `{safe_text}`;
var chunks = {chunks_js};
var voiceLang = "{voice_lang}";
var gttsLang = "{gtts_lang}";
var useGtts = {str(use_gtts).lower()};
var btnLabel = "{vbtn_label}";
var stopLabel = "{vstop_label}";
var audioQueue = [];
var currentAudio = null;
var chunkIdx = 0;

function setOn() {{
    speaking = true;
    document.getElementById('btn').classList.add('on');
    document.getElementById('bars').style.display = 'inline';
    document.getElementById('lbl').textContent = stopLabel;
}}
function setOff() {{
    speaking = false;
    document.getElementById('btn').classList.remove('on');
    document.getElementById('bars').style.display = 'none';
    document.getElementById('lbl').textContent = btnLabel;
    chunkIdx = 0;
    currentAudio = null;
}}

// ── STRATEGY 1: Google Translate TTS (for Telugu, Tamil, Kannada, Gujarati) ──
// Plays each sentence chunk as audio sequentially for natural-sounding speech
function playGttsSentence(idx) {{
    if (!speaking || idx >= chunks.length) {{ setOff(); return; }}
    var txt = chunks[idx];
    var url = 'https://translate.google.com/translate_tts?ie=UTF-8&tl=' + gttsLang +
              '&client=tw-ob&q=' + encodeURIComponent(txt);
    var audio = new Audio(url);
    audio.volume = 1.0;
    currentAudio = audio;
    audio.onended = function() {{ if (speaking) playGttsSentence(idx + 1); }};
    audio.onerror = function() {{
        // Google TTS blocked/failed — fallback to Web Speech for this chunk
        speakWithBrowser(chunks.slice(idx).join(' '));
    }};
    audio.play().catch(function() {{
        // Autoplay blocked — try Web Speech fallback
        speakWithBrowser(chunks.slice(idx).join(' '));
    }});
}}

// ── STRATEGY 2: Web Speech API (primary for Hindi/English, fallback for others) ──
function speakWithBrowser(text) {{
    var u = new SpeechSynthesisUtterance(text);
    u.lang = voiceLang;
    u.rate = 0.82;
    u.pitch = 1.0;
    u.volume = 1.0;
    var voices = synth.getVoices();
    // Try exact match → partial match → any Indian English voice → default
    var matched = voices.filter(v => v.lang === voiceLang);
    if (!matched.length) matched = voices.filter(v => v.lang.startsWith(voiceLang.split('-')[0]));
    if (!matched.length && voiceLang !== 'en-IN') {{
        matched = voices.filter(v => v.lang === 'en-IN' || v.lang === 'hi-IN');
    }}
    if (matched.length) u.voice = matched[0];
    u.onstart = function() {{ setOn(); }};
    u.onend = function() {{ setOff(); }};
    u.onerror = function() {{ setOff(); }};
    synth.speak(u);
}}

function toggle() {{
    if (speaking) {{
        // Stop everything
        if (currentAudio) {{ currentAudio.pause(); currentAudio = null; }}
        synth.cancel();
        setOff();
        return;
    }}
    setOn();
    if (useGtts) {{
        // Use Google TTS for regional languages — much better quality
        playGttsSentence(0);
    }} else {{
        // Use browser Web Speech for Hindi and English
        if (synth.getVoices().length === 0) {{
            synth.onvoiceschanged = function() {{ synth.onvoiceschanged = null; speakWithBrowser(fullText); }};
        }} else {{
            speakWithBrowser(fullText);
        }}
    }}
}}
if (synth && synth.getVoices) synth.getVoices();
</script>
</body></html>"""

    components.html(voice_html, height=72, scrolling=False)
    st.markdown("<br>", unsafe_allow_html=True)

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
                  <div class="podium-rank">{medal_labels[i]}</div>
                  <div class="podium-name">{translated_name}</div>
                  <div class="podium-profit">₹{r["NetProfit"]:,}</div>
                  <div class="podium-detail">{tr["dist"]}: {r["Distance_km"]} km</div>
                  <div class="podium-detail">{tr["rev"]}: ₹{r["Revenue"]:,}</div>
                  <div class="podium-detail">{tr["trans"]}: ₹{r["Transport"]:,}</div>
                  <span class="podium-cat">{cat_translated}</span>
                </div>''', unsafe_allow_html=True)

        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown(f"#### {tr['top3_breakdown']}")
        top3 = top10[:3]
        names3 = [tm(r["Name"],lang)[:22] for r in top3]
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            name=tr["profit"], x=names3, y=[r["NetProfit"] for r in top3],
            marker_color=["#FFD700","#C0C0C0","#CD7F32"],
            text=[f"₹{r['NetProfit']:,}" for r in top3], textposition="auto",
            textfont=dict(color="black", size=13),
        ))
        fig3.add_trace(go.Bar(
            name=tr["trans"], x=names3, y=[r["Transport"] for r in top3],
            marker_color=["rgba(255,150,50,0.6)","rgba(180,180,180,0.6)","rgba(160,100,50,0.6)"],
            text=[f"₹{r['Transport']:,}" for r in top3], textposition="auto",
        ))
        fig3.update_layout(
            barmode="group", height=320,
            plot_bgcolor="rgba(6,18,9,0.85)", paper_bgcolor="rgba(0,0,0,0)",
            yaxis_title="₹",
            font=dict(color="#ffd166"),
            xaxis=dict(gridcolor="rgba(255,165,0,0.1)"),
            yaxis=dict(gridcolor="rgba(255,165,0,0.1)"),
            legend=dict(orientation="h",y=1.08,bgcolor="rgba(0,0,0,0)",font=dict(color="#ffd166")),
            margin=dict(l=10,r=10,t=40,b=10)
        )
        st.plotly_chart(fig3, use_container_width=True)

    # ── TAB 2: ALL OPTIONS ──
    with tab2:
        mp=best["NetProfit"]; rows_html=""
        for i,r in enumerate(top10):
            pct=int(r["NetProfit"]/mp*100) if mp>0 else 0
            medal="🥇" if i==0 else "🥈" if i==1 else "🥉" if i==2 else f"#{i+1}"
            rc="r1" if i==0 else "r2" if i==1 else "r3" if i==2 else "rn"
            ck=r["Category"].replace(" ","")
            ct=tc(r["Category"],lang)
            translated_name = tm(r["Name"],lang)
            bar=f'<div class="profit-bar-wrap"><div class="profit-bar-bg"><div class="profit-bar-fill" style="width:{pct}%"></div></div><span style="font-size:11px;color:#ffa500">{pct}%</span></div>'
            rows_html+=f'<tr><td><span class="rank-badge {rc}">{medal}</span></td><td><b style="color:#ffd166">{translated_name}</b></td><td><span class="cat-tag {ck}">{ct}</span></td><td style="color:#74c89b">{r["Distance_km"]} km</td><td style="color:#a7f3d0">₹{r["Revenue"]:,}</td><td style="color:#ff9a4a">₹{r["Transport"]:,}</td><td><b style="color:#ffd166;font-size:15px">₹{r["NetProfit"]:,}</b></td><td>{bar}</td></tr>'
        st.markdown(f'''<div class="rt-wrap"><table class="result-table"><thead><tr><th>{tr["rank"]}</th><th>{tr["market"]}</th><th>{tr["cat"]}</th><th>{tr["dist"]}</th><th>{tr["rev"]}</th><th>{tr["trans"]}</th><th>{tr["profit"]}</th><th>%</th></tr></thead><tbody>{rows_html}</tbody></table></div>''',unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
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
            tr["download_btn"],
            df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig'),
            f"mango_profit_{R['village']}_{R['variety']}_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv", use_container_width=True
        )

    # ── TAB 3: CHARTS ──
    with tab3:
        ca,cb=st.columns(2)
        with ca:
            st.markdown(f"#### {tr['chart_title']}")
            names=[tm(r["Name"],lang)[:20] for r in top10]
            fig=go.Figure()
            fig.add_trace(go.Bar(name=tr["profit"],y=names,x=[r["NetProfit"] for r in top10],orientation="h",
                marker=dict(color=ROUTE_COLORS[:len(top10)]),
                text=[f"₹{r['NetProfit']:,}" for r in top10],textposition="auto"))
            fig.add_trace(go.Bar(name=tr["trans"],y=names,x=[r["Transport"] for r in top10],orientation="h",
                marker_color="rgba(255,165,0,0.4)",
                text=[f"₹{r['Transport']:,}" for r in top10],textposition="auto"))
            fig.update_layout(
                barmode="group",height=440,
                plot_bgcolor="rgba(6,18,9,0.85)",paper_bgcolor="rgba(0,0,0,0)",
                xaxis_title="₹",
                font=dict(color="#ffd166"),
                xaxis=dict(gridcolor="rgba(255,165,0,0.1)"),
                yaxis=dict(gridcolor="rgba(255,165,0,0.1)"),
                legend=dict(orientation="h",y=1.08,bgcolor="rgba(0,0,0,0)"),
                margin=dict(l=10,r=10,t=40,b=10)
            )
            st.plotly_chart(fig,use_container_width=True)
        with cb:
            st.markdown(f"#### {tr['pie_title']}")
            cs={}
            for r in top10: k=tc(r["Category"],lang); cs[k]=cs.get(k,0)+r["NetProfit"]
            fp=px.pie(names=list(cs.keys()),values=list(cs.values()),
                color_discrete_sequence=["#ffd166","#52b788","#e74c3c","#3498db","#9b59b6","#ff8c00"],hole=0.45)
            fp.update_traces(textposition="inside",textinfo="percent+label",
                marker=dict(line=dict(color="rgba(0,0,0,0.5)",width=2)))
            fp.update_layout(
                height=440,font=dict(color="#ffd166"),
                paper_bgcolor="rgba(0,0,0,0)",showlegend=True,
                legend=dict(orientation="h",y=-0.15,bgcolor="rgba(0,0,0,0)"),
                margin=dict(l=10,r=10,t=10,b=10)
            )
            st.plotly_chart(fp,use_container_width=True)

        st.markdown("---")
        st.markdown(f"#### {tr['prices_title']}")
        np2=sorted(PRICES,key=lambda p:hav(R["v_lat"],R["v_lon"],p["lat"],p["lon"]))[:12]
        fp2=go.Figure()
        fp2.add_trace(go.Bar(name=tr["today_price"],x=[tm(p["place"],lang)[:18] for p in np2],y=[p["today"] for p in np2],
            marker_color=["#52b788" if p["today"]>=p["yesterday"] else "#e74c3c" for p in np2],
            text=[f"₹{p['today']}" for p in np2],textposition="auto"))
        fp2.add_trace(go.Bar(name=tr["yesterday_price"],x=[tm(p["place"],lang)[:18] for p in np2],y=[p["yesterday"] for p in np2],
            marker_color="rgba(120,120,120,0.5)",text=[f"₹{p['yesterday']}" for p in np2],textposition="auto"))
        fp2.update_layout(
            barmode="group",height=380,
            plot_bgcolor="rgba(6,18,9,0.85)",paper_bgcolor="rgba(0,0,0,0)",
            yaxis_title="₹/kg",xaxis_tickangle=-45,
            font=dict(color="#ffd166"),
            xaxis=dict(gridcolor="rgba(255,165,0,0.1)"),
            yaxis=dict(gridcolor="rgba(255,165,0,0.1)"),
            legend=dict(orientation="h",y=1.08,bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=10,r=10,t=40,b=90)
        )
        st.plotly_chart(fp2,use_container_width=True)

    # ── TAB 4: MAP ──
    with tab4:
        st.markdown(f"#### {tr['map_title']}")
        st.caption(tr["map_cap"])

        markers_js = ""
        for i, r in enumerate(top10):
            col = ROUTE_COLORS[i % len(ROUTE_COLORS)]
            medal = "🥇" if i==0 else "🥈" if i==1 else "🥉" if i==2 else f"#{i+1}"
            translated_name = tm(r["Name"], lang)
            cat_t = tc(r["Category"], lang)
            markers_js += f"""{{lat:{r["Lat"]},lon:{r["Lon"]},name:"{translated_name.replace('"','').replace("'","")}", cat:"{cat_t}",profit:"₹{r['NetProfit']:,}",dist:"{r['Distance_km']} km",rev:"₹{r['Revenue']:,}",trans:"₹{r['Transport']:,}",medal:"{medal}",color:"{col}",rank:{i}}},"""

        osm_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  body,html{{margin:0;padding:0;background:#020d05;}}
  #map{{width:100%;height:580px;border-radius:16px;}}
  .legend{{background:rgba(2,13,5,0.94);color:#ffd166;padding:12px 14px;border-radius:12px;border:1px solid rgba(255,165,0,0.3);font-size:12px;max-height:300px;overflow-y:auto;}}
  .legend-item{{display:flex;align-items:center;gap:8px;padding:4px 0;}}
  .legend-dot{{width:12px;height:12px;border-radius:50%;flex-shrink:0;}}
  .info-panel{{background:rgba(2,13,5,0.94);color:#ffd166;padding:10px 14px;border-radius:10px;border:1px solid rgba(255,165,0,0.3);font-size:12px;line-height:1.6;}}
</style></head>
<body>
<div id="map"></div>
<script>
var map = L.map('map',{{zoomControl:true}}).setView([{R["v_lat"]},{R["v_lon"]}],9);
L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{attribution:'© OpenStreetMap',maxZoom:18}}).addTo(map);

var vLat={R["v_lat"]}, vLon={R["v_lon"]};
var villageIcon=L.divIcon({{html:'<div style="background:#ffd166;width:30px;height:30px;border-radius:50%;border:3px solid #ff8c00;display:flex;align-items:center;justify-content:center;font-size:16px;box-shadow:0 3px 12px rgba(255,165,0,0.6)">🏘️</div>',className:'',iconSize:[30,30],iconAnchor:[15,15]}});
L.marker([vLat,vLon],{{icon:villageIcon}}).addTo(map).bindPopup('<b style="color:#ffd166">🏘️ {vd}</b>');

var markets=[{markers_js}];
var rc={ROUTE_COLORS};
async function fetchRoute(f1,f2,t1,t2,color,w,op){{
    try{{
        var r=await fetch('https://router.project-osrm.org/route/v1/driving/'+f2+','+f1+';'+t2+','+t1+'?overview=full&geometries=geojson');
        var d=await r.json();
        if(d.code==='Ok'){{
            var c=d.routes[0].geometry.coordinates.map(c=>[c[1],c[0]]);
            L.polyline(c,{{color:color,weight:w,opacity:op,lineJoin:'round'}}).addTo(map);
            return {{dist:(d.routes[0].distance/1000).toFixed(1),dur:Math.round(d.routes[0].duration/60)}};
        }}
    }}catch(e){{L.polyline([[f1,f2],[t1,t2]],{{color:color,weight:w,opacity:op,dashArray:'6,4'}}).addTo(map);}}
    return null;
}}
async function load(){{
    for(var i=0;i<markets.length;i++){{
        var m=markets[i],color=rc[i%rc.length],w=i===0?5:i<3?3:2,op=i===0?0.95:i<3?0.8:0.55;
        var sz=i<3?32:26;
        var icon=L.divIcon({{html:'<div style="background:'+m.color+';width:'+sz+'px;height:'+sz+'px;border-radius:50%;border:2.5px solid rgba(255,255,255,0.8);display:flex;align-items:center;justify-content:center;font-size:'+(i<3?14:11)+'px;box-shadow:0 3px 12px rgba(0,0,0,0.6);font-weight:900;color:white">'+m.medal+'</div>',className:'',iconSize:[sz,sz],iconAnchor:[sz/2,sz/2]}});
        var mk=L.marker([m.lat,m.lon],{{icon:icon}}).addTo(map);
        mk.bindPopup('<div style="background:#061209;color:#ffd166;padding:10px;border-radius:8px;min-width:200px"><b style="color:'+m.color+';font-size:15px">'+m.medal+' '+m.name+'</b><br><span style="color:#52b788;font-size:11px">'+m.cat+'</span><br><hr style="border-color:rgba(255,165,0,0.2);margin:6px 0">💰 <b>'+m.profit+'</b><br>📍 '+m.dist+'<br><span id="rd'+i+'">🛣️ ...</span><br>📈 '+m.rev+'<br>🚛 '+m.trans+'</div>');
        var res=await fetchRoute(vLat,vLon,m.lat,m.lon,color,w,op);
        if(res){{var el=document.getElementById('rd'+i);if(el)el.textContent='🛣️ '+res.dist+' km ('+res.dur+' min)';}}
        if(i<markets.length-1)await new Promise(r=>setTimeout(r,300));
    }}
}}
load();
var legend=L.control({{position:'bottomright'}});
legend.onAdd=function(){{
    var d=L.DomUtil.create('div','legend');
    d.innerHTML='<b style="font-size:11px;text-transform:uppercase;letter-spacing:1px">📍 {tr["market"]}</b><br>';
    markets.forEach(function(m,i){{d.innerHTML+='<div class="legend-item"><div class="legend-dot" style="background:'+m.color+'"></div><span>'+m.medal+' '+m.name.substring(0,22)+'</span></div>';}});
    return d;
}};
legend.addTo(map);
</script></body></html>"""
        components.html(osm_html, height=600, scrolling=False)

    # ── TAB 5: SMART ADVICE ──
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
        st.markdown(f'''<div style="background:linear-gradient(135deg,rgba(30,70,15,0.9),rgba(6,18,9,0.95));border:2px solid rgba(255,165,0,0.35);border-radius:18px;padding:24px;text-align:center;margin-top:22px">
          <div style="font-size:38px;margin-bottom:12px">🌾 &nbsp; 🥭 &nbsp; 💛 &nbsp; 🌿 &nbsp; 🏡 &nbsp; 🚛 &nbsp; 💰</div>
          <p style="color:#ffd166;font-size:14px;margin:0;font-weight:700">{tr["footer"]}</p>
        </div>''',unsafe_allow_html=True)

else:
    # ── WELCOME SCREEN ──
    st.markdown(f"""
    <style>
    @keyframes walk {{
        0%   {{ transform: translateX(-120px) scaleX(1); }}
        45%  {{ transform: translateX(calc(50vw - 80px)) scaleX(1); }}
        50%  {{ transform: translateX(calc(50vw - 80px)) scaleX(-1); }}
        95%  {{ transform: translateX(-120px) scaleX(-1); }}
        100% {{ transform: translateX(-120px) scaleX(1); }}
    }}
    @keyframes sunPulse {{ 0%,100%{{transform:scale(1) rotate(0deg)}} 50%{{transform:scale(1.08) rotate(8deg)}} }}
    @keyframes cloudDrift {{ 0%{{transform:translateX(0)}} 100%{{transform:translateX(60px)}} }}
    @keyframes mangoSwing {{ 0%,100%{{transform:rotate(-8deg)}} 50%{{transform:rotate(8deg)}} }}
    @keyframes groundMove {{ 0%{{background-position:0 0}} 100%{{background-position:-200px 0}} }}
    .farmer-scene {{
        position:relative;width:100%;height:230px;
        background:linear-gradient(180deg,#0a1f08 0%,#0f2e0f 40%,#1a4a12 70%,#0d2e0a 100%);
        border-radius:22px;overflow:hidden;margin-bottom:22px;
        border:2px solid rgba(255,165,0,0.35);
        box-shadow:0 10px 40px rgba(0,0,0,0.6),inset 0 0 60px rgba(255,165,0,0.05);
    }}
    .scene-ground {{
        position:absolute;bottom:0;left:0;right:0;height:55px;
        background:repeating-linear-gradient(90deg,#1e5a10 0,#1e5a10 30px,#186010 30px,#186010 60px);
        animation:groundMove 2s linear infinite;
    }}
    .scene-sun {{ position:absolute;top:18px;right:65px;font-size:44px;animation:sunPulse 3s ease-in-out infinite; }}
    .scene-cloud1 {{ position:absolute;top:22px;left:80px;font-size:30px;opacity:.7;animation:cloudDrift 8s ease-in-out infinite alternate; }}
    .scene-cloud2 {{ position:absolute;top:42px;left:200px;font-size:22px;opacity:.5;animation:cloudDrift 11s ease-in-out infinite alternate-reverse; }}
    .scene-tree1 {{ position:absolute;bottom:50px;right:90px;font-size:56px;animation:mangoSwing 4s ease-in-out infinite;transform-origin:bottom center; }}
    .scene-tree2 {{ position:absolute;bottom:50px;right:185px;font-size:44px;animation:mangoSwing 5s ease-in-out infinite 1s;transform-origin:bottom center; }}
    .scene-tree3 {{ position:absolute;bottom:50px;left:30px;font-size:40px;animation:mangoSwing 4.5s ease-in-out infinite .5s;transform-origin:bottom center; }}
    .scene-farmer {{ position:absolute;bottom:50px;font-size:46px;animation:walk 7s linear infinite; }}
    .scene-mango1 {{ position:absolute;top:55px;left:42%;font-size:24px;animation:mangoSwing 2s ease-in-out infinite; }}
    .scene-mango2 {{ position:absolute;top:70px;right:110px;font-size:18px;animation:mangoSwing 2.5s ease-in-out infinite 0.5s; }}
    .scene-title {{ animation:fadeDown .8s ease both;text-align:center;padding:10px 0 0; }}
    </style>
    <div class="farmer-scene">
        <div class="scene-cloud1">☁️</div>
        <div class="scene-cloud2">⛅</div>
        <div class="scene-sun">☀️</div>
        <div class="scene-tree1">🌳</div>
        <div class="scene-tree2">🌴</div>
        <div class="scene-tree3">🌿</div>
        <div class="scene-mango1">🥭</div>
        <div class="scene-mango2">🥭</div>
        <div class="scene-farmer">👨‍🌾</div>
        <div class="scene-ground"></div>
    </div>
    <div class="scene-title">
      <h2 style="font-size:2rem;font-weight:900;margin:0 0 12px;
          background:linear-gradient(135deg,#ffd166,#a7f3d0,#ffd166);
          background-size:200% auto;-webkit-background-clip:text;
          -webkit-text-fill-color:transparent;background-clip:text;
          animation:shimmerText 4s linear infinite">
        {tr["wctitle"]}
      </h2>
      <p style="color:#52b788;max-width:520px;margin:0 auto;line-height:1.8;font-size:15px;font-weight:600">
        {tr["wcsub"]}
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    w1,w2,w3=st.columns(3)
    for col,(icon,title,sub) in zip([w1,w2,w3],[
        ("📍", tr["wc1_title"], tr["wc1_sub"]),
        ("🥭", tr["wc2_title"], tr["wc2_sub"]),
        ("💰", tr["wc3_title"], tr["wc3_sub"]),
    ]):
        with col:
            st.markdown(f'''<div class="wc-feature">
              <div class="wc-feat-icon">{icon}</div>
              <div class="wc-title">{title}</div>
              <div class="wc-sub">{sub}</div>
            </div>''', unsafe_allow_html=True)

st.markdown(f'''<div style="text-align:center;color:#5a7a4a;font-size:12px;padding:22px 0;margin-top:28px;border-top:1px solid rgba(255,165,0,0.15)">
  {tr["footer"]}
</div>''',unsafe_allow_html=True)
