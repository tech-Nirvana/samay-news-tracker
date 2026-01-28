"""
=============================================================================
NIRVANA READ - Enhanced News System
9 categories, relaxed filtering, 72-hour freshness
WITH BACKGROUND THREADING FOR RENDER DEPLOYMENT
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
import threading
import time
from rss_sources import (
    CURATED_SOURCES, FOCUS_CATEGORIES, get_all_feed_urls,
    is_relevant_to_citizen
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
CACHE_DURATION = timedelta(hours=12)
CACHE_LOCK = threading.Lock()
CACHE_REFRESHING = False

# RELAXED SETTINGS for more news
MAX_RSS_BATCH_SIZE = 5
MAX_NEWS_PER_FEED = 15  # Increased from 10
NEWS_FRESHNESS_HOURS = 72  # 3 days instead of 2
AI_SCORE_THRESHOLD = 40  # Lowered from 55

# Initialize Supabase
init_supabase()

# ============== RSS PARSING ==============

def parse_rss_feed_optimized(feed_url, source_name, language):
    """Optimized RSS parser"""
    try:
        headers = {
            'User-Agent': 'NirvanaRead/1.0',
            'Accept-Encoding': 'gzip, deflate'
        }
        
        response = requests.get(feed_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []
        
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
                
                # Check freshness (72 hours)
                hours_old = (datetime.now(timezone.utc) - pub_date).total_seconds() / 3600
                if hours_old > NEWS_FRESHNESS_HOURS:
                    continue
                
                # Extract content
                title = entry.get('title', '').strip()
                description = entry.get('summary', entry.get('description', '')).strip()
                description = re.sub(r'<[^>]+>', '', description)
                description = description[:300]
                
                if not title or not description:
                    continue
                
                # Quick relevance check
                is_relevant, matched_category, confidence = is_relevant_to_citizen(title, description)
                if not is_relevant:
                    continue
                
                item = {
                    'title': title,
                    'description': description,
                    'url': entry.get('link', ''),
                    'publishedAt': pub_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'source': source_name,
                    'language': language,
                    'matched_category': matched_category,
                    'confidence': confidence
                }
                
                items.append(item)
                
            except Exception as e:
                continue
        
        return items
        
    except Exception as e:
        print(f"Error fetching {feed_url}: {str(e)}")
        return []

# ============== AI SCORING (SIMPLIFIED) ==============

def ai_citizen_impact_score(article, category):
    """AI citizen impact scoring"""
    if not GROQ_API_KEY:
        # Fallback: Use confidence from keyword matching
        return {
            'score': min(50 + int(article.get('confidence', 1) * 10), 85),
            'reasoning': 'Rule-based scoring (AI unavailable)',
            'breakdown': {'impact': 65, 'urgency': 65, 'action': 65, 'relevance': 65}
        }
    
    category_info = FOCUS_CATEGORIES.get(category, {})
    category_name = category_info.get('name_en', category)
    
    prompt = f"""Evaluate this news for an average Indian citizen.

**Category**: {category_name}
**Title**: {article.get('title', '')}
**Description**: {article.get('description', '')[:200]}

Rate on 4 criteria (0-100 each):
1. **Direct Impact**: Daily life effect?
2. **Urgency**: How soon to know?
3. **Actionability**: Can citizen act?
4. **Citizen Relevance**: Relevant to majority?

Respond ONLY with JSON:
{{
    "direct_impact": 0-100,
    "urgency": 0-100,
    "actionability": 0-100,
    "citizen_relevance": 0-100,
    "reasoning": "brief explanation"
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
                'max_tokens': 200
            },
            timeout=15
        )
        
        if response.status_code == 200:
            result_text = response.json()['choices'][0]['message']['content']
            json_match = re.search(r'\{[^}]+\}', result_text, re.DOTALL)
            
            if json_match:
                ai_result = json.loads(json_match.group())
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
        print(f"AI error: {str(e)}")
    
    # Fallback
    return {
        'score': min(50 + int(article.get('confidence', 1) * 10), 75),
        'reasoning': 'AI analysis unavailable',
        'breakdown': {'impact': 65, 'urgency': 65, 'action': 65, 'relevance': 65}
    }

# ============== MAIN NEWS FETCHING ==============

def fetch_and_score_news():
    """Fetch news from RSS feeds"""
    print(f"🔄 Fetching news at {datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S IST')}")
    
    all_feeds = get_all_feed_urls()
    all_news = []
    processed_urls = set()
    
    stats = {'fetched': 0, 'filtered': 0, 'ai_processed': 0, 'final': 0}
    
    # Process feeds in batches
    for i in range(0, len(all_feeds), MAX_RSS_BATCH_SIZE):
        batch = all_feeds[i:i + MAX_RSS_BATCH_SIZE]
        batch_num = i//MAX_RSS_BATCH_SIZE + 1
        total_batches = (len(all_feeds)-1)//MAX_RSS_BATCH_SIZE + 1
        
        print(f"📡 Batch {batch_num}/{total_batches}: Processing {len(batch)} feeds")
        
        for feed_info in batch:
            try:
                articles = parse_rss_feed_optimized(
                    feed_info['url'],
                    feed_info['source_name'],
                    feed_info['language']
                )
                
                stats['fetched'] += len(articles)
                
                for article in articles:
                    if article['url'] in processed_urls:
                        continue
                    processed_urls.add(article['url'])
                    
                    stats['filtered'] += 1
                    
                    # AI scoring
                    category = article['matched_category']
                    ai_result = ai_citizen_impact_score(article, category)
                    
                    stats['ai_processed'] += 1
                    
                    # RELAXED: Accept score >= 40
                    if ai_result['score'] < AI_SCORE_THRESHOLD:
                        continue
                    
                    # Calculate final score
                    final_score = calculate_personalized_score(
                        ai_result['score'],
                        article['url'],
                        category
                    )
                    
                    # Convert to IST
                    pub_date = datetime.strptime(
                        article['publishedAt'],
                        '%Y-%m-%dT%H:%M:%SZ'
                    ).replace(tzinfo=timezone.utc)
                    pub_date_ist = pub_date.astimezone(IST)
                    
                    # Time ago
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
                    stats['final'] += 1
                    
            except Exception as e:
                print(f"Error processing {feed_info['source_name']}: {str(e)}")
                continue
    
    # Sort by score
    all_news.sort(key=lambda x: x['score'], reverse=True)
    
    # Limit to top 150 (increased from 100)
    all_news = all_news[:150]
    
    print(f"✅ Stats: Fetched={stats['fetched']}, Filtered={stats['filtered']}, "
          f"AI Processed={stats['ai_processed']}, Final={len(all_news)}")
    
    return all_news

def update_cache():
    """Update news cache (thread-safe)"""
    global NEWS_CACHE, CACHE_TIMESTAMP, CACHE_REFRESHING
    
    with CACHE_LOCK:
        if CACHE_REFRESHING:
            print("⏳ Cache refresh already in progress, skipping...")
            return
        CACHE_REFRESHING = True
    
    try:
        new_cache = fetch_and_score_news()
        
        with CACHE_LOCK:
            NEWS_CACHE = new_cache
            CACHE_TIMESTAMP = datetime.now(IST)
            print(f"💾 Cache updated: {len(NEWS_CACHE)} items at {CACHE_TIMESTAMP.strftime('%H:%M:%S')}")
    
    except Exception as e:
        print(f"❌ Cache update failed: {str(e)}")
    
    finally:
        with CACHE_LOCK:
            CACHE_REFRESHING = False

def background_cache_refresh():
    """Background thread to refresh cache periodically"""
    while True:
        try:
            with CACHE_LOCK:
                needs_refresh = (
                    not CACHE_TIMESTAMP or 
                    (datetime.now(IST) - CACHE_TIMESTAMP) > CACHE_DURATION
                )
            
            if needs_refresh:
                print("🔄 Background: Cache expired, refreshing...")
                update_cache()
            
            # Sleep for 30 minutes before checking again
            time.sleep(1800)
        
        except Exception as e:
            print(f"❌ Background refresh error: {str(e)}")
            time.sleep(300)  # Sleep 5 min on error

def get_cached_news():
    """Get news from cache"""
    with CACHE_LOCK:
        return NEWS_CACHE.copy()

# ============== FLASK ROUTES ==============

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/news')
def get_news():
    try:
        news = get_cached_news()
        
        # If cache is empty, trigger refresh but still respond
        if not news:
            print("⚠️ Cache empty, triggering background refresh...")
            threading.Thread(target=update_cache, daemon=True).start()
            return jsonify({
                'success': True,
                'news': [],
                'total': 0,
                'message': 'Loading news... Please refresh in a moment.',
                'cached_at': None,
                'timestamp': datetime.now(IST).isoformat()
            })
        
        # Filters
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
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/refresh', methods=['POST'])
def force_refresh():
    try:
        # Start refresh in background
        threading.Thread(target=update_cache, daemon=True).start()
        
        return jsonify({
            'success': True,
            'message': 'Cache refresh started in background',
            'total': len(NEWS_CACHE),
            'timestamp': datetime.now(IST).isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/track', methods=['POST'])
def track_user_action():
    try:
        data = request.json
        user_id = data.get('user_id', 'anonymous')
        news_url = data.get('news_url')
        action = data.get('action')
        category = data.get('category')
        reading_time = data.get('reading_time', 0)
        
        track_interaction(user_id, news_url, action, category, reading_time)
        update_news_feedback(news_url, action)
        
        if reading_time > 0:
            update_category_stats(category, reading_time)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export')
def export_csv():
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
    with CACHE_LOCK:
        cache_age = int((datetime.now(IST) - CACHE_TIMESTAMP).total_seconds() / 60) if CACHE_TIMESTAMP else None
        is_refreshing = CACHE_REFRESHING
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now(IST).isoformat(),
        'cache_size': len(NEWS_CACHE),
        'cache_age_minutes': cache_age,
        'cache_refreshing': is_refreshing,
        'ai_enabled': bool(GROQ_API_KEY),
        'settings': {
            'freshness_hours': NEWS_FRESHNESS_HOURS,
            'ai_threshold': AI_SCORE_THRESHOLD,
            'max_news': 150
        }
    })

# ============== STARTUP ==============

def initialize_app():
    """Initialize app - non-blocking startup"""
    print("🚀 Starting Nirvana Read...")
    print(f"⚙️ Settings: {NEWS_FRESHNESS_HOURS}h freshness, Score threshold {AI_SCORE_THRESHOLD}+")
    
    # Start background refresh thread
    refresh_thread = threading.Thread(target=background_cache_refresh, daemon=True)
    refresh_thread.start()
    print("🔄 Background refresh thread started")
    
    # Do initial cache load in background (non-blocking)
    initial_load = threading.Thread(target=update_cache, daemon=True)
    initial_load.start()
    print("📰 Initial news load started in background")
    print("✅ App ready to serve requests")

# Initialize when module is imported
initialize_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
