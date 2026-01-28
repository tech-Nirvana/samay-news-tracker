"""
=============================================================================
NIRVANA READ - FIXED RSS Sources (Fast & Working Feeds Only)
=============================================================================
"""

# ============== VERIFIED WORKING SOURCES ==============
CURATED_SOURCES = {
    # ============== ENGLISH SOURCES ==============
    'times_of_india': {
        'name': 'Times of India',
        'language': 'english',
        'reliability': 8,
        'feeds': {
            'top': 'https://timesofindia.indiatimes.com/rssfeedstopstories.cms'
        },
        'focus': ['social', 'economic', 'crime']
    },
    'indian_express': {
        'name': 'Indian Express',
        'language': 'english',
        'reliability': 10,
        'feeds': {
            'india': 'https://indianexpress.com/section/india/feed/'
        },
        'focus': ['rights', 'social', 'economic', 'crime']
    },
    'ndtv': {
        'name': 'NDTV',
        'language': 'english',
        'reliability': 8,
        'feeds': {
            'india': 'https://feeds.feedburner.com/ndtvnews-top-stories'
        },
        'focus': ['social', 'health', 'economic', 'crime']
    },
    'hindustan_times': {
        'name': 'Hindustan Times',
        'language': 'english',
        'reliability': 8,
        'feeds': {
            'india': 'https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml'
        },
        'focus': ['social', 'health', 'economic', 'crime']
    },
    'the_print': {
        'name': 'The Print',
        'language': 'english',
        'reliability': 8,
        'feeds': {
            'india': 'https://theprint.in/category/india/feed/'
        },
        'focus': ['rights', 'economic', 'social']
    },
    'livemint': {
        'name': 'Livemint',
        'language': 'english',
        'reliability': 9,
        'feeds': {
            'news': 'https://www.livemint.com/rss/news'
        },
        'focus': ['economic', 'rights', 'science']
    },
    'the_quint': {
        'name': 'The Quint',
        'language': 'english',
        'reliability': 8,
        'feeds': {
            'news': 'https://www.thequint.com/api/v1/feed'
        },
        'focus': ['rights', 'social', 'health', 'crime']
    },
    'news18': {
        'name': 'News18',
        'language': 'english',
        'reliability': 7,
        'feeds': {
            'india': 'https://www.news18.com/rss/india.xml'
        },
        'focus': ['social', 'economic', 'crime']
    },
    'firstpost': {
        'name': 'Firstpost',
        'language': 'english',
        'reliability': 7,
        'feeds': {
            'india': 'https://www.firstpost.com/rss/india.xml'
        },
        'focus': ['social', 'economic', 'rights']
    },
    'down_to_earth': {
        'name': 'Down To Earth',
        'language': 'english',
        'reliability': 9,
        'feeds': {
            'health': 'https://www.downtoearth.org.in/rss/health'
        },
        'focus': ['health', 'environment']
    },
    
    # ============== HINDI SOURCES ==============
    'bbc_hindi': {
        'name': 'BBC Hindi',
        'language': 'hindi',
        'reliability': 10,
        'feeds': {
            'india': 'https://feeds.bbci.co.uk/hindi/india/rss.xml'
        },
        'focus': ['social', 'health', 'economic', 'rights', 'crime']
    },
    'navbharat_times': {
        'name': 'नवभारत टाइम्स',
        'language': 'hindi',
        'reliability': 8,
        'feeds': {
            'news': 'https://navbharattimes.indiatimes.com/rssfeedstopstories.cms'
        },
        'focus': ['social', 'economic', 'crime']
    },
    'dainik_jagran': {
        'name': 'दैनिक जागरण',
        'language': 'hindi',
        'reliability': 8,
        'feeds': {
            'national': 'https://www.jagran.com/rss/news-national-hindi.xml'
        },
        'focus': ['social', 'economic', 'rights', 'crime']
    },
    'ndtv_hindi': {
        'name': 'NDTV Hindi',
        'language': 'hindi',
        'reliability': 8,
        'feeds': {
            'news': 'https://khabar.ndtv.com/rss/india'
        },
        'focus': ['social', 'health', 'economic', 'crime']
    }
}

# ============== 9 ENHANCED CATEGORIES ==============
FOCUS_CATEGORIES = {
    'rights': {
        'name_en': 'Rights & Laws',
        'name_hi': 'अधिकार व कानून',
        'keywords': [
            'rights', 'law', 'court', 'judgment', 'verdict', 'supreme court',
            'high court', 'legal', 'justice', 'constitution', 'freedom',
            'civil rights', 'human rights', 'arrest', 'bail', 'custody',
            'petition', 'ruling', 'advocate', 'lawyer', 'PIL',
            'अधिकार', 'कानून', 'न्यायालय', 'फैसला', 'सुप्रीम कोर्ट',
            'न्याय', 'संविधान', 'गिरफ्तारी', 'जमानत', 'याचिका'
        ],
        'context_words': ['verdict', 'ruling', 'legal', 'constitutional'],
        'india_keywords': ['supreme court india', 'high court', 'cji', 'पीआईएल'],
        'color': 'purple',
        'weight': 1.0
    },
    
    'health': {
        'name_en': 'Health & Safety',
        'name_hi': 'स्वास्थ्य व सुरक्षा',
        'keywords': [
            'health', 'hospital', 'doctor', 'medicine', 'disease', 'outbreak',
            'vaccine', 'treatment', 'medical', 'patient', 'covid', 'flu',
            'dengue', 'malaria', 'tuberculosis', 'diabetes', 'cancer',
            'food safety', 'drug', 'healthcare', 'ambulance', 'emergency',
            'air quality', 'pollution', 'aqi', 'smog', 'breathing',
            'स्वास्थ्य', 'अस्पताल', 'डॉक्टर', 'दवा', 'बीमारी',
            'टीका', 'इलाज', 'मरीज', 'प्रदूषण', 'वायु'
        ],
        'context_words': ['epidemic', 'pandemic', 'contamination', 'safety alert'],
        'india_keywords': ['aiims', 'icmr', 'ayush', 'delhi pollution'],
        'color': 'green',
        'weight': 1.2
    },
    
    'social': {
        'name_en': 'Social Issues',
        'name_hi': 'सामाजिक मुद्दे',
        'keywords': [
            'women', 'rape', 'harassment', 'violence', 'women safety',
            'child abuse', 'domestic violence', 'dowry', 'trafficking',
            'caste', 'dalit', 'discrimination', 'atrocity', 'lynching',
            'mob violence', 'protest', 'demonstration', 'strike',
            'unemployment', 'job loss', 'layoff', 'worker', 'labor',
            'महिला', 'बलात्कार', 'हिंसा', 'जाति', 'दलित',
            'भेदभाव', 'विरोध', 'प्रदर्शन', 'बेरोजगारी', 'मजदूर'
        ],
        'context_words': ['activism', 'movement', 'solidarity', 'marginalized'],
        'india_keywords': ['reservation', 'sc st', 'obc', 'आरक्षण'],
        'color': 'blue',
        'weight': 1.1
    },
    
    'economic': {
        'name_en': 'Economic Impact',
        'name_hi': 'आर्थिक प्रभाव',
        'keywords': [
            'price', 'inflation', 'petrol', 'diesel', 'lpg', 'gas cylinder',
            'food price', 'onion', 'tomato', 'wheat', 'rice', 'dal',
            'ration', 'subsidy', 'pds', 'ration card',
            'bank', 'atm', 'loan', 'interest rate', 'emi', 'credit',
            'salary', 'pension', 'income', 'tax', 'gst', 'income tax',
            'scheme', 'yojana', 'benefit', 'welfare', 'dbt',
            'train', 'railway', 'bus', 'metro', 'toll', 'fare',
            'electricity', 'power cut', 'water supply', 'bill',
            'budget', 'economy', 'fiscal', 'gdp', 'growth',
            'rupee', 'dollar', 'currency', 'rbi', 'reserve bank',
            'कीमत', 'महंगाई', 'पेट्रोल', 'गैस', 'राशन',
            'बैंक', 'लोन', 'पेंशन', 'कर', 'योजना',
            'रेलवे', 'बिजली', 'पानी', 'बजट', 'रुपया'
        ],
        'context_words': ['hike', 'reduction', 'announcement', 'relief'],
        'india_keywords': ['union budget', 'finance minister', 'rbi governor'],
        'color': 'yellow',
        'weight': 1.3
    },
    
    'religion': {
        'name_en': 'Religion & Superstition',
        'name_hi': 'धर्म व अंधविश्वास',
        'keywords': [
            'religious', 'communal', 'intolerance', 'fundamentalism',
            'extremism', 'sectarian', 'superstition', 'orthodox',
            'riot', 'violence', 'hate crime', 'mob lynching',
            'temple', 'mosque', 'church', 'worship', 'ritual',
            'godman', 'baba', 'fake baba', 'miracle', 'faith healer',
            'black magic', 'witchcraft', 'occult', 'astrology scam',
            'सांप्रदायिक', 'धार्मिक', 'अंधविश्वास', 'कट्टरपंथ',
            'दंगा', 'मॉब लिंचिंग', 'मंदिर', 'मस्जिद', 'गिरजाघर',
            'बाबा', 'चमत्कार', 'टोना', 'काला जादू', 'ज्योतिष'
        ],
        'context_words': ['radical', 'fanatic', 'belief', 'conversion'],
        'india_keywords': ['hindu muslim', 'mandir masjid', 'धार्मिक तनाव'],
        'color': 'red',
        'weight': 1.0
    },
    
    'science': {
        'name_en': 'Science & Innovation',
        'name_hi': 'विज्ञान व तकनीक',
        'keywords': [
            'science', 'research', 'innovation', 'technology',
            'discovery', 'invention', 'scientist', 'laboratory',
            'isro', 'space', 'satellite', 'mission', 'rocket',
            'ai', 'artificial intelligence', 'machine learning',
            'digital', 'internet', 'cyber', 'data',
            'vaccine', 'cure', 'treatment', 'medical breakthrough',
            'energy', 'solar', 'renewable', 'green tech',
            'विज्ञान', 'अनुसंधान', 'तकनीक', 'खोज',
            'इसरो', 'अंतरिक्ष', 'उपग्रह', 'डिजिटल'
        ],
        'context_words': ['breakthrough', 'innovation', 'advancement', 'development'],
        'india_keywords': ['isro', 'drdo', 'csir', 'iit', 'chandrayaan'],
        'color': 'indigo',
        'weight': 0.9
    },
    
    'environment': {
        'name_en': 'Environment & Climate',
        'name_hi': 'पर्यावरण व जलवायु',
        'keywords': [
            'climate change', 'global warming', 'greenhouse', 'emissions',
            'deforestation', 'forest', 'trees', 'wildlife',
            'pollution', 'air quality', 'water pollution', 'river',
            'flood', 'drought', 'cyclone', 'earthquake', 'disaster',
            'monsoon', 'rainfall', 'weather', 'heatwave', 'cold wave',
            'renewable', 'solar', 'wind', 'hydro', 'clean energy',
            'plastic', 'waste', 'garbage', 'sanitation', 'cleanliness',
            'जलवायु', 'पर्यावरण', 'प्रदूषण', 'वन', 'वन्यजीव',
            'बाढ़', 'सूखा', 'चक्रवात', 'भूकंप', 'आपदा',
            'मानसून', 'बारिश', 'गर्मी', 'प्लास्टिक', 'कचरा'
        ],
        'context_words': ['conservation', 'protection', 'sustainability', 'eco-friendly'],
        'india_keywords': ['ganga', 'yamuna', 'himalaya', 'sundarbans', 'delhi pollution'],
        'color': 'teal',
        'weight': 1.1
    },
    
    'crime': {
        'name_en': 'Crime & Justice',
        'name_hi': 'अपराध व न्याय',
        'keywords': [
            'crime', 'murder', 'theft', 'robbery', 'kidnapping',
            'fraud', 'scam', 'corruption', 'bribery', 'embezzlement',
            'police', 'arrest', 'investigation', 'cbi', 'ed',
            'accused', 'suspect', 'criminal', 'convict', 'prisoner',
            'rape', 'assault', 'attack', 'violence', 'shooting',
            'drug', 'narcotic', 'smuggling', 'trafficking',
            'cybercrime', 'hacking', 'online fraud', 'phishing',
            'अपराध', 'हत्या', 'चोरी', 'डकैती', 'अपहरण',
            'घोटाला', 'भ्रष्टाचार', 'पुलिस', 'गिरफ्तारी',
            'बलात्कार', 'हमला', 'साइबर अपराध', 'धोखाधड़ी'
        ],
        'context_words': ['charged', 'booked', 'fir', 'case registered'],
        'india_keywords': ['cbi', 'ed', 'ncb', 'सीबीआई', 'एनसीबी'],
        'color': 'rose',
        'weight': 1.0
    },
    
    'education': {
        'name_en': 'Education & Youth',
        'name_hi': 'शिक्षा व युवा',
        'keywords': [
            'education', 'school', 'college', 'university', 'student',
            'exam', 'board', 'cbse', 'icse', 'neet', 'jee', 'iit',
            'admission', 'fee', 'scholarship', 'hostel',
            'teacher', 'professor', 'principal', 'vice chancellor',
            'syllabus', 'curriculum', 'degree', 'certificate',
            'coaching', 'tuition', 'private tuition',
            'youth', 'teenager', 'young', 'campus',
            'suicide', 'depression', 'stress', 'pressure',
            'dropout', 'attendance', 'marks', 'result',
            'शिक्षा', 'स्कूल', 'कॉलेज', 'छात्र', 'परीक्षा',
            'बोर्ड', 'नीट', 'जेईई', 'शुल्क', 'छात्रवृत्ति',
            'शिक्षक', 'पाठ्यक्रम', 'कोचिंग', 'युवा', 'आत्महत्या'
        ],
        'context_words': ['academic', 'learning', 'examination', 'admission'],
        'india_keywords': ['cbse', 'neet', 'jee', 'ugc', 'ncert'],
        'color': 'cyan',
        'weight': 1.0
    }
}

# ============== HELPER FUNCTIONS ==============

def get_all_feed_urls():
    """Get all RSS feed URLs with metadata"""
    feeds = []
    for source_key, source_data in CURATED_SOURCES.items():
        for feed_key, feed_url in source_data['feeds'].items():
            feeds.append({
                'source_key': source_key,
                'source_name': source_data['name'],
                'language': source_data['language'],
                'reliability': source_data['reliability'],
                'feed_key': feed_key,
                'url': feed_url,
                'focus_areas': source_data['focus']
            })
    return feeds

def get_category_keywords(category_key):
    """Get keywords for a specific category"""
    return FOCUS_CATEGORIES.get(category_key, {}).get('keywords', [])

def is_relevant_to_citizen(title, description):
    """
    Quick check: Is this news relevant to an average Indian citizen?
    Returns: (is_relevant, matched_category, confidence)
    """
    text = f"{title} {description}".lower()
    
    best_match = None
    best_score = 0
    
    # Check each category
    for category_key, category_data in FOCUS_CATEGORIES.items():
        keywords = category_data['keywords']
        matches = sum(1 for kw in keywords if kw in text)
        
        # Weight by category importance
        weighted_score = matches * category_data.get('weight', 1.0)
        
        # If 1+ keywords match, consider relevant
        if weighted_score > best_score:
            best_score = weighted_score
            best_match = category_key
    
    if best_match and best_score >= 1:
        return True, best_match, best_score
    
    return False, None, 0
