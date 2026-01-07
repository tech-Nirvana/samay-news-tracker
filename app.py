"""
=============================================================================
SAMAY - Hybrid News Intelligence System (Rules + Open Source AI)
Version 2.0 - Production Ready
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

app = Flask(__name__)

# ============== CONFIGURATION ==============
NEWS_API_KEY = '38d4ca41a5d94c02a27e74228691e795'
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')  # Environment variable से

# Indian Timezone
IST = timezone(timedelta(hours=5, minutes=30))

# ============== CATEGORIES WITH AI PROMPTS ==============
CATEGORIES = {
    'consciousness': {
        'name': 'मानव चेतना व आध्यात्मिकता',
        'keywords': ['consciousness', 'spirituality', 'meditation', 'vedanta', 'philosophy', 
                    'awakening', 'mindfulness', 'self-awareness', 'enlightenment'],
        'context_words': ['inner peace', 'self-realization', 'spiritual growth', 'awareness'],
        'india_keywords': ['vedanta', 'upanishad', 'gita', 'ramana maharshi', 'acharya'],
        'color': 'purple',
        'ai_prompt': """Core Mission: Spiritual awakening and consciousness evolution.
RELEVANT: Meditation practices, spiritual teachings, self-inquiry, consciousness studies, philosophy of mind.
NOT RELEVANT: New age mysticism, astrology, fortune telling, superstitions.
India Focus: Vedanta, Upanishads, but universal spirituality also important."""
    },
    
    'climate': {
        'name': 'जलवायु परिवर्तन व पर्यावरण',
        'keywords': ['climate change', 'global warming', 'greenhouse', 'emissions', 'carbon',
                    'deforestation', 'pollution', 'environment', 'sustainability'],
        'context_words': ['temperature', 'fossil fuels', 'renewable', 'conservation', 'extinction'],
        'india_keywords': ['delhi pollution', 'ganga', 'himalaya', 'monsoon', 'india climate'],
        'color': 'green',
        'ai_prompt': """Core Mission: Climate activism and environmental protection.
RELEVANT: Climate policy, emissions, deforestation, pollution, activism, renewable energy.
NOT RELEVANT: Weather forecasts, climate control technology, air conditioning.
India Focus: Yes, but global climate action equally important."""
    },
    
    'animal': {
        'name': 'पशु अधिकार व क्रूरता',
        'keywords': ['animal rights', 'cruelty', 'vegan', 'vegetarian', 'wildlife',
                    'meat industry', 'factory farming', 'animal welfare', 'slaughter'],
        'context_words': ['compassion', 'sentient', 'livestock', 'dairy', 'leather'],
        'india_keywords': ['cow', 'cattle', 'sacred', 'ahimsa', 'india animal'],
        'color': 'orange',
        'ai_prompt': """Core Mission: Animal rights activism and ending cruelty.
RELEVANT: Factory farming, animal cruelty, veganism, wildlife protection, exploitation.
NOT RELEVANT: Pet care tips, animal behavior studies, zoo entertainment, animal sports.
India Focus: Cattle/religious aspects important, but global animal rights crucial."""
    },
    
    'women': {
        'name': 'महिला सशक्तिकरण व समानता',
        'keywords': ['women rights', 'feminism', 'gender equality', 'women empowerment',
                    'women safety', 'sexual harassment', 'patriarchy', 'misogyny'],
        'context_words': ['violence', 'discrimination', 'pay gap', 'domestic abuse'],
        'india_keywords': ['india women', 'delhi', 'rape', 'dowry', 'honour killing'],
        'color': 'pink',
        'ai_prompt': """Core Mission: Women's rights and ending patriarchal oppression.
RELEVANT: Gender violence, discrimination, equal rights, safety, empowerment movements.
NOT RELEVANT: Women's fashion, beauty tips, celebrity gossip, women in entertainment.
India Focus: Yes, Indian context critical but global feminism also important."""
    },
    
    'education': {
        'name': 'शिक्षा प्रणाली व युवा',
        'keywords': ['education', 'students', 'youth', 'university', 'schools',
                    'examination', 'career pressure', 'learning', 'academic'],
        'context_words': ['stress', 'competition', 'rote learning', 'reform', 'mental health'],
        'india_keywords': ['iit', 'neet', 'jee', 'cbse', 'board exam', 'coaching'],
        'color': 'blue',
        'ai_prompt': """Core Mission: Critique of exam-obsessed education and youth awakening.
RELEVANT: Education reform, exam stress, career pressure, true learning vs rote.
NOT RELEVANT: School rankings, admission news, education technology products.
India Focus: Yes, Indian coaching/exam culture especially relevant."""
    },
    
    'religious': {
        'name': 'धार्मिक कट्टरता व अंधविश्वास',
        'keywords': ['religious', 'communal', 'intolerance', 'fundamentalism',
                    'extremism', 'sectarian', 'superstition', 'orthodox'],
        'context_words': ['violence', 'hatred', 'persecution', 'discrimination', 'radicalization'],
        'india_keywords': ['hindu muslim', 'communal', 'mob lynching', 'india religious'],
        'color': 'red',
        'ai_prompt': """Core Mission: Exposing religious fundamentalism and blind faith.
RELEVANT: Religious violence, intolerance, extremism, superstition, communalism.
NOT RELEVANT: Religious festivals, temple/mosque news, spiritual teachings.
India Focus: Yes, communal tensions very important."""
    },
    
    'capitalism': {
        'name': 'उपभोक्तावाद व पूंजीवाद',
        'keywords': ['capitalism', 'consumerism', 'corporate', 'inequality',
                    'poverty', 'wealth gap', 'exploitation', 'greed'],
        'context_words': ['billionaire', 'profit', 'workers rights', 'unemployment'],
        'india_keywords': ['adani', 'ambani', 'india inequality', 'farmer protest'],
        'color': 'yellow',
        'ai_prompt': """Core Mission: Critique of consumerism and economic injustice.
RELEVANT: Wealth inequality, corporate greed, exploitation, anti-capitalism movements.
NOT RELEVANT: Stock market tips, business success stories, product launches.
India Focus: Yes, but global capitalism also relevant."""
    },
    
    'media': {
        'name': 'मीडिया Manipulation व Fake News',
        'keywords': ['fake news', 'misinformation', 'propaganda', 'media bias',
                    'censorship', 'social media', 'manipulation'],
        'context_words': ['truth', 'journalism', 'press freedom', 'fact check'],
        'india_keywords': ['godi media', 'india press', 'whatsapp', 'india censorship'],
        'color': 'indigo',
        'ai_prompt': """Core Mission: Exposing media manipulation and misinformation.
RELEVANT: Fake news, propaganda, press freedom, media bias, censorship.
NOT RELEVANT: Media industry news, entertainment media, social media features.
India Focus: Yes, Indian media landscape very important."""
    },
    
    'caste': {
        'name': 'जातिवाद व सामाजिक भेदभाव',
        'keywords': ['caste', 'discrimination', 'dalit', 'reservation',
                    'social justice', 'untouchability', 'brahmin', 'oppression'],
        'context_words': ['atrocity', 'marginalized', 'inequality', 'systemic'],
        'india_keywords': ['india caste', 'dalit', 'sc st', 'ambedkar'],
        'color': 'gray',
        'ai_prompt': """Core Mission: Fighting caste discrimination and social inequality.
RELEVANT: Caste violence, discrimination, dalit rights, anti-caste movements.
NOT RELEVANT: Caste census data, caste in politics (unless about discrimination).
India Focus: Primarily Indian issue, very important."""
    },
    
    'mental': {
        'name': 'Mental Health व आत्महत्या',
        'keywords': ['mental health', 'depression', 'suicide', 'anxiety',
                    'stress', 'psychological', 'therapy', 'counseling'],
        'context_words': ['crisis', 'disorder', 'trauma', 'awareness', 'stigma'],
        'india_keywords': ['india suicide', 'student suicide', 'kota', 'mental health india'],
        'color': 'teal',
        'ai_prompt': """Core Mission: Mental health awareness and suicide prevention.
RELEVANT: Mental health crisis, suicide rates, stigma, awareness, prevention.
NOT RELEVANT: Mental health apps, therapy business, self-help products.
India Focus: Yes, student/youth suicide especially critical."""
    },
    
    'relationships': {
        'name': 'संबंधों की विकृतियाँ',
        'keywords': ['marriage', 'divorce', 'relationship', 'family',
                    'domestic violence', 'abuse', 'toxic', 'patriarchy'],
        'context_words': ['emotional', 'control', 'manipulation', 'unhealthy'],
        'india_keywords': ['arranged marriage', 'dowry', 'india divorce', 'domestic abuse india'],
        'color': 'rose',
        'ai_prompt': """Core Mission: Exposing toxic relationship patterns and abuse.
RELEVANT: Domestic violence, toxic relationships, marriage problems, abuse.
NOT RELEVANT: Dating tips, relationship advice, celebrity relationships.
India Focus: Yes, arranged marriage culture and domestic violence important."""
    },
    
    'career': {
        'name': 'Career Obsession व Success की दौड़',
        'keywords': ['career', 'job', 'employment', 'success',
                    'competition', 'burnout', 'hustle culture', 'ambition'],
        'context_words': ['pressure', 'stress', 'workaholic', 'rat race', 'meaningless'],
        'india_keywords': ['india jobs', 'unemployment', 'startup culture', 'corporate india'],
        'color': 'cyan',
        'ai_prompt': """Core Mission: Critique of career obsession and meaningless success pursuit.
RELEVANT: Work culture toxicity, burnout, career pressure, meaningless success.
NOT RELEVANT: Job postings, career tips, success stories, motivational content.
India Focus: Yes, Indian corporate/startup culture relevant."""
    }
}

# ============== TRUSTED SOURCES ==============
TIER1_SOURCES = {'reuters', 'bbc', 'guardian', 'aljazeera', 'the hindu', 
                 'indian express', 'the wire', 'down to earth', 'scroll'}
TIER2_SOURCES = {'times of india', 'hindustan times', 'ndtv', 'cnn', 
                 'washington post', 'new york times', 'bloomberg'}
TIER3_SOURCES = {'india today', 'economic times', 'deccan herald', 'firstpost'}

# ============== RULE-BASED SCORING ==============

def calculate_context_score(text, category):
    """Layer 1: Context matching (25 points)"""
    text_lower = text.lower()
    score = 0
    
    keywords = category['keywords']
    context_words = category['context_words']
    
    # Primary keyword match
    keyword_matches = sum(1 for kw in keywords if kw in text_lower)
    if keyword_matches > 0:
        score += min(keyword_matches * 3, 15)
    
    # Context words boost
    context_matches = sum(1 for cw in context_words if cw in text_lower)
    if keyword_matches > 0 and context_matches > 0:
        score += min(context_matches * 2, 10)
    
    return min(score, 25)

def calculate_india_score(text):
    """Layer 2: India relevance (20 points)"""
    text_lower = text.lower()
    
    # Tier 1: Direct India (20 points)
    tier1 = ['india', 'indian', 'delhi', 'mumbai', 'bangalore', 'kolkata',
             'modi', 'parliament', 'supreme court india', 'indian government']
    if any(kw in text_lower for kw in tier1):
        return 20
    
    # Tier 2: South Asia (15 points)
    tier2 = ['pakistan', 'bangladesh', 'nepal', 'sri lanka', 'south asia']
    if any(kw in text_lower for kw in tier2):
        return 15
    
    # Tier 3: Global but relevant (10 points)
    tier3 = ['un', 'who', 'climate summit', 'paris agreement', 'world bank']
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
    
    return 3  # Unknown source

def calculate_recency_score(published_at):
    """Layer 4: Recency (15 points)"""
    try:
        pub_date = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        hours_old = (now - pub_date).total_seconds() / 3600
        
        if hours_old < 3:
            return 15
        elif hours_old < 12:
            return 12
        elif hours_old < 24:
            return 8
        elif hours_old < 72:
            return 4
        else:
            return 0
    except:
        return 0

def calculate_category_alignment(text, category):
    """Layer 5: Category alignment (15 points)"""
    text_lower = text.lower()
    
    # Primary keywords (strong match)
    primary_matches = sum(1 for kw in category['keywords'] if kw in text_lower)
    score = min(primary_matches * 3, 15)
    
    # India-specific boost
    india_matches = sum(1 for kw in category['india_keywords'] if kw in text_lower)
    if india_matches > 0:
        score += 5
    
    return min(score, 15)

def calculate_semantic_similarity(text, category):
    """Layer 6: Semantic similarity (10 points)"""
    try:
        # Create ideal text for category
        ideal_text = ' '.join(category['keywords'] + category['context_words'])
        
        # TF-IDF vectorization
        vectorizer = TfidfVectorizer(stop_words='english')
        vectors = vectorizer.fit_transform([ideal_text, text])
        
        # Cosine similarity
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        
        return int(similarity * 10)
    except:
        return 0

def rule_based_scoring(article, category):
    """Complete rule-based scoring pipeline"""
    text = f"{article.get('title', '')} {article.get('description', '')}"
    
    score = 0
    breakdown = {}
    
    # Layer 1: Context
    context_score = calculate_context_score(text, category)
    score += context_score
    breakdown['context'] = context_score
    
    # Layer 2: India relevance
    india_score = calculate_india_score(text)
    score += india_score
    breakdown['india'] = india_score
    
    # Layer 3: Source
    source_score = calculate_source_score(article.get('source', {}).get('name', ''))
    score += source_score
    breakdown['source'] = source_score
    
    # Layer 4: Recency
    recency_score = calculate_recency_score(article.get('publishedAt', ''))
    score += recency_score
    breakdown['recency'] = recency_score
    
    # Layer 5: Category alignment
    alignment_score = calculate_category_alignment(text, category)
    score += alignment_score
    breakdown['alignment'] = alignment_score
    
    # Layer 6: Semantic similarity
    semantic_score = calculate_semantic_similarity(text, category)
    score += semantic_score
    breakdown['semantic'] = semantic_score
    
    return {
        'score': min(score, 100),
        'breakdown': breakdown,
        'pass_to_ai': score >= 40
    }

# ============== AI ANALYSIS (GROQ) ==============

def ai_deep_analysis(article, category, rule_score):
    """Deep AI analysis using Groq (Free LLM)"""
    
    if not GROQ_API_KEY:
        # Fallback: अगर API key नहीं है तो rule score ही use करो
        return {
            'relevance_score': rule_score,
            'is_india_relevant': 'india' in article.get('title', '').lower(),
            'reasoning': 'AI analysis unavailable (no API key)',
            'core_issue': True,
            'recommended_action': 'monitor' if rule_score >= 60 else 'skip'
        }
    
    # Construct prompt
    prompt = f"""Analyze this news for relevance to the mission category.

**Category**: {category['name']}
{category['ai_prompt']}

**News**:
Title: {article.get('title', '')}
Description: {article.get('description', '')}
Source: {article.get('source', {}).get('name', '')}

**Analyze**:
1. Is this TRULY about the core issue?
2. India relevance?
3. Alignment with mission values?
4. Importance for awareness?

**Output JSON only**:
{{
    "relevance_score": 0-100,
    "is_india_relevant": true/false,
    "reasoning": "one line explanation",
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
                    {'role': 'system', 'content': 'You are an expert news analyst. Respond only with valid JSON.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.3,
                'max_tokens': 150
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result_text = response.json()['choices'][0]['message']['content']
            
            # Extract JSON from response
            json_match = re.search(r'\{[^}]+\}', result_text, re.DOTALL)
            if json_match:
                ai_result = json.loads(json_match.group())
                return ai_result
        
    except Exception as e:
        print(f"AI analysis error: {str(e)}")
    
    # Fallback
    return {
        'relevance_score': rule_score,
        'is_india_relevant': False,
        'reasoning': 'AI analysis failed',
        'core_issue': True,
        'recommended_action': 'monitor'
    }

# ============== HYBRID SCORING ==============

def hybrid_scoring(article, category):
    """Combine rules + AI for final score"""
    
    # Stage 1: Rule-based filter
    rule_result = rule_based_scoring(article, category)
    
    # If low score, reject without AI
    if not rule_result['pass_to_ai']:
        return {
            'final_score': rule_result['score'],
            'rule_score': rule_result['score'],
            'ai_score': None,
            'breakdown': rule_result['breakdown'],
            'reasoning': 'Low rule score, skipped AI',
            'action': 'skip',
            'show': False
        }
    
    # Stage 2: AI deep analysis
    ai_result = ai_deep_analysis(article, category, rule_result['score'])
    
    # Stage 3: Fusion
    final_score = (
        rule_result['score'] * 0.4 +
        ai_result['relevance_score'] * 0.6
    )
    
    # Apply modifiers
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

# ============== NEWS FETCHING ==============

def fetch_all_news():
    """Fetch and score news from all categories"""
    all_news = []
    
    for cat_key, cat_data in CATEGORIES.items():
        try:
            # Build query
            query = ' OR '.join(cat_data['keywords'][:3])
            
            # API call
            url = 'https://newsapi.org/v2/everything'
            params = {
                'q': query,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': 10,
                'apiKey': NEWS_API_KEY
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for article in data.get('articles', []):
                    if article.get('title') and article.get('description'):
                        # Hybrid scoring
                        scoring = hybrid_scoring(article, cat_data)
                        
                        if scoring['show']:  # Only if passes threshold
                            # Convert to IST
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
                                'description': article['description'],
                                'source': article.get('source', {}).get('name', 'Unknown'),
                                'url': article['url'],
                                'imageUrl': article.get('urlToImage'),
                                'publishedAt': article['publishedAt'],
                                'publishedAtIST': pub_date_ist.strftime('%Y-%m-%d %H:%M:%S IST'),
                                'score': scoring['final_score'],
                                'ruleScore': scoring['rule_score'],
                                'aiScore': scoring['ai_score'],
                                'breakdown': scoring['breakdown'],
                                'reasoning': scoring['reasoning'],
                                'action': scoring['action'],
                                'impactScore': min(scoring['final_score'] + 5, 100),
                                'viralityScore': min(scoring['final_score'] + 10, 100)
                            }
                            
                            all_news.append(news_item)
        
        except Exception as e:
            print(f"Error fetching {cat_key}: {str(e)}")
            continue
    
    # Sort by score
    all_news.sort(key=lambda x: x['score'], reverse=True)
    
    # Remove duplicates
    seen_titles = set()
    unique_news = []
    for item in all_news:
        if item['title'] not in seen_titles:
            seen_titles.add(item['title'])
            unique_news.append(item)
    
    return unique_news

# ============== FLASK ROUTES ==============

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/news')
def get_news():
    try:
        news = fetch_all_news()
        return jsonify({
            'success': True,
            'news': news,
            'timestamp': datetime.now(IST).isoformat(),
            'total': len(news),
            'ai_enabled': bool(GROQ_API_KEY)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export')
def export_csv():
    try:
        news = fetch_all_news()
        
        output = StringIO()
        writer = csv.writer(output)
        
        writer.writerow(['Title', 'Category', 'Source', 'Score', 'Rule Score', 
                        'AI Score', 'Reasoning', 'Published (IST)', 'URL'])
        
        for item in news:
            writer.writerow([
                item['title'],
                item['category'],
                item['source'],
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
            'Content-Disposition': f'attachment; filename=samay-news-{datetime.now(IST).strftime("%Y%m%d")}.csv'
        }
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now(IST).isoformat(),
        'ai_enabled': bool(GROQ_API_KEY)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
