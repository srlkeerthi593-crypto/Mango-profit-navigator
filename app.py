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
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
html,body,[class*="css"]{font-family:'Poppins',sans-serif!important}
.main{background:linear-gradient(135deg,#f0faf4 0%,#e8f5e9 50%,#f5f7f0 100%)!important}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0d2b1a 0%,#1b4332 40%,#2d6a4f 100%)!important}
[data-testid="stSidebar"] *{color:white!important}
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stSelectbox>div>div,
[data-testid="stSidebar"] .stNumberInput input{
  background:rgba(255,255,255,0.12)!important;color:white!important;
  border:1.5px solid rgba(255,255,255,0.25)!important;border-radius:10px!important;font-size:14px!important}
[data-testid="stSidebar"] label{color:#a7f3d0!important;font-weight:600!important;font-size:12px!important;letter-spacing:0.5px!important}
[data-testid="stSidebar"] .stMarkdown p{color:#c8f0b0!important}
[data-testid="stSidebar"] .stMarkdown h3{color:#ffd166!important}

@keyframes fadeDown{from{opacity:0;transform:translateY(-25px)}to{opacity:1;transform:translateY(0)}}
@keyframes fadeUp{from{opacity:0;transform:translateY(25px)}to{opacity:1;transform:translateY(0)}}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes gradShift{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
@keyframes float1{0%,100%{transform:translateY(0) rotate(-5deg)}50%{transform:translateY(-18px) rotate(5deg)}}
@keyframes float2{0%,100%{transform:translateY(0) rotate(5deg)}50%{transform:translateY(-14px) rotate(-5deg)}}
@keyframes float3{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-20px) scale(1.15)}}
@keyframes ticker{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(82,183,136,0.4)}70%{box-shadow:0 0 0 12px rgba(82,183,136,0)}}
@keyframes shimmer{0%{background-position:-200% 0}100%{background-position:200% 0}}
@keyframes popIn{0%{opacity:0;transform:scale(0.5) translateY(20px)}60%{transform:scale(1.08) translateY(-4px)}100%{opacity:1;transform:scale(1) translateY(0)}}
@keyframes rankGlow{0%,100%{box-shadow:0 0 15px rgba(255,215,0,0.5)}50%{box-shadow:0 0 30px rgba(255,215,0,0.9)}}
@keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}

.hero{background:linear-gradient(270deg,#0d2b1a,#1b4332,#2d6a4f,#40916c,#52b788,#2d6a4f,#1b4332);
  background-size:500% 500%;animation:gradShift 8s ease infinite;border-radius:24px;
  padding:40px 48px 32px;margin-bottom:20px;color:white;text-align:center;
  position:relative;overflow:hidden;box-shadow:0 12px 40px rgba(13,43,26,0.4)}
.hero::before{content:"";position:absolute;inset:0;
  background:radial-gradient(ellipse at 20% 50%,rgba(82,183,136,0.15),transparent 60%),
             radial-gradient(ellipse at 80% 50%,rgba(64,145,108,0.15),transparent 60%)}
.hero-emojis{display:flex;justify-content:center;gap:20px;margin-bottom:16px}
.e1{animation:float1 3s ease-in-out infinite;font-size:32px;display:inline-block}
.e2{animation:float2 3.5s ease-in-out infinite 0.4s;font-size:28px;display:inline-block}
.e3{animation:float3 2.8s ease-in-out infinite 0.8s;font-size:30px;display:inline-block}
.e4{animation:float1 4s ease-in-out infinite 1.2s;font-size:26px;display:inline-block}
.e5{animation:float2 3.2s ease-in-out infinite 0.6s;font-size:32px;display:inline-block}
.hero-title{font-size:2.6rem;font-weight:900;margin:0 0 8px;
  text-shadow:0 3px 16px rgba(0,0,0,0.4);animation:fadeDown 0.8s ease;letter-spacing:-0.5px}
.hero-sub{font-size:1.05rem;opacity:0.88;animation:fadeDown 1s ease;font-weight:400}

.ticker-wrap{background:linear-gradient(90deg,#0a2218,#0d2b1a,#0a2218);
  border-radius:12px;padding:0;margin-bottom:20px;overflow:hidden;
  position:relative;box-shadow:0 4px 16px rgba(0,0,0,0.25);border:1px solid rgba(82,183,136,0.2)}
.ticker-lbl{position:absolute;left:0;top:0;height:100%;
  background:linear-gradient(90deg,#0a2218 80%,transparent);
  padding:0 20px;display:flex;align-items:center;
  color:#52b788;font-size:10px;font-weight:800;text-transform:uppercase;
  letter-spacing:2px;z-index:2;gap:6px;white-space:nowrap}
.ticker-scroll{padding:10px 0 10px 160px;overflow:hidden}
.ticker-inner{display:flex;animation:ticker 40s linear infinite;gap:0}
.tick{display:inline-flex;align-items:center;gap:8px;margin-right:40px;white-space:nowrap;padding:2px 0}
.tp{color:#a7f3d0;font-size:12px;font-weight:500}
.tv{color:#ffd166;font-size:14px;font-weight:800}
.tu{color:#4ade80;font-size:12px}
.td{color:#f87171;font-size:12px}

.mc{background:white;border:2px solid #d1fae5;border-radius:18px;
  padding:22px 20px;text-align:center;animation:fadeUp 0.6s ease;
  transition:all 0.25s;box-shadow:0 4px 16px rgba(45,106,79,0.06)}
.mc:hover{transform:translateY(-6px);box-shadow:0 12px 32px rgba(45,106,79,0.16);border-color:#52b788}
.mc.best{background:linear-gradient(135deg,#0d2b1a,#1b4332,#2d6a4f);
  border-color:#52b788;box-shadow:0 6px 24px rgba(13,43,26,0.4);animation:pulse 2.5s infinite}
.mc .lbl{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1px;
  color:#6b9e80;margin-bottom:8px}
.mc.best .lbl{color:#6ee7b7}
.mc .val{font-size:28px;font-weight:900;color:#1b4332;line-height:1.1}
.mc.best .val{color:#ffd166}
.mc .sub{font-size:11px;color:#7a9e8a;margin-top:5px;font-weight:500}
.mc.best .sub{color:#a7f3d0}

.rtable{width:100%;border-collapse:separate;border-spacing:0;font-size:13px;border-radius:16px;overflow:hidden}
.rtable thead tr th{background:linear-gradient(90deg,#0d2b1a,#1b4332);color:white;
  font-weight:700;font-size:10px;text-transform:uppercase;letter-spacing:1px;
  padding:14px 16px;text-align:left;white-space:nowrap}
.rtable thead tr th:first-child{border-radius:0}
.rtable tbody tr{transition:all 0.2s;animation:fadeIn 0.4s ease}
.rtable tbody tr:hover{background:#f0fdf4!important;transform:scale(1.002)}
.rtable tbody tr.top1{background:linear-gradient(90deg,rgba(255,215,0,0.08),rgba(255,215,0,0.03))!important;border-left:4px solid #FFD700}
.rtable tbody tr.top2{background:linear-gradient(90deg,rgba(192,192,192,0.08),rgba(192,192,192,0.03))!important;border-left:4px solid #C0C0C0}
.rtable tbody tr.top3{background:linear-gradient(90deg,rgba(205,127,50,0.08),rgba(205,127,50,0.03))!important;border-left:4px solid #CD7F32}
.rtable tbody tr td{padding:13px 16px;border-bottom:1px solid #f0fdf4;vertical-align:middle}
.rtable tbody tr:last-child td{border-bottom:none}

.rb{width:34px;height:34px;border-radius:50%;display:inline-flex;align-items:center;
  justify-content:center;font-weight:900;font-size:14px}
.rb1{background:linear-gradient(135deg,#FFD700,#FFA000);color:#5a3e00;
  box-shadow:0 3px 10px rgba(255,215,0,0.5);animation:rankGlow 2s ease-in-out infinite}
.rb2{background:linear-gradient(135deg,#D0D0D0,#A0A0A0);color:#2a2a2a;
  box-shadow:0 3px 8px rgba(150,150,150,0.4)}
.rb3{background:linear-gradient(135deg,#CD7F32,#8B4513);color:white;
  box-shadow:0 3px 8px rgba(205,127,50,0.4)}
.rbn{background:linear-gradient(135deg,#d1fae5,#a7f3d0);color:#1b4332;font-size:12px}

.podium-wrap{display:flex;gap:16px;margin-bottom:24px;animation:fadeUp 0.6s ease}
.pod{border-radius:20px;padding:24px 20px;text-align:center;position:relative;
  transition:all 0.3s;cursor:default;flex:1}
.pod1{background:linear-gradient(135deg,#0d2b1a,#1b4332);
  border:2px solid rgba(255,215,0,0.5);box-shadow:0 8px 32px rgba(13,43,26,0.5);
  animation:popIn 0.7s ease,pulse 3s infinite 0.7s;transform:scale(1.05)}
.pod2{background:linear-gradient(135deg,#1a3a2a,#2d5a40);
  border:2px solid rgba(192,192,192,0.4);box-shadow:0 6px 24px rgba(26,58,42,0.4);
  animation:popIn 0.7s ease 0.15s both}
.pod3{background:linear-gradient(135deg,#1a3a2a,#2d5a40);
  border:2px solid rgba(205,127,50,0.4);box-shadow:0 6px 24px rgba(26,58,42,0.4);
  animation:popIn 0.7s ease 0.3s both}
.pod-crown{font-size:36px;margin-bottom:6px;display:block}
.pod-rank{font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:2px;
  color:rgba(255,255,255,0.6);margin-bottom:4px}
.pod1 .pod-rank{color:#ffd166}
.pod-name{font-size:13px;font-weight:700;color:white;margin-bottom:6px;line-height:1.3}
.pod-cat{font-size:10px;padding:3px 10px;border-radius:20px;font-weight:700;
  display:inline-block;margin-bottom:10px}
.pod-profit{font-size:22px;font-weight:900;margin-bottom:2px}
.pod1 .pod-profit{color:#ffd166}
.pod2 .pod-profit,.pod3 .pod-profit{color:#6ee7b7}
.pod-dist{font-size:11px;color:rgba(255,255,255,0.6)}

.cat-tag{display:inline-block;padding:4px 11px;border-radius:20px;
  font-size:11px;font-weight:700;white-space:nowrap;letter-spacing:0.3px}
.Mandi,.మండీ,.मंडी,.மண்டி{background:#dbeafe;color:#1e40af}
.Processing,.ప్రాసెసింగ్,.प्रसंस्करण,.பதப்படுத்தல்{background:#f3e8ff;color:#7e22ce}
.Pulp,.పల్ప్,.पल्प,.பழச்சாறு{background:#fef9c3;color:#a16207}
.Pickle,.ఊరగాయ,.अचार,.ஊறுகாய்{background:#fce7f3;color:#be185d}
.LocalExport,.స్థానికఎగుమతి,.स्थानीयनिर्यात,.உள்நாட்டுஏற்றுமதி{background:#dcfce7;color:#15803d}
.AbroadExport,.విదేశీఎగుమతి,.विदेशनिर्यात,.வெளிநாட்டுஏற்றుமதி{background:#ccfbf1;color:#0f766e}

.pbar-wrap{display:flex;align-items:center;gap:8px}
.pbar-bg{height:8px;background:#e8f5e9;border-radius:4px;flex:1;min-width:60px;overflow:hidden}
.pbar-fill{height:8px;border-radius:4px;
  background:linear-gradient(90deg,#52b788,#2d6a4f);transition:width 1s ease}

.adv-card{background:white;border:2px solid #d1fae5;border-radius:16px;
  padding:20px;animation:fadeUp 0.5s ease;transition:all 0.25s;
  box-shadow:0 3px 12px rgba(45,106,79,0.07)}
.adv-card:hover{transform:translateY(-4px);box-shadow:0 10px 28px rgba(45,106,79,0.14);border-color:#52b788}
.adv-icon{font-size:32px;margin-bottom:10px;display:block}
.adv-title{font-weight:700;color:#1b4332;font-size:14px;margin-bottom:6px}
.adv-body{font-size:13px;color:#4a7a5f;line-height:1.65}

.auth-wrap{background:white;border:2px solid #d1fae5;border-radius:24px;
  padding:40px 44px;box-shadow:0 12px 40px rgba(45,106,79,0.12);animation:popIn 0.6s ease}
.auth-title{font-size:1.9rem;font-weight:900;color:#1b4332;text-align:center;margin-bottom:4px}
.auth-sub{font-size:13px;color:#6b9e80;text-align:center;margin-bottom:28px}

.wc-feat{background:white;border:2px solid #d1fae5;border-radius:18px;
  padding:24px 18px;text-align:center;animation:popIn 0.5s ease;
  transition:all 0.25s;box-shadow:0 3px 12px rgba(45,106,79,0.07)}
.wc-feat:hover{transform:translateY(-6px);box-shadow:0 12px 28px rgba(45,106,79,0.14)}
.wc-icon{font-size:40px;margin-bottom:12px;display:block}

.tip-box{background:linear-gradient(135deg,#fffbeb,#fef3c7);
  border:2px solid rgba(252,211,77,0.5);border-radius:12px;
  padding:14px 16px;font-size:12.5px;color:#78350f;line-height:1.65;margin-top:14px}

.namaste-bar{background:linear-gradient(90deg,#0d2b1a,#1b4332,#2d6a4f);
  color:white;border-radius:16px;padding:18px 24px;margin-bottom:22px;
  font-size:16px;font-weight:700;animation:fadeDown 0.5s ease;
  box-shadow:0 6px 20px rgba(13,43,26,0.3);display:flex;align-items:center;
  flex-wrap:wrap;gap:8px}

.sdivider{height:3px;background:linear-gradient(90deg,transparent,#52b788,#a7f3d0,#52b788,transparent);
  border:none;margin:24px 0;border-radius:2px}

.gif-strip{display:flex;gap:14px;justify-content:center;margin:16px 0;flex-wrap:wrap}
.gif-item{border-radius:14px;overflow:hidden;border:2px solid #d1fae5;
  box-shadow:0 4px 14px rgba(0,0,0,0.1);transition:transform 0.2s}
.gif-item:hover{transform:scale(1.06)}

.stButton>button[kind="primary"]{
  background:linear-gradient(135deg,#1b4332,#2d6a4f)!important;
  border:none!important;border-radius:12px!important;
  font-weight:700!important;font-size:15px!important;
  padding:12px 24px!important;letter-spacing:0.3px!important;
  box-shadow:0 4px 16px rgba(27,67,50,0.35)!important;transition:all 0.2s!important}
.stButton>button[kind="primary"]:hover{
  transform:translateY(-3px)!important;
  box-shadow:0 10px 24px rgba(27,67,50,0.45)!important}
</style>
""", unsafe_allow_html=True)

# ── USERS ──
USERS_FILE="users.json"
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

# ── TRANSLATIONS ──
T={
"en":{"title":"🥭 Farmer\'s Mango Profit Navigator","subtitle":"Find the Best Market. Earn the Highest Return.",
 "ticker_lbl":"LIVE PRICES","lname":"👤 Farmer Name","mandal_lbl":"📍 Mandal","lvillage":"🏘️ Village",
 "lvar":"🥭 Mango Variety","lqty":"📦 Quantity (Quintals)","run_btn":"🚀 Find Best Market",
 "tip":"💡 Sell with nearby farmers to split transport costs and boost your profit!",
 "wctitle":"Welcome, Mango Farmer! 🌾","wcsub":"Select your village, variety & quantity — then click Find Best Market to see the Top 10 options.",
 "namaste":"Namaste","base_price":"Today\'s Price","best_profit":"Best Net Profit",
 "best_market":"Best Market","your_village":"Your Village","qty_lbl":"Quantity",
 "tab1":"🥭 Top 10 Options","tab2":"📊 Profit Charts","tab3":"🗺️ Market Map","tab4":"💡 Selling Advice",
 "rank":"Rank","market":"Market / Buyer","cat":"Type","dist":"Dist (km)",
 "rev":"Revenue (₹)","trans":"Transport (₹)","profit":"Net Profit (₹)","pct":"% Best",
 "chart_title":"Profit Comparison — Top 10","pie_title":"Profit Share by Category",
 "prices_title":"📈 Nearby Market Prices","today_lbl":"Today","yest_lbl":"Yesterday",
 "adv_title":"Selling Advice",
 "adv":[("🌅","Best Time to Sell","Sell early morning when Mandi prices are highest (before 9am). Export buyers prefer pre-sorted Grade A fruit."),
        ("🤝","Negotiate Better","Contact 2–3 buyers at the same time. Show competitor prices — this forces sellers to give you a better deal."),
        ("🚛","Transport Tip","Combine your load with neighbouring farmers to split transport cost per kg — this directly increases your net profit."),
        ("⭐","Quality = More Money","Grade A fruit fetches 15–25% more. Sort & remove damaged fruit before loading to maximise your return.")],
 "login":"Login","register":"Register","logout":"Logout",
 "login_title":"👤 Login to Continue","reg_title":"📝 Create Account",
 "username":"Username","password":"Password","full_name":"Full Name","phone":"Phone (optional)",
 "login_btn":"🔓 Login →","reg_btn":"✅ Register →",
 "have_account":"Already have an account? Login here","no_account":"New user? Create free account",
 "mandal_ph":"Select Mandal","village_ph":"Select Village","name_ph":"Enter your name","qty_label":"quintals",
 "var_labels":{"Banganapalli":"Banganapalli\n⭐ Export","Totapuri":"Totapuri\n⭐ Processing",
               "Neelam":"Neelam\n⭐ Mandi","Rasalu":"Rasalu\n⭐ Pickle"},
 "podium_title":"🏆 Top 3 Best Options for You",
 "top3_sub":"These are your most profitable selling options",
 "full_table":"📋 Full Top 10 Ranking",
 "dl_csv":"📥 Download Results (CSV)"},

"te":{"title":"🥭 రైతు మామిడి లాభాల నావిగేటర్","subtitle":"అత్యుత్తమ మార్కెట్ కనుగొనండి. అధిక లాభం సంపాదించండి.",
 "ticker_lbl":"నేటి ధరలు","lname":"👤 రైతు పేరు","mandal_lbl":"📍 మండల్","lvillage":"🏘️ మీ గ్రామం",
 "lvar":"🥭 మామిడి రకం","lqty":"📦 పరిమాణం (క్వింటాల్లు)","run_btn":"🚀 అత్యుత్తమ మార్కెట్ కనుగొనండి",
 "tip":"💡 పొరుగు రైతులతో కలిసి అమ్మండి — రవాణా ఖర్చు తక్కువ, లాభం ఎక్కువ!",
 "wctitle":"స్వాగతం, మామిడి రైతు! 🌾","wcsub":"మీ గ్రామం, రకం మరియు పరిమాణం ఎంచుకుని టాప్ 10 ఎంపికలు చూడండి.",
 "namaste":"నమస్తే","base_price":"నేటి ధర","best_profit":"అత్యధిక నికర లాభం",
 "best_market":"అత్యుత్తమ మార్కెట్","your_village":"మీ గ్రామం","qty_lbl":"పరిమాణం",
 "tab1":"🥭 టాప్ 10 ఎంపికలు","tab2":"📊 లాభాల పోలిక","tab3":"🗺️ మార్కెట్ మ్యాప్","tab4":"💡 అమ్మకపు సలహా",
 "rank":"వరుస","market":"మార్కెట్ / కొనుగోలుదారు","cat":"రకం","dist":"దూరం (కి.మీ)",
 "rev":"ఆదాయం (₹)","trans":"రవాణా (₹)","profit":"నికర లాభం (₹)","pct":"% అత్యుత్తమం",
 "chart_title":"లాభాల పోలిక — టాప్ 10","pie_title":"వర్గం వారీ లాభం",
 "prices_title":"📈 సమీప మార్కెట్ ధరలు","today_lbl":"నేడు","yest_lbl":"నిన్న",
 "adv_title":"అమ్మకపు సలహా",
 "adv":[("🌅","అమ్మడానికి అత్యుత్తమ సమయం","తెల్లవారుజామున అమ్మండి — ఉదయం 9 గంటలకు ముందు మండీలో ధరలు ఎక్కువగా ఉంటాయి."),
        ("🤝","మెరుగైన ధర చర్చించండి","2-3 మంది కొనుగోలుదారులను ఒకేసారి సంప్రదించి పోటీ ధరలు చూపించండి."),
        ("🚛","రవాణా సూచన","పొరుగు రైతులతో కలిసి రవాణా చేయండి — కిలో కు రవాణా ఖర్చు తక్కువవుతుంది."),
        ("⭐","నాణ్యత = ఎక్కువ డబ్బు","గ్రేడ్ A మామిడి 15-25% ఎక్కువ ధర పొందుతుంది. లోడ్ చేయడానికి ముందు వేర్పరచండి.")],
 "login":"లాగిన్","register":"రిజిస్టర్","logout":"లాగ్ అవుట్",
 "login_title":"👤 కొనసాగించడానికి లాగిన్","reg_title":"📝 ఖాతా సృష్టించండి",
 "username":"వినియోగదారు పేరు","password":"పాస్వర్డ్","full_name":"పూర్తి పేరు","phone":"ఫోన్ (ఐచ్ఛికం)",
 "login_btn":"🔓 లాగిన్ →","reg_btn":"✅ రిజిస్టర్ →",
 "have_account":"ఖాతా ఉందా? లాగిన్ చేయండి","no_account":"కొత్తగా? ఖాతా సృష్టించండి",
 "mandal_ph":"మండల్ ఎంచుకోండి","village_ph":"గ్రామం ఎంచుకోండి","name_ph":"మీ పేరు నమోదు చేయండి","qty_label":"క్వింటాల్లు",
 "var_labels":{"Banganapalli":"బంగినపల్లి\n⭐ ఎగుమతి","Totapuri":"తోటపురి\n⭐ ప్రాసెసింగ్",
               "Neelam":"నీలం\n⭐ మండీ","Rasalu":"రసాలు\n⭐ ఊరగాయ"},
 "podium_title":"🏆 మీకు టాప్ 3 అత్యుత్తమ ఎంపికలు",
 "top3_sub":"ఇవి మీ అత్యంత లాభదాయకమైన అమ్మకపు ఎంపికలు",
 "full_table":"📋 పూర్తి టాప్ 10 జాబితా",
 "dl_csv":"📥 ఫలితాలు డౌన్‌లోడ్ చేయండి (CSV)"},

"hi":{"title":"🥭 किसान का आम लाभ नेविगेटर","subtitle":"सबसे अच्छा बाजार खोजें। सबसे ज्यादा मुनाफा कमाएं।",
 "ticker_lbl":"आज के भाव","lname":"👤 किसान का नाम","mandal_lbl":"📍 मंडल","lvillage":"🏘️ आपका गांव",
 "lvar":"🥭 आम की किस्म","lqty":"📦 मात्रा (क्विंटल)","run_btn":"🚀 सबसे अच्छा बाजार खोजें",
 "tip":"💡 पड़ोसी किसानों के साथ मिलकर बेचें — परिवहन लागत कम होगी, मुनाफा बढ़ेगा!",
 "wctitle":"स्वागत है, आम किसान! 🌾","wcsub":"अपना गांव, किस्म और मात्रा चुनें — टॉप 10 विकल्प देखने के लिए क्लिक करें।",
 "namaste":"नमस्ते","base_price":"आज का भाव","best_profit":"सर्वाधिक शुद्ध लाभ",
 "best_market":"सबसे अच्छा बाजार","your_village":"आपका गांव","qty_lbl":"मात्रा",
 "tab1":"🥭 टॉप 10 विकल्प","tab2":"📊 लाभ तुलना","tab3":"🗺️ बाजार मानचित्र","tab4":"💡 बिक्री सलाह",
 "rank":"क्रम","market":"बाजार / खरीदार","cat":"प्रकार","dist":"दूरी (कि.मी.)",
 "rev":"आय (₹)","trans":"परिवहन (₹)","profit":"शुद्ध लाभ (₹)","pct":"% सर्वोत्तम",
 "chart_title":"लाभ तुलना — टॉप 10","pie_title":"श्रेणी अनुसार लाभ",
 "prices_title":"📈 पास के बाजार के भाव","today_lbl":"आज","yest_lbl":"कल",
 "adv_title":"बिक्री सलाह",
 "adv":[("🌅","बेचने का सबसे अच्छा समय","सुबह जल्दी बेचें — मंडी में सुबह 9 बजे से पहले भाव सबसे ज्यादा होते हैं।"),
        ("🤝","बेहतर भाव मांगें","2-3 खरीदारों से एक साथ बात करें और प्रतिस्पर्धी भाव दिखाएं।"),
        ("🚛","परिवहन सुझाव","पड़ोसी किसानों के साथ मिलकर परिवहन करें — प्रति किलो लागत कम होगी।"),
        ("⭐","गुणवत्ता = ज्यादा पैसे","ग्रेड A आम 15-25% ज्यादा भाव पाता है। लोड करने से पहले छांटें।")],
 "login":"लॉगिन","register":"रजिस्टर","logout":"लॉगआउट",
 "login_title":"👤 जारी रखने के लिए लॉगिन","reg_title":"📝 खाता बनाएं",
 "username":"यूज़रनेम","password":"पासवर्ड","full_name":"पूरा नाम","phone":"फोन (वैकल्पिक)",
 "login_btn":"🔓 लॉगिन →","reg_btn":"✅ रजिस्टर →",
 "have_account":"खाता है? लॉगिन करें","no_account":"नए हैं? खाता बनाएं",
 "mandal_ph":"मंडल चुनें","village_ph":"गांव चुनें","name_ph":"अपना नाम","qty_label":"क्विंटल",
 "var_labels":{"Banganapalli":"बंगनपल्ली\n⭐ निर्यात","Totapuri":"तोतापुरी\n⭐ प्रसंस्करण",
               "Neelam":"नीलम\n⭐ मंडी","Rasalu":"रसालु\n⭐ अचार"},
 "podium_title":"🏆 आपके लिए टॉप 3 सर्वोत्तम विकल्प",
 "top3_sub":"ये आपके सबसे ज्यादा फायदेमंद बिक्री के विकल्प हैं",
 "full_table":"📋 पूरी टॉप 10 सूची",
 "dl_csv":"📥 परिणाम डाउनलोड करें (CSV)"},

"ta":{"title":"🥭 விவசாயியின் மாம்பழ லாப வழிகாட்டி","subtitle":"சிறந்த சந்தையைக் கண்டறியுங்கள். அதிக வருவாய் ஈட்டுங்கள்.",
 "ticker_lbl":"இன்றைய விலைகள்","lname":"👤 விவசாயி பெயர்","mandal_lbl":"📍 மண்டலம்","lvillage":"🏘️ கிராமம்",
 "lvar":"🥭 மாம்பழ வகை","lqty":"📦 அளவு (குவிண்டால்)","run_btn":"🚀 சிறந்த சந்தையைக் கண்டறி",
 "tip":"💡 அண்டை விவசாயிகளுடன் சேர்ந்து விற்கவும் — போக்குவரத்து செலவு குறையும்!",
 "wctitle":"வரவேற்கிறோம், மாம்பழ விவசாயி! 🌾","wcsub":"கிராமம், வகை மற்றும் அளவை தேர்ந்தெடுத்து சிறந்த 10 விருப்பங்களை காணுங்கள்.",
 "namaste":"வணக்கம்","base_price":"இன்றைய விலை","best_profit":"அதிகபட்ச லாபம்",
 "best_market":"சிறந்த சந்தை","your_village":"கிராமம்","qty_lbl":"அளவு",
 "tab1":"🥭 சிறந்த 10","tab2":"📊 லாப ஒப்பீடு","tab3":"🗺️ வரைபடம்","tab4":"💡 ஆலோசனை",
 "rank":"வரிசை","market":"சந்தை / வாங்குபவர்","cat":"வகை","dist":"தூரம்",
 "rev":"வருவாய் (₹)","trans":"போக்குவரத்து (₹)","profit":"நிகர லாபம் (₹)","pct":"% சிறந்தது",
 "chart_title":"லாப ஒப்பீடு — சிறந்த 10","pie_title":"வகை வாரியான லாபம்",
 "prices_title":"📈 சந்தை விலைகள்","today_lbl":"இன்று","yest_lbl":"நேற்று",
 "adv_title":"விற்பனை ஆலோசனை",
 "adv":[("🌅","சிறந்த விற்பனை நேரம்","காலை 9 மணிக்கு முன் விற்கவும் — மண்டியில் விலை அதிகமாக இருக்கும்."),
        ("🤝","சிறந்த விலை பேசுங்கள்","2-3 வாங்குபவர்களிடம் ஒரே நேரத்தில் பேசி போட்டி விலைகளை காட்டுங்கள்."),
        ("🚛","போக்குவரத்து குறிப்பு","அண்டை விவசாயிகளுடன் சேர்ந்து போக்குவரத்து செய்யுங்கள்."),
        ("⭐","தரம் = அதிக பணம்","தரம் A மாம்பழம் 15-25% அதிக விலை பெறும். ஏற்றுவதற்கு முன் வகைப்படுத்துங்கள்.")],
 "login":"உள்நுழைவு","register":"பதிவு","logout":"வெளியேறு",
 "login_title":"👤 தொடர உள்நுழைக","reg_title":"📝 கணக்கு உருவாக்கு",
 "username":"பயனர்பெயர்","password":"கடவுச்சொல்","full_name":"முழு பெயர்","phone":"தொலைபேசி (விருப்பம்)",
 "login_btn":"🔓 உள்நுழைவு →","reg_btn":"✅ பதிவு →",
 "have_account":"கணக்கு உள்ளதா? உள்நுழைக","no_account":"புதியவரா? கணக்கு உருவாக்கு",
 "mandal_ph":"மண்டலம் தேர்ந்தெடு","village_ph":"கிராமம் தேர்ந்தெடு","name_ph":"உங்கள் பெயர்","qty_label":"குவிண்டால்",
 "var_labels":{"Banganapalli":"பங்கனபல்லி\n⭐ ஏற்றுமதி","Totapuri":"தொதாபுரி\n⭐ பதப்படுத்தல்",
               "Neelam":"நீலம்\n⭐ மண்டி","Rasalu":"ரசாலு\n⭐ ஊறுகாய்"},
 "podium_title":"🏆 உங்களுக்கு சிறந்த 3 விருப்பங்கள்",
 "top3_sub":"இவை உங்களுக்கு மிகவும் லாபகரமான விற்பனை விருப்பங்கள்",
 "full_table":"📋 முழுமையான சிறந்த 10",
 "dl_csv":"📥 முடிவுகளை பதிவிறக்கம் செய்க (CSV)"},
}

# Market name translations
MNT={
"te":{
  "Tirupati APMC (RC Road)":"తిరుపతి APMC (RC రోడ్)","Pakala Main Mango APMC":"పాకల మాంగో APMC",
  "Railway Kodur APMC Yard":"రైల్వే కోడూరు APMC","Puttur Mango Market Yard":"పుత్తూరు మాంగో మార్కెట్",
  "Chandragiri APMC":"చంద్రగిరి APMC","Srikalahasti APMC":"శ్రీకాళహస్తి APMC",
  "Venkatagiri APMC":"వెంకటగిరి APMC","Nagalapuram APMC":"నాగలాపురం APMC",
  "Naidupeta APMC":"నాయుడుపేట APMC","Satyavedu APMC":"సత్యవేడు APMC",
  "Sullurpeta APMC":"సుళ్ళూరుపేట APMC","Bangarupalem":"బంగారుపాలెం",
  "Chittoor":"చిత్తూరు","Punganur":"పుంగనూరు","Pakala":"పాకల","Pileru":"పిలేరు",
  "Madanapalle AMC":"మదనపల్లె AMC","Gurramkonda e-NAM":"గుర్రంకొండ e-NAM",
  "Galiveedu Market Yard":"గాలివీడు మార్కెట్","Jamiya Mango Yard":"జమియా మాంగో యార్డ్",
  "Nimmanapalle Yard":"నిమ్మనపల్లె యార్డ్","Burakayalakota Hub":"బురకాయలకోట హబ్",
  "Nandini Private Mandi":"నందిని ప్రైవేట్ మండీ","Chowdepalle Yard":"చౌడేపల్లి యార్డ్",
  "Galla Foods Rayachoti":"గల్లా ఫుడ్స్ రాయచోటి","Roshan Fruits India":"రోషన్ ఫ్రూట్స్ ఇండియా",
  "Sri Varsha Food Products":"శ్రీ వర్ష ఫుడ్ ప్రొడక్ట్స్","Hayath Foods":"హయాత్ ఫుడ్స్",
  "Grofresh Agrofoods":"గ్రోఫ్రెష్ అగ్రోఫుడ్స్","Srini Food Park":"శ్రీని ఫుడ్ పార్క్",
  "Sree Sannidhi Foods":"శ్రీ సన్నిధి ఫుడ్స్","PLR Foods Pvt Ltd":"PLR ఫుడ్స్",
  "Vijay Food Processing":"విజయ్ ఫుడ్ ప్రాసెసింగ్","Bright Mangoes":"బ్రైట్ మాంగోస్",
  "Navya Foods Pvt Ltd":"నవ్య ఫుడ్స్","Ohms Food Products":"ఓమ్స్ ఫుడ్ ప్రొడక్ట్స్",
  "Galla Foods Ltd":"గల్లా ఫుడ్స్","Paiyur Group Mango Pulp":"పాయ్యూర్ గ్రూప్",
  "B M Fruits":"బి.ఎం. ఫ్రూట్స్",
  "Rayachoti Pickles":"రాయచోటి పికిల్స్","Tirupati Pickle Works":"తిరుపతి పికిల్ వర్క్స్",
  "Padmavathi Pickles":"పద్మావతి పికిల్స్","Puttur Pickle Makers":"పుత్తూరు పికిల్స్",
  "Srikalahasti Pickle Industries":"శ్రీకాళహస్తి పికిల్ ఇండస్ట్రీస్",
  "Pileru Pickle Works":"పిలేరు పికిల్ వర్క్స్","Punganur Mango Pickle":"పుంగనూరు మాంగో పికిల్",
  "Kalikiri Pickle":"కాళికిరి పికిల్","Chittoor Pack Pickle":"చిత్తూరు పికిల్",
  "Madanapalle Pickle":"మదనపల్లె పికిల్",
  "Rayachoti APMC Export":"రాయచోటి APMC ఎగుమతి","Rajampet APMC":"రాజంపేట APMC",
  "Tirupati APMC Export":"తిరుపతి APMC ఎగుమతి","Renigunta Packhouse":"రేణిగుంట ప్యాక్‌హౌస్",
  "Srikalahasti Cold Room":"శ్రీకాళహస్తి కోల్డ్ రూమ్","Puttur Export Yard":"పుత్తూరు ఎగుమతి యార్డ్",
  "Bangarupalem APMC":"బంగారుపాలెం APMC","Chittoor APMC":"చిత్తూరు APMC",
  "Punganur Market Yard":"పుంగనూరు మార్కెట్","Pileru Packhouse":"పిలేరు ప్యాక్‌హౌస్",
  "Tirupati APMC Int Export":"తిరుపతి APMC అంతర్జాతీయ ఎగుమతి",
  "Renigunta Cold Room Export":"రేణిగుంట కోల్డ్ రూమ్ ఎగుమతి",
  "Rayachoti APMC Int":"రాయచోటి APMC అంతర్జాతీయ","Rajampet APMC Int":"రాజంపేట APMC అంతర్జాతీయ",
  "Srikalahasti Int Collection":"శ్రీకాళహస్తి అంతర్జాతీయ",
  "Chandragiri Packhouse":"చంద్రగిరి ప్యాక్‌హౌస్",
  "Grofresh Export Pack":"గ్రోఫ్రెష్ ఎగుమతి","Roshan Fruits Export":"రోషన్ ఫ్రూట్స్ ఎగుమతి",
  "Navya Foods Export":"నవ్య ఫుడ్స్ ఎగుమతి","Bright Mangoes Export":"బ్రైట్ మాంగోస్ ఎగుమతి",
},
"hi":{
  "Tirupati APMC (RC Road)":"तिरुपति APMC (RC रोड)","Pakala Main Mango APMC":"पाकला मैंगो APMC",
  "Railway Kodur APMC Yard":"रेलवे कोदूर APMC","Puttur Mango Market Yard":"पुत्तूर मैंगो मार्केट",
  "Chandragiri APMC":"चंद्रगिरि APMC","Srikalahasti APMC":"श्रीकालहस्ती APMC",
  "Venkatagiri APMC":"वेंकटगिरि APMC","Bangarupalem":"बंगारुपालेम","Chittoor":"चित्तूर",
  "Madanapalle AMC":"मदनपल्ले AMC","Gurramkonda e-NAM":"गुर्रामकोंडा e-NAM",
  "Renigunta Packhouse":"रेनिगुंटा पैकहाउस","Chandragiri Packhouse":"चंद्रगिरि पैकहाउस",
},
"ta":{
  "Tirupati APMC (RC Road)":"திருப்பதி APMC (RC சாலை)","Chandragiri APMC":"சந்திரகிரி APMC",
  "Srikalahasti APMC":"ஸ்ரீகாளஹஸ்தி APMC","Venkatagiri APMC":"வெங்கடகிரி APMC",
  "Bangarupalem":"பங்காரு பாலெம்","Renigunta Packhouse":"ரேணிகுண்டா பேக்ஹவுஸ்",
  "Chandragiri Packhouse":"சந்திரகிரி பேக்ஹவுஸ்",
},
}

CTR={"te":{"Mandi":"మండీ","Processing":"ప్రాసెసింగ్","Pulp":"పల్ప్","Pickle":"ఊరగాయ",
     "Local Export":"స్థానిక ఎగుమతి","Abroad Export":"విదేశీ ఎగుమతి"},
"hi":{"Mandi":"मंडी","Processing":"प्रसंस्करण","Pulp":"पल्प","Pickle":"अचार",
     "Local Export":"स्थानीय निर्यात","Abroad Export":"विदेश निर्यात"},
"ta":{"Mandi":"மண்டி","Processing":"பதப்படுத்தல்","Pulp":"பழச்சாறு","Pickle":"ஊறுகாய்",
     "Local Export":"உள்நாட்டு ஏற்றுமதி","Abroad Export":"வெளிநாட்டு ஏற்றுமதி"},
"en":{"Mandi":"Mandi","Processing":"Processing","Pulp":"Pulp","Pickle":"Pickle",
     "Local Export":"Local Export","Abroad Export":"Abroad Export"}}

VTR={"te":{
  "BALAYAPALLI":"బాలయపల్లి","ALIMILI":"అలిమిలి","BHYRAVARAM":"భైరవారం",
  "CHILAMANURU":"చిలమనూరు","GOTTIKADU":"గొట్టికాడు","HASTHAKAVERI":"హస్తకావేరి",
  "JAYAMPU":"జయంపు","KADAGUNTA":"కాదగుంట","KALAGANDA":"కళగండ","KAMAKURU":"కామకూరు",
  "KATRAGUNTA":"కాట్రగుంట","KAYYURU":"కయ్యూరు","KOTAMBEDU":"కొటంబేడు",
  "MANNURU":"మన్నూరు","NIDIGALLU":"నిడిగళ్ళు","CHANDRAGIRI":"చంద్రగిరి",
  "AGARALA":"అగరాల","THONDAWADA":"తొండవాడ","MITTAPALEM":"మిట్టపాలెం",
  "GADANKI":"గాడంకి","PAKALA":"పాకల","DAMALCHERUVU":"దామలచెరువు",
  "RENIGUNTA":"రేణిగుంట","KARAKAMBADI":"కారకంబాడి","ATHURU":"ఆతూరు",
  "AVILALA":"అవిలాల","TIRUCHANUR":"తిరుచానూరు","THUMMALAGUNTA":"తుమ్మలగుంట",
  "MANGALAM":"మంగళం","RANADHEERPURAM":"రానాధీర్పురం",
  "SRIKALAHASTHI":"శ్రీకాళహస్తి","AMMAPALEM":"అమ్మపాలెం","EMPEDU":"ఎంపేడు",
  "YERPEDU":"యేర్పేడు","GUDIMALLAM":"గుడిమళ్ళం","PAPANAIDUPET":"పాపనాయుడుపేట",
  "NAIDUPET":"నాయుడుపేట","ANNAMEDU":"అన్నమేడు",
  "NAGALAPURAM":"నాగలాపురం","KRISHNAPURAM":"కృష్ణపురం",
  "SULLURPET":"సుళ్ళూరుపేట","ABAKA":"అబాక","TADA":"తాడ","MAMBATTU":"మంబట్టు",
  "VAKADU":"వకాడు","KALLURU":"కళ్ళూరు","VENKATAGIRI":"వెంకటగిరి",
  "PUTTUR":"పుత్తూరు","NESANUR":"నేసనూరు","OZILI":"ఓజిలి","GURRAMKONDA":"గుర్రంకొండ",
  "DAKKILI":"దక్కిలి","AMUDURU":"అముదూరు","SATYAVEDU":"సత్యవేడు","AROOR":"అరూర్",
  "NARAYANAVANAM":"నారాయణవనం","BHEEMUNICHERUVU":"భీమునిచెరువు",
  "PELLAKUR":"పెళ్ళకూరు","ANAKAVOLU":"అనకవోలు",
  "VARADAIAHPALEM":"వరదయ్యపాలెం","AMBUR":"అంబూరు",
  "THOTTAMBEDU":"తొట్టంబేడు","BONUPALLE":"బొన్నుపల్లె",
  "TIRUPATI (RURAL)":"తిరుపతి (గ్రామీణ)","TIRUPATI (URBAN)":"తిరుపతి (పట్టణ)"},
"hi":{"CHANDRAGIRI":"चंद्रगिरि","GADANKI":"गाडंकी","PAKALA":"पाकला","RENIGUNTA":"रेनिगुंटा",
  "TIRUPATI (RURAL)":"तिरुपति (ग्रामीण)","TIRUPATI (URBAN)":"तिरुपति (शहरी)",
  "SRIKALAHASTHI":"श्रीकालहस्ती","YERPEDU":"येरपेडु","NAIDUPET":"नायडुपेट",
  "NAGALAPURAM":"नागलापुरम","SULLURPET":"सुल्लूरपेट","VENKATAGIRI":"वेंकटगिरि",
  "PUTTUR":"पुत्तूर","SATYAVEDU":"सत्यवेडु"},
"ta":{"TIRUPATI (RURAL)":"திருப்பதி","CHANDRAGIRI":"சந்திரகிரி","PAKALA":"பாக்கல",
  "SRIKALAHASTHI":"ஸ்ரீகாளஹஸ்தி","RENIGUNTA":"ரேணிகுண்டா","SULLURPET":"சுல்லூர்பேட்",
  "VENKATAGIRI":"வெங்கடகிரி","PUTTUR":"புத்தூர்","SATYAVEDU":"சத்யவேடு"},
}

MTR={"te":{
  "BALAYAPALLI":"బాలయపల్లి","CHANDRAGIRI":"చంద్రగిరి","PAKALA":"పాకల",
  "TIRUPATI (RURAL)":"తిరుపతి (గ్రామీణ)","TIRUPATI (URBAN)":"తిరుపతి (పట్టణ)",
  "SRIKALAHASTHI":"శ్రీకాళహస్తి","RENIGUNTA":"రేణిగుంట","YERPEDU":"యేర్పేడు",
  "NAIDUPET":"నాయుడుపేట","NAGALAPURAM":"నాగలాపురం","SULLURPET":"సుళ్ళూరుపేట",
  "TADA":"తాడ","VAKADU":"వకాడు","VENKATAGIRI":"వెంకటగిరి","PUTTUR":"పుత్తూరు",
  "OZILI":"ఓజిలి","DAKKILI":"దక్కిలి","SATYAVEDU":"సత్యవేడు",
  "NARAYANAVANAM":"నారాయణవనం","PELLAKUR":"పెళ్ళకూరు",
  "VARADAIAHPALEM":"వరదయ్యపాలెం","THOTTAMBEDU":"తొట్టంబేడు"},
"hi":{"TIRUPATI (RURAL)":"तिरुपति (ग्रामीण)","CHANDRAGIRI":"चंद्रगिरि","RENIGUNTA":"रेनिगुंटा",
  "SULLURPET":"सुल्लूरपेट","VENKATAGIRI":"वेंकटगिरि","PUTTUR":"पुत्तूर"},
"ta":{"TIRUPATI (RURAL)":"திருப்பதி","CHANDRAGIRI":"சந்திரகிரி","RENIGUNTA":"ரேணிகுண்டா"},
}

def tm(name,l):
    if l=="en": return name
    return MNT.get(l,{}).get(name, name)
def tv(n,l):
    if l=="en": return n
    return VTR.get(l,{}).get(n.upper(),n)
def tmt(m,l):
    if l=="en": return m
    return MTR.get(l,{}).get(m.upper(),m)
def tc(c,l): return CTR.get(l,CTR["en"]).get(c,c)

VILLAGES=[
{"M":"BALAYAPALLI","GP":"ALIMILI","La":14.0152,"Lo":79.6124},
{"M":"BALAYAPALLI","GP":"BALAYAPALLI","La":13.9856,"Lo":79.6452},
{"M":"BALAYAPALLI","GP":"BHYRAVARAM","La":14.0221,"Lo":79.6845},
{"M":"BALAYAPALLI","GP":"CHILAMANURU","La":14.0512,"Lo":79.6231},
{"M":"BALAYAPALLI","GP":"GOTTIKADU","La":13.9621,"Lo":79.6712},
{"M":"BALAYAPALLI","GP":"HASTHAKAVERI","La":13.9455,"Lo":79.6322},
{"M":"BALAYAPALLI","GP":"JAYAMPU","La":13.9922,"Lo":79.7011},
{"M":"BALAYAPALLI","GP":"KADAGUNTA","La":14.0312,"Lo":79.5912},
{"M":"BALAYAPALLI","GP":"KALAGANDA","La":13.9112,"Lo":79.6241},
{"M":"BALAYAPALLI","GP":"KAMAKURU","La":13.9521,"Lo":79.5844},
{"M":"BALAYAPALLI","GP":"KATRAGUNTA","La":14.0012,"Lo":79.6543},
{"M":"BALAYAPALLI","GP":"KAYYURU","La":13.8821,"Lo":79.6912},
{"M":"BALAYAPALLI","GP":"KOTAMBEDU","La":13.9244,"Lo":79.7121},
{"M":"BALAYAPALLI","GP":"MANNURU","La":13.9712,"Lo":79.7342},
{"M":"BALAYAPALLI","GP":"NIDIGALLU","La":14.0421,"Lo":79.6921},
{"M":"CHANDRAGIRI","GP":"CHANDRAGIRI","La":13.5834,"Lo":79.3214},
{"M":"CHANDRAGIRI","GP":"AGARALA","La":13.6012,"Lo":79.3145},
{"M":"CHANDRAGIRI","GP":"THONDAWADA","La":13.6122,"Lo":79.3712},
{"M":"CHANDRAGIRI","GP":"MITTAPALEM","La":13.5822,"Lo":79.3611},
{"M":"PAKALA","GP":"GADANKI","La":13.5321,"Lo":79.2112},
{"M":"PAKALA","GP":"PAKALA","La":13.4512,"Lo":79.1121},
{"M":"PAKALA","GP":"DAMALCHERUVU","La":13.5112,"Lo":79.1011},
{"M":"RENIGUNTA","GP":"RENIGUNTA","La":13.6345,"Lo":79.5124},
{"M":"RENIGUNTA","GP":"KARAKAMBADI","La":13.6645,"Lo":79.4712},
{"M":"RENIGUNTA","GP":"ATHURU","La":13.6812,"Lo":79.5122},
{"M":"TIRUPATI (RURAL)","GP":"AVILALA","La":13.6012,"Lo":79.4121},
{"M":"TIRUPATI (RURAL)","GP":"TIRUCHANUR","La":13.6111,"Lo":79.4512},
{"M":"TIRUPATI (RURAL)","GP":"THUMMALAGUNTA","La":13.6044,"Lo":79.4011},
{"M":"TIRUPATI (URBAN)","GP":"MANGALAM","La":13.6545,"Lo":79.4512},
{"M":"TIRUPATI (URBAN)","GP":"RANADHEERPURAM","La":13.6411,"Lo":79.4311},
{"M":"SRIKALAHASTHI","GP":"SRIKALAHASTHI","La":13.7498,"Lo":79.7034},
{"M":"SRIKALAHASTHI","GP":"AMMAPALEM","La":13.7411,"Lo":79.6212},
{"M":"SRIKALAHASTHI","GP":"EMPEDU","La":13.8112,"Lo":79.7122},
{"M":"YERPEDU","GP":"YERPEDU","La":13.6845,"Lo":79.5945},
{"M":"YERPEDU","GP":"GUDIMALLAM","La":13.6421,"Lo":79.5511},
{"M":"YERPEDU","GP":"PAPANAIDUPET","La":13.6645,"Lo":79.5823},
{"M":"NAIDUPET","GP":"NAIDUPET","La":13.9142,"Lo":79.8944},
{"M":"NAIDUPET","GP":"ANNAMEDU","La":13.8812,"Lo":79.9111},
{"M":"NAGALAPURAM","GP":"NAGALAPURAM","La":13.4022,"Lo":79.9214},
{"M":"NAGALAPURAM","GP":"KRISHNAPURAM","La":13.3812,"Lo":79.9411},
{"M":"SULLURPET","GP":"SULLURPET","La":13.7008,"Lo":80.0211},
{"M":"SULLURPET","GP":"ABAKA","La":13.7012,"Lo":80.0112},
{"M":"TADA","GP":"TADA","La":13.5845,"Lo":80.0312},
{"M":"TADA","GP":"MAMBATTU","La":13.5611,"Lo":80.0211},
{"M":"VAKADU","GP":"VAKADU","La":14.0124,"Lo":80.1012},
{"M":"VAKADU","GP":"KALLURU","La":14.0512,"Lo":80.0911},
{"M":"VENKATAGIRI","GP":"VENKATAGIRI","La":13.9575,"Lo":79.5847},
{"M":"VENKATAGIRI","GP":"AMMAPALEM","La":13.9812,"Lo":79.5412},
{"M":"PUTTUR","GP":"PUTTUR","La":13.4419,"Lo":79.553},
{"M":"PUTTUR","GP":"NESANUR","La":13.4722,"Lo":79.5911},
{"M":"OZILI","GP":"OZILI","La":13.9845,"Lo":79.9124},
{"M":"OZILI","GP":"GURRAMKONDA","La":13.9512,"Lo":79.8412},
{"M":"DAKKILI","GP":"DAKKILI","La":14.1345,"Lo":79.6122},
{"M":"DAKKILI","GP":"AMUDURU","La":14.1211,"Lo":79.6012},
{"M":"SATYAVEDU","GP":"SATYAVEDU","La":13.5045,"Lo":79.9712},
{"M":"SATYAVEDU","GP":"AROOR","La":13.5112,"Lo":79.9011},
{"M":"NARAYANAVANAM","GP":"NARAYANAVANAM","La":13.4211,"Lo":79.5822},
{"M":"NARAYANAVANAM","GP":"BHEEMUNICHERUVU","La":13.4111,"Lo":79.5512},
{"M":"PELLAKUR","GP":"PELLAKUR","La":13.8345,"Lo":79.8544},
{"M":"PELLAKUR","GP":"ANAKAVOLU","La":13.8412,"Lo":79.8512},
{"M":"VARADAIAHPALEM","GP":"VARADAIAHPALEM","La":13.5945,"Lo":79.9221},
{"M":"VARADAIAHPALEM","GP":"AMBUR","La":13.5612,"Lo":79.9112},
{"M":"THOTTAMBEDU","GP":"THOTTAMBEDU","La":13.8445,"Lo":79.7543},
{"M":"THOTTAMBEDU","GP":"BONUPALLE","La":13.8212,"Lo":79.7211},
]

PRICES=[
{"p":"Tirupati APMC (RC Road)","la":13.6231,"lo":79.4125,"t":29,"y":34},
{"p":"Pakala Main Mango APMC","la":13.4568,"lo":79.1174,"t":27,"y":32},
{"p":"Railway Kodur APMC Yard","la":13.9515,"lo":79.3514,"t":28,"y":33},
{"p":"Puttur Mango Market Yard","la":13.4428,"lo":79.5531,"t":41,"y":44},
{"p":"Chandragiri APMC","la":13.5828,"lo":79.3142,"t":25,"y":30},
{"p":"Srikalahasti APMC","la":13.7498,"lo":79.7034,"t":30,"y":35},
{"p":"Venkatagiri APMC","la":13.9575,"lo":79.5847,"t":28,"y":33},
{"p":"Nagalapuram APMC","la":13.3985,"lo":79.7915,"t":27,"y":32},
{"p":"Naidupeta APMC","la":13.9142,"lo":79.8944,"t":29,"y":34},
{"p":"Satyavedu APMC","la":13.5076,"lo":79.9715,"t":26,"y":31},
{"p":"Sullurpeta APMC","la":13.7008,"lo":80.0211,"t":25,"y":30},
{"p":"Bangarupalem","la":13.2,"lo":78.9333,"t":34,"y":42},
{"p":"Chittoor","la":13.2172,"lo":79.1003,"t":36,"y":39},
{"p":"Punganur","la":13.3667,"lo":78.5667,"t":29,"y":36},
{"p":"Pakala","la":13.4667,"lo":79.1167,"t":37,"y":41},
{"p":"Pileru","la":13.65,"lo":78.95,"t":34,"y":39},
{"p":"Madanapalle AMC","la":13.6114,"lo":78.4716,"t":33,"y":40},
{"p":"Gurramkonda e-NAM","la":13.782,"lo":78.584,"t":39,"y":45},
{"p":"Galiveedu Market Yard","la":14.1035,"lo":78.5142,"t":36,"y":43},
{"p":"Jamiya Mango Yard","la":14.0562,"lo":78.751,"t":38,"y":45},
{"p":"Nimmanapalle Yard","la":13.5932,"lo":78.6011,"t":38,"y":44},
{"p":"Burakayalakota Hub","la":13.801,"lo":78.354,"t":39,"y":41},
{"p":"Nandini Private Mandi","la":13.5824,"lo":78.5025,"t":37,"y":39},
{"p":"Chowdepalle Yard","la":13.4116,"lo":78.6148,"t":36,"y":45},
]
PROCESSING=[
{"n":"Galla Foods Rayachoti","la":14.0585,"lo":78.749},
{"n":"Roshan Fruits India","la":13.6517,"lo":78.9415},
{"n":"Sri Varsha Food Products","la":13.6275,"lo":79.4312},
{"n":"Hayath Foods","la":13.6212,"lo":79.468},
{"n":"Grofresh Agrofoods","la":14.1825,"lo":79.171},
{"n":"Srini Food Park","la":13.185,"lo":78.961},
{"n":"Sree Sannidhi Foods","la":14.2015,"lo":79.145},
{"n":"Ohms Food Products","la":14.061,"lo":78.7425},
{"n":"Navya Foods Pvt Ltd","la":14.085,"lo":78.7315},
{"n":"Bright Mangoes","la":13.935,"lo":79.365},
{"n":"PLR Foods Pvt Ltd","la":13.0639,"lo":78.8248},
{"n":"Vijay Food Processing","la":13.2092,"lo":79.1326},
]
PULP=[
{"n":"PLR Foods Pvt Ltd","la":13.0639,"lo":78.8248},
{"n":"Vijay Food Processing","la":13.2092,"lo":79.1326},
{"n":"Galla Foods Ltd","la":13.2092,"lo":79.1326},
{"n":"Srini Food Park","la":13.2106,"lo":79.1161},
{"n":"Sree Sannidhi Foods","la":13.2148,"lo":79.0982},
{"n":"Hayath Foods","la":13.3091,"lo":79.0774},
{"n":"Navya Foods Pvt Ltd","la":14.1952,"lo":79.1573},
{"n":"Grofresh Agrofoods","la":13.6541,"lo":78.9489},
{"n":"B M Fruits","la":13.6425,"lo":79.5033},
{"n":"Paiyur Group Mango Pulp","la":14.042,"lo":78.761},
]
PICKLE=[
{"n":"Rayachoti Pickles","la":14.0585,"lo":78.749},
{"n":"Tirupati Pickle Works","la":13.629,"lo":79.4285},
{"n":"Padmavathi Pickles","la":13.6025,"lo":79.441},
{"n":"Puttur Pickle Makers","la":13.4415,"lo":79.553},
{"n":"Srikalahasti Pickle Industries","la":13.755,"lo":79.7045},
{"n":"Pileru Pickle Works","la":13.6515,"lo":78.941},
{"n":"Punganur Mango Pickle","la":13.364,"lo":78.5825},
{"n":"Kalikiri Pickle","la":13.645,"lo":78.782},
{"n":"Chittoor Pack Pickle","la":13.2215,"lo":79.112},
{"n":"Madanapalle Pickle","la":13.551,"lo":78.5215},
]
LOCAL_X=[
{"n":"Rayachoti APMC Export","la":14.062,"lo":78.742},
{"n":"Rajampet APMC","la":14.1885,"lo":79.156},
{"n":"Tirupati APMC Export","la":13.6285,"lo":79.4192},
{"n":"Renigunta Packhouse","la":13.6385,"lo":79.5068},
{"n":"Srikalahasti Cold Room","la":13.751,"lo":79.702},
{"n":"Puttur Export Yard","la":13.445,"lo":79.548},
{"n":"Bangarupalem APMC","la":13.212,"lo":78.968},
{"n":"Chittoor APMC","la":13.2115,"lo":79.112},
{"n":"Punganur Market Yard","la":13.362,"lo":78.5805},
{"n":"Pileru Packhouse","la":13.6515,"lo":78.941},
]
ABROAD_X=[
{"n":"Tirupati APMC Int Export","la":13.6288,"lo":79.4192},
{"n":"Renigunta Cold Room Export","la":13.6519,"lo":79.5126},
{"n":"Rayachoti APMC Int","la":14.0532,"lo":78.7516},
{"n":"Rajampet APMC Int","la":14.195,"lo":79.1585},
{"n":"Srikalahasti Int Collection","la":13.749,"lo":79.702},
{"n":"Chandragiri Packhouse","la":13.566,"lo":79.317},
{"n":"Grofresh Export Pack","la":13.215,"lo":79.055},
{"n":"Roshan Fruits Export","la":14.06,"lo":78.755},
{"n":"Navya Foods Export","la":13.21,"lo":78.745},
{"n":"Bright Mangoes Export","la":13.205,"lo":78.76},
]

RCOLS=["#e74c3c","#3498db","#2ecc71","#f39c12","#9b59b6","#1abc9c","#e67e22","#e91e63","#00bcd4","#8bc34a"]
CCAT_COLORS={"Mandi":"#dbeafe","Processing":"#f3e8ff","Pulp":"#fef9c3",
             "Pickle":"#fce7f3","Local Export":"#dcfce7","Abroad Export":"#ccfbf1"}
CCAT_TEXT={"Mandi":"#1e40af","Processing":"#7e22ce","Pulp":"#a16207",
           "Pickle":"#be185d","Local Export":"#15803d","Abroad Export":"#0f766e"}

def hav(la1,lo1,la2,lo2):
    R=6371
    a=math.sin(math.radians((la2-la1)/2))**2+math.cos(math.radians(la1))*math.cos(math.radians(la2))*math.sin(math.radians((lo2-lo1)/2))**2
    return R*2*math.asin(math.sqrt(a))

def get_bp(vla,vlo):
    best,price=float("inf"),29
    for p in PRICES:
        d=hav(vla,vlo,p["la"],p["lo"])
        if d<best: best=d; price=p["t"]
    return price

def compute(vla,vlo,bp,qty,var):
    acc={"Mandi":["Banganapalli","Totapuri","Neelam","Rasalu"],
         "Processing":["Totapuri","Neelam"],"Pulp":["Totapuri"],
         "Pickle":["Totapuri","Rasalu"],"Local Export":["Banganapalli"],
         "Abroad Export":["Banganapalli"]}
    mg={"Mandi":0,"Processing":0.03,"Pulp":0.04,"Pickle":0.025,
        "Local Export":0.05,"Abroad Export":0.07}
    ds={"Mandi":[(p["p"],p["la"],p["lo"]) for p in PRICES],
        "Processing":[(r["n"],r["la"],r["lo"]) for r in PROCESSING],
        "Pulp":[(r["n"],r["la"],r["lo"]) for r in PULP],
        "Pickle":[(r["n"],r["la"],r["lo"]) for r in PICKLE],
        "Local Export":[(r["n"],r["la"],r["lo"]) for r in LOCAL_X],
        "Abroad Export":[(r["n"],r["la"],r["lo"]) for r in ABROAD_X]}
    res,seen=[],set()
    for cat,rows in ds.items():
        if var not in acc[cat]: continue
        for nm,la,lo in rows:
            k=f"{nm}|{cat}"
            if k in seen: continue
            seen.add(k)
            dist=hav(vla,vlo,la,lo)
            rev=bp*(1+mg[cat])*100*qty
            tran=dist*12*qty
            res.append({"Cat":cat,"Name":nm,"Dist":round(dist,1),
                        "Rev":int(rev),"Trans":int(tran),"Net":int(rev-tran),
                        "La":la,"Lo":lo})
    res.sort(key=lambda x:-x["Net"])
    return res[:10]

# ── SESSION STATE ──
for k,v in [("lang","en"),("li",False),("un",""),("fn",""),
             ("am","login"),("var","Banganapalli"),("res",None)]:
    if k not in st.session_state: st.session_state[k]=v

lang=st.session_state.lang; tr=T[lang]

def lang_bar(show_logout=False):
    cols=st.columns([1,1,1,1,4,1] if show_logout else [1,1,1,1,6])
    for col,l,lbl in zip(cols[:4],["en","te","hi","ta"],["🇬🇧 EN","తె","हि","த"]):
        with col:
            if st.button(lbl,use_container_width=True,
                         type="primary" if st.session_state.lang==l else "secondary",
                         key=f"lb_{l}"):
                st.session_state.lang=l; st.rerun()
    if show_logout:
        with cols[5]:
            if st.button(f"🔴",use_container_width=True,key="logout_btn"):
                st.session_state.li=False; st.session_state.res=None; st.rerun()

def hero_html(tr):
    return f"""<div class="hero">
  <div class="hero-emojis">
    <span class="e1">🥭</span><span class="e2">🌿</span><span class="e3">🌾</span>
    <span class="e4">💚</span><span class="e5">🥭</span>
  </div>
  <div class="hero-title">{tr["title"]}</div>
  <div class="hero-sub">{tr["subtitle"]}</div>
</div>"""

def ticker_html(tr,lang):
    items=""
    for p in PRICES:
        d=p["t"]-p["y"]; ar="▲" if d>=0 else "▼"; cl="tu" if d>=0 else "td"
        pn=tm(p["p"],lang)
        items+=f'<span class="tick"><span class="tp">{pn}</span><span class="tv">₹{p["t"]}/kg</span><span class="{cl}">{ar}{abs(d)}</span></span>'
    dbl=items+items
    return f'''<div class="ticker-wrap">
  <div class="ticker-lbl">📈 {tr["ticker_lbl"]}</div>
  <div class="ticker-scroll"><div class="ticker-inner">{dbl}</div></div>
</div>'''

# ── AUTH ──
if not st.session_state.li:
    lang_bar()
    tr=T[st.session_state.lang]; lang=st.session_state.lang
    st.markdown(hero_html(tr),unsafe_allow_html=True)
    st.markdown(ticker_html(tr,lang),unsafe_allow_html=True)
    st.markdown('''<div class="gif-strip">
      <div class="gif-item"><img src="https://media.giphy.com/media/l0HlBO7eyXzSZkJri/giphy.gif" width="170" height="128" style="display:block"/></div>
      <div class="gif-item"><img src="https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif" width="170" height="128" style="display:block"/></div>
      <div class="gif-item"><img src="https://media.giphy.com/media/xT9IgG50Lg7rusRgre/giphy.gif" width="170" height="128" style="display:block"/></div>
      <div class="gif-item"><img src="https://media.giphy.com/media/l46CyJmS9KUbokzsI/giphy.gif" width="170" height="128" style="display:block"/></div>
    </div>''',unsafe_allow_html=True)

    _,ca,_=st.columns([1,1.8,1])
    with ca:
        if st.session_state.am=="login":
            st.markdown(f'''<div class="auth-wrap">
              <div class="auth-title">{tr["login_title"]}</div>
              <div class="auth-sub">🌾 {tr["subtitle"]}</div>''',unsafe_allow_html=True)
            with st.form("lf",clear_on_submit=False):
                un=st.text_input(tr["username"],placeholder=tr["username"])
                pw=st.text_input(tr["password"],type="password",placeholder="••••••••")
                if st.form_submit_button(tr["login_btn"],use_container_width=True,type="primary"):
                    if not un or not pw: st.error("⚠️ Please fill all fields")
                    else:
                        ok,msg=login_user(un,pw)
                        if ok:
                            st.session_state.li=True; st.session_state.un=un
                            st.session_state.fn=msg; st.balloons(); st.rerun()
                        else: st.error(f"❌ {msg}")
            st.markdown("</div>",unsafe_allow_html=True)
            if st.button(f"📝 {tr['no_account']}",use_container_width=True,key="go_reg"):
                st.session_state.am="register"; st.rerun()
        else:
            st.markdown(f'''<div class="auth-wrap">
              <div class="auth-title">{tr["reg_title"]}</div>
              <div class="auth-sub">🥭 Join thousands of farmers!</div>''',unsafe_allow_html=True)
            with st.form("rf",clear_on_submit=False):
                fn=st.text_input(tr["full_name"],placeholder=tr["name_ph"])
                un=st.text_input(tr["username"],placeholder=tr["username"])
                ph=st.text_input(tr["phone"],placeholder="9XXXXXXXXX")
                pw=st.text_input(tr["password"],type="password",placeholder="Min 6 characters")
                pw2=st.text_input("Confirm Password",type="password",placeholder="Re-enter password")
                if st.form_submit_button(tr["reg_btn"],use_container_width=True,type="primary"):
                    if not fn or not un or not pw: st.error("⚠️ Fill all required fields")
                    elif pw!=pw2: st.error("❌ Passwords do not match!")
                    elif len(pw)<6: st.error("❌ Password needs min 6 characters")
                    else:
                        ok,msg=register_user(un,pw,fn,ph)
                        if ok: st.success(f"✅ {msg}"); st.session_state.am="login"; st.rerun()
                        else: st.error(f"❌ {msg}")
            st.markdown("</div>",unsafe_allow_html=True)
            if st.button(f"👤 {tr['have_account']}",use_container_width=True,key="go_login"):
                st.session_state.am="login"; st.rerun()
    st.stop()

# ── MAIN APP ──
lang=st.session_state.lang; tr=T[lang]
lang_bar(show_logout=True)
tr=T[st.session_state.lang]; lang=st.session_state.lang

st.markdown(hero_html(tr),unsafe_allow_html=True)
st.markdown(ticker_html(tr,lang),unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"### 👋 {tr['namaste']}")
    st.markdown(f"**{st.session_state.fn}** 🌾")
    st.markdown("---")
    fname=st.text_input(tr["lname"],value=st.session_state.fn,placeholder=tr["name_ph"])
    mandals=sorted(set(v["M"] for v in VILLAGES))
    mdmap={tmt(m,lang):m for m in mandals}
    selmd=st.selectbox(tr["mandal_lbl"],["— "+tr["mandal_ph"]+" —"]+sorted(mdmap.keys()))
    vval=None
    if selmd and not selmd.startswith("—"):
        men=mdmap[selmd]
        vills=[v["GP"] for v in VILLAGES if v["M"]==men]
        vmap={tv(v,lang):v for v in vills}
        selvd=st.selectbox(tr["lvillage"],["— "+tr["village_ph"]+" —"]+sorted(vmap.keys()))
        if selvd and not selvd.startswith("—"): vval=vmap[selvd]
    else:
        st.selectbox(tr["lvillage"],["— "+tr["village_ph"]+" —"],disabled=True)
    st.markdown(f"**{tr['lvar']}**")
    vc=st.columns(2)
    for i,v in enumerate(["Banganapalli","Totapuri","Neelam","Rasalu"]):
        lbl=tr["var_labels"][v]
        with vc[i%2]:
            if st.button(lbl,key=f"vb_{v}",use_container_width=True,
                         type="primary" if v==st.session_state.var else "secondary"):
                st.session_state.var=v; st.rerun()
    qty=st.number_input(tr["lqty"],min_value=1,max_value=500,value=10)
    st.markdown("<br>",unsafe_allow_html=True)
    run=st.button(tr["run_btn"],use_container_width=True,type="primary")
    st.markdown(f'<div class="tip-box">{tr["tip"]}</div>',unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"**{tr['prices_title']}**")
    show_p=PRICES
    if vval:
        vr=next((v for v in VILLAGES if v["GP"]==vval),None)
        if vr: show_p=sorted(PRICES,key=lambda p:hav(vr["La"],vr["Lo"],p["la"],p["lo"]))[:8]
    for p in show_p[:8]:
        d=p["t"]-p["y"]; ic="🟢" if d>=0 else "🔴"
        chg=f"+{d}" if d>=0 else str(d)
        pn=tm(p["p"],lang)
        st.markdown(f"{ic} **{pn[:26]}**  \n₹{p['t']}/kg ({chg})")

if run:
    if not vval: st.error("⚠️ "+("Please select your village first!" if lang=="en" else "మీ గ్రామం ఎంచుకోండి!" if lang=="te" else "गांव चुनें!" if lang=="hi" else "கிராமம் தேர்ந்தெடுக்கவும்!"))
    else:
        vr=next((v for v in VILLAGES if v["GP"]==vval),None)
        if vr:
            bp=get_bp(vr["La"],vr["Lo"])
            with st.spinner("🔄 Analyzing..."):
                top10=compute(vr["La"],vr["Lo"],bp,qty,st.session_state.var)
            if top10:
                st.session_state.res={"data":top10,"fn":fname or st.session_state.fn,
                    "vill":vval,"bp":bp,"qty":qty,"vla":vr["La"],"vlo":vr["Lo"],
                    "var":st.session_state.var}
            else: st.warning("No results. Try Banganapalli or Totapuri.")

if st.session_state.res:
    R=st.session_state.res; t10=R["data"]; best=t10[0]
    vd=tv(R["vill"],lang)

    st.markdown(f'''<div class="namaste-bar">
      🥭 {tr["namaste"]}, <span style="color:#ffd166;font-size:1.1em">{R["fn"]}</span>
      &nbsp;·&nbsp; 🏘️ {vd} &nbsp;·&nbsp; 🥭 {R["var"]}
      &nbsp;·&nbsp; 📦 {R["qty"]} {tr["qty_label"]}
    </div>''',unsafe_allow_html=True)

    m1,m2,m3,m4=st.columns(4)
    with m1: st.markdown(f'''<div class="mc"><div class="lbl">📈 {tr["base_price"]}</div>
      <div class="val">₹{R["bp"]}/kg</div><div class="sub">{vd}</div></div>''',unsafe_allow_html=True)
    with m2: st.markdown(f'''<div class="mc"><div class="lbl">📦 {tr["qty_lbl"]}</div>
      <div class="val">{R["qty"]} qtl</div><div class="sub">{R["qty"]*100} kg total</div></div>''',unsafe_allow_html=True)
    with m3: st.markdown(f'''<div class="mc best"><div class="lbl">🏆 {tr["best_profit"]}</div>
      <div class="val">₹{best["Net"]:,}</div>
      <div class="sub">{tm(best["Name"],lang)[:28]}</div></div>''',unsafe_allow_html=True)
    with m4:
        diff=best["Net"]-t10[1]["Net"] if len(t10)>1 else 0
        st.markdown(f'''<div class="mc"><div class="lbl">🥭 {tr["best_market"]}</div>
          <div class="val" style="font-size:14px;line-height:1.25">{tm(best["Name"],lang)[:22]}</div>
          <div class="sub">{best["Dist"]} km · {tc(best["Cat"],lang)}</div></div>''',unsafe_allow_html=True)

    st.markdown("<hr class='sdivider'>",unsafe_allow_html=True)
    tab1,tab2,tab3,tab4=st.tabs([tr["tab1"],tr["tab2"],tr["tab3"],tr["tab4"]])

    with tab1:
        # ── PODIUM TOP 3 ──
        st.markdown(f"#### {tr['podium_title']}")
        st.markdown(f'<p style="color:#6b9e80;font-size:13px;margin-bottom:16px">{tr["top3_sub"]}</p>',unsafe_allow_html=True)
        crowns=["👑","🥈","🥉"]
        pod_classes=["pod1","pod2","pod3"]
        pod_cols=st.columns(3)
        for i,(col,r) in enumerate(zip(pod_cols,t10[:3])):
            ctag=tc(r["Cat"],lang); cname=tm(r["Name"],lang)
            cbg=CCAT_COLORS.get(r["Cat"],"#e8f5e9"); ctxt=CCAT_TEXT.get(r["Cat"],"#1b4332")
            with col:
                st.markdown(f'''<div class="{pod_classes[i]} pod">
                  <span class="pod-crown">{crowns[i]}</span>
                  <div class="pod-rank">#{i+1} {"BEST CHOICE" if i==0 else "2nd BEST" if i==1 else "3rd BEST"}</div>
                  <div class="pod-name">{cname}</div>
                  <span class="pod-cat" style="background:{cbg};color:{ctxt}">{ctag}</span>
                  <div class="pod-profit">₹{r["Net"]:,}</div>
                  <div class="pod-dist">📍 {r["Dist"]} km away</div>
                </div>''',unsafe_allow_html=True)

        st.markdown(f"<br>#### {tr['full_table']}",unsafe_allow_html=True)
        mp=best["Net"]; rows=""
        for i,r in enumerate(t10):
            pct=int(r["Net"]/mp*100) if mp>0 else 0
            medal="🥇" if i==0 else "🥈" if i==1 else "🥉" if i==2 else f"#{i+1}"
            rc="rb1" if i==0 else "rb2" if i==1 else "rb3" if i==2 else "rbn"
            tc_=tc(r["Cat"],lang); cname=tm(r["Name"],lang)
            ck=r["Cat"].replace(" ","")
            bar=f'<div class="pbar-wrap"><div class="pbar-bg"><div class="pbar-fill" style="width:{pct}%"></div></div><span style="font-size:11px;color:#6b9e80;white-space:nowrap">{pct}%</span></div>'
            tr_cls="top1" if i==0 else "top2" if i==1 else "top3" if i==2 else ""
            rows+=f'<tr class="{tr_cls}"><td><span class="rb {rc}">{medal}</span></td><td><b>{cname}</b></td><td><span class="cat-tag {ck}">{tc_}</span></td><td>{r["Dist"]} km</td><td>₹{r["Rev"]:,}</td><td>₹{r["Trans"]:,}</td><td><b style="color:#1b4332;font-size:14px">₹{r["Net"]:,}</b></td><td>{bar}</td></tr>'
        st.markdown(f'''<div style="overflow-x:auto;border-radius:16px;border:2px solid #d1fae5;
          box-shadow:0 4px 20px rgba(45,106,79,0.1);overflow:hidden">
          <table class="rtable"><thead><tr>
            <th>{tr["rank"]}</th><th>{tr["market"]}</th><th>{tr["cat"]}</th>
            <th>{tr["dist"]}</th><th>{tr["rev"]}</th><th>{tr["trans"]}</th>
            <th>{tr["profit"]}</th><th>{tr["pct"]}</th>
          </tr></thead><tbody>{rows}</tbody></table></div>''',unsafe_allow_html=True)

        # ── CSV DOWNLOAD — UTF-8 BOM for Excel ──
        st.markdown("<br>",unsafe_allow_html=True)
        rows_dl=[]
        for i,r in enumerate(t10):
            rows_dl.append({
                tr["rank"]: i+1,
                tr["market"]: tm(r["Name"],lang),
                tr["cat"]: tc(r["Cat"],lang),
                tr["dist"]: r["Dist"],
                tr["rev"]: r["Rev"],
                tr["trans"]: r["Trans"],
                tr["profit"]: r["Net"],
            })
        df=pd.DataFrame(rows_dl)
        # UTF-8 with BOM — Excel opens Telugu/Hindi correctly
        import io
        buf=io.StringIO()
        df.to_csv(buf,index=False,encoding="utf-8")
        csv_bytes=("\ufeff"+buf.getvalue()).encode("utf-8")
        st.download_button(tr["dl_csv"],csv_bytes,
            f"mango_top10_{R['vill']}.csv","text/csv;charset=utf-8-sig",
            use_container_width=True)

    with tab2:
        ca,cb=st.columns(2)
        with ca:
            st.markdown(f"#### {tr['chart_title']}")
            names=[tm(r["Name"],lang) for r in t10]
            names_short=[n[:20]+"…" if len(n)>20 else n for n in names]
            fig=go.Figure()
            fig.add_trace(go.Bar(name=tr["profit"],y=names_short,x=[r["Net"] for r in t10],
                orientation="h",marker=dict(color=RCOLS[:len(t10)]),
                text=[f"₹{r['Net']:,}" for r in t10],textposition="auto"))
            fig.add_trace(go.Bar(name=tr["trans"],y=names_short,x=[r["Trans"] for r in t10],
                orientation="h",marker_color="rgba(252,211,77,0.65)",
                text=[f"₹{r['Trans']:,}" for r in t10],textposition="auto"))
            fig.update_layout(barmode="group",height=460,plot_bgcolor="#f0fdf4",
                paper_bgcolor="white",xaxis_title="₹ Amount",
                font=dict(family="Poppins"),legend=dict(orientation="h",y=1.08),
                margin=dict(l=10,r=10,t=40,b=10))
            st.plotly_chart(fig,use_container_width=True)
        with cb:
            st.markdown(f"#### {tr['pie_title']}")
            cs={}
            for r in t10:
                k=tc(r["Cat"],lang); cs[k]=cs.get(k,0)+r["Net"]
            fp=px.pie(names=list(cs.keys()),values=list(cs.values()),
                color_discrete_sequence=["#1b4332","#52b788","#f39c12","#e74c3c","#3498db","#9b59b6"],
                hole=0.48)
            fp.update_traces(textposition="inside",textinfo="percent+label",
                marker=dict(line=dict(color="white",width=3)))
            fp.update_layout(height=460,font=dict(family="Poppins"),
                showlegend=True,legend=dict(orientation="h",y=-0.2),
                margin=dict(l=10,r=10,t=10,b=10))
            st.plotly_chart(fp,use_container_width=True)
        st.markdown("<hr class='sdivider'>",unsafe_allow_html=True)
        st.markdown(f"#### {tr['prices_title']}")
        np2=sorted(PRICES,key=lambda p:hav(R["vla"],R["vlo"],p["la"],p["lo"]))[:12]
        fp2=go.Figure()
        fp2.add_trace(go.Bar(name=tr["today_lbl"],
            x=[tm(p["p"],lang) for p in np2],y=[p["t"] for p in np2],
            marker_color=["#2d6a4f" if p["t"]>=p["y"] else "#e74c3c" for p in np2],
            text=[f"₹{p['t']}" for p in np2],textposition="auto"))
        fp2.add_trace(go.Bar(name=tr["yest_lbl"],
            x=[tm(p["p"],lang) for p in np2],y=[p["y"] for p in np2],
            marker_color="rgba(200,200,200,0.6)",
            text=[f"₹{p['y']}" for p in np2],textposition="auto"))
        fp2.update_layout(barmode="group",height=400,plot_bgcolor="#f0fdf4",
            yaxis_title="₹ per kg",xaxis_tickangle=-40,
            font=dict(family="Poppins"),legend=dict(orientation="h",y=1.08),
            margin=dict(l=10,r=10,t=40,b=100))
        st.plotly_chart(fp2,use_container_width=True)

    with tab3:
        st.markdown(f"#### 🗺️ {tr['tab3']} — Each color = different alternative")
        fm=go.Figure()
        vd_map=tv(R["vill"],lang)
        fm.add_trace(go.Scattermapbox(lat=[R["vla"]],lon=[R["vlo"]],mode="markers+text",
            marker=dict(size=24,color="#0d2b1a",symbol="star"),
            text=[f"🏘️ {vd_map}"],textposition="top right",name=f"🏘️ {vd_map}",
            hovertemplate=f"<b>Your Village</b><br>{vd_map}<extra></extra>"))
        for i,r in enumerate(t10):
            col=RCOLS[i%len(RCOLS)]
            medal="🥇" if i==0 else "🥈" if i==1 else "🥉" if i==2 else f"#{i+1}"
            cname=tm(r["Name"],lang); ctag=tc(r["Cat"],lang)
            fm.add_trace(go.Scattermapbox(lat=[R["vla"],r["La"]],lon=[R["vlo"],r["Lo"]],
                mode="lines",line=dict(width=4 if i==0 else 2.5 if i<3 else 1.8,color=col),
                opacity=0.9 if i==0 else 0.7 if i<3 else 0.55,
                showlegend=False,hoverinfo="skip"))
            fm.add_trace(go.Scattermapbox(lat=[r["La"]],lon=[r["Lo"]],mode="markers+text",
                marker=dict(size=20 if i==0 else 16 if i<3 else 13,color=col),
                text=[medal],textposition="top center",
                name=f"{medal} {cname[:30]}",
                hovertemplate=(f"<b>{medal} {cname}</b><br>"
                    f"Type: {ctag}<br>Distance: {r['Dist']} km<br>"
                    f"Revenue: ₹{r['Rev']:,}<br>Transport: ₹{r['Trans']:,}<br>"
                    f"<b>Net Profit: ₹{r['Net']:,}</b><extra></extra>")))
        fm.update_layout(
            mapbox=dict(style="open-street-map",center=dict(lat=R["vla"],lon=R["vlo"]),zoom=8),
            height=560,margin=dict(l=0,r=0,t=0,b=0),
            legend=dict(orientation="v",x=0.01,y=0.99,
                bgcolor="rgba(255,255,255,0.92)",bordercolor="#d1fae5",
                borderwidth=2,font=dict(size=11,family="Poppins")),
            font=dict(family="Poppins"))
        st.plotly_chart(fm,use_container_width=True)
        st.markdown("**🎨 Color Legend:**")
        lc=st.columns(5)
        for i,r in enumerate(t10):
            medal="🥇" if i==0 else "🥈" if i==1 else "🥉" if i==2 else f"#{i+1}"
            cname=tm(r["Name"],lang)
            with lc[i%5]:
                st.markdown(f'''<div style="display:flex;align-items:center;gap:6px;margin-bottom:8px;
                  padding:6px 8px;background:white;border-radius:8px;border:1px solid #d1fae5">
                  <div style="width:14px;height:14px;border-radius:50%;background:{RCOLS[i%len(RCOLS)]};flex-shrink:0;box-shadow:0 1px 4px rgba(0,0,0,0.2)"></div>
                  <span style="font-size:11px;font-weight:600;color:#1b4332">{medal} {cname[:16]}</span>
                </div>''',unsafe_allow_html=True)

    with tab4:
        vl=tr["var_labels"].get(R["var"],R["var"]).split("\n")[0]
        st.markdown(f"#### {tr['adv_title']} — {vl}")
        ac1,ac2=st.columns(2)
        for i,(icon,title,body) in enumerate(tr["adv"]):
            with [ac1,ac2][i%2]:
                st.markdown(f'''<div class="adv-card">
                  <span class="adv-icon">{icon}</span>
                  <div class="adv-title">{title}</div>
                  <div class="adv-body">{body}</div>
                </div>''',unsafe_allow_html=True)
        st.markdown('''<div style="background:linear-gradient(135deg,#0d2b1a,#1b4332,#2d6a4f);
          border-radius:18px;padding:24px;text-align:center;margin-top:20px">
          <div style="font-size:40px;margin-bottom:10px;letter-spacing:8px">
            🌾 🥭 💚 🌿 🏡 🚛 💰
          </div>
          <p style="color:#a7f3d0;font-size:14px;margin:0;font-weight:500">
            Empowering Indian Mango Farmers with Market Intelligence 🇮🇳
          </p>
        </div>''',unsafe_allow_html=True)

else:
    st.markdown(f'''<div style="text-align:center;padding:60px 20px;animation:fadeUp 0.8s ease">
      <div style="font-size:96px;animation:float3 3s ease-in-out infinite;display:inline-block">🥭</div>
      <h2 style="color:#1b4332;margin:20px 0 10px;font-size:2rem;font-weight:800">{tr["wctitle"]}</h2>
      <p style="color:#6b9e80;max-width:480px;margin:0 auto;line-height:1.75;font-size:14px">{tr["wcsub"]}</p>
    </div>''',unsafe_allow_html=True)
    st.markdown('''<div class="gif-strip">
      <div class="gif-item"><img src="https://media.giphy.com/media/l0HlBO7eyXzSZkJri/giphy.gif" width="190" height="142" style="display:block"/></div>
      <div class="gif-item"><img src="https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif" width="190" height="142" style="display:block"/></div>
      <div class="gif-item"><img src="https://media.giphy.com/media/xT9IgG50Lg7rusRgre/giphy.gif" width="190" height="142" style="display:block"/></div>
    </div>''',unsafe_allow_html=True)
    w1,w2,w3=st.columns(3)
    for col,(icon,title,sub) in zip([w1,w2,w3],[
        ("📍","Pick Your Village","We find all nearby markets, cold storages & buyers within 200km"),
        ("🥭","Choose Your Variety","Matched to right buyers — Export, Mandi, Processing, Pickle"),
        ("💰","Top 10 + Podium","See best 3 highlighted + full ranked table with profit comparison")]):
        with col:
            st.markdown(f'''<div class="wc-feat">
              <span class="wc-icon">{icon}</span>
              <div style="font-weight:800;color:#1b4332;font-size:15px;margin-bottom:6px">{title}</div>
              <div style="font-size:12px;color:#6b9e80;line-height:1.6">{sub}</div>
            </div>''',unsafe_allow_html=True)

st.markdown('''<div style="text-align:center;color:#8db49a;font-size:12px;
  padding:20px 0;margin-top:24px;border-top:2px solid #d1fae5;font-weight:500">
  🥭 Farmer\'s Mango Profit Navigator &nbsp;·&nbsp;
  Empowering farmers across Andhra Pradesh &nbsp;·&nbsp;
  🇮🇳 Made in India with ❤️
</div>''',unsafe_allow_html=True)
