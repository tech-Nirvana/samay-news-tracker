"""
=============================================================================
SAMAY - News Intelligence System for Acharya Prashant
Production-Ready Code for Render.com Deployment
=============================================================================

SETUP INSTRUCTIONS:
1. Create a folder named "samay-news-tracker"
2. Save this file as "app.py" 
3. Create "requirements.txt" (I'll provide separately)
4. Create "templates" folder and save HTML (I'll provide separately)
5. Deploy to Render.com

=============================================================================
"""

from flask import Flask, render_template, jsonify, send_file
import requests
from datetime import datetime, timedelta
import json
from io import StringIO
import csv

app = Flask(__name__)

# आपकी NewsAPI Key (already integrated)
NEWS_API_KEY = '38d4ca41a5d94c02a27e74228691e795'

# 12 Categories - आचार्य जी के मिशन के अनुसार
CATEGORIES = {
    'consciousness': {
        'name': 'मानव चेतना व आध्यात्मिकता',
        'keywords': ['consciousness', 'spirituality', 'meditation', 'vedanta', 'philosophy', 'awakening', 'mindfulness'],
        'color': 'purple'
    },
    'climate': {
        'name': 'जलवायु परिवर्तन व पर्यावरण',
        'keywords': ['climate change', 'environment', 'pollution', 'global warming', 'deforestation', 'sustainability'],
        'color': 'green'
    },
    'animal': {
        'name': 'पशु अधिकार व क्रूरता',
        'keywords': ['animal rights', 'vegan', 'vegetarian', 'wildlife', 'meat industry', 'animal welfare'],
        'color': 'orange'
    },
    'women': {
        'name': 'महिला सशक्तिकरण व समानता',
        'keywords': ['women rights', 'feminism', 'gender equality', 'women empowerment', 'women safety'],
        'color': 'pink'
    },
    'education': {
        'name': 'शिक्षा प्रणाली व युवा',
        'keywords': ['education', 'students', 'youth', 'university', 'schools', 'learning', 'career pressure'],
        'color': 'blue'
    },
    'religious': {
        'name': 'धार्मिक कट्टरता व अंधविश्वास',
        'keywords': ['religious', 'communal', 'intolerance', 'superstition', 'fundamentalism', 'extremism'],
        'color': 'red'
    },
    'capitalism': {
        'name': 'उपभोक्तावाद व पूंजीवाद',
        'keywords': ['capitalism', 'consumerism', 'corporate', 'inequality', 'poverty', 'wealth gap'],
        'color': 'yellow'
    },
    'media': {
        'name': 'मीडिया Manipulation व Fake News',
        'keywords': ['fake news', 'misinformation', 'propaganda', 'media bias', 'censorship'],
        'color': 'indigo'
    },
    'caste': {
        'name': 'जातिवाद व सामाजिक भेदभाव',
        'keywords': ['caste', 'discrimination', 'dalit', 'reservation', 'social justice'],
        'color': 'gray'
    },
    'mental': {
        'name': 'Mental Health व आत्महत्या',
        'keywords': ['mental health', 'depression', 'suicide', 'anxiety', 'stress'],
        'color': 'teal'
    },
    'relationships': {
        'name': 'संबंधों की विकृतियाँ',
        'keywords': ['marriage', 'divorce', 'relationship', 'family', 'domestic violence'],
        'color': 'rose'
    },
    'career': {
        'name': 'Career Obsession व Success की दौड़',
        'keywords': ['career', 'job', 'employment', 'success', 'competition', 'burnout'],
        'color': 'cyan'
    }
}

def calculate_score(article, category_keywords):
    """News को score करने का function"""
    score = 50  # Base score
    
    text = f"{article.get('title', '')} {article.get('description', '')}".lower()
    
    # Keywords matching
    match_count = sum(1 for kw in category_keywords if kw.lower() in text)
    score += match_count * 5
    
    # Recency bonus
    try:
        pub_date = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        hours_old = (datetime.utcnow() - pub_date).total_seconds() / 3600
        
        if hours_old < 6:
            score += 20
        elif hours_old < 24:
            score += 10
        elif hours_old < 72:
            score += 5
    except:
        pass
    
    # Source reliability
    trusted = ['bbc', 'reuters', 'guardian', 'aljazeera', 'thehindu', 'wire']
    source_name = article.get('source', {}).get('name', '').lower()
    if any(t in source_name for t in trusted):
        score += 10
    
    return min(score, 100)

def fetch_all_news():
    """सभी categories से news fetch करो"""
    all_news = []
    
    for cat_key, cat_data in CATEGORIES.items():
        try:
            # Query बनाओ (पहले 3 keywords use करो)
            query = ' OR '.join(cat_data['keywords'][:3])
            
            # NewsAPI call
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
                        score = calculate_score(article, cat_data['keywords'])
                        
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
                            'score': score,
                            'impactScore': min(score + 5, 100),
                            'viralityScore': min(score + 10, 100)
                        }
                        
                        all_news.append(news_item)
        
        except Exception as e:
            print(f"Error fetching {cat_key}: {str(e)}")
            continue
    
    # Score से sort करो
    all_news.sort(key=lambda x: x['score'], reverse=True)
    
    # Duplicates remove करो (same title)
    seen_titles = set()
    unique_news = []
    for item in all_news:
        if item['title'] not in seen_titles:
            seen_titles.add(item['title'])
            unique_news.append(item)
    
    return unique_news

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/news')
def get_news():
    """API endpoint to fetch news"""
    try:
        news = fetch_all_news()
        return jsonify({
            'success': True,
            'news': news,
            'timestamp': datetime.utcnow().isoformat(),
            'total': len(news)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export')
def export_csv():
    """Export news to CSV"""
    try:
        news = fetch_all_news()
        
        # CSV बनाओ
        output = StringIO()
        writer = csv.writer(output)
        
        # Headers
        writer.writerow(['Title', 'Category', 'Source', 'Score', 'Published', 'URL'])
        
        # Data
        for item in news:
            writer.writerow([
                item['title'],
                item['category'],
                item['source'],
                item['score'],
                item['publishedAt'],
                item['url']
            ])
        
        # Response
        output.seek(0)
        return output.getvalue(), 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': f'attachment; filename=samay-news-{datetime.now().strftime("%Y%m%d")}.csv'
        }
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    # Local testing के लिए
    app.run(debug=True, host='0.0.0.0', port=5000)
