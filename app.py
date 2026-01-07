"""
=============================================================================
SAMAY - RSS-Based Hybrid News Intelligence System
Version 3.0 - Pure Indian Sources (English + Hindi)
=============================================================================
"""

from flask import Flask, render_template, jsonify
import requests
from datetime import datetime, timedelta, timezone
import json
from io import StringIO
import csv
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import feedparser
from rss_sources import get_category_feeds, CATEGORY_RSS_MAPPING, get_all_rss_urls

app = Flask(__name__)

# ============== CONFIGURATION ==============
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')

# Indian Timezone
IST = timezone(timedelta(hours=5, minutes=30))

# Cache variables (in-memory)
news_cache = []
last_update_time = None

# ============== CATEGORIES (Same as before) ==============
CATEGORIES = {
    'consciousness': {
        'name': 'मानव चेतना व आध्यात्मिकता',
        'keywords': ['consciousness', 'spirituality', 'meditation', 'vedanta', 'philosophy', 
                    'awakening', 'mindfulness', 'self-awareness', 'enlightenment', 'आध्यात्म', 'चेतना'],
        'context_words': ['inner peace', 'self-realization', 'spiritual growth', 'awareness', 'ध्यान'],
        'india_keywords': ['vedanta', 'upanishad', 'gita', 'ramana maharshi', 'acharya', 'वेदांत'],
        'color': 'purple',
        'ai_prompt': """Core Mission: Spiritual awakening and consciousness evolution.
RELEVANT: Meditation practices, spiritual teachings, self-inquiry, consciousness studies.
NOT RELEVANT: Astrology, superstitions, religious rituals."""
    },
    
    'climate': {
        'name': 'जलवायु परिवर्तन व पर्यावरण',
        'keywords': ['climate change', 'global warming', 'greenhouse', 'emissions', 'carbon',
                    'deforestation', 'pollution', 'environment', 'sustainability', 'जलवायु', 'पर्यावरण', 'प्रदूषण'],
        'context_words': ['temperature', 'fossil fuels', 'renewable', 'conservation', 'extinction'],
        'india_keywords': ['delhi pollution', 'ganga', 'himalaya', 'monsoon', 'india climate', 'दिल्ली प्रदूषण'],
        'color': 'green',
        'ai_prompt': """Core Mission: Climate activism and environmental protection.
RELEVANT: Climate policy, emissions, deforestation, pollution, activism, renewable energy.
NOT RELEVANT: Weather forecasts, climate control technology."""
    },
    
    'animal': {
        'name': 'पशु अधिकार व क्रूरता',
        'keywords': ['animal rights', 'cruelty', 'vegan', 'vegetarian', 'wildlife',
                    'meat industry', 'factory farming', 'animal welfare', 'slaughter', 'पशु', 'क्रूरता'],
        'context_words': ['compassion', 'sentient', 'livestock', 'dairy', 'leather'],
        'india_keywords': ['cow', 'cattle', 'sacred', 'ahimsa', 'india animal', 'गाय', 'अहिंसा'],
        'color': 'orange',
        'ai_prompt': """Core Mission: Animal rights activism and ending cruelty.
RELEVANT: Factory farming, animal cruelty, veganism, wildlife protection.
NOT RELEVANT: Pet care tips, zoo entertainment."""
    },
    
    'women': {
        'name': 'महिला सशक्तिकरण व समानता',
        'keywords': ['women rights', 'feminism', 'gender equality', 'women empowerment',
                    'women safety', 'sexual harassment', 'patriarchy', 'misogyny', 'महिला', 'नारी'],
        'context_words': ['violence', 'discrimination', 'pay gap', 'domestic abuse', 'हिंसा'],
        'india_keywords': ['india women', 'delhi', 'rape', 'dowry', 'honour killing', 'भारतीय महिला', 'दहेज'],
        'color': 'pink',
        'ai_prompt': """Core Mission: Women's rights and ending patriarchal oppression.
RELEVANT: Gender violence, discrimination, equal rights, safety.
NOT RELEVANT: Fashion, beauty tips, celebrity gossip."""
    },
    
    'education': {
        'name': 'शिक्षा प्रणाली व युवा',
        'keywords': ['education', 'students', 'youth', 'university', 'schools',
                    'examination', 'career pressure', 'learning', 'academic', 'शिक्षा', 'छात्र', 'युवा'],
        'context_words': ['stress', 'competition', 'rote learning', 'reform', 'mental health'],
        'india_keywords': ['iit', 'neet', 'jee', 'cbse', 'board exam', 'coaching', 'आईआईटी'],
        'color': 'blue',
        'ai_prompt': """Core Mission: Critique of exam-obsessed education and youth awakening.
RELEVANT: Education reform, exam stress, career pressure, true learning.
NOT RELEVANT: School rankings, admission news."""
    },
    
    'religious': {
        'name': 'धार्मिक कट्टरता व अंधविश्वास',
        'keywords': ['religious', 'communal', 'intolerance', 'fundamentalism',
                    'extremism', 'sectarian', 'superstition', 'orthodox', 'सांप्रदायिक', 'अंधविश्वास'],
        'context_words': ['violence', 'hatred', 'persecution', 'discrimination', 'radicalization'],
        'india_keywords': ['hindu muslim', 'communal', 'mob lynching', 'india religious', 'हिंदू मुस्लिम'],
        'color': 'red',
        'ai_prompt': """Core Mission: Exposing religious fundamentalism and blind faith.
RELEVANT: Religious violence, intolerance, extremism, superstition.
NOT RELEVANT: Religious festivals, temple/mosque news."""
    },
    
    'capitalism': {
        'name': 'उपभोक्तावाद व पूंजीवाद',
        'keywords': ['capitalism', 'consumerism', 'corporate', 'inequality',
                    'poverty', 'wealth gap', 'exploitation', 'greed', 'पूंजीवाद', 'असमानता'],
        'context_words': ['billionaire', 'profit', 'workers rights', 'unemployment'],
        'india_keywords': ['adani', 'ambani', 'india inequality', 'farmer protest', 'किसान आंदोलन'],
        'color': 'yellow',
        'ai_prompt': """Core Mission: Critique of consumerism and economic injustice.
RELEVANT: Wealth inequality, corporate greed, exploitation.
NOT RELEVANT: Stock tips, business success stories."""
    },
    
    'media': {
        'name': 'मीडिया Manipulation व Fake News',
        'keywords': ['fake news', 'misinformation', 'propaganda', 'media bias',
                    'censorship', 'social media', 'manipulation', 'फर्जी खबर', 'प्रोपेगंडा'],
        'context_words': ['truth', 'journalism', 'press freedom', 'fact check'],
        'india_keywords': ['godi media', 'india press', 'whatsapp', 'india censorship'],
        'color': 'indigo',
        'ai_prompt': """Core Mission: Exposing media manipulation and misinformation.
RELEVANT: Fake news, propaganda, press freedom, media bias.
NOT RELEVANT: Entertainment media, social media features."""
    },
    
    'caste': {
        'name': 'जातिवाद व सामाजिक भेदभाव',
        'keywords': ['caste', 'discrimination', 'dalit', 'reservation',
                    'social justice', 'untouchability', 'brahmin', 'oppression', 'जाति', 'दलित'],
        'context_words': ['atrocity', 'marginalized', 'inequality', 'systemic'],
        'india_keywords': ['india caste', 'dalit', 'sc st', 'ambedkar', 'अंबेडकर'],
        'color': 'gray',
        'ai_prompt': """Core Mission: Fighting caste discrimination and social inequality.
RELEVANT: Caste violence, discrimination, dalit rights.
NOT RELEVANT: Caste census data (unless about discrimination)."""
    },
    
    'mental': {
        'name': 'Mental Health व आत्महत्या',
        'keywords': ['mental health', 'depression', 'suicide', 'anxiety',
                    'stress', 'psychological', 'therapy', 'counseling', 'मानसिक स्वास्थ्य', 'आत्महत्या'],
        'context_words': ['crisis', 'disorder', 'trauma', 'awareness', 'stigma'],
        'india_keywords': ['india suicide', 'student suicide', 'kota', 'mental health india'],
        'color': 'teal',
        'ai_prompt': """Core Mission: Mental health awareness and suicide prevention.
RELEVANT: Mental health crisis, suicide rates, stigma, awareness.
NOT RELEVANT: Mental health apps, therapy business."""
    },
    
    'relationships': {
        'name': 'संबंधों की विकृतियाँ',
        'keywords': ['marriage', 'divorce', 'relationship', 'family',
                    'domestic violence', 'abuse', 'toxic', 'patriarchy', 'विवाह', 'तलाक'],
        'context_words': ['emotional', 'control', 'manipulation', 'unhealthy'],
        'india_keywords': ['arranged marriage', 'dowry', 'india divorce', 'domestic abuse india', 'दहेज'],
        'color': 'rose',
        'ai_prompt': """Core Mission: Exposing toxic relationship patterns and abuse.
RELEVANT: Domestic violence, toxic relationships, marriage problems.
NOT RELEVANT: Dating tips, celebrity relationships."""
    },
    
    'career': {
        'name': 'Career Obsession व Success की दौड़',
        'keywords': ['career', 'job', 'employment', 'success',
                    'competition', 'burnout', 'hustle culture', 'ambition', 'नौकरी', 'करियर'],
        'context_words': ['pressure', 'stress', 'workaholic', 'rat race', 'meaningless'],
        'india_keywords': ['india jobs', 'unemployment', 'startup culture', 'corporate india', 'बेरोजगारी'],
        'color': 'cyan',
        'ai_prompt': """Core Mission: Critique of career obsession and meaningless success.
RELEVANT: Work culture toxicity, burnout, career pressure.
NOT RELEVANT: Job postings, career tips."""
    }
}

# ============== TRUSTED SOURCES ==============
TIER1_SOURCES = {'the hindu', 'indian express', 'the wire', 'scroll', 'down to earth', 
                 'mongabay india', 'bbc hindi', 'feminism in india'}
TIER2_SOURCES = {'ndtv', 'hindustan times', 'the print', 'news18', 'firstpost',
                 'navbharat times', 'dainik jagran', 'livemint'}
TIER3_SOURCES = {'deccan herald', 'telegraph india', 'outlook india', 'amar ujala', 'patrika'}

# ============== RSS PARSING FUNCTIONS ==============

def parse_rss_feed(feed_url, source_name):
    """Parse RSS feed and extract news items"""
    try:
        feed = feedparser.parse(feed_url)
        items = []
        
        for entry in feed.entries[:15]:  # Top 15 per feed
            try:
                # Extract published date
                pub_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    pub_date = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
                else:
                    pub_date = datetime.now(timezone.utc)
                
                # Skip old news (older than 7 days)
                if (datetime.now(timezone.utc) - pub_date).days > 7:
                    continue
                
                item = {
                    'title': entry.get('title', '').strip(),
                    'description': entry.get('summary', entry.get('description', '')).strip(),
                    'url': entry.get('link', ''),
                    'publishedAt': pub_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'source': {'name': source_name}
                }
                
                if item['title'] and item['description']:
                    items.append(item)
                    
            except Exception as e:
                print(f"Error parsing entry from {source_name}: {str(e)}")
                continue
        
        return items
        
    except Exception as e:
        print(f"Error fetching RSS feed {feed_url}: {str(e)}")
        return []

# ============== RULE-BASED SCORING (Same as before) ==============

def calculate_context_score(text, category):
    """Layer 1: Context matching (25 points)"""
    text_lower = text.lower()
    score = 0
    
    keywords = category['keywords']
    context_words = category['context_words']
    
    keyword_matches = sum(1 for kw in keywords if kw in text_lower)
    if keyword_matches > 0:
        score += min(keyword_matches * 3, 15)
    
    context_matches = sum(1 for cw in context_words if cw in text_lower)
    if keyword_matches > 0 and context_matches > 0:
        score += min(context_matches * 2, 10)
    
    return min(score, 25)

def calculate_india_score(text):
    """Layer 2: India relevance (20 points)"""
    text_lower = text.lower()
    
    tier1 = ['india', 'indian', 'bharat', 'delhi', 'mumbai', 'bangalore', 'kolkata',
             'modi', 'parliament', 'supreme court india', 'भारत', 'दिल्ली', 'मुंबई']
    if any(kw in text_lower for kw in tier1):
        return 20
    
    tier2 = ['pakistan', 'bangladesh', 'nepal', 'sri lanka', 'south asia']
    if any(kw in text_lower for kw in tier2):
        return 15
    
    tier3 = ['un', 'who', 'climate summit', 'paris agreement']
    if any(kw in text_lower for kw in tier3):
        return 10
    
    return 0

def calculate_source_score(source_name):
    """Layer 3: Source credibility (15 points)"""
    source_lower = source_name.lower()
    
    if any(s in source_lower for s in TIER1_SOURCES):
        return 15
    elif any(s in source_lower for s in TIER2_SOURCES):
        return 10
    elif any(s in source_lower for s in TIER3_SOURCES):
        return 5
    
    return 3

def calculate_recency_score(published_at):
    """Layer 4: Recency (15 points)"""
    try:
        pub_date = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        hours_old = (datetime.now(timezone.utc) - pub_date).total_seconds() / 3600
        
        if hours_old < 6:
            return 15
        elif hours_old < 24:
            return 12
        elif hours_old < 48:
            return 8
        elif hours_old < 120:
            return 4
        else:
            return 0
    except:
        return 0

def calculate_category_alignment(text, category):
    """Layer 5: Category alignment (15 points)"""
    text_lower = text.lower()
    
    primary_matches = sum(1 for kw in category['keywords'] if kw in text_lower)
    score = min(primary_matches * 3, 15)
    
    india_matches = sum(1 for kw in category['india_keywords'] if kw in text_lower)
    if india_matches > 0:
        score += 5
    
    return min(score, 15)

def calculate_semantic_similarity(text, category):
    """Layer 6: Semantic similarity (10 points)"""
    try:
        ideal_text = ' '.join(category['keywords'] + category['context_words'])
        vectorizer = TfidfVectorizer(stop_words='english')
        vectors = vectorizer.fit_transform([ideal_text, text])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        return int(similarity * 10)
    except:
        return 0

def rule_based_scoring(article, category):
    """Complete rule-based scoring"""
    text = f"{article.get('title', '')} {article.get('description', '')}"
    
    score = 0
    breakdown = {}
    
    breakdown['context'] = calculate_context_score(text, category)
    score += breakdown['context']
    
    breakdown['india'] = calculate_india_score(text)
    score += breakdown['india']
    
    breakdown['source'] = calculate_source_score(article.get('source', {}).get('name', ''))
    score += breakdown['source']
    
    breakdown['recency'] = calculate_recency_score(article.get('publishedAt', ''))
    score += breakdown['recency']
    
    breakdown['alignment'] = calculate_category_alignment(text, category)
    score += breakdown['alignment']
    
    breakdown['semantic'] = calculate_semantic_similarity(text, category)
    score += breakdown['semantic']
    
    return {
        'score': min(score, 100),
        'breakdown': breakdown,
        'pass_to_ai': score >= 40
    }

# ============== AI ANALYSIS (Same as before) ==============

def ai_deep_analysis(article, category, rule_score):
    """AI analysis using Groq"""
    if not GROQ_API_KEY:
        return {
            'relevance_score': rule_score,
            'is_india_relevant': 'india' in article.get('title', '').lower(),
            'reasoning': 'AI unavailable (no API key)',
            'core_issue': True,
            'recommended_action': 'monitor' if rule_score >= 60 else 'skip'
        }
    
    prompt = f"""Analyze this news for relevance.

**Category**: {category['name']}
{category['ai_prompt']}

**News**:
Title: {article.get('title', '')}
Description: {article.get('description', '')[:300]}
Source: {article.get('source', {}).get('name', '')}

**Output JSON only**:
{{
    "relevance_score": 0-100,
    "is_india_relevant": true/false,
    "reasoning": "brief explanation",
    "core_issue": true/false,
    "recommended_action": "urgent/monitor/skip"
}}"""

    try:
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'llama-3.1-8b-instant',
                'messages': [
                    {'role': 'system', 'content': 'Respond only with valid JSON.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.3,
                'max_tokens': 150
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result_text = response.json()['choices'][0]['message']['content']
            json_match = re.search(r'\{[^}]+\}', result_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
    except Exception as e:
        print(f"AI error: {str(e)}")
    
    return {
        'relevance_score': rule_score,
        'is_india_relevant': False,
        'reasoning': 'AI analysis failed',
        'core_issue': True,
        'recommended_action': 'monitor'
    }

def hybrid_scoring(article, category):
    """Hybrid scoring (rules + AI)"""
    rule_result = rule_based_scoring(article, category)
    
    if not rule_result['pass_to_ai']:
        return {
            'final_score': rule_result['score'],
            'rule_score': rule_result['score'],
            'ai_score': None,
            'breakdown': rule_result['breakdown'],
            'reasoning': 'Low rule score',
            'action': 'skip',
            'show': False
        }
    
    ai_result = ai_deep_analysis(article, category, rule_result['score'])
    
    final_score = (
        rule_result['score'] * 0.4 +
        ai_result['relevance_score'] * 0.6
    )
    
    if not ai_result['core_issue']:
        final_score -= 15
    
    if ai_result['is_india_relevant']:
        final_score += 10
    
    final_score = max(0, min(final_score, 100))
    
    return {
        'final_score': int(final_score),
        'rule_score': rule_result['score'],
        'ai_score': ai_result['relevance_score'],
        'breakdown': rule_result['breakdown'],
        'reasoning': ai_result['reasoning'],
        'action': ai_result['recommended_action'],
        'show': final_score >= 60
    }

# ============== MAIN NEWS FETCHING ==============

def fetch_all_news_from_rss():
    """Fetch news from RSS feeds for all categories"""
    all_news = []
    
    for cat_key, cat_data in CATEGORIES.items():
        try:
            # Get relevant RSS feeds for this category
            feeds = get_category_feeds(cat_key)
            
            for feed_info in feeds:
                try:
                    # Parse RSS feed
                    articles = parse_rss_feed(feed_info['url'], feed_info['source'])
                    
                    for article in articles:
                        # Hybrid scoring
                        scoring = hybrid_scoring(article, cat_data)
                        
                        if scoring['show']:
                            pub_date = datetime.strptime(
                                article['publishedAt'], 
                                '%Y-%m-%dT%H:%M:%SZ'
                            ).replace(tzinfo=timezone.utc)
                            pub_date_ist = pub_date.astimezone(IST)
                            
                            news_item = {
                                'id': f"{cat_key}-{hash(article['url'])}",
                                'category': cat_data['name'],
                                'categoryKey': cat_key,
                                'color': cat_data['color'],
                                'title': article['title'],
                                'description': article['description'][:300] + '...' if len(article['description']) > 300 else article['description'],
                                'source': article.get('source', {}).get('name', 'Unknown'),
                                'url': article['url'],
                                'imageUrl': None,  # RSS usually doesn't have images
                                'publishedAt': article['publishedAt'],
                                'publishedAtIST': pub_date_ist.strftime('%d %b %Y, %I:%M %p IST'),
                                'score': scoring['final_score'],
                                'ruleScore': scoring['rule_score'],
                                'aiScore': scoring['ai_score'],
                                'breakdown': scoring['breakdown'],
                                'reasoning': scoring['reasoning'],
                                'action': scoring['action'],
                                'impactScore': min(scoring['final_score'] + 5, 100),
                                'viralityScore': min(scoring['final_score'] + 10, 100),
                                'language': feed_info['language']
                            }
                            
                            all_news.append(news_item)
                
                except Exception as e:
                    print(f"Error processing feed {feed_info['url']}: {str(e)}")
                    continue
        
        except Exception as e:
            print(f"Error fetching category {cat_key}: {str(e)}")
            continue
    
    # Sort by score
    all_news.sort(key=lambda x: x['score'], reverse=True)
    
    # Remove duplicates
    seen_titles = set()
    unique_news = []
    for item in all_news:
        title_normalized = item['title'].lower().strip()
        if title_normalized not in seen_titles:
            seen_titles.add(title_normalized)
            unique_news.append(item)
    
    return unique_news

def update_news_cache():
    """Update the news cache"""
    global news_cache, last_update_time
    
    print(f"Updating news cache at {datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S IST')}")
    news_cache = fetch_all_news_from_rss()
    last_update_time = datetime.now(IST)
    print(f"Cache updated with {len(news_cache)} news items")

# ============== FLASK ROUTES ==============

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/news')
def get_news():
    global news_cache, last_update_time
    
    try:
        # Check if cache needs refresh (6 hours = 21600 seconds)
        if not last_update_time or (datetime.now(IST) - last_update_time).total_seconds() > 21600:
            update_news_cache()
        
        return jsonify({
            'success': True,
            'news': news_cache,
            'timestamp': datetime.now(IST).isoformat(),
            'last_update': last_update_time.isoformat() if last_update_time else None,
            'total': len(news_cache),
            'ai_enabled': bool(GROQ_API_KEY)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/refresh')
def force_refresh():
    """Manual refresh endpoint"""
    try:
        update_news_cache()
        return jsonify({
            'success': True,
            'message': 'Cache refreshed successfully',
            'timestamp': datetime.now(IST).isoformat(),
            'total': len(news_cache)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export')
def export_csv():
    try:
        output = StringIO()
        writer = csv.writer(output)
        
        writer.writerow(['Title', 'Category', 'Source', 'Language', 'Score', 
                        'Rule Score', 'AI Score', 'Reasoning', 'Published (IST)', 'URL'])
        
        for item in news_cache:
            writer.writerow([
                item['title'],
                item['category'],
                item['source'],
                item.get('language', 'unknown'),
                item['score'],
                item['ruleScore'],
                item['aiScore'] if item['aiScore'] else 'N/A',
                item['reasoning'],
                item['publishedAtIST'],
                item['url']
            ])
        
        output.seek(0)
        return output.getvalue(), 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': f'attachment; filename=samay-rss-news-{datetime.now(IST).strftime("%Y%m%d")}.csv'
        }
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now(IST).isoformat(),
        'last_update': last_update_time.isoformat() if last_update_time else 'Never',
        'cached_items': len(news_cache),
        'ai_enabled': bool(GROQ_API_KEY)
    })

if __name__ == '__main__':
    # Initialize cache on startup
    update_news_cache()
    app.run(debug=True, host='0.0.0.0', port=5000)
