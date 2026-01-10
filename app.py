"""
=============================================================================
NIRVANA READ - News Curated for You
A citizen-centric news platform for India
=============================================================================
"""

from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime, timedelta, timezone
import json
from io import StringIO
import csv
import os
import feedparser
import re
import hashlib
from rss_sources import (
    CURATED_SOURCES, FOCUS_CATEGORIES, get_all_feed_urls,
    is_relevant_to_citizen, get_exclusion_keywords
)
from supabase_client import (
    init_supabase, track_interaction, update_news_feedback,
    update_category_stats, calculate_personalized_score
)

app = Flask(__name__)

# ============== CONFIGURATION ==============
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
IST = timezone(timedelta(hours=5, minutes=30))

# Cache configuration
NEWS_CACHE = []
CACHE_TIMESTAMP = None
CACHE_DURATION = timedelta(hours=12)  # 12 hour cache

# Performance optimization for Render free tier
MAX_RSS_BATCH_SIZE = 5  # Process 5 feeds at a time
MAX_NEWS_PER_FEED = 10  # Max 10 news per feed
NEWS_FRESHNESS_HOURS = 48  # Only last 48 hours

# Initialize Supabase on startup
init_supabase()

# ============== RSS PARSING ==============

def parse_rss_feed_optimized(feed_url, source_name, language):
    """
    Optimized RSS parser for slow networks
    - Timeout: 10 seconds
    - Max entries: 10
    - Compressed fetching
    """
    try:
        # Use requests with timeout for better control
        headers = {
            'User-Agent': 'NirvanaRead/1.0',
            'Accept-Encoding': 'gzip, deflate'
        }
        
        response = requests.get(feed_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []
        
        # Parse with feedparser
        feed = feedparser.parse(response.content)
        items = []
        
        for entry in feed.entries[:MAX_NEWS_PER_FEED]:
            try:
                # Extract published date
                pub_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    pub_date = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
                else:
                    pub_date = datetime.now(timezone.utc)
                
                # Check freshness (48 hours)
                hours_old = (datetime.now(timezone.utc) - pub_date).total_seconds() / 3600
                if hours_old > NEWS_FRESHNESS_HOURS:
                    continue
                
                # Extract content
                title = entry.get('title', '').strip()
                description = entry.get('summary', entry.get('description', '')).strip()
                
                # Clean HTML tags from description
                description = re.sub(r'<[^>]+>', '', description)
                description = description[:300]  # Limit description length
                
                if not title or not description:
                    continue
                
                # Quick relevance check
                is_relevant, matched_category = is_relevant_to_citizen(title, description)
                if not is_relevant:
                    continue
                
                item = {
                    'title': title,
                    'description': description,
                    'url': entry.get('link', ''),
                    'publishedAt': pub_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'source': source_name,
                    'language': language,
                    'matched_category': matched_category
                }
                
                items.append(item)
                
            except Exception as e:
                print(f"Error parsing entry from {source_name}: {str(e)}")
                continue
        
        return items
        
    except requests.Timeout:
        print(f"Timeout fetching {feed_url}")
        return []
    except Exception as e:
        print(f"Error fetching {feed_url}: {str(e)}")
        return []

# ============== AI SCORING ==============

def ai_citizen_impact_score(article, category):
    """
    AI evaluates: How much does this news impact an average Indian citizen?
    
    Scoring criteria:
    1. Direct impact on daily life (0-100)
    2. Urgency/timeliness (0-100)
    3. Actionability (can citizen do something?) (0-100)
    4. Relevance to average person (0-100)
    
    Returns: average score
    """
    if not GROQ_API_KEY:
        # Fallback to rule-based if no AI
        return 65  # Default medium score
    
    category_info = FOCUS_CATEGORIES.get(category, {})
    category_name = category_info.get('name_en', category)
    
    prompt = f"""You are evaluating news for an average Indian citizen.

**Category**: {category_name}
**News Title**: {article.get('title', '')}
**Description**: {article.get('description', '')[:200]}

**Evaluate on 4 criteria** (0-100 each):

1. **Direct Impact**: Does this directly affect citizen's daily life? (prices, rights, safety, health, income)
2. **Urgency**: How soon does citizen need to know? (immediate action needed vs general awareness)
3. **Actionability**: Can an average citizen take action or benefit from knowing this?
4. **Citizen Relevance**: Is this relevant to majority of Indians, not just specific groups?

**Respond ONLY with JSON**:
{{
    "direct_impact": 0-100,
    "urgency": 0-100,
    "actionability": 0-100,
    "citizen_relevance": 0-100,
    "reasoning": "one line explanation"
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
                    {'role': 'system', 'content': 'You are a news analyst. Respond only with valid JSON.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.3,
                'max_tokens': 200
            },
            timeout=15
        )
        
        if response.status_code == 200:
            result_text = response.json()['choices'][0]['message']['content']
            json_match = re.search(r'\{[^}]+\}', result_text, re.DOTALL)
            
            if json_match:
                ai_result = json.loads(json_match.group())
                
                # Calculate average score
                avg_score = (
                    ai_result.get('direct_impact', 50) +
                    ai_result.get('urgency', 50) +
                    ai_result.get('actionability', 50) +
                    ai_result.get('citizen_relevance', 50)
                ) / 4
                
                return {
                    'score': int(avg_score),
                    'reasoning': ai_result.get('reasoning', ''),
                    'breakdown': {
                        'impact': ai_result.get('direct_impact', 50),
                        'urgency': ai_result.get('urgency', 50),
                        'action': ai_result.get('actionability', 50),
                        'relevance': ai_result.get('citizen_relevance', 50)
                    }
                }
    
    except Exception as e:
        print(f"AI scoring error: {str(e)}")
    
    # Fallback
    return {
        'score': 65,
        'reasoning': 'AI analysis unavailable',
        'breakdown': {'impact': 65, 'urgency': 65, 'action': 65, 'relevance': 65}
    }

# ============== MAIN NEWS FETCHING ==============

def fetch_and_score_news():
    """
    Fetch news from RSS feeds and score them
    Optimized for Render free tier and slow networks
    """
    print(f"🔄 Fetching news at {datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S IST')}")
    
    all_feeds = get_all_feed_urls()
    all_news = []
    processed_urls = set()
    
    # Process feeds in batches (network optimization)
    for i in range(0, len(all_feeds), MAX_RSS_BATCH_SIZE):
        batch = all_feeds[i:i + MAX_RSS_BATCH_SIZE]
        
        print(f"📡 Processing batch {i//MAX_RSS_BATCH_SIZE + 1}/{(len(all_feeds)-1)//MAX_RSS_BATCH_SIZE + 1}")
        
        for feed_info in batch:
            try:
                articles = parse_rss_feed_optimized(
                    feed_info['url'],
                    feed_info['source_name'],
                    feed_info['language']
                )
                
                for article in articles:
                    # Skip duplicates
                    if article['url'] in processed_urls:
                        continue
                    processed_urls.add(article['url'])
                    
                    # AI scoring (batch processed for efficiency)
                    category = article['matched_category']
                    ai_result = ai_citizen_impact_score(article, category)
                    
                    # Skip low-scoring news (filter noise)
                    if ai_result['score'] < 55:
                        continue
                    
                    # Get collective intelligence score (if available)
                    final_score = calculate_personalized_score(
                        ai_result['score'],
                        article['url'],
                        category
                    )
                    
                    # Convert timestamp to IST
                    pub_date = datetime.strptime(
                        article['publishedAt'],
                        '%Y-%m-%dT%H:%M:%SZ'
                    ).replace(tzinfo=timezone.utc)
                    pub_date_ist = pub_date.astimezone(IST)
                    
                    # Calculate time ago
                    hours_ago = int((datetime.now(timezone.utc) - pub_date).total_seconds() / 3600)
                    if hours_ago < 1:
                        time_ago = "Just now"
                    elif hours_ago < 24:
                        time_ago = f"{hours_ago}h ago"
                    else:
                        days_ago = hours_ago // 24
                        time_ago = f"{days_ago}d ago"
                    
                    news_item = {
                        'id': hashlib.md5(article['url'].encode()).hexdigest(),
                        'title': article['title'],
                        'description': article['description'],
                        'url': article['url'],
                        'source': article['source'],
                        'language': article['language'],
                        'category': FOCUS_CATEGORIES[category]['name_en'],
                        'category_hi': FOCUS_CATEGORIES[category]['name_hi'],
                        'categoryKey': category,
                        'publishedAt': article['publishedAt'],
                        'publishedAtIST': pub_date_ist.strftime('%d %b, %I:%M %p'),
                        'timeAgo': time_ago,
                        'score': int(final_score),
                        'aiScore': ai_result['score'],
                        'reasoning': ai_result['reasoning'],
                        'breakdown': ai_result['breakdown']
                    }
                    
                    all_news.append(news_item)
                    
            except Exception as e:
                print(f"Error processing feed {feed_info['source_name']}: {str(e)}")
                continue
    
    # Sort by score (highest first)
    all_news.sort(key=lambda x: x['score'], reverse=True)
    
    # Limit to top 100 news (performance optimization)
    all_news = all_news[:100]
    
    print(f"✅ Fetched {len(all_news)} news items")
    
    return all_news

def update_cache():
    """Update news cache"""
    global NEWS_CACHE, CACHE_TIMESTAMP
    
    NEWS_CACHE = fetch_and_score_news()
    CACHE_TIMESTAMP = datetime.now(IST)
    
    print(f"💾 Cache updated: {len(NEWS_CACHE)} items at {CACHE_TIMESTAMP.strftime('%H:%M:%S')}")

def get_cached_news():
    """Get news from cache, refresh if needed"""
    global NEWS_CACHE, CACHE_TIMESTAMP
    
    # Check if cache needs refresh
    if not CACHE_TIMESTAMP or (datetime.now(IST) - CACHE_TIMESTAMP) > CACHE_DURATION:
        print("🔄 Cache expired, refreshing...")
        update_cache()
    
    return NEWS_CACHE

# ============== FLASK ROUTES ==============

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/news')
def get_news():
    """Get news API endpoint"""
    try:
        news = get_cached_news()
        
        # Apply filters if provided
        category = request.args.get('category')
        language = request.args.get('language')
        search = request.args.get('search', '').lower()
        
        filtered = news
        
        if category and category != 'all':
            filtered = [n for n in filtered if n['categoryKey'] == category]
        
        if language and language != 'all':
            filtered = [n for n in filtered if n['language'] == language]
        
        if search:
            filtered = [n for n in filtered if 
                       search in n['title'].lower() or 
                       search in n['description'].lower()]
        
        return jsonify({
            'success': True,
            'news': filtered,
            'total': len(filtered),
            'cached_at': CACHE_TIMESTAMP.isoformat() if CACHE_TIMESTAMP else None,
            'timestamp': datetime.now(IST).isoformat()
        })
        
    except Exception as e:
        print(f"Error in /api/news: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/refresh', methods=['POST'])
def force_refresh():
    """Manual refresh endpoint"""
    try:
        update_cache()
        return jsonify({
            'success': True,
            'message': 'Cache refreshed',
            'total': len(NEWS_CACHE),
            'timestamp': CACHE_TIMESTAMP.isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/track', methods=['POST'])
def track_user_action():
    """Track user interaction for learning"""
    try:
        data = request.json
        
        user_id = data.get('user_id', 'anonymous')
        news_url = data.get('news_url')
        action = data.get('action')  # 'view', 'read_full', 'mark_reviewed'
        category = data.get('category')
        reading_time = data.get('reading_time', 0)
        
        # Track in Supabase
        track_interaction(user_id, news_url, action, category, reading_time)
        update_news_feedback(news_url, action)
        
        if reading_time > 0:
            update_category_stats(category, reading_time)
        
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Error tracking: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export')
def export_csv():
    """Export news to CSV"""
    try:
        news = get_cached_news()
        
        output = StringIO()
        writer = csv.writer(output)
        
        writer.writerow([
            'Title', 'Category', 'Source', 'Language', 
            'Score', 'AI Reasoning', 'Time', 'URL'
        ])
        
        for item in news:
            writer.writerow([
                item['title'],
                item['category'],
                item['source'],
                item['language'],
                item['score'],
                item['reasoning'],
                item['publishedAtIST'],
                item['url']
            ])
        
        output.seek(0)
        return output.getvalue(), 200, {
            'Content-Type': 'text/csv; charset=utf-8',
            'Content-Disposition': f'attachment; filename=nirvana-read-{datetime.now(IST).strftime("%Y%m%d")}.csv'
        }
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now(IST).isoformat(),
        'cache_size': len(NEWS_CACHE),
        'cache_age_minutes': int((datetime.now(IST) - CACHE_TIMESTAMP).total_seconds() / 60) if CACHE_TIMESTAMP else None,
        'ai_enabled': bool(GROQ_API_KEY)
    })

# ============== STARTUP ==============

if __name__ == '__main__':
    # Initialize cache on startup
    print("🚀 Starting Nirvana Read...")
    update_cache()
    
    # Run server
    app.run(debug=True, host='0.0.0.0', port=5000)
