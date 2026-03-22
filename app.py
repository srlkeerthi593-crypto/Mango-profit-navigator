import streamlit as st
import pandas as pd
import numpy as np
import math
import requests
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Farmer's Mango Profit Navigator",
    page_icon="🥭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.main { background-color: #f5f7f0; }

.hero-banner {
    background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 50%, #52b788 100%);
    border-radius: 16px;
    padding: 32px 40px;
    margin-bottom: 24px;
    color: white;
    text-align: center;
}
.hero-banner h1 { font-size: 2.2rem; font-weight: 800; margin: 0; }
.hero-banner p  { font-size: 1rem; opacity: 0.85; margin-top: 8px; }

.metric-card {
    background: white;
    border: 2px solid #c8e6c9;
    border-radius: 14px;
    padding: 18px 20px;
    text-align: center;
    margin-bottom: 10px;
}
.metric-card.best {
    background: linear-gradient(135deg, #1b4332, #2d6a4f);
    border-color: #2d6a4f;
    color: white;
}
.metric-card .label {
    font-size: 11px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.6px;
    color: #5a7a5f; margin-bottom: 6px;
}
.metric-card.best .label { color: #a7f3d0; }
.metric-card .value {
    font-size: 26px; font-weight: 800; color: #2d6a4f;
}
.metric-card.best .value { color: white; }
.metric-card .sub { font-size: 11px; color: #5a7a5f; margin-top: 4px; }
.metric-card.best .sub { color: #c8f0b0; }

.ticker-bar {
    background: #0a2e14;
    border-radius: 10px;
    padding: 10px 18px;
    margin-bottom: 18px;
    overflow-x: auto;
    white-space: nowrap;
    color: #a7f3d0;
    font-size: 13px;
}
.ticker-item { display: inline-block; margin-right: 28px; }
.ticker-price { color: #ffd166; font-weight: 800; }
.ticker-up { color: #4ade80; }
.ticker-down { color: #f87171; }

.cat-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
}
.rank-gold   { background:#FFD700; color:#7a5c00; border-radius:50%; width:28px; height:28px;
               display:inline-flex; align-items:center; justify-content:center; font-weight:800; }
.rank-silver { background:#C0C0C0; color:#444; border-radius:50%; width:28px; height:28px;
               display:inline-flex; align-items:center; justify-content:center; font-weight:800; }
.rank-bronze { background:#CD7F32; color:#fff; border-radius:50%; width:28px; height:28px;
               display:inline-flex; align-items:center; justify-content:center; font-weight:800; }

.advice-card {
    background: white;
    border: 1.5px solid #c8e6c9;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
}
.advice-card .icon { font-size: 28px; margin-bottom: 8px; }
.advice-card .title { font-weight: 700; color: #2d6a4f; font-size: 14px; margin-bottom: 4px; }
.advice-card .body  { font-size: 13px; color: #5a7a5f; line-height: 1.55; }

.tip-box {
    background: #fffbeb;
    border: 1.5px solid #fcd34d;
    border-radius: 10px;
    padding: 12px 14px;
    font-size: 13px;
    color: #78350f;
    line-height: 1.6;
    margin-top: 10px;
}

[data-testid="stSidebar"] { background: white; border-right: 2px solid #c8e6c9; }
div[data-testid="stSidebar"] > div:first-child { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TRANSLATIONS
# ─────────────────────────────────────────────
T = {
    "en": {
        "title": "🥭 Farmer's Mango Profit Navigator",
        "subtitle": "Find the Best Market. Earn the Highest Return.",
        "ticker_label": "📈 Today's Mango Prices",
        "lname": "👤 Farmer Name", "lvillage": "🏘️ Your Village",
        "lvar": "🥭 Mango Variety", "lqty": "📦 Quantity (Quintals)",
        "run_btn": "🚀 Find Best Market",
        "tip": "💡 Selling more quintals together reduces transport cost per kg — coordinate with nearby farmers!",
        "wctitle": "Welcome, Mango Farmer!",
        "wcsub": "Fill in your details on the left and click 'Find Best Market' to compare all selling options.",
        "namaste": "Namaste",
        "base_price": "Today's Base Price", "best_profit": "Best Net Profit",
        "best_market": "Best Market", "your_village": "Your Village",
        "tab1": "🥭 Top 10 Options", "tab2": "📊 Profit Chart",
        "tab3": "🗺️ Market Map", "tab4": "💡 Selling Advice",
        "rank": "Rank", "market": "Market / Buyer", "cat": "Type",
        "dist": "Distance (km)", "rev": "Revenue (₹)", "trans": "Transport (₹)", "profit": "Net Profit (₹)",
        "chart_title": "Profit Comparison — Top 10 Options",
        "pie_title": "Profit Share by Category",
        "map_title": "Top 10 Markets on Map",
        "adv_title": "Selling Advice for Your Variety",
        "adv": [
            ("🌅", "Best Time to Sell", "Sell early morning when prices are highest at Mandi. Export buyers prefer pre-sorted fruit."),
            ("🤝", "Negotiate Better", "Quote 2–3 buyers simultaneously. Show competitor prices to get a better deal."),
            ("🚛", "Transport Tip", "Combine your load with neighbouring farmers to split transport cost and increase net profit."),
            ("⭐", "Quality Matters", "Grade A fruit fetches 15–25% more. Sort before loading to maximise return."),
        ],
        "loading": "Calculating best markets...",
        "no_results": "No markets found for this variety. Try a different variety.",
        "var_labels": {
            "Banganapalli": "Banganapalli\n⭐ Export",
            "Totapuri":     "Totapuri\n⭐ Processing",
            "Neelam":       "Neelam\n⭐ Mandi",
            "Rasalu":       "Rasalu\n⭐ Pickle",
        },
        "qty_label": "quintals",
        "mandal_ph": "Select Mandal first",
        "village_ph": "Select village...",
        "name_ph": "Enter your name",
    },
    "te": {
        "title": "🥭 రైతు మామిడి లాభాల నావిగేటర్",
        "subtitle": "అత్యుత్తమ మార్కెట్ కనుగొనండి. అధిక లాభం సంపాదించండి.",
        "ticker_label": "📈 నేటి మామిడి ధరలు",
        "lname": "👤 రైతు పేరు", "lvillage": "🏘️ మీ గ్రామం",
        "lvar": "🥭 మామిడి రకం", "lqty": "📦 పరిమాణం (క్వింటాల్లు)",
        "run_btn": "🚀 అత్యుత్తమ మార్కెట్ కనుగొనండి",
        "tip": "💡 ఎక్కువ క్వింటాల్లు కలిసి అమ్మినట్లయితే రవాణా ఖర్చు తక్కువగా ఉంటుంది!",
        "wctitle": "స్వాగతం, మామిడి రైతు!",
        "wcsub": "ఎడమ వైపు వివరాలు నమోదు చేసి 'అత్యుత్తమ మార్కెట్' క్లిక్ చేయండి.",
        "namaste": "నమస్తే",
        "base_price": "నేటి మార్కెట్ ధర", "best_profit": "అత్యధిక నికర లాభం",
        "best_market": "అత్యుత్తమ మార్కెట్", "your_village": "మీ గ్రామం",
        "tab1": "🥭 టాప్ 10 ఎంపికలు", "tab2": "📊 లాభాల పోలిక",
        "tab3": "🗺️ మార్కెట్ మ్యాప్", "tab4": "💡 అమ్మకపు సలహా",
        "rank": "వరుస", "market": "మార్కెట్ / కొనుగోలుదారు", "cat": "రకం",
        "dist": "దూరం (కి.మీ)", "rev": "ఆదాయం (₹)", "trans": "రవాణా (₹)", "profit": "నికర లాభం (₹)",
        "chart_title": "లాభాల పోలిక — టాప్ 10",
        "pie_title": "వర్గం వారీ లాభం",
        "map_title": "మ్యాప్‌లో టాప్ 10 మార్కెట్లు",
        "adv_title": "మీ రకానికి అమ్మకపు సలహా",
        "adv": [
            ("🌅", "అమ్మడానికి అత్యుత్తమ సమయం", "తెల్లవారుజామున అమ్మండి — మండీలో ధరలు అప్పుడు ఎక్కువగా ఉంటాయి."),
            ("🤝", "మెరుగైన ధర చర్చించండి", "2-3 మంది కొనుగోలుదారులను ఒకేసారి సంప్రదించి పోటీ ధరలు చూపించండి."),
            ("🚛", "రవాణా సూచన", "పొరుగు రైతులతో కలిసి రవాణా చేయండి — ఖర్చు తక్కువవుతుంది."),
            ("⭐", "నాణ్యత ముఖ్యం", "గ్రేడ్ A మామిడి 15-25% ఎక్కువ ధర పొందుతుంది. లోడ్ చేయడానికి ముందే వేర్పరచండి."),
        ],
        "loading": "అత్యుత్తమ మార్కెట్లు లెక్కిస్తున్నాం...",
        "no_results": "ఈ రకానికి మార్కెట్లు కనుగొనబడలేదు.",
        "var_labels": {
            "Banganapalli": "బంగినపల్లి\n⭐ ఎగుమతి",
            "Totapuri":     "తోటపురి\n⭐ ప్రాసెసింగ్",
            "Neelam":       "నీలం\n⭐ మండీ",
            "Rasalu":       "రసాలు\n⭐ ఊరగాయ",
        },
        "qty_label": "క్వింటాల్లు",
        "mandal_ph": "మండల్ ఎంచుకోండి",
        "village_ph": "గ్రామం ఎంచుకోండి...",
        "name_ph": "మీ పేరు నమోదు చేయండి",
    },
    "hi": {
        "title": "🥭 किसान का आम लाभ नेविगेटर",
        "subtitle": "सबसे अच्छा बाजार खोजें। सबसे ज्यादा मुनाफा कमाएं।",
        "ticker_label": "📈 आज के आम के भाव",
        "lname": "👤 किसान का नाम", "lvillage": "🏘️ आपका गांव",
        "lvar": "🥭 आम की किस्म", "lqty": "📦 मात्रा (क्विंटल)",
        "run_btn": "🚀 सबसे अच्छा बाजार खोजें",
        "tip": "💡 ज्यादा क्विंटल एक साथ बेचने से परिवहन लागत कम होती है!",
        "wctitle": "स्वागत है, आम किसान!",
        "wcsub": "बाईं तरफ विवरण भरें और 'सबसे अच्छा बाजार खोजें' पर क्लिक करें।",
        "namaste": "नमस्ते",
        "base_price": "आज का बाजार भाव", "best_profit": "सर्वाधिक शुद्ध लाभ",
        "best_market": "सबसे अच्छा बाजार", "your_village": "आपका गांव",
        "tab1": "🥭 टॉप 10 विकल्प", "tab2": "📊 लाभ तुलना",
        "tab3": "🗺️ बाजार मानचित्र", "tab4": "💡 बिक्री सलाह",
        "rank": "क्रम", "market": "बाजार / खरीदार", "cat": "प्रकार",
        "dist": "दूरी (कि.मी.)", "rev": "आय (₹)", "trans": "परिवहन (₹)", "profit": "शुद्ध लाभ (₹)",
        "chart_title": "लाभ तुलना — टॉप 10 विकल्प",
        "pie_title": "श्रेणी अनुसार लाभ",
        "map_title": "मानचित्र पर टॉप 10 बाजार",
        "adv_title": "आपकी किस्म के लिए बिक्री सलाह",
        "adv": [
            ("🌅", "बेचने का सबसे अच्छा समय", "सुबह जल्दी बेचें — मंडी में भाव ऊंचे होते हैं।"),
            ("🤝", "बेहतर भाव मांगें", "2-3 खरीदारों से एक साथ बात करें और प्रतिस्पर्धी भाव दिखाएं।"),
            ("🚛", "परिवहन सुझाव", "पड़ोसी किसानों के साथ मिलकर परिवहन करें — लागत बंटेगी।"),
            ("⭐", "गुणवत्ता महत्वपूर्ण है", "ग्रेड A आम 15-25% ज्यादा भाव पाता है। लोड करने से पहले छांटें।"),
        ],
        "loading": "सबसे अच्छे बाजार ढूंढ रहे हैं...",
        "no_results": "इस किस्म के लिए बाजार नहीं मिला।",
        "var_labels": {
            "Banganapalli": "बंगनपल्ली\n⭐ निर्यात",
            "Totapuri":     "तोतापुरी\n⭐ प्रसंस्करण",
            "Neelam":       "नीलम\n⭐ मंडी",
            "Rasalu":       "रसालु\n⭐ अचार",
        },
        "qty_label": "क्विंटल",
        "mandal_ph": "मंडल चुनें",
        "village_ph": "गांव चुनें...",
        "name_ph": "अपना नाम डालें",
    },
    "ta": {
        "title": "🥭 விவசாயியின் மாம்பழ லாப வழிகாட்டி",
        "subtitle": "சிறந்த சந்தையைக் கண்டறியுங்கள். அதிக வருவாய் ஈட்டுங்கள்.",
        "ticker_label": "📈 இன்றைய மாம்பழ விலைகள்",
        "lname": "👤 விவசாயி பெயர்", "lvillage": "🏘️ உங்கள் கிராமம்",
        "lvar": "🥭 மாம்பழ வகை", "lqty": "📦 அளவு (குவிண்டால்)",
        "run_btn": "🚀 சிறந்த சந்தையைக் கண்டறி",
        "tip": "💡 அதிக குவிண்டால் சேர்த்து விற்பனை செய்தால் போக்குவரத்து செலவு குறையும்!",
        "wctitle": "வரவேற்கிறோம், மாம்பழ விவசாயி!",
        "wcsub": "இடதுபுறம் விவரங்களை நிரப்பி 'சிறந்த சந்தை' என்பதை கிளிக் செய்யுங்கள்.",
        "namaste": "வணக்கம்",
        "base_price": "இன்றைய அடிப்படை விலை", "best_profit": "அதிகபட்ச நிகர லாபம்",
        "best_market": "சிறந்த சந்தை", "your_village": "உங்கள் கிராமம்",
        "tab1": "🥭 சிறந்த 10 விருப்பங்கள்", "tab2": "📊 லாப ஒப்பீடு",
        "tab3": "🗺️ சந்தை வரைபடம்", "tab4": "💡 விற்பனை ஆலோசனை",
        "rank": "வரிசை", "market": "சந்தை / வாங்குபவர்", "cat": "வகை",
        "dist": "தூரம் (கி.மீ)", "rev": "வருவாய் (₹)", "trans": "போக்குவரத்து (₹)", "profit": "நிகர லாபம் (₹)",
        "chart_title": "லாப ஒப்பீடு — சிறந்த 10",
        "pie_title": "வகை வாரியான லாபம்",
        "map_title": "வரைபடத்தில் சிறந்த 10 சந்தைகள்",
        "adv_title": "உங்கள் வகைக்கான விற்பனை ஆலோசனை",
        "adv": [
            ("🌅", "விற்பனைக்கு சிறந்த நேரம்", "அதிகாலையில் விற்கவும் — மண்டியில் விலை அதிகமாக இருக்கும்."),
            ("🤝", "சிறந்த விலை பேசுங்கள்", "2-3 வாங்குபவர்களிடம் ஒரே நேரத்தில் பேசி போட்டி விலைகளை காட்டுங்கள்."),
            ("🚛", "போக்குவரத்து குறிப்பு", "அண்டை விவசாயிகளுடன் சேர்ந்து போக்குவரத்து செய்யுங்கள்."),
            ("⭐", "தரம் முக்கியம்", "தரம் A மாம்பழம் 15-25% அதிக விலை பெறும்."),
        ],
        "loading": "சிறந்த சந்தைகளை கணக்கிடுகிறோம்...",
        "no_results": "இந்த வகைக்கு சந்தை கிடைக்கவில்லை.",
        "var_labels": {
            "Banganapalli": "பங்கனபல்லி\n⭐ ஏற்றுமதி",
            "Totapuri":     "தொதாபுரி\n⭐ பதப்படுத்தல்",
            "Neelam":       "நீலம்\n⭐ மண்டி",
            "Rasalu":       "ரசாலு\n⭐ ஊறுகாய்",
        },
        "qty_label": "குவிண்டால்",
        "mandal_ph": "மண்டலம் தேர்ந்தெடுக்கவும்",
        "village_ph": "கிராமம் தேர்ந்தெடுக்கவும்...",
        "name_ph": "உங்கள் பெயரை உள்ளிடவும்",
    },
}

# Village name translations (sample key villages — extend as needed)
VILLAGE_TRANSLATIONS = {
    "te": {
        "ALIMILI": "అలిమిలి", "BALAYAPALLI": "బాలయపల్లి", "BHYRAVARAM": "భైరవారం",
        "CHILAMANURU": "చిలమనూరు", "GOTTIKADU": "గొట్టికాడు", "HASTHAKAVERI": "హస్తకావేరి",
        "JAYAMPU": "జయంపు", "KADAGUNTA": "కాదగుంట", "KALAGANDA": "కళగండ",
        "KAMAKURU": "కామకూరు", "KATRAGUNTA": "కాట్రగుంట", "KAYYURU": "కయ్యూరు",
        "KOTAMBEDU": "కొటంబేడు", "MANNURU": "మన్నూరు", "NIDIGALLU": "నిడిగళ్ళు",
        "PAKAPUDI": "పాకపుడి", "PALLIPADU": "పల్లిపాడు", "PIGILAM": "పిగిలం",
        "PERIMIDI": "పేరిమిడి", "SANGAVARAM": "సంగవరం", "SIDDAGUNTA": "సిద్ధగుంట",
        "UTLAPALLE": "ఉట్లపల్లె", "VENGAMAMBAPURAM": "వెంగమాంబాపురం", "NINDALI": "నిందళి",
        "CHANDRAGIRI": "చంద్రగిరి", "GADANKI": "గాడంకి", "PAKALA": "పాకల",
        "TIRUPATI": "తిరుపతి", "SRIKALAHASTHI": "శ్రీకాళహస్తి", "RENIGUNTA": "రేణిగుంట",
        "YERPEDU": "యేర్పేడు", "NAIDUPET": "నాయుడుపేట", "NAGALAPURAM": "నాగలాపురం",
        "SULLURPET": "సుళ్ళూరుపేట", "TADA": "తాడ", "VAKADU": "వకాడు",
        "VENKATAGIRI": "వెంకటగిరి", "PUTTUR": "పుత్తూరు", "OZILI": "ఓజిలి",
        "DAKKILI": "దక్కిలి", "SATYAVEDU": "సత్యవేడు",
        "NARAYANAVANAM": "నారాయణవనం", "PELLAKUR": "పెళ్ళకూరు",
        "VARADAIAHPALEM": "వరదయ్యపాలెం", "THOTTAMBEDU": "తొట్టంబేడు",
    },
    "hi": {
        "ALIMILI": "अलिमिली", "BALAYAPALLI": "बालयपल्ली", "CHANDRAGIRI": "चंद्रगिरि",
        "GADANKI": "गाडंकी", "PAKALA": "पाकला", "TIRUPATI": "तिरुपति",
        "SRIKALAHASTHI": "श्रीकालहस्ती", "RENIGUNTA": "रेनिगुंटा", "YERPEDU": "येरपेडु",
        "NAIDUPET": "नायडुपेट", "NAGALAPURAM": "नागलापुरम", "SULLURPET": "सुल्लूरपेट",
        "TADA": "ताडा", "VAKADU": "वकाडु", "VENKATAGIRI": "वेंकटगिरि",
        "PUTTUR": "पुत्तूर", "OZILI": "ओज़िली", "DAKKILI": "दक्किली",
        "SATYAVEDU": "सत्यवेडु", "NARAYANAVANAM": "नारायणवनम", "PELLAKUR": "पेल्लकुर",
    },
    "ta": {
        "TIRUPATI": "திருப்பதி", "CHANDRAGIRI": "சந்திரகிரி", "PAKALA": "பாக்கல",
        "SRIKALAHASTHI": "ஸ்ரீகாளஹஸ்தி", "RENIGUNTA": "ரேணிகுண்டா", "YERPEDU": "யர்பேடு",
        "NAIDUPET": "நாயுடுபேட்", "NAGALAPURAM": "நாகலாபுரம்", "SULLURPET": "சுல்லூர்பேட்",
        "TADA": "தாடா", "VENKATAGIRI": "வெங்கடகிரி", "PUTTUR": "புத்தூர்",
        "SATYAVEDU": "சத்யவேடு", "NARAYANAVANAM": "நாராயணவனம்",
    },
}

# Category translations
CAT_TRANSLATIONS = {
    "te": {
        "Mandi": "మండీ", "Processing": "ప్రాసెసింగ్", "Pulp": "పల్ప్",
        "Pickle": "ఊరగాయ", "Local Export": "స్థానిక ఎగుమతి", "Abroad Export": "విదేశీ ఎగుమతి"
    },
    "hi": {
        "Mandi": "मंडी", "Processing": "प्रसंस्करण", "Pulp": "पल्प",
        "Pickle": "अचार", "Local Export": "स्थानीय निर्यात", "Abroad Export": "विदेश निर्यात"
    },
    "ta": {
        "Mandi": "மண்டி", "Processing": "பதப்படுத்தல்", "Pulp": "பழச்சாறு",
        "Pickle": "ஊறுகாய்", "Local Export": "உள்நாட்டு ஏற்றுமதி", "Abroad Export": "வெளிநாட்டு ஏற்றுமதி"
    },
    "en": {
        "Mandi": "Mandi", "Processing": "Processing", "Pulp": "Pulp",
        "Pickle": "Pickle", "Local Export": "Local Export", "Abroad Export": "Abroad Export"
    }
}

# ─────────────────────────────────────────────
# DATA (same as your original app.py CSV data)
# ─────────────────────────────────────────────
VILLAGES_DATA = [
    {"Mandal":"BALAYAPALLI","Gram Panchayat":"ALIMILI","Latitude":14.0152,"Longitude":79.6124},
    {"Mandal":"BALAYAPALLI","Gram Panchayat":"BALAYAPALLI","Latitude":13.9856,"Longitude":79.6452},
    {"Mandal":"BALAYAPALLI","Gram Panchayat":"BHYRAVARAM","Latitude":14.0221,"Longitude":79.6845},
    {"Mandal":"BALAYAPALLI","Gram Panchayat":"CHILAMANURU","Latitude":14.0512,"Longitude":79.6231},
    {"Mandal":"BALAYAPALLI","Gram Panchayat":"GOTTIKADU","Latitude":13.9621,"Longitude":79.6712},
    {"Mandal":"BALAYAPALLI","Gram Panchayat":"HASTHAKAVERI","Latitude":13.9455,"Longitude":79.6322},
    {"Mandal":"BALAYAPALLI","Gram Panchayat":"JAYAMPU","Latitude":13.9922,"Longitude":79.7011},
    {"Mandal":"BALAYAPALLI","Gram Panchayat":"KADAGUNTA","Latitude":14.0312,"Longitude":79.5912},
    {"Mandal":"BALAYAPALLI","Gram Panchayat":"KALAGANDA","Latitude":13.9112,"Longitude":79.6241},
    {"Mandal":"BALAYAPALLI","Gram Panchayat":"KAMAKURU","Latitude":13.9521,"Longitude":79.5844},
    {"Mandal":"BALAYAPALLI","Gram Panchayat":"KATRAGUNTA","Latitude":14.0012,"Longitude":79.6543},
    {"Mandal":"BALAYAPALLI","Gram Panchayat":"KAYYURU","Latitude":13.8821,"Longitude":79.6912},
    {"Mandal":"BALAYAPALLI","Gram Panchayat":"KOTAMBEDU","Latitude":13.9244,"Longitude":79.7121},
    {"Mandal":"BALAYAPALLI","Gram Panchayat":"MANNURU","Latitude":13.9712,"Longitude":79.7342},
    {"Mandal":"BALAYAPALLI","Gram Panchayat":"NIDIGALLU","Latitude":14.0421,"Longitude":79.6921},
    {"Mandal":"CHANDRAGIRI","Gram Panchayat":"CHANDRAGIRI","Latitude":13.5834,"Longitude":79.3214},
    {"Mandal":"CHANDRAGIRI","Gram Panchayat":"AGARALA","Latitude":13.6012,"Longitude":79.3145},
    {"Mandal":"CHANDRAGIRI","Gram Panchayat":"THONDAWADA","Latitude":13.6122,"Longitude":79.3712},
    {"Mandal":"PAKALA","Gram Panchayat":"GADANKI","Latitude":13.5321,"Longitude":79.2112},
    {"Mandal":"PAKALA","Gram Panchayat":"PAKALA","Latitude":13.4512,"Longitude":79.1121},
    {"Mandal":"PAKALA","Gram Panchayat":"DAMALCHERUVU","Latitude":13.5112,"Longitude":79.1011},
    {"Mandal":"RENIGUNTA","Gram Panchayat":"RENIGUNTA","Latitude":13.6345,"Longitude":79.5124},
    {"Mandal":"RENIGUNTA","Gram Panchayat":"KARAKAMBADI","Latitude":13.6645,"Longitude":79.4712},
    {"Mandal":"RENIGUNTA","Gram Panchayat":"ATHURU","Latitude":13.6812,"Longitude":79.5122},
    {"Mandal":"TIRUPATI (RURAL)","Gram Panchayat":"AVILALA","Latitude":13.6012,"Longitude":79.4121},
    {"Mandal":"TIRUPATI (RURAL)","Gram Panchayat":"TIRUCHANUR","Latitude":13.6111,"Longitude":79.4512},
    {"Mandal":"TIRUPATI (RURAL)","Gram Panchayat":"THUMMALAGUNTA","Latitude":13.6044,"Longitude":79.4011},
    {"Mandal":"TIRUPATI (URBAN)","Gram Panchayat":"MANGALAM","Latitude":13.6545,"Longitude":79.4512},
    {"Mandal":"TIRUPATI (URBAN)","Gram Panchayat":"RANADHEERPURAM","Latitude":13.6411,"Longitude":79.4311},
    {"Mandal":"SRIKALAHASTHI","Gram Panchayat":"SRIKALAHASTHI","Latitude":13.7498,"Longitude":79.7034},
    {"Mandal":"SRIKALAHASTHI","Gram Panchayat":"AMMAPALEM","Latitude":13.7411,"Longitude":79.6212},
    {"Mandal":"SRIKALAHASTHI","Gram Panchayat":"EMPEDU","Latitude":13.8112,"Longitude":79.7122},
    {"Mandal":"YERPEDU","Gram Panchayat":"YERPEDU","Latitude":13.6845,"Longitude":79.5945},
    {"Mandal":"YERPEDU","Gram Panchayat":"GUDIMALLAM","Latitude":13.6421,"Longitude":79.5511},
    {"Mandal":"YERPEDU","Gram Panchayat":"PAPANAIDUPET","Latitude":13.6645,"Longitude":79.5823},
    {"Mandal":"NAIDUPET","Gram Panchayat":"NAIDUPET","Latitude":13.9142,"Longitude":79.8944},
    {"Mandal":"NAIDUPET","Gram Panchayat":"ANNAMEDU","Latitude":13.8812,"Longitude":79.9111},
    {"Mandal":"NAGALAPURAM","Gram Panchayat":"NAGALAPURAM","Latitude":13.4022,"Longitude":79.9214},
    {"Mandal":"NAGALAPURAM","Gram Panchayat":"KRISHNAPURAM","Latitude":13.3812,"Longitude":79.9411},
    {"Mandal":"SULLURPET","Gram Panchayat":"SULLURPET","Latitude":13.7008,"Longitude":80.0211},
    {"Mandal":"SULLURPET","Gram Panchayat":"ABAKA","Latitude":13.7012,"Longitude":80.0112},
    {"Mandal":"TADA","Gram Panchayat":"TADA","Latitude":13.5845,"Longitude":80.0312},
    {"Mandal":"TADA","Gram Panchayat":"MAMBATTU","Latitude":13.5611,"Longitude":80.0211},
    {"Mandal":"VAKADU","Gram Panchayat":"VAKADU","Latitude":14.0124,"Longitude":80.1012},
    {"Mandal":"VAKADU","Gram Panchayat":"KALLURU","Latitude":14.0512,"Longitude":80.0911},
    {"Mandal":"VENKATAGIRI","Gram Panchayat":"VENKATAGIRI","Latitude":13.9575,"Longitude":79.5847},
    {"Mandal":"VENKATAGIRI","Gram Panchayat":"AMMAPALEM","Latitude":13.9812,"Longitude":79.5412},
    {"Mandal":"PUTTUR","Gram Panchayat":"PUTTUR","Latitude":13.4419,"Longitude":79.553},
    {"Mandal":"PUTTUR","Gram Panchayat":"NESANUR","Latitude":13.4722,"Longitude":79.5911},
    {"Mandal":"OZILI","Gram Panchayat":"OZILI","Latitude":13.9845,"Longitude":79.9124},
    {"Mandal":"OZILI","Gram Panchayat":"GURRAMKONDA","Latitude":13.9512,"Longitude":79.8412},
    {"Mandal":"DAKKILI","Gram Panchayat":"DAKKILI","Latitude":14.1345,"Longitude":79.6122},
    {"Mandal":"DAKKILI","Gram Panchayat":"AMUDURU","Latitude":14.1211,"Longitude":79.6012},
    {"Mandal":"SATYAVEDU","Gram Panchayat":"SATYAVEDU","Latitude":13.5045,"Longitude":79.9712},
    {"Mandal":"SATYAVEDU","Gram Panchayat":"AROOR","Latitude":13.5112,"Longitude":79.9011},
    {"Mandal":"NARAYANAVANAM","Gram Panchayat":"NARAYANAVANAM","Latitude":13.4211,"Longitude":79.5822},
    {"Mandal":"NARAYANAVANAM","Gram Panchayat":"BHEEMUNICHERUVU","Latitude":13.4111,"Longitude":79.5512},
    {"Mandal":"PELLAKUR","Gram Panchayat":"PELLAKUR","Latitude":13.8345,"Longitude":79.8544},
    {"Mandal":"PELLAKUR","Gram Panchayat":"ANAKAVOLU","Latitude":13.8412,"Longitude":79.8512},
    {"Mandal":"VARADAIAHPALEM","Gram Panchayat":"VARADAIAHPALEM","Latitude":13.5945,"Longitude":79.9221},
    {"Mandal":"VARADAIAHPALEM","Gram Panchayat":"AMBUR","Latitude":13.5612,"Longitude":79.9112},
    {"Mandal":"THOTTAMBEDU","Gram Panchayat":"THOTTAMBEDU","Latitude":13.8445,"Longitude":79.7543},
    {"Mandal":"THOTTAMBEDU","Gram Panchayat":"BONUPALLE","Latitude":13.8212,"Longitude":79.7211},
]

PRICES_DATA = [
    {"place":"Tirupati APMC (RC Road)","lat":13.6231,"long":79.4125,"today_price":29,"yesterday_price":34},
    {"place":"Pakala Main Mango APMC","lat":13.4568,"long":79.1174,"today_price":27,"yesterday_price":32},
    {"place":"Railway Kodur APMC Yard","lat":13.9515,"long":79.3514,"today_price":28,"yesterday_price":33},
    {"place":"Puttur Mango Market Yard","lat":13.4428,"long":79.5531,"today_price":26,"yesterday_price":31},
    {"place":"Chandragiri APMC","lat":13.5828,"long":79.3142,"today_price":25,"yesterday_price":30},
    {"place":"Srikalahasti APMC","lat":13.7498,"long":79.7034,"today_price":30,"yesterday_price":35},
    {"place":"Venkatagiri APMC","lat":13.9575,"long":79.5847,"today_price":28,"yesterday_price":33},
    {"place":"Nagalapuram APMC","lat":13.3985,"long":79.7915,"today_price":27,"yesterday_price":32},
    {"place":"Naidupeta APMC","lat":13.9142,"long":79.8944,"today_price":29,"yesterday_price":34},
    {"place":"Satyavedu APMC","lat":13.5076,"long":79.9715,"today_price":26,"yesterday_price":31},
    {"place":"Sullurpeta APMC","lat":13.7008,"long":80.0211,"today_price":25,"yesterday_price":30},
    {"place":"Puttur","lat":13.4419,"long":79.553,"today_price":41,"yesterday_price":44},
    {"place":"Bangarupalem","lat":13.2,"long":78.9333,"today_price":34,"yesterday_price":42},
    {"place":"Chittoor","lat":13.2172,"long":79.1003,"today_price":36,"yesterday_price":39},
    {"place":"Pakala","lat":13.4667,"long":79.1167,"today_price":37,"yesterday_price":41},
    {"place":"Madanapalle AMC (Main)","lat":13.6114,"long":78.4716,"today_price":33,"yesterday_price":40},
    {"place":"Gurramkonda e-NAM","lat":13.782,"long":78.584,"today_price":39,"yesterday_price":45},
    {"place":"Galiveedu Market Yard","lat":14.1035,"long":78.5142,"today_price":36,"yesterday_price":43},
    {"place":"Jamiya Mango Yard","lat":14.0562,"long":78.751,"today_price":38,"yesterday_price":45},
]

PROCESSING_DATA = [
    {"facility_name":"Galla Foods (Rayachoti unit)","latitude":14.0585,"longitude":78.749},
    {"facility_name":"Roshan Fruits India Pvt. Ltd.","latitude":13.6517,"longitude":78.9415},
    {"facility_name":"Sri Varsha Food Products India Ltd","latitude":13.6275,"longitude":79.4312},
    {"facility_name":"Hayath Foods","latitude":13.6212,"longitude":79.468},
    {"facility_name":"Grofresh Agrofoods Pvt Ltd","latitude":14.1825,"longitude":79.171},
    {"facility_name":"Srini Food Park - Processing Units","latitude":13.185,"longitude":78.961},
    {"facility_name":"Sree Sannidhi Foods Pvt Ltd","latitude":14.2015,"longitude":79.145},
    {"facility_name":"Ohms Food Products Pvt Ltd","latitude":14.061,"longitude":78.7425},
    {"facility_name":"Navya Foods Pvt Ltd","latitude":14.085,"longitude":78.7315},
    {"facility_name":"Bright Mangoes","latitude":13.935,"longitude":79.365},
]

PULP_DATA = [
    {"Facility Name":"PLR Foods Pvt Ltd","Latitude":13.0639,"Longitude":78.8248},
    {"Facility Name":"Vijay Food Processing Unit","Latitude":13.2092,"Longitude":79.1326},
    {"Facility Name":"Galla Foods Ltd","Latitude":13.2092,"Longitude":79.1326},
    {"Facility Name":"Srini Food Park Pvt Ltd","Latitude":13.2106,"Longitude":79.1161},
    {"Facility Name":"Sree Sannidhi Foods Pvt Ltd","Latitude":13.2148,"Longitude":79.0982},
    {"Facility Name":"Hayath Foods","Latitude":13.3091,"Longitude":79.0774},
    {"Facility Name":"Abc Fruits Chittoor","Latitude":13.2138,"Longitude":79.0516},
    {"Facility Name":"Navya Foods Pvt Ltd","Latitude":14.1952,"Longitude":79.1573},
    {"Facility Name":"Grofresh Agrofoods Pvt Ltd","Latitude":13.6541,"Longitude":78.9489},
    {"Facility Name":"B M Fruits","Latitude":13.6425,"Longitude":79.5033},
]

PICKLE_DATA = [
    {"firm_name":"Rayachoti Pickles & Foods","latitude":14.0585,"longitude":78.749},
    {"firm_name":"Tirupati Pickle Works","latitude":13.629,"longitude":79.4285},
    {"firm_name":"Padmavathi Pickles","latitude":13.6025,"longitude":79.441},
    {"firm_name":"Puttur Traditional Pickle Makers","latitude":13.4415,"longitude":79.553},
    {"firm_name":"Srikalahasti Pickle Industries","latitude":13.755,"longitude":79.7045},
    {"firm_name":"Hayath Pickles & Foods","latitude":13.6215,"longitude":79.4685},
    {"firm_name":"Pileru Pickle & Chutney Works","latitude":13.6515,"longitude":78.941},
    {"firm_name":"Punganur Mango Pickle Unit","latitude":13.364,"longitude":78.5825},
    {"firm_name":"Chittoor Pack & Pickle Pvt","latitude":13.2215,"longitude":79.112},
    {"firm_name":"Kalikiri Pickle & Preserves","latitude":13.645,"longitude":78.782},
]

LOCAL_EXPORT_DATA = [
    {"hub_/_firm_name":"Rayachoti APMC / Market Yard","latitude":14.062,"longitude":78.742},
    {"hub_/_firm_name":"Rajampet APMC / Market Yard","latitude":14.1885,"longitude":79.156},
    {"hub_/_firm_name":"Tirupati APMC / Market Yard","latitude":13.6285,"longitude":79.4192},
    {"hub_/_firm_name":"Renigunta Packhouse & Cold Room","latitude":13.6385,"longitude":79.5068},
    {"hub_/_firm_name":"Srikalahasti Collection & Cold Room","latitude":13.751,"longitude":79.702},
    {"hub_/_firm_name":"Puttur Export Yard (seasonal)","latitude":13.445,"longitude":79.548},
    {"hub_/_firm_name":"Bangarupalem APMC","latitude":13.212,"longitude":78.968},
    {"hub_/_firm_name":"Chittoor APMC","latitude":13.2115,"longitude":79.112},
    {"hub_/_firm_name":"Punganur Market Yard","latitude":13.362,"longitude":78.5805},
    {"hub_/_firm_name":"Pileru Market / Packhouse","latitude":13.6515,"longitude":78.941},
]

ABROAD_EXPORT_DATA = [
    {"place_name":"Tirupati APMC / Market Yard","latitude":13.6288,"longitude":79.4192},
    {"place_name":"Renigunta Packhouse & Cold Room","latitude":13.6519,"longitude":79.5126},
    {"place_name":"Rayachoti APMC","latitude":14.0532,"longitude":78.7516},
    {"place_name":"Rajampet APMC","latitude":14.195,"longitude":79.1585},
    {"place_name":"Srikalahasti Collection & Cold Room","latitude":13.749,"longitude":79.702},
    {"place_name":"Chandragiri Packhouse","latitude":13.566,"longitude":79.317},
    {"place_name":"Grofresh Agrofoods Export Pack","latitude":13.215,"longitude":79.055},
    {"place_name":"Roshan Fruits India Pvt Ltd","latitude":14.06,"longitude":78.755},
    {"place_name":"Navya Foods Export Unit","latitude":13.21,"longitude":78.745},
    {"place_name":"Bright Mangoes Export Packers","latitude":13.205,"longitude":78.76},
]

COLD_STORAGE_DATA = [
    {"storage_name":"New Frostys Cold Storage","latitude":13.6295,"longitude":79.435},
    {"storage_name":"Renigunta Cold Storage","latitude":13.6385,"longitude":79.5068},
    {"storage_name":"Rayachoti Cold Storage Pvt Ltd","latitude":14.0532,"longitude":78.751},
    {"storage_name":"Rajampet Cold Storage","latitude":14.1852,"longitude":79.1623},
    {"storage_name":"Madanapalle Road Cold Storage","latitude":13.5644,"longitude":78.4812},
    {"storage_name":"Annamayya Fruits Cold Storage","latitude":14.045,"longitude":78.761},
    {"storage_name":"MKB Cold Storage","latitude":13.3644,"longitude":78.5831},
    {"storage_name":"Murugan Cold Storage Pvt Ltd","latitude":13.3598,"longitude":78.5712},
    {"storage_name":"KN Cold Storage","latitude":13.6515,"longitude":78.4892},
    {"storage_name":"Balaji Banana & Fruits","latitude":13.439,"longitude":79.552},
]

FPO_DATA = [
    {"fpo_name":"Tirupati Horticulture Producer Company Ltd","latitude":13.6288,"longitude":79.4192},
    {"fpo_name":"Renigunta Mango Growers FPC","latitude":13.6519,"longitude":79.5126},
    {"fpo_name":"Srikalahasti Horticulture FPC","latitude":13.749,"longitude":79.702},
    {"fpo_name":"Puttur Farmers Producer Company","latitude":13.44,"longitude":79.55},
    {"fpo_name":"Chittoor Farmer Producer Company","latitude":13.217,"longitude":79.1},
    {"fpo_name":"Pileru Horticulture Farmer Producer Company","latitude":13.44,"longitude":78.98},
    {"fpo_name":"Punganur Growers FPC","latitude":13.366,"longitude":78.571},
    {"fpo_name":"Rayachoti Mango Growers FPC","latitude":14.0532,"longitude":78.7516},
    {"fpo_name":"Venkatagiri / Tirupati Regional FPC","latitude":13.96,"longitude":79.58},
    {"fpo_name":"Naidupeta Area FPC","latitude":13.9,"longitude":79.9},
]

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def translate_village(name, lang):
    if lang == "en":
        return name
    d = VILLAGE_TRANSLATIONS.get(lang, {})
    return d.get(name.upper(), name)

def translate_mandal(name, lang):
    return translate_village(name, lang)

def translate_cat(cat, lang):
    return CAT_TRANSLATIONS.get(lang, CAT_TRANSLATIONS["en"]).get(cat, cat)

def compute_results(v_lat, v_lon, base_price, qty, variety):
    var_accept = {
        "Mandi":        ["Banganapalli","Totapuri","Neelam","Rasalu"],
        "Processing":   ["Totapuri","Neelam"],
        "Pulp":         ["Totapuri"],
        "Pickle":       ["Totapuri","Rasalu"],
        "Local Export": ["Banganapalli"],
        "Abroad Export":["Banganapalli"],
    }
    margin_map = {
        "Mandi":0, "Processing":0.03, "Pulp":0.04,
        "Pickle":0.025, "Local Export":0.05, "Abroad Export":0.07
    }
    datasets = {
        "Mandi":        [(r["place"],   r["lat"],       r["long"])       for r in PRICES_DATA],
        "Processing":   [(r["facility_name"], r["latitude"], r["longitude"]) for r in PROCESSING_DATA],
        "Pulp":         [(r["Facility Name"], r["Latitude"], r["Longitude"]) for r in PULP_DATA],
        "Pickle":       [(r["firm_name"],r["latitude"], r["longitude"])  for r in PICKLE_DATA],
        "Local Export": [(r["hub_/_firm_name"],r["latitude"],r["longitude"]) for r in LOCAL_EXPORT_DATA],
        "Abroad Export":[(r["place_name"],r["latitude"],r["longitude"])  for r in ABROAD_EXPORT_DATA],
    }
    results = []
    for cat, rows in datasets.items():
        if variety not in var_accept[cat]:
            continue
        margin = margin_map[cat]
        for name, lat, lon in rows:
            dist = haversine(v_lat, v_lon, lat, lon)
            transport = dist * 12 * qty
            revenue   = base_price * (1 + margin) * 100 * qty
            net       = revenue - transport
            results.append({
                "Category": cat, "Name": name,
                "Distance_km": round(dist, 1),
                "Revenue": int(revenue),
                "Transport": int(transport),
                "NetProfit": int(net),
                "Lat": lat, "Lon": lon,
            })
    seen = set()
    deduped = []
    for r in results:
        k = r["Name"] + "|" + r["Category"]
        if k not in seen:
            seen.add(k)
            deduped.append(r)
    deduped.sort(key=lambda x: -x["NetProfit"])
    return deduped[:10]

def get_base_price(v_lat, v_lon):
    best_dist, price = float("inf"), 29
    for p in PRICES_DATA:
        d = haversine(v_lat, v_lon, p["lat"], p["long"])
        if d < best_dist:
            best_dist = d
            price = p["today_price"]
    return price

CAT_COLORS = {
    "Mandi":"#1565C0","Processing":"#6A1B9A","Pulp":"#F57F17",
    "Pickle":"#880E4F","Local Export":"#1B5E20","Abroad Export":"#004D40"
}
CAT_BG = {
    "Mandi":"#e3f2fd","Processing":"#f3e5f5","Pulp":"#fff8e1",
    "Pickle":"#fce4ec","Local Export":"#e8f5e9","Abroad Export":"#e0f2f1"
}
ROUTE_COLORS = ["#e74c3c","#3498db","#2ecc71","#f39c12","#9b59b6",
                "#1abc9c","#e67e22","#e91e63","#00bcd4","#8bc34a"]

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "results" not in st.session_state:
    st.session_state.results = None
if "variety" not in st.session_state:
    st.session_state.variety = "Banganapalli"

# ─────────────────────────────────────────────
# LANGUAGE SELECTOR (top bar)
# ─────────────────────────────────────────────
lang_col1, lang_col2, lang_col3, lang_col4, lang_col5 = st.columns([1, 1, 1, 1, 6])
with lang_col1:
    if st.button("🇬🇧 English", use_container_width=True,
                 type="primary" if st.session_state.lang == "en" else "secondary"):
        st.session_state.lang = "en"; st.rerun()
with lang_col2:
    if st.button("తెలుగు", use_container_width=True,
                 type="primary" if st.session_state.lang == "te" else "secondary"):
        st.session_state.lang = "te"; st.rerun()
with lang_col3:
    if st.button("हिंदी", use_container_width=True,
                 type="primary" if st.session_state.lang == "hi" else "secondary"):
        st.session_state.lang = "hi"; st.rerun()
with lang_col4:
    if st.button("தமிழ்", use_container_width=True,
                 type="primary" if st.session_state.lang == "ta" else "secondary"):
        st.session_state.lang = "ta"; st.rerun()

lang = st.session_state.lang
tr = T[lang]

# ─────────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero-banner">
  <h1>{tr['title']}</h1>
  <p>{tr['subtitle']}</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PRICE TICKER
# ─────────────────────────────────────────────
ticker_items = ""
for p in PRICES_DATA[:12]:
    diff = p["today_price"] - p["yesterday_price"]
    arrow = "▲" if diff >= 0 else "▼"
    cls   = "ticker-up" if diff >= 0 else "ticker-down"
    ticker_items += f'<span class="ticker-item">{p["place"]}: <span class="ticker-price">₹{p["today_price"]}/kg</span> <span class="{cls}">{arrow}</span></span>'
st.markdown(f'<div class="ticker-bar">📈 {tr["ticker_label"]} &nbsp;&nbsp; {ticker_items}</div>',
            unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### " + tr["lname"])
    farmer_name = st.text_input("", placeholder=tr["name_ph"], label_visibility="collapsed")

    # Mandal selector (translated)
    mandals = sorted(set(v["Mandal"] for v in VILLAGES_DATA))
    mandal_display = [translate_mandal(m, lang) for m in mandals]
    mandal_map = dict(zip(mandal_display, mandals))

    st.markdown("### 📍 " + ("మండల్" if lang=="te" else "मंडल" if lang=="hi" else "மண்டலம்" if lang=="ta" else "Mandal"))
    sel_mandal_disp = st.selectbox("", ["— " + tr["mandal_ph"] + " —"] + mandal_display, label_visibility="collapsed")

    # Village selector (translated)
    st.markdown("### " + tr["lvillage"])
    village_val = None
    if sel_mandal_disp and not sel_mandal_disp.startswith("—"):
        sel_mandal_en = mandal_map[sel_mandal_disp]
        villages_in_mandal = [v["Gram Panchayat"] for v in VILLAGES_DATA if v["Mandal"] == sel_mandal_en]
        village_display = [translate_village(v, lang) for v in villages_in_mandal]
        vill_map = dict(zip(village_display, villages_in_mandal))
        sel_vill_disp = st.selectbox("", ["— " + tr["village_ph"] + " —"] + village_display, label_visibility="collapsed")
        if sel_vill_disp and not sel_vill_disp.startswith("—"):
            village_val = vill_map[sel_vill_disp]
    else:
        st.selectbox("", ["— " + tr["village_ph"] + " —"], label_visibility="collapsed", disabled=True)

    # Variety selection
    st.markdown("### " + tr["lvar"])
    varieties = ["Banganapalli", "Totapuri", "Neelam", "Rasalu"]
    var_labels = [tr["var_labels"][v] for v in varieties]
    sel_var_idx = varieties.index(st.session_state.variety)
    cols_v = st.columns(2)
    for i, (v, lbl) in enumerate(zip(varieties, var_labels)):
        with cols_v[i % 2]:
            selected = (v == st.session_state.variety)
            btn_type = "primary" if selected else "secondary"
            if st.button(lbl, key=f"var_{v}", use_container_width=True, type=btn_type):
                st.session_state.variety = v
                st.rerun()

    # Quantity
    st.markdown("### " + tr["lqty"])
    qty = st.number_input("", min_value=1, max_value=500, value=10, label_visibility="collapsed")

    # Run button
    st.markdown("<br>", unsafe_allow_html=True)
    run_clicked = st.button(tr["run_btn"], use_container_width=True, type="primary")

    # Tip box
    st.markdown(f'<div class="tip-box">{tr["tip"]}</div>', unsafe_allow_html=True)

    # Cold storage & FPO info
    st.markdown("---")
    st.markdown("#### 🏭 Cold Storages Near You")
    if village_val:
        vrow = next((v for v in VILLAGES_DATA if v["Gram Panchayat"] == village_val), None)
        if vrow:
            cs_dists = [(haversine(vrow["Latitude"], vrow["Longitude"], c["latitude"], c["longitude"]), c["storage_name"]) for c in COLD_STORAGE_DATA]
            cs_dists.sort()
            for d, name in cs_dists[:3]:
                st.markdown(f"🏢 **{name}** — {round(d,1)} km")
    else:
        st.info("Select village to see nearby cold storages")

    st.markdown("#### 🤝 FPOs Near You")
    if village_val:
        vrow = next((v for v in VILLAGES_DATA if v["Gram Panchayat"] == village_val), None)
        if vrow:
            fpo_dists = [(haversine(vrow["Latitude"], vrow["Longitude"], f["latitude"], f["longitude"]), f["fpo_name"]) for f in FPO_DATA]
            fpo_dists.sort()
            for d, name in fpo_dists[:3]:
                st.markdown(f"🌱 **{name}** — {round(d,1)} km")
    else:
        st.info("Select village to see nearby FPOs")

# ─────────────────────────────────────────────
# RUN ANALYSIS
# ─────────────────────────────────────────────
if run_clicked:
    if not village_val:
        st.error("⚠️ Please select your village first!")
    else:
        vrow = next((v for v in VILLAGES_DATA if v["Gram Panchayat"] == village_val), None)
        if vrow:
            v_lat = vrow["Latitude"]
            v_lon = vrow["Longitude"]
            base_price = get_base_price(v_lat, v_lon)
            with st.spinner(tr["loading"]):
                results = compute_results(v_lat, v_lon, base_price, qty, st.session_state.variety)
            if results:
                st.session_state.results = {
                    "data": results,
                    "farmer_name": farmer_name or "Farmer",
                    "village": village_val,
                    "base_price": base_price,
                    "qty": qty,
                    "v_lat": v_lat,
                    "v_lon": v_lon,
                    "variety": st.session_state.variety,
                }
            else:
                st.warning(tr["no_results"])

# ─────────────────────────────────────────────
# DISPLAY RESULTS
# ─────────────────────────────────────────────
if st.session_state.results:
    R = st.session_state.results
    top10 = R["data"]
    best  = top10[0]
    name  = R["farmer_name"]
    village_disp = translate_village(R["village"], lang)

    # Greeting
    st.markdown(f"""
    <div style="background:linear-gradient(90deg,#1b4332,#2d6a4f);color:white;border-radius:12px;
                padding:14px 20px;margin-bottom:18px;font-size:17px;font-weight:700">
        🥭 {tr['namaste']}, <span style="color:#ffd166">{name}</span>!
    </div>
    """, unsafe_allow_html=True)

    # Metric cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""<div class="metric-card">
            <div class="label">📈 {tr['base_price']}</div>
            <div class="value">₹{R['base_price']}/kg</div>
            <div class="sub">{tr['your_village']}: {village_disp}</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class="metric-card">
            <div class="label">📦 Quantity</div>
            <div class="value">{R['qty']} qtl</div>
            <div class="sub">{R['qty']*100} kg total</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class="metric-card best">
            <div class="label">🏆 {tr['best_profit']}</div>
            <div class="value">₹{best['NetProfit']:,}</div>
            <div class="sub">{best['Name'][:28]}</div>
        </div>""", unsafe_allow_html=True)
    with m4:
        st.markdown(f"""<div class="metric-card">
            <div class="label">🥭 {tr['best_market']}</div>
            <div class="value" style="font-size:15px;line-height:1.3">{best['Name'][:22]}</div>
            <div class="sub">{best['Distance_km']} km away</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── TABS ──
    tab1, tab2, tab3, tab4 = st.tabs([tr["tab1"], tr["tab2"], tr["tab3"], tr["tab4"]])

    # ── TAB 1: TABLE ──
    with tab1:
        st.markdown(f"#### {tr['tab1']}")
        max_profit = best["NetProfit"]
        table_rows = []
        for i, r in enumerate(top10):
            pct = int(r["NetProfit"] / max_profit * 100)
            rank_emoji = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"
            cat_translated = translate_cat(r["Category"], lang)
            table_rows.append({
                tr["rank"]:     rank_emoji,
                tr["market"]:   r["Name"],
                tr["cat"]:      cat_translated,
                tr["dist"]:     f"{r['Distance_km']} km",
                tr["rev"]:      f"₹{r['Revenue']:,}",
                tr["trans"]:    f"₹{r['Transport']:,}",
                tr["profit"]:   f"₹{r['NetProfit']:,}",
                "% of Best":    f"{pct}%",
            })
        df = pd.DataFrame(table_rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

    # ── TAB 2: CHARTS ──
    with tab2:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"#### {tr['chart_title']}")
            names  = [r["Name"][:22]+"..." if len(r["Name"])>22 else r["Name"] for r in top10]
            profits = [r["NetProfit"] for r in top10]
            transports = [r["Transport"] for r in top10]
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                name=tr["profit"], y=names, x=profits,
                orientation="h", marker_color=["#2d6a4f"]+["#52b788"]*9,
                text=[f"₹{p:,}" for p in profits], textposition="auto"
            ))
            fig_bar.add_trace(go.Bar(
                name=tr["trans"], y=names, x=transports,
                orientation="h", marker_color="#fcd34d",
                text=[f"₹{t:,}" for t in transports], textposition="auto"
            ))
            fig_bar.update_layout(
                barmode="group", height=420,
                xaxis_title="₹ Amount", yaxis_title="",
                font=dict(family="Poppins"), plot_bgcolor="#f9fdf5",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_b:
            st.markdown(f"#### {tr['pie_title']}")
            cat_sums = {}
            for r in top10:
                cat_translated = translate_cat(r["Category"], lang)
                cat_sums[cat_translated] = cat_sums.get(cat_translated, 0) + r["NetProfit"]
            fig_pie = px.pie(
                names=list(cat_sums.keys()),
                values=list(cat_sums.values()),
                color_discrete_sequence=["#2d6a4f","#52b788","#f39c12","#e74c3c","#3498db","#9b59b6"],
                hole=0.4
            )
            fig_pie.update_layout(height=420, font=dict(family="Poppins"))
            st.plotly_chart(fig_pie, use_container_width=True)

    # ── TAB 3: MAP ──
    with tab3:
        st.markdown(f"#### {tr['map_title']}")
        import plotly.graph_objects as go_map

        fig_map = go.Figure()

        # Village marker
        fig_map.add_trace(go.Scattermapbox(
            lat=[R["v_lat"]], lon=[R["v_lon"]],
            mode="markers+text",
            marker=dict(size=20, color="#1a2e1a", symbol="star"),
            text=[f"🏘️ {village_disp}"],
            textposition="top right",
            name=f"🏘️ {village_disp}",
            hovertemplate=f"<b>Your Village</b><br>{village_disp}<extra></extra>"
        ))

        # Market markers with lines
        for i, r in enumerate(top10):
            color = ROUTE_COLORS[i % len(ROUTE_COLORS)]
            cat_tr = translate_cat(r["Category"], lang)
            # Line from village to market
            fig_map.add_trace(go.Scattermapbox(
                lat=[R["v_lat"], r["Lat"]],
                lon=[R["v_lon"], r["Lon"]],
                mode="lines",
                line=dict(width=2, color=color),
                showlegend=False,
                hoverinfo="skip"
            ))
            # Market point
            medal = "🥇" if i==0 else "🥈" if i==1 else "🥉" if i==2 else f"#{i+1}"
            fig_map.add_trace(go.Scattermapbox(
                lat=[r["Lat"]], lon=[r["Lon"]],
                mode="markers+text",
                marker=dict(size=16, color=color),
                text=[f"{medal} {r['Name'][:18]}"],
                textposition="top right",
                name=f"{medal} {r['Name'][:22]}",
                hovertemplate=(
                    f"<b>{medal} {r['Name']}</b><br>"
                    f"Type: {cat_tr}<br>"
                    f"Distance: {r['Distance_km']} km<br>"
                    f"Net Profit: ₹{r['NetProfit']:,}<extra></extra>"
                )
            ))

        fig_map.update_layout(
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=R["v_lat"], lon=R["v_lon"]),
                zoom=8
            ),
            height=520,
            margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(
                orientation="v", x=0.01, y=0.99,
                bgcolor="rgba(255,255,255,0.85)",
                bordercolor="#c8e6c9", borderwidth=1
            ),
            font=dict(family="Poppins")
        )
        st.plotly_chart(fig_map, use_container_width=True)

    # ── TAB 4: ADVICE ──
    with tab4:
        st.markdown(f"#### {tr['adv_title']} ({translate_village(R['variety'], lang) if lang!='en' else R['variety']})")
        cols_adv = st.columns(2)
        for i, (icon, title, body) in enumerate(tr["adv"]):
            with cols_adv[i % 2]:
                st.markdown(f"""
                <div class="advice-card">
                    <div class="icon">{icon}</div>
                    <div class="title">{title}</div>
                    <div class="body">{body}</div>
                </div>
                """, unsafe_allow_html=True)

        # Download results
        st.markdown("---")
        st.markdown("#### 📥 Download Results")
        df_download = pd.DataFrame([{
            tr["rank"]:   i+1,
            tr["market"]: r["Name"],
            tr["cat"]:    translate_cat(r["Category"], lang),
            tr["dist"]:   r["Distance_km"],
            tr["rev"]:    r["Revenue"],
            tr["trans"]:  r["Transport"],
            tr["profit"]: r["NetProfit"],
        } for i, r in enumerate(top10)])
        csv = df_download.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"mango_profit_results_{R['village']}.csv",
            mime="text/csv",
            use_container_width=True
        )

else:
    # Welcome screen
    st.markdown(f"""
    <div style="text-align:center; padding:60px 20px">
        <div style="font-size:80px; animation:sway 3s ease-in-out infinite">🥭</div>
        <h2 style="color:#2d6a4f; margin:16px 0 8px">{tr['wctitle']}</h2>
        <p style="color:#5a7a5f; max-width:420px; margin:0 auto; line-height:1.7">{tr['wcsub']}</p>
    </div>
    <style>
    @keyframes sway {{0%,100%{{transform:rotate(-10deg)}}50%{{transform:rotate(10deg)}}}}
    </style>
    """, unsafe_allow_html=True)

    wc1, wc2, wc3 = st.columns(3)
    wc_data = [
        ("📍", tr.get("wctitle","Pick Village"), "We find nearby markets"),
        ("🥭", "Select Variety", "Matched to right buyers"),
        ("💰", "See Profit", "Compare all options instantly"),
    ]
    for col, (icon, title, sub) in zip([wc1, wc2, wc3], wc_data):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="padding:20px">
                <div style="font-size:32px; margin-bottom:8px">{icon}</div>
                <div style="font-weight:700; color:#1a2e1a; font-size:14px; margin-bottom:4px">{title}</div>
                <div style="font-size:12px; color:#5a7a5f">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#5a7a5f; font-size:12px; padding:8px 0">
    🥭 Farmer's Mango Profit Navigator &nbsp;|&nbsp; Helping farmers across Andhra Pradesh &nbsp;|&nbsp; 🇮🇳
</div>
""", unsafe_allow_html=True)
