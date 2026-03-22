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
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800;900&display=swap');
html,body,[class*="css"]{font-family:'Poppins',sans-serif}
.main{background:linear-gradient(135deg,#f0faf4 0%,#e8f5e9 50%,#f5f7f0 100%)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#1b4332 0%,#2d6a4f 60%,#1b4332 100%)!important}
[data-testid="stSidebar"] *{color:white!important}
[data-testid="stSidebar"] .stTextInput input,[data-testid="stSidebar"] .stSelectbox>div>div,[data-testid="stSidebar"] .stNumberInput input{background:rgba(255,255,255,0.15)!important;color:white!important;border:1px solid rgba(255,255,255,0.3)!important;border-radius:8px!important}
[data-testid="stSidebar"] label{color:#a7f3d0!important;font-weight:600}
@keyframes fadeSlideDown{from{opacity:0;transform:translateY(-30px)}to{opacity:1;transform:translateY(0)}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
@keyframes bounceIn{0%{opacity:0;transform:scale(0.3)}50%{opacity:1;transform:scale(1.05)}70%{transform:scale(0.9)}100%{transform:scale(1)}}
@keyframes gradientShift{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
@keyframes emojiFloat1{0%,100%{transform:translateY(0) rotate(0deg)}50%{transform:translateY(-20px) rotate(10deg)}}
@keyframes emojiFloat2{0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}
@keyframes sparkle{0%,100%{opacity:1;transform:scale(1)}50%{opacity:0.6;transform:scale(1.3)}}
@keyframes ticker{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.02)}}

.hero-banner{background:linear-gradient(270deg,#1b4332,#2d6a4f,#40916c,#52b788,#2d6a4f,#1b4332);background-size:400% 400%;animation:gradientShift 6s ease infinite,fadeSlideDown 0.8s ease;border-radius:20px;padding:36px 40px 28px;margin-bottom:20px;color:white;text-align:center;position:relative;overflow:hidden;box-shadow:0 8px 32px rgba(27,67,50,0.3)}
.hero-title{font-size:2.4rem;font-weight:900;margin:0;text-shadow:0 2px 12px rgba(0,0,0,0.3)}
.hero-sub{font-size:1.05rem;opacity:0.9;margin-top:8px}
.fe1{animation:emojiFloat1 3s ease-in-out infinite;font-size:28px;display:inline-block}
.fe2{animation:emojiFloat2 3.5s ease-in-out infinite 0.5s;font-size:24px;display:inline-block}
.fe3{animation:emojiFloat1 2.8s ease-in-out infinite 1s;font-size:26px;display:inline-block}

.ticker-wrap{background:linear-gradient(90deg,#0a2e14,#1b4332,#0a2e14);border-radius:10px;padding:12px 0;margin-bottom:18px;overflow:hidden;position:relative;box-shadow:0 4px 12px rgba(0,0,0,0.2)}
.ticker-label-fixed{position:absolute;left:0;top:0;height:100%;background:linear-gradient(90deg,#0a2e14 70%,transparent);padding:0 16px;display:flex;align-items:center;color:#6ee7b7;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;z-index:2;white-space:nowrap}
.ticker-inner{display:flex;animation:ticker 35s linear infinite}
.ticker-item{display:inline-flex;align-items:center;gap:6px;margin-right:36px;white-space:nowrap}
.ticker-place{color:#a7f3d0;font-size:12px}
.ticker-price{color:#ffd166;font-size:14px;font-weight:800}
.ticker-up{color:#4ade80}
.ticker-down{color:#f87171}

.metric-card{background:white;border:2px solid #c8e6c9;border-radius:16px;padding:20px;text-align:center;animation:bounceIn 0.5s ease;transition:transform 0.2s,box-shadow 0.2s;box-shadow:0 2px 12px rgba(45,106,79,0.08)}
.metric-card:hover{transform:translateY(-4px);box-shadow:0 8px 24px rgba(45,106,79,0.15)}
.metric-card.best{background:linear-gradient(135deg,#1b4332,#2d6a4f);border-color:#2d6a4f;color:white;box-shadow:0 4px 20px rgba(27,67,50,0.35)}
.metric-card .lbl{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.6px;color:#5a7a5f;margin-bottom:6px}
.metric-card.best .lbl{color:#a7f3d0}
.metric-card .val{font-size:26px;font-weight:800;color:#2d6a4f}
.metric-card.best .val{color:white}
.metric-card .sub{font-size:11px;color:#5a7a5f;margin-top:4px}
.metric-card.best .sub{color:#c8f0b0}

.result-table{width:100%;border-collapse:collapse;font-size:13px}
.result-table th{background:linear-gradient(90deg,#1b4332,#2d6a4f);color:white;font-weight:700;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;padding:12px 14px;text-align:left}
.result-table td{padding:11px 14px;border-bottom:1px solid #e8f5e9;vertical-align:middle}
.result-table tr:last-child td{border-bottom:none}
.result-table tr:hover td{background:#f0faf0}

.rank-badge{width:30px;height:30px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-weight:800;font-size:13px}
.r1{background:linear-gradient(135deg,#FFD700,#FFA500);color:#7a5c00;box-shadow:0 2px 8px rgba(255,215,0,0.4)}
.r2{background:linear-gradient(135deg,#C0C0C0,#A8A8A8);color:#333}
.r3{background:linear-gradient(135deg,#CD7F32,#A0522D);color:#fff}
.rn{background:#e8f5e9;color:#2d6a4f}

.profit-bar-wrap{display:flex;align-items:center;gap:8px}
.profit-bar-bg{height:8px;background:#e8f5e9;border-radius:4px;flex:1;min-width:50px;overflow:hidden}
.profit-bar-fill{height:8px;border-radius:4px;background:linear-gradient(90deg,#52b788,#2d6a4f)}

.cat-tag{display:inline-block;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;white-space:nowrap}
.Mandi{background:#e3f2fd;color:#1565C0}
.Processing{background:#f3e5f5;color:#6A1B9A}
.Pulp{background:#fff8e1;color:#F57F17}
.Pickle{background:#fce4ec;color:#880E4F}
.LocalExport{background:#e8f5e9;color:#1B5E20}
.AbroadExport{background:#e0f2f1;color:#004D40}

.advice-card{background:white;border:1.5px solid #c8e6c9;border-radius:14px;padding:18px;margin-bottom:14px;transition:transform 0.2s,box-shadow 0.2s}
.advice-card:hover{transform:translateY(-3px);box-shadow:0 6px 20px rgba(45,106,79,0.12)}
.advice-icon{font-size:30px;margin-bottom:10px;animation:sparkle 2s ease-in-out infinite;display:block}
.advice-title{font-weight:700;color:#2d6a4f;font-size:14px;margin-bottom:5px}
.advice-body{font-size:13px;color:#5a7a5f;line-height:1.6}

.auth-card{background:white;border:2px solid #c8e6c9;border-radius:20px;padding:36px 40px;box-shadow:0 8px 32px rgba(45,106,79,0.12);animation:bounceIn 0.6s ease}
.auth-title{font-size:1.8rem;font-weight:800;color:#2d6a4f;text-align:center;margin-bottom:6px}

.wc-feature{background:white;border:1.5px solid #c8e6c9;border-radius:14px;padding:20px 16px;text-align:center;transition:transform 0.2s;animation:bounceIn 0.5s ease}
.wc-feature:hover{transform:translateY(-4px)}
.wc-feat-icon{font-size:36px;margin-bottom:10px;animation:sparkle 2.5s ease-in-out infinite;display:block}

.tip-box{background:linear-gradient(135deg,#fffbeb,#fef3c7);border:1.5px solid #fcd34d;border-radius:12px;padding:13px 15px;font-size:12.5px;color:#78350f;line-height:1.6;margin-top:12px;animation:pulse 3s ease-in-out infinite}
.namaste-bar{background:linear-gradient(90deg,#1b4332,#2d6a4f,#40916c);color:white;border-radius:14px;padding:16px 22px;margin-bottom:20px;font-size:17px;font-weight:700;display:flex;align-items:center;gap:10px;animation:fadeSlideDown 0.6s ease;box-shadow:0 4px 16px rgba(27,67,50,0.25)}
.section-divider{height:3px;background:linear-gradient(90deg,transparent,#52b788,transparent);border:none;margin:20px 0;border-radius:2px}
.gif-strip{display:flex;gap:12px;overflow-x:auto;margin:12px 0;padding:8px 0;scrollbar-width:none;justify-content:center}
.gif-item{flex-shrink:0;border-radius:12px;overflow:hidden;border:2px solid #c8e6c9;box-shadow:0 2px 10px rgba(0,0,0,0.1);transition:transform 0.2s}
.gif-item:hover{transform:scale(1.05)}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#1b4332,#2d6a4f)!important;border:none!important;border-radius:10px!important;font-weight:700!important;font-size:15px!important;transition:all 0.2s!important;box-shadow:0 4px 14px rgba(27,67,50,0.3)!important}
.stButton>button[kind="primary"]:hover{transform:translateY(-2px)!important;box-shadow:0 8px 20px rgba(27,67,50,0.4)!important}
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
"en":{"title":"🥭 Farmer's Mango Profit Navigator","subtitle":"Find the Best Market. Earn the Highest Return.",
 "ticker_label":"LIVE PRICES","lname":"👤 Farmer Name","lvillage":"🏘️ Village","lvar":"🥭 Mango Variety",
 "lqty":"📦 Quantity (Quintals)","run_btn":"🚀 Find Best Market",
 "tip":"💡 Sell with nearby farmers to cut transport costs and boost profit!",
 "wctitle":"Welcome, Mango Farmer!","wcsub":"Select your village, variety, quantity — then click Find Best Market.",
 "namaste":"Namaste","base_price":"Today's Market Price","best_profit":"Best Net Profit",
 "best_market":"Best Market","your_village":"Your Village",
 "tab1":"🥭 Top 10 Options","tab2":"📊 Profit Charts","tab3":"🗺️ Market Map","tab4":"💡 Selling Advice",
 "rank":"Rank","market":"Market / Buyer","cat":"Type","dist":"Dist (km)",
 "rev":"Revenue (₹)","trans":"Transport (₹)","profit":"Net Profit (₹)",
 "chart_title":"Profit Comparison — Top 10","pie_title":"Profit Share by Category",
 "adv_title":"Selling Advice for","prices_title":"📈 Nearby Market Prices",
 "today_price":"Today","yesterday_price":"Yesterday",
 "adv":[("🌅","Best Time to Sell","Sell early morning — Mandi prices are highest before 9am."),
        ("🤝","Negotiate Better","Contact 2-3 buyers simultaneously. Show competitor prices."),
        ("🚛","Transport Tip","Combine load with neighbour farmers to split transport costs."),
        ("⭐","Quality Matters","Grade A fruit fetches 15-25% more. Sort before loading.")],
 "login":"Login","register":"Register","logout":"Logout",
 "login_title":"👤 Login to Continue","reg_title":"📝 Create Account",
 "username":"Username","password":"Password","full_name":"Full Name","phone":"Phone (optional)",
 "login_btn":"Login →","reg_btn":"Register →",
 "have_account":"Already have account? Login","no_account":"New user? Create account",
 "mandal_ph":"Select Mandal","village_ph":"Select Village","name_ph":"Enter your name","qty_label":"quintals",
 "var_labels":{"Banganapalli":"Banganapalli\n⭐ Export","Totapuri":"Totapuri\n⭐ Processing",
               "Neelam":"Neelam\n⭐ Mandi","Rasalu":"Rasalu\n⭐ Pickle"}},
"te":{"title":"🥭 రైతు మామిడి లాభాల నావిగేటర్","subtitle":"అత్యుత్తమ మార్కెట్ కనుగొనండి. అధిక లాభం సంపాదించండి.",
 "ticker_label":"నేటి ధరలు","lname":"👤 రైతు పేరు","lvillage":"🏘️ మీ గ్రామం","lvar":"🥭 మామిడి రకం",
 "lqty":"📦 పరిమాణం (క్వింటాల్లు)","run_btn":"🚀 అత్యుత్తమ మార్కెట్ కనుగొనండి",
 "tip":"💡 పొరుగు రైతులతో కలిసి అమ్మండి — రవాణా ఖర్చు తక్కువ!",
 "wctitle":"స్వాగతం, మామిడి రైతు!","wcsub":"మీ గ్రామం, రకం, పరిమాణం ఎంచుకుని క్లిక్ చేయండి.",
 "namaste":"నమస్తే","base_price":"నేటి మార్కెట్ ధర","best_profit":"అత్యధిక నికర లాభం",
 "best_market":"అత్యుత్తమ మార్కెట్","your_village":"మీ గ్రామం",
 "tab1":"🥭 టాప్ 10 ఎంపికలు","tab2":"📊 లాభాల పోలిక","tab3":"🗺️ మార్కెట్ మ్యాప్","tab4":"💡 అమ్మకపు సలహా",
 "rank":"వరుస","market":"మార్కెట్","cat":"రకం","dist":"దూరం (కి.మీ)",
 "rev":"ఆదాయం (₹)","trans":"రవాణా (₹)","profit":"నికర లాభం (₹)",
 "chart_title":"లాభాల పోలిక — టాప్ 10","pie_title":"వర్గం వారీ లాభం",
 "adv_title":"అమ్మకపు సలహా","prices_title":"📈 సమీప మార్కెట్ ధరలు",
 "today_price":"నేడు","yesterday_price":"నిన్న",
 "adv":[("🌅","అమ్మడానికి అత్యుత్తమ సమయం","తెల్లవారుజామున అమ్మండి — మండీలో ధరలు ఎక్కువగా ఉంటాయి."),
        ("🤝","మెరుగైన ధర చర్చించండి","2-3 మంది కొనుగోలుదారులను ఒకేసారి సంప్రదించండి."),
        ("🚛","రవాణా సూచన","పొరుగు రైతులతో కలిసి రవాణా చేయండి."),
        ("⭐","నాణ్యత ముఖ్యం","గ్రేడ్ A మామిడి 15-25% ఎక్కువ ధర పొందుతుంది.")],
 "login":"లాగిన్","register":"రిజిస్టర్","logout":"లాగ్ అవుట్",
 "login_title":"👤 కొనసాగించడానికి లాగిన్","reg_title":"📝 ఖాతా సృష్టించండి",
 "username":"వినియోగదారు పేరు","password":"పాస్వర్డ్","full_name":"పూర్తి పేరు","phone":"ఫోన్ (ఐచ్ఛికం)",
 "login_btn":"లాగిన్ →","reg_btn":"రిజిస్టర్ →",
 "have_account":"ఖాతా ఉందా? లాగిన్","no_account":"కొత్తగా? ఖాతా సృష్టించండి",
 "mandal_ph":"మండల్ ఎంచుకోండి","village_ph":"గ్రామం ఎంచుకోండి","name_ph":"మీ పేరు","qty_label":"క్వింటాల్లు",
 "var_labels":{"Banganapalli":"బంగినపల్లి\n⭐ ఎగుమతి","Totapuri":"తోటపురి\n⭐ ప్రాసెసింగ్",
               "Neelam":"నీలం\n⭐ మండీ","Rasalu":"రసాలు\n⭐ ఊరగాయ"}},
"hi":{"title":"🥭 किसान का आम लाभ नेविगेटर","subtitle":"सबसे अच्छा बाजार खोजें। सबसे ज्यादा मुनाफा कमाएं।",
 "ticker_label":"आज के भाव","lname":"👤 किसान का नाम","lvillage":"🏘️ आपका गांव","lvar":"🥭 आम की किस्म",
 "lqty":"📦 मात्रा (क्विंटल)","run_btn":"🚀 सबसे अच्छा बाजार खोजें",
 "tip":"💡 पड़ोसी किसानों के साथ मिलकर बेचें — परिवहन लागत कम होगी!",
 "wctitle":"स्वागत है, आम किसान!","wcsub":"अपना गांव, किस्म और मात्रा चुनें — फिर क्लिक करें।",
 "namaste":"नमस्ते","base_price":"आज का बाजार भाव","best_profit":"सर्वाधिक शुद्ध लाभ",
 "best_market":"सबसे अच्छा बाजार","your_village":"आपका गांव",
 "tab1":"🥭 टॉप 10 विकल्प","tab2":"📊 लाभ तुलना","tab3":"🗺️ बाजार मानचित्र","tab4":"💡 बिक्री सलाह",
 "rank":"क्रम","market":"बाजार","cat":"प्रकार","dist":"दूरी (कि.मी.)",
 "rev":"आय (₹)","trans":"परिवहन (₹)","profit":"शुद्ध लाभ (₹)",
 "chart_title":"लाभ तुलना — टॉप 10","pie_title":"श्रेणी अनुसार लाभ",
 "adv_title":"बिक्री सलाह","prices_title":"📈 पास के बाजार के भाव",
 "today_price":"आज","yesterday_price":"कल",
 "adv":[("🌅","बेचने का सबसे अच्छा समय","सुबह जल्दी बेचें — मंडी में भाव ऊंचे होते हैं।"),
        ("🤝","बेहतर भाव मांगें","2-3 खरीदारों से एक साथ बात करें।"),
        ("🚛","परिवहन सुझाव","पड़ोसी किसानों के साथ मिलकर परिवहन करें।"),
        ("⭐","गुणवत्ता महत्वपूर्ण","ग्रेड A आम 15-25% ज्यादा भाव पाता है।")],
 "login":"लॉगिन","register":"रजिस्टर","logout":"लॉगआउट",
 "login_title":"👤 लॉगिन करें","reg_title":"📝 खाता बनाएं",
 "username":"यूज़रनेम","password":"पासवर्ड","full_name":"पूरा नाम","phone":"फोन (वैकल्पिक)",
 "login_btn":"लॉगिन →","reg_btn":"रजिस्टर →",
 "have_account":"खाता है? लॉगिन करें","no_account":"नए हैं? खाता बनाएं",
 "mandal_ph":"मंडल चुनें","village_ph":"गांव चुनें","name_ph":"अपना नाम","qty_label":"क्विंटल",
 "var_labels":{"Banganapalli":"बंगनपल्ली\n⭐ निर्यात","Totapuri":"तोतापुरी\n⭐ प्रसंस्करण",
               "Neelam":"नीलम\n⭐ मंडी","Rasalu":"रसालु\n⭐ अचार"}},
"ta":{"title":"🥭 விவசாயியின் மாம்பழ லாப வழிகாட்டி","subtitle":"சிறந்த சந்தையைக் கண்டறியுங்கள்.",
 "ticker_label":"இன்றைய விலைகள்","lname":"👤 விவசாயி பெயர்","lvillage":"🏘️ கிராமம்","lvar":"🥭 மாம்பழ வகை",
 "lqty":"📦 அளவு (குவிண்டால்)","run_btn":"🚀 சிறந்த சந்தையைக் கண்டறி",
 "tip":"💡 அண்டை விவசாயிகளுடன் சேர்ந்து விற்கவும்!",
 "wctitle":"வரவேற்கிறோம்!","wcsub":"கிராமம், வகை, அளவை தேர்ந்தெடுத்து கிளிக் செய்யுங்கள்.",
 "namaste":"வணக்கம்","base_price":"இன்றைய விலை","best_profit":"அதிகபட்ச லாபம்",
 "best_market":"சிறந்த சந்தை","your_village":"கிராமம்",
 "tab1":"🥭 சிறந்த 10","tab2":"📊 லாப ஒப்பீடு","tab3":"🗺️ வரைபடம்","tab4":"💡 ஆலோசனை",
 "rank":"வரிசை","market":"சந்தை","cat":"வகை","dist":"தூரம்",
 "rev":"வருவாய் (₹)","trans":"போக்குவரத்து (₹)","profit":"நிகர லாபம் (₹)",
 "chart_title":"லாப ஒப்பீடு","pie_title":"வகை வாரியான லாபம்",
 "adv_title":"விற்பனை ஆலோசனை","prices_title":"📈 சந்தை விலைகள்",
 "today_price":"இன்று","yesterday_price":"நேற்று",
 "adv":[("🌅","சிறந்த நேரம்","அதிகாலையில் விற்கவும் — விலை அதிகமாக இருக்கும்."),
        ("🤝","விலை பேசுங்கள்","2-3 வாங்குபவர்களிடம் ஒரே நேரத்தில் பேசுங்கள்."),
        ("🚛","போக்குவரத்து குறிப்பு","அண்டை விவசாயிகளுடன் சேர்ந்து போக்குவரத்து செய்யுங்கள்."),
        ("⭐","தரம் முக்கியம்","தரம் A மாம்பழம் 15-25% அதிக விலை பெறும்.")],
 "login":"உள்நுழைவு","register":"பதிவு","logout":"வெளியேறு",
 "login_title":"👤 உள்நுழைக","reg_title":"📝 கணக்கு உருவாக்கு",
 "username":"பயனர்பெயர்","password":"கடவுச்சொல்","full_name":"முழு பெயர்","phone":"தொலைபேசி (விருப்பம்)",
 "login_btn":"உள்நுழைவு →","reg_btn":"பதிவு →",
 "have_account":"கணக்கு உள்ளதா? உள்நுழைக","no_account":"புதியவரா? கணக்கு உருவாக்கு",
 "mandal_ph":"மண்டலம் தேர்ந்தெடு","village_ph":"கிராமம் தேர்ந்தெடு","name_ph":"உங்கள் பெயர்","qty_label":"குவிண்டால்",
 "var_labels":{"Banganapalli":"பங்கனபல்லி\n⭐ ஏற்றுமதி","Totapuri":"தொதாபுரி\n⭐ பதப்படுத்தல்",
               "Neelam":"நீலம்\n⭐ மண்டி","Rasalu":"ரசாலு\n⭐ ஊறுகாய்"}},
}

VTR={"te":{"BALAYAPALLI":"బాలయపల్లి","ALIMILI":"అలిమిలి","BHYRAVARAM":"భైరవారం","CHILAMANURU":"చిలమనూరు",
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
 "TADA":"ताडा","VENKATAGIRI":"वेंकटगिरि","PUTTUR":"पुत्तूर","SATYAVEDU":"सत्यवेडु"},
"ta":{"TIRUPATI (RURAL)":"திருப்பதி","CHANDRAGIRI":"சந்திரகிரி","PAKALA":"பாக்கல",
 "SRIKALAHASTHI":"ஸ்ரீகாளஹஸ்தி","RENIGUNTA":"ரேணிகுண்டா","SULLURPET":"சுல்லூர்பேட்",
 "VENKATAGIRI":"வெங்கடகிரி","PUTTUR":"புத்தூர்","SATYAVEDU":"சத்யவேடு"}}

CTR={"te":{"Mandi":"మండీ","Processing":"ప్రాసెసింగ్","Pulp":"పల్ప్","Pickle":"ఊరగాయ",
     "Local Export":"స్థానిక ఎగుమతి","Abroad Export":"విదేశీ ఎగుమతి"},
"hi":{"Mandi":"मंडी","Processing":"प्रसंस्करण","Pulp":"पल्प","Pickle":"अचार",
     "Local Export":"स्थानीय निर्यात","Abroad Export":"विदेश निर्यात"},
"ta":{"Mandi":"மண்டி","Processing":"பதப்படுத்தல்","Pulp":"பழச்சாறு","Pickle":"ஊறுகாய்",
     "Local Export":"உள்நாட்டு ஏற்றுமதி","Abroad Export":"வெளிநாட்டு ஏற்றுமதி"},
"en":{"Mandi":"Mandi","Processing":"Processing","Pulp":"Pulp","Pickle":"Pickle",
     "Local Export":"Local Export","Abroad Export":"Abroad Export"}}

def tv(n,l):
    if l=="en": return n
    return VTR.get(l,{}).get(n.upper(),n)
def tc(c,l): return CTR.get(l,CTR["en"]).get(c,c)

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

ROUTE_COLORS=["#e74c3c","#3498db","#2ecc71","#f39c12","#9b59b6","#1abc9c","#e67e22","#e91e63","#00bcd4","#8bc34a"]

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

# ── AUTH SCREEN ──
if not st.session_state.logged_in:
    lc1,lc2,lc3,lc4,_=st.columns([1,1,1,1,5])
    for col,l,lbl in zip([lc1,lc2,lc3,lc4],["en","te","hi","ta"],["🇬🇧 EN","తె","हि","த"]):
        with col:
            if st.button(lbl,use_container_width=True,type="primary" if lang==l else "secondary"):
                st.session_state.lang=l; st.rerun()
    tr=T[st.session_state.lang]

    st.markdown(f"""<div class="hero-banner">
      <div style="margin-bottom:12px"><span class="fe1">🥭</span>&nbsp;&nbsp;<span class="fe2">🌿</span>&nbsp;&nbsp;<span class="fe3">🌾</span>&nbsp;&nbsp;<span class="fe1">💚</span>&nbsp;&nbsp;<span class="fe2">🥭</span></div>
      <h1 class="hero-title">{tr["title"]}</h1>
      <p class="hero-sub">{tr["subtitle"]}</p></div>""", unsafe_allow_html=True)

    st.markdown("""<div class="gif-strip">
      <div class="gif-item"><img src="https://media.giphy.com/media/l0HlBO7eyXzSZkJri/giphy.gif" width="160" height="120" style="display:block"/></div>
      <div class="gif-item"><img src="https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif" width="160" height="120" style="display:block"/></div>
      <div class="gif-item"><img src="https://media.giphy.com/media/xT9IgG50Lg7rusRgre/giphy.gif" width="160" height="120" style="display:block"/></div>
      <div class="gif-item"><img src="https://media.giphy.com/media/l46CyJmS9KUbokzsI/giphy.gif" width="160" height="120" style="display:block"/></div>
    </div>""", unsafe_allow_html=True)

    _,ca,_=st.columns([1,2,1])
    with ca:
        mode=st.session_state.auth_mode
        if mode=="login":
            st.markdown(f'''<div class="auth-card"><div class="auth-title">{tr["login_title"]}</div>''',unsafe_allow_html=True)
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
            st.markdown(f'''<div class="auth-card"><div class="auth-title">{tr["reg_title"]}</div>''',unsafe_allow_html=True)
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
lc1,lc2,lc3,lc4,lc5,lc6=st.columns([1,1,1,1,4,1])
for col,l,lbl in zip([lc1,lc2,lc3,lc4],["en","te","hi","ta"],["🇬🇧 EN","తె","हि","த"]):
    with col:
        if st.button(lbl,use_container_width=True,type="primary" if lang==l else "secondary"):
            st.session_state.lang=l; st.rerun()
with lc6:
    if st.button(f"🔴 {tr['logout']}",use_container_width=True):
        st.session_state.logged_in=False; st.session_state.results=None; st.rerun()

tr=T[st.session_state.lang]; lang=st.session_state.lang

st.markdown(f"""<div class="hero-banner">
  <div style="margin-bottom:12px"><span class="fe1">🥭</span>&nbsp;&nbsp;<span class="fe2">🌿</span>&nbsp;&nbsp;<span class="fe3">🌾</span>&nbsp;&nbsp;<span class="fe1">💚</span>&nbsp;&nbsp;<span class="fe2">🥭</span></div>
  <h1 class="hero-title">{tr["title"]}</h1>
  <p class="hero-sub">{tr["subtitle"]}</p></div>""", unsafe_allow_html=True)

thtml=""
for p in PRICES:
    d=p["today"]-p["yesterday"]; ar="▲" if d>=0 else "▼"; cl="ticker-up" if d>=0 else "ticker-down"
    thtml+=f'<span class="ticker-item"><span class="ticker-place">{p["place"]}</span> <span class="ticker-price">₹{p["today"]}/kg</span> <span class="{cl}">{ar}{abs(d)}</span></span>'
dbl=thtml+thtml
st.markdown(f'''<div class="ticker-wrap"><div class="ticker-label-fixed">📈 {tr["ticker_label"]}</div><div style="padding-left:150px"><div class="ticker-inner">{dbl}</div></div></div>''',unsafe_allow_html=True)

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
        st.markdown(f"{ic} **{p['place'][:22]}**  \n₹{p['today']}/kg ({chg})")

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
    st.markdown(f'''<div class="namaste-bar">🥭 {tr["namaste"]}, <span style="color:#ffd166;margin:0 6px">{R["farmer_name"]}</span>! &nbsp;|&nbsp; 🏘️ {vd} &nbsp;|&nbsp; 🥭 {R["variety"]} &nbsp;|&nbsp; 📦 {R["qty"]} {tr["qty_label"]}</div>''',unsafe_allow_html=True)
    m1,m2,m3,m4=st.columns(4)
    with m1: st.markdown(f'''<div class="metric-card"><div class="lbl">📈 {tr["base_price"]}</div><div class="val">₹{R["base_price"]}/kg</div><div class="sub">{vd}</div></div>''',unsafe_allow_html=True)
    with m2: st.markdown(f'''<div class="metric-card"><div class="lbl">📦 Quantity</div><div class="val">{R["qty"]} qtl</div><div class="sub">{R["qty"]*100} kg</div></div>''',unsafe_allow_html=True)
    with m3: st.markdown(f'''<div class="metric-card best"><div class="lbl">🏆 {tr["best_profit"]}</div><div class="val">₹{best["NetProfit"]:,}</div><div class="sub">{best["Name"][:26]}</div></div>''',unsafe_allow_html=True)
    with m4: st.markdown(f'''<div class="metric-card"><div class="lbl">🥭 {tr["best_market"]}</div><div class="val" style="font-size:15px;line-height:1.3">{best["Name"][:24]}</div><div class="sub">{best["Distance_km"]} km · {tc(best["Category"],lang)}</div></div>''',unsafe_allow_html=True)
    st.markdown("<hr class='section-divider'>",unsafe_allow_html=True)

    tab1,tab2,tab3,tab4=st.tabs([tr["tab1"],tr["tab2"],tr["tab3"],tr["tab4"]])
    with tab1:
        mp=best["NetProfit"]; rows_html=""
        for i,r in enumerate(top10):
            pct=int(r["NetProfit"]/mp*100) if mp>0 else 0
            medal="🥇" if i==0 else "🥈" if i==1 else "🥉" if i==2 else f"#{i+1}"
            rc="r1" if i==0 else "r2" if i==1 else "r3" if i==2 else "rn"
            ck=r["Category"].replace(" ","")
            ct=tc(r["Category"],lang)
            bar=f'<div class="profit-bar-wrap"><div class="profit-bar-bg"><div class="profit-bar-fill" style="width:{pct}%"></div></div><span style="font-size:11px;color:#5a7a5f">{pct}%</span></div>'
            rows_html+=f'<tr><td><span class="rank-badge {rc}">{medal}</span></td><td><b>{r["Name"]}</b></td><td><span class="cat-tag {ck}">{ct}</span></td><td>{r["Distance_km"]} km</td><td>₹{r["Revenue"]:,}</td><td>₹{r["Transport"]:,}</td><td><b style="color:#2d6a4f">₹{r["NetProfit"]:,}</b></td><td>{bar}</td></tr>'
        st.markdown(f'''<div style="overflow-x:auto;background:white;border-radius:14px;border:1.5px solid #c8e6c9;box-shadow:0 2px 12px rgba(45,106,79,0.08)"><table class="result-table"><thead><tr><th>{tr["rank"]}</th><th>{tr["market"]}</th><th>{tr["cat"]}</th><th>{tr["dist"]}</th><th>{tr["rev"]}</th><th>{tr["trans"]}</th><th>{tr["profit"]}</th><th>% Best</th></tr></thead><tbody>{rows_html}</tbody></table></div>''',unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        df=pd.DataFrame([{tr["rank"]:i+1,tr["market"]:r["Name"],tr["cat"]:tc(r["Category"],lang),tr["dist"]:r["Distance_km"],tr["rev"]:r["Revenue"],tr["trans"]:r["Transport"],tr["profit"]:r["NetProfit"]} for i,r in enumerate(top10)])
        st.download_button("📥 Download CSV",df.to_csv(index=False).encode(),f"mango_top10_{R['village']}.csv","text/csv",use_container_width=True)

    with tab2:
        ca,cb=st.columns(2)
        with ca:
            st.markdown(f"#### {tr['chart_title']}")
            names=[r["Name"][:20]+"…" if len(r["Name"])>20 else r["Name"] for r in top10]
            fig=go.Figure()
            fig.add_trace(go.Bar(name=tr["profit"],y=names,x=[r["NetProfit"] for r in top10],orientation="h",
                marker=dict(color=ROUTE_COLORS[:len(top10)]),text=[f"₹{r['NetProfit']:,}" for r in top10],textposition="auto"))
            fig.add_trace(go.Bar(name=tr["trans"],y=names,x=[r["Transport"] for r in top10],orientation="h",
                marker_color="rgba(252,211,77,0.7)",text=[f"₹{r['Transport']:,}" for r in top10],textposition="auto"))
            fig.update_layout(barmode="group",height=440,plot_bgcolor="#f9fdf5",paper_bgcolor="white",
                xaxis_title="₹ Amount",font=dict(family="Poppins"),legend=dict(orientation="h",y=1.08),margin=dict(l=10,r=10,t=40,b=10))
            st.plotly_chart(fig,use_container_width=True)
        with cb:
            st.markdown(f"#### {tr['pie_title']}")
            cs={}
            for r in top10: k=tc(r["Category"],lang); cs[k]=cs.get(k,0)+r["NetProfit"]
            fp=px.pie(names=list(cs.keys()),values=list(cs.values()),
                color_discrete_sequence=["#2d6a4f","#52b788","#f39c12","#e74c3c","#3498db","#9b59b6"],hole=0.45)
            fp.update_traces(textposition="inside",textinfo="percent+label",marker=dict(line=dict(color="white",width=2)))
            fp.update_layout(height=440,font=dict(family="Poppins"),showlegend=True,legend=dict(orientation="h",y=-0.15),margin=dict(l=10,r=10,t=10,b=10))
            st.plotly_chart(fp,use_container_width=True)
        st.markdown("---")
        st.markdown(f"#### {tr['prices_title']}")
        np2=sorted(PRICES,key=lambda p:hav(R["v_lat"],R["v_lon"],p["lat"],p["lon"]))[:12]
        fp2=go.Figure()
        fp2.add_trace(go.Bar(name=tr["today_price"],x=[p["place"][:18] for p in np2],y=[p["today"] for p in np2],
            marker_color=["#2d6a4f" if p["today"]>=p["yesterday"] else "#e74c3c" for p in np2],
            text=[f"₹{p['today']}" for p in np2],textposition="auto"))
        fp2.add_trace(go.Bar(name=tr["yesterday_price"],x=[p["place"][:18] for p in np2],y=[p["yesterday"] for p in np2],
            marker_color="rgba(196,196,196,0.6)",text=[f"₹{p['yesterday']}" for p in np2],textposition="auto"))
        fp2.update_layout(barmode="group",height=380,plot_bgcolor="#f9fdf5",yaxis_title="₹ per kg",
            xaxis_tickangle=-45,font=dict(family="Poppins"),legend=dict(orientation="h",y=1.08),margin=dict(l=10,r=10,t=40,b=80))
        st.plotly_chart(fp2,use_container_width=True)

    with tab3:
        st.markdown("#### 🗺️ Market Map — Each color = different market")
        fm=go.Figure()
        fm.add_trace(go.Scattermapbox(lat=[R["v_lat"]],lon=[R["v_lon"]],mode="markers+text",
            marker=dict(size=22,color="#1a2e1a",symbol="star"),text=[f"🏘️ {vd}"],textposition="top right",
            name=f"🏘️ {vd}",hovertemplate=f"<b>Your Village</b><br>{vd}<extra></extra>"))
        for i,r in enumerate(top10):
            col=ROUTE_COLORS[i%len(ROUTE_COLORS)]; medal="🥇" if i==0 else "🥈" if i==1 else "🥉" if i==2 else f"#{i+1}"
            fm.add_trace(go.Scattermapbox(lat=[R["v_lat"],r["Lat"]],lon=[R["v_lon"],r["Lon"]],mode="lines",
                line=dict(width=3 if i==0 else 2,color=col),opacity=0.85 if i==0 else 0.65,showlegend=False,hoverinfo="skip"))
            fm.add_trace(go.Scattermapbox(lat=[r["Lat"]],lon=[r["Lon"]],mode="markers+text",
                marker=dict(size=18 if i<3 else 14,color=col),text=[medal],textposition="top center",
                name=f"{medal} {r['Name'][:28]}",
                hovertemplate=f"<b>{medal} {r['Name']}</b><br>Type: {tc(r['Category'],lang)}<br>Distance: {r['Distance_km']} km<br>Revenue: ₹{r['Revenue']:,}<br>Transport: ₹{r['Transport']:,}<br><b>Net Profit: ₹{r['NetProfit']:,}</b><extra></extra>"))
        fm.update_layout(mapbox=dict(style="open-street-map",center=dict(lat=R["v_lat"],lon=R["v_lon"]),zoom=8),
            height=560,margin=dict(l=0,r=0,t=0,b=0),
            legend=dict(orientation="v",x=0.01,y=0.99,bgcolor="rgba(255,255,255,0.9)",bordercolor="#c8e6c9",borderwidth=1,font=dict(size=11)),
            font=dict(family="Poppins"))
        st.plotly_chart(fm,use_container_width=True)
        st.markdown("**Color Legend:**")
        lc=st.columns(5)
        for i,r in enumerate(top10):
            medal="🥇" if i==0 else "🥈" if i==1 else "🥉" if i==2 else f"#{i+1}"
            with lc[i%5]:
                st.markdown(f'''<div style="display:flex;align-items:center;gap:6px;margin-bottom:6px"><div style="width:14px;height:14px;border-radius:50%;background:{ROUTE_COLORS[i%len(ROUTE_COLORS)]};flex-shrink:0"></div><span style="font-size:11px">{medal} {r["Name"][:18]}</span></div>''',unsafe_allow_html=True)

    with tab4:
        vl=tr["var_labels"].get(R["variety"],R["variety"]).split("\\n")[0]
        st.markdown(f"#### {tr['adv_title']} {vl}")
        ac1,ac2=st.columns(2)
        for i,(icon,title,body) in enumerate(tr["adv"]):
            with [ac1,ac2][i%2]:
                st.markdown(f'''<div class="advice-card"><div class="advice-icon">{icon}</div><div class="advice-title">{title}</div><div class="advice-body">{body}</div></div>''',unsafe_allow_html=True)
        st.markdown('''<div style="background:linear-gradient(135deg,#1b4332,#2d6a4f);border-radius:14px;padding:20px;text-align:center;margin-top:16px"><div style="font-size:36px;margin-bottom:8px">🌾 &nbsp; 🥭 &nbsp; 💚 &nbsp; 🌿 &nbsp; 🏡 &nbsp; 🚛 &nbsp; 💰</div><p style="color:#a7f3d0;font-size:14px;margin:0">Empowering Indian Farmers with Market Intelligence 🇮🇳</p></div>''',unsafe_allow_html=True)
else:
    st.markdown(f'''<div style="text-align:center;padding:50px 20px"><div style="font-size:90px;animation:float 3s ease-in-out infinite;display:inline-block">🥭</div><h2 style="color:#2d6a4f;margin:16px 0 8px">{tr["wctitle"]}</h2><p style="color:#5a7a5f;max-width:440px;margin:0 auto;line-height:1.7">{tr["wcsub"]}</p></div>''',unsafe_allow_html=True)
    st.markdown('''<div class="gif-strip"><div class="gif-item"><img src="https://media.giphy.com/media/l0HlBO7eyXzSZkJri/giphy.gif" width="180" height="135" style="display:block"/></div><div class="gif-item"><img src="https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif" width="180" height="135" style="display:block"/></div><div class="gif-item"><img src="https://media.giphy.com/media/xT9IgG50Lg7rusRgre/giphy.gif" width="180" height="135" style="display:block"/></div></div>''',unsafe_allow_html=True)
    w1,w2,w3=st.columns(3)
    for col,(icon,title,sub) in zip([w1,w2,w3],[("📍","Pick Your Village","Find all nearby markets within 200km"),("🥭","Choose Your Variety","Matched to the right buyers for your mango"),("💰","See Top 10 Profits","Compare all options and pick the best deal")]):
        with col:
            st.markdown(f'''<div class="wc-feature"><div class="wc-feat-icon">{icon}</div><div style="font-weight:700;color:#1a2e1a;font-size:14px;margin-bottom:5px">{title}</div><div style="font-size:12px;color:#5a7a5f">{sub}</div></div>''',unsafe_allow_html=True)

st.markdown('''<div style="text-align:center;color:#5a7a5f;font-size:12px;padding:16px 0;margin-top:20px;border-top:1px solid #c8e6c9">🥭 Farmer\'s Mango Profit Navigator &nbsp;·&nbsp; Empowering farmers across Andhra Pradesh &nbsp;·&nbsp; 🇮🇳 Made in India</div>''',unsafe_allow_html=True)
