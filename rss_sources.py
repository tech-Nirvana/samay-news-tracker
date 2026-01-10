"""
=============================================================================
NIRVANA READ - Top 20 Curated Indian News Sources
Focus: Rights, Health, Social Issues, Economic Impact on Citizens
=============================================================================
"""

# ============== TOP 20 CURATED SOURCES ==============

# Focus Categories:
# B: Rights & Laws
# C: Health & Safety
# D: Social Issues
# E: Economic (citizen impact)

CURATED_SOURCES = {
    # ============== ENGLISH SOURCES (12) ==============
    'the_hindu': {
        'name': 'The Hindu',
        'language': 'english',
        'reliability': 10,  # 1-10 scale
        'feeds': {
            'national': 'https://www.thehindu.com/news/national/feeder/default.rss',
            'cities': 'https://www.thehindu.com/news/cities/feeder/default.rss'
        },
        'focus': ['rights', 'social', 'health', 'economic']
    },
    
    'indian_express': {
        'name': 'Indian Express',
        'language': 'english',
        'reliability': 10,
        'feeds': {
            'india': 'https://indianexpress.com/section/india/feed/',
            'cities': 'https://indianexpress.com/section/cities/feed/'
        },
        'focus': ['rights', 'social', 'economic']
    },
    
    'the_wire': {
        'name': 'The Wire',
        'language': 'english',
        'reliability': 9,
        'feeds': {
            'rights': 'https://thewire.in/rights/feed',
            'politics': 'https://thewire.in/politics/feed',
            'health': 'https://thewire.in/health/feed'
        },
        'focus': ['rights', 'social', 'health']
    },
    
    'scroll': {
        'name': 'Scroll.in',
        'language': 'english',
        'reliability': 9,
        'feeds': {
            'india': 'https://scroll.in/feeds/india.rss'
        },
        'focus': ['rights', 'social', 'economic']
    },
    
    'ndtv': {
        'name': 'NDTV',
        'language': 'english',
        'reliability': 8,
        'feeds': {
            'india': 'https://feeds.feedburner.com/ndtv/India'
        },
        'focus': ['social', 'health', 'economic']
    },
    
    'hindustan_times': {
        'name': 'Hindustan Times',
        'language': 'english',
        'reliability': 8,
        'feeds': {
            'india': 'https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml',
            'cities': 'https://www.hindustantimes.com/feeds/rss/cities/rssfeed.xml'
        },
        'focus': ['social', 'health', 'economic']
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
            'politics': 'https://www.livemint.com/rss/politics',
            'news': 'https://www.livemint.com/rss/news'
        },
        'focus': ['economic', 'rights']
    },
    
    'down_to_earth': {
        'name': 'Down To Earth',
        'language': 'english',
        'reliability': 9,
        'feeds': {
            'health': 'https://www.downtoearth.org.in/rss/health',
            'pollution': 'https://www.downtoearth.org.in/rss/air'
        },
        'focus': ['health', 'social']
    },
    
    'the_quint': {
        'name': 'The Quint',
        'language': 'english',
        'reliability': 8,
        'feeds': {
            'news': 'https://www.thequint.com/api/v1/feed'
        },
        'focus': ['rights', 'social', 'health']
    },
    
    'news18': {
        'name': 'News18',
        'language': 'english',
        'reliability': 7,
        'feeds': {
            'india': 'https://www.news18.com/rss/india.xml'
        },
        'focus': ['social', 'economic']
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
    
    # ============== HINDI SOURCES (8) ==============
    'bbc_hindi': {
        'name': 'BBC Hindi',
        'language': 'hindi',
        'reliability': 10,
        'feeds': {
            'india': 'https://feeds.bbci.co.uk/hindi/india/rss.xml'
        },
        'focus': ['social', 'health', 'economic', 'rights']
    },
    
    'navbharat_times': {
        'name': 'नवभारत टाइम्स',
        'language': 'hindi',
        'reliability': 8,
        'feeds': {
            'news': 'https://navbharattimes.indiatimes.com/rssfeedstopstories.cms'
        },
        'focus': ['social', 'economic']
    },
    
    'dainik_jagran': {
        'name': 'दैनिक जागरण',
        'language': 'hindi',
        'reliability': 8,
        'feeds': {
            'national': 'https://www.jagran.com/rss/news-national-hindi.xml'
        },
        'focus': ['social', 'economic', 'rights']
    },
    
    'amar_ujala': {
        'name': 'अमर उजाला',
        'language': 'hindi',
        'reliability': 8,
        'feeds': {
            'india': 'https://www.amarujala.com/rss/india-news.xml'
        },
        'focus': ['social', 'economic']
    },
    
    'ndtv_hindi': {
        'name': 'NDTV Hindi',
        'language': 'hindi',
        'reliability': 8,
        'feeds': {
            'news': 'https://khabar.ndtv.com/rss/india'
        },
        'focus': ['social', 'health', 'economic']
    },
    
    'patrika': {
        'name': 'पत्रिका',
        'language': 'hindi',
        'reliability': 7,
        'feeds': {
            'india': 'https://www.patrika.com/rss/india-news.xml'
        },
        'focus': ['social', 'economic']
    },
    
    'jagran_josh': {
        'name': 'Jagran Josh',
        'language': 'hindi',
        'reliability': 7,
        'feeds': {
            'current_affairs': 'https://www.jagranjosh.com/rss/current-affairs.xml'
        },
        'focus': ['rights', 'social', 'economic']
    },
    
    'nai_dunia': {
        'name': 'नई दुनिया',
        'language': 'hindi',
        'reliability': 7,
        'feeds': {
            'national': 'https://www.naidunia.com/rss/national-news'
        },
        'focus': ['social', 'economic']
    }
}

# ============== CATEGORY DEFINITIONS ==============

FOCUS_CATEGORIES = {
    'rights': {
        'name_en': 'Rights & Laws',
        'name_hi': 'अधिकार व कानून',
        'keywords': [
            # Rights
            'rights', 'law', 'court', 'judgment', 'verdict', 'supreme court',
            'high court', 'legal', 'justice', 'constitution', 'freedom',
            'civil rights', 'human rights', 'arrest', 'bail', 'custody',
            # Hindi
            'अधिकार', 'कानून', 'न्यायालय', 'फैसला', 'सुप्रीम कोर्ट',
            'कोर्ट', 'न्याय', 'संविधान', 'स्वतंत्रता', 'गिरफ्तारी'
        ],
        'exclude': ['cricket', 'football', 'entertainment', 'celebrity']
    },
    
    'health': {
        'name_en': 'Health & Safety',
        'name_hi': 'स्वास्थ्य व सुरक्षा',
        'keywords': [
            # Health
            'health', 'hospital', 'doctor', 'medicine', 'disease', 'outbreak',
            'vaccine', 'treatment', 'medical', 'patient', 'covid', 'flu',
            'dengue', 'malaria', 'tuberculosis', 'diabetes', 'cancer',
            'food safety', 'drug', 'healthcare', 'ambulance', 'emergency',
            # Air quality & pollution (citizen safety)
            'air quality', 'pollution', 'aqi', 'smog', 'breathing',
            # Hindi
            'स्वास्थ्य', 'अस्पताल', 'डॉक्टर', 'दवा', 'बीमारी', 'टीका',
            'इलाज', 'मरीज', 'प्रदूषण', 'वायु गुणवत्ता'
        ],
        'exclude': ['fitness app', 'beauty', 'cosmetic', 'gym']
    },
    
    'social': {
        'name_en': 'Social Issues',
        'name_hi': 'सामाजिक मुद्दे',
        'keywords': [
            # Women & children
            'women', 'rape', 'harassment', 'violence', 'women safety',
            'child abuse', 'domestic violence', 'dowry', 'trafficking',
            # Caste & discrimination
            'caste', 'dalit', 'discrimination', 'atrocity', 'lynching',
            'mob violence', 'communal', 'riot', 'hate crime',
            # Education & youth
            'education', 'school', 'student', 'exam', 'suicide',
            'mental health', 'depression', 'dropout', 'scholarship',
            # Labor & workers
            'worker', 'labor', 'wage', 'minimum wage', 'strike',
            'unemployment', 'job loss', 'layoff',
            # Hindi
            'महिला', 'बलात्कार', 'हिंसा', 'सुरक्षा', 'जाति', 'दलित',
            'भेदभाव', 'शिक्षा', 'छात्र', 'आत्महत्या', 'मजदूर', 'बेरोजगारी'
        ],
        'exclude': ['celebrity', 'film', 'entertainment', 'sports']
    },
    
    'economic': {
        'name_en': 'Economic Impact',
        'name_hi': 'आर्थिक प्रभाव',
        'keywords': [
            # Prices & cost of living
            'price', 'inflation', 'petrol', 'diesel', 'lpg', 'gas cylinder',
            'food price', 'onion', 'tomato', 'wheat', 'rice', 'dal',
            'ration', 'subsidy', 'pds', 'ration card',
            # Banking & money
            'bank', 'atm', 'loan', 'interest rate', 'emi', 'credit',
            'debit card', 'upi', 'digital payment', 'cash',
            # Employment & income
            'salary', 'pension', 'income', 'tax', 'tds', 'itr',
            'gst', 'income tax', 'refund',
            # Government schemes
            'scheme', 'yojana', 'benefit', 'welfare', 'subsidy',
            'aadhaar', 'pan card', 'direct benefit transfer', 'dbt',
            # Transport & infrastructure
            'train', 'railway', 'bus', 'metro', 'toll', 'highway',
            'road', 'bridge', 'water supply', 'electricity', 'power cut',
            # Hindi
            'कीमत', 'महंगाई', 'पेट्रोल', 'डीजल', 'गैस', 'राशन',
            'सब्सिडी', 'बैंक', 'लोन', 'वेतन', 'पेंशन', 'कर',
            'योजना', 'आधार', 'रेलवे', 'बिजली', 'पानी'
        ],
        'exclude': ['stock market', 'sensex', 'nifty', 'shares', 'ipo',
                   'mutual fund', 'investment tips', 'startup funding']
    }
}

# ============== EXCLUSION PATTERNS ==============

EXCLUSIONS = {
    'entertainment': [
        'bollywood', 'hollywood', 'film', 'movie', 'actor', 'actress',
        'celebrity', 'star', 'entertainment', 'box office', 'trailer',
        'bigg boss', 'reality show', 'tv show', 'web series', 'ott'
    ],
    'sports': [
        'cricket', 'ipl', 'football', 'hockey', 'kabaddi', 'sports',
        'match', 'tournament', 'player', 'team', 'score', 'wicket',
        'goal', 'champion', 'league'
        # Exception: Olympics, World Cup finals allowed (handled in code)
    ],
    'tech_gadgets': [
        'smartphone', 'iphone', 'android', 'laptop', 'tablet',
        'gadget', 'launch event', 'product launch', 'specs',
        'review', 'unboxing', 'gaming'
    ],
    'business': [
        'quarterly results', 'earnings', 'profit', 'revenue',
        'stock price', 'market cap', 'ipo', 'fy quarter'
    ]
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

def get_exclusion_keywords():
    """Get all exclusion keywords"""
    all_exclusions = []
    for category, keywords in EXCLUSIONS.items():
        all_exclusions.extend(keywords)
    return all_exclusions

def is_relevant_to_citizen(title, description):
    """
    Quick check: Is this news relevant to an average Indian citizen?
    Returns: (is_relevant, matched_category)
    """
    text = f"{title} {description}".lower()
    
    # Check exclusions first (faster rejection)
    exclusion_keywords = get_exclusion_keywords()
    for keyword in exclusion_keywords:
        if keyword in text:
            # Exception for major events
            major_event_indicators = ['world cup final', 'olympics gold', 
                                     'national emergency', 'breaking']
            if not any(indicator in text for indicator in major_event_indicators):
                return False, None
    
    # Check category relevance
    for category_key, category_data in FOCUS_CATEGORIES.items():
        keywords = category_data['keywords']
        matches = sum(1 for kw in keywords if kw in text)
        
        # If 2+ keywords match, consider relevant
        if matches >= 2:
            return True, category_key
    
    return False, None
