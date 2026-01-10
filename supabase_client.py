"""
=============================================================================
NIRVANA READ - Supabase Learning System
Collective intelligence for better news curation
=============================================================================
"""

import os
from datetime import datetime
from supabase import create_client, Client
import json

# ============== SUPABASE CONFIGURATION ==============

SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY', '')
SUPABASE_SERVICE_KEY = os.environ.get('SUPABASE_SERVICE_KEY', '')

# Initialize client (will be None if keys not set)
supabase_client: Client = None

def init_supabase():
    """Initialize Supabase client"""
    global supabase_client
    
    if SUPABASE_URL and SUPABASE_SERVICE_KEY:
        try:
            supabase_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
            print("✅ Supabase initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Supabase initialization failed: {str(e)}")
            return False
    else:
        print("⚠️ Supabase credentials not found - running without cloud sync")
        return False

# ============== USER INTERACTION TRACKING ==============

def track_interaction(user_id, news_url, action, category, reading_time=0):
    """
    Track user interaction with news
    
    Actions: 'view', 'read_full', 'mark_reviewed'
    """
    if not supabase_client:
        return False
    
    try:
        data = {
            'user_id': user_id,
            'news_url': news_url,
            'action': action,
            'category': category,
            'reading_time': reading_time,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        result = supabase_client.table('user_interactions').insert(data).execute()
        return True
        
    except Exception as e:
        print(f"Error tracking interaction: {str(e)}")
        return False

def get_user_preferences(user_id, days=30):
    """
    Get user's category preferences based on past behavior
    Returns dict: {category: engagement_score}
    """
    if not supabase_client:
        return {}
    
    try:
        # Get user interactions from last N days
        result = supabase_client.rpc(
            'get_user_category_preferences',
            {'p_user_id': user_id, 'p_days': days}
        ).execute()
        
        if result.data:
            return {row['category']: row['score'] for row in result.data}
        return {}
        
    except Exception as e:
        print(f"Error getting user preferences: {str(e)}")
        return {}

# ============== NEWS QUALITY FEEDBACK ==============

def update_news_feedback(news_url, action):
    """
    Update collective feedback for a news item
    
    Actions impact:
    - 'view': +1 to total_views
    - 'read_full': +1 to total_reads, indicates quality
    - 'mark_reviewed': +1 to total_reads, high engagement
    """
    if not supabase_client:
        return False
    
    try:
        # Check if news already exists
        existing = supabase_client.table('news_feedback').select('*').eq('news_url', news_url).execute()
        
        if existing.data:
            # Update existing
            current = existing.data[0]
            updates = {'last_updated': datetime.utcnow().isoformat()}
            
            if action == 'view':
                updates['total_views'] = current['total_views'] + 1
            elif action in ['read_full', 'mark_reviewed']:
                updates['total_reads'] = current['total_reads'] + 1
            
            # Calculate relevance score
            if updates.get('total_views', current['total_views']) > 0:
                read_rate = updates.get('total_reads', current['total_reads']) / updates.get('total_views', current['total_views'])
                updates['relevance_score'] = min(read_rate * 100, 100)
            
            supabase_client.table('news_feedback').update(updates).eq('news_url', news_url).execute()
        else:
            # Insert new
            data = {
                'news_url': news_url,
                'total_views': 1 if action == 'view' else 0,
                'total_reads': 1 if action in ['read_full', 'mark_reviewed'] else 0,
                'relevance_score': 0,
                'last_updated': datetime.utcnow().isoformat()
            }
            supabase_client.table('news_feedback').insert(data).execute()
        
        return True
        
    except Exception as e:
        print(f"Error updating news feedback: {str(e)}")
        return False

def get_news_quality_score(news_url):
    """
    Get collective quality score for a news item
    Returns: float 0-100 (or None if not enough data)
    """
    if not supabase_client:
        return None
    
    try:
        result = supabase_client.table('news_feedback').select('relevance_score, total_views').eq('news_url', news_url).execute()
        
        if result.data and result.data[0]['total_views'] >= 5:  # Minimum threshold
            return result.data[0]['relevance_score']
        return None
        
    except Exception as e:
        print(f"Error getting news quality: {str(e)}")
        return None

# ============== CATEGORY STATISTICS ==============

def update_category_stats(category, engagement_time):
    """Update aggregate statistics for a category"""
    if not supabase_client:
        return False
    
    try:
        # Check if category exists
        existing = supabase_client.table('category_stats').select('*').eq('category', category).execute()
        
        if existing.data:
            current = existing.data[0]
            total_interactions = current['total_interactions'] + 1
            
            # Moving average for engagement time
            new_avg_time = (
                (current['avg_engagement_time'] * current['total_interactions'] + engagement_time) 
                / total_interactions
            )
            
            updates = {
                'total_interactions': total_interactions,
                'avg_engagement_time': new_avg_time,
                'popularity_score': min(total_interactions / 10, 100),  # Normalize
                'last_updated': datetime.utcnow().isoformat()
            }
            
            supabase_client.table('category_stats').update(updates).eq('category', category).execute()
        else:
            data = {
                'category': category,
                'total_interactions': 1,
                'avg_engagement_time': engagement_time,
                'popularity_score': 10,
                'last_updated': datetime.utcnow().isoformat()
            }
            supabase_client.table('category_stats').insert(data).execute()
        
        return True
        
    except Exception as e:
        print(f"Error updating category stats: {str(e)}")
        return False

def get_trending_categories(limit=5):
    """
    Get trending categories based on recent engagement
    Returns: list of (category, score) tuples
    """
    if not supabase_client:
        return []
    
    try:
        result = supabase_client.table('category_stats').select('category, popularity_score').order('popularity_score', desc=True).limit(limit).execute()
        
        if result.data:
            return [(row['category'], row['popularity_score']) for row in result.data]
        return []
        
    except Exception as e:
        print(f"Error getting trending categories: {str(e)}")
        return []

# ============== LEARNING ALGORITHM ==============

def calculate_personalized_score(base_score, news_url, category, user_id=None):
    """
    Adjust base AI score using collective intelligence and user preferences
    
    Returns: adjusted_score (0-100)
    """
    adjusted_score = base_score
    
    # Factor 1: Collective quality score (weight: 20%)
    quality_score = get_news_quality_score(news_url)
    if quality_score is not None:
        adjusted_score = adjusted_score * 0.8 + quality_score * 0.2
    
    # Factor 2: Category popularity (weight: 10%)
    try:
        trending = dict(get_trending_categories())
        if category in trending:
            category_boost = (trending[category] / 100) * 10
            adjusted_score += category_boost
    except:
        pass
    
    # Factor 3: User preferences (weight: 15%) - if user_id provided
    if user_id:
        try:
            preferences = get_user_preferences(user_id)
            if category in preferences:
                user_boost = (preferences[category] / 100) * 15
                adjusted_score += user_boost
        except:
            pass
    
    # Cap at 100
    return min(adjusted_score, 100)

# ============== DATABASE INITIALIZATION ==============

def setup_database_tables():
    """
    Create necessary tables in Supabase
    
    Run this once during initial setup
    """
    if not supabase_client:
        print("❌ Cannot setup database - Supabase not initialized")
        return False
    
    sql_queries = [
        # User interactions table
        """
        CREATE TABLE IF NOT EXISTS user_interactions (
            id BIGSERIAL PRIMARY KEY,
            user_id TEXT NOT NULL,
            news_url TEXT NOT NULL,
            action TEXT NOT NULL,
            category TEXT,
            reading_time INTEGER DEFAULT 0,
            timestamp TIMESTAMP DEFAULT NOW(),
            INDEX idx_user_id (user_id),
            INDEX idx_news_url (news_url),
            INDEX idx_category (category),
            INDEX idx_timestamp (timestamp)
        );
        """,
        
        # News feedback table
        """
        CREATE TABLE IF NOT EXISTS news_feedback (
            id BIGSERIAL PRIMARY KEY,
            news_url TEXT UNIQUE NOT NULL,
            total_views INTEGER DEFAULT 0,
            total_reads INTEGER DEFAULT 0,
            avg_reading_time FLOAT DEFAULT 0,
            relevance_score FLOAT DEFAULT 0,
            last_updated TIMESTAMP DEFAULT NOW(),
            INDEX idx_news_url (news_url),
            INDEX idx_relevance_score (relevance_score)
        );
        """,
        
        # Category statistics table
        """
        CREATE TABLE IF NOT EXISTS category_stats (
            category TEXT PRIMARY KEY,
            total_interactions INTEGER DEFAULT 0,
            avg_engagement_time FLOAT DEFAULT 0,
            popularity_score FLOAT DEFAULT 0,
            last_updated TIMESTAMP DEFAULT NOW()
        );
        """
    ]
    
    # Note: In Supabase, you'll need to run these SQL queries manually
    # in the SQL Editor tab of your project dashboard
    
    print("⚠️ Please run the following SQL in Supabase SQL Editor:")
    print("=" * 70)
    for query in sql_queries:
        print(query)
        print()
    print("=" * 70)
    
    return True

# ============== CLEANUP & MAINTENANCE ==============

def cleanup_old_data(days=90):
    """Remove data older than N days to manage storage"""
    if not supabase_client:
        return False
    
    try:
        cutoff_date = datetime.utcnow().isoformat()
        
        # Delete old interactions
        supabase_client.table('user_interactions').delete().lt('timestamp', cutoff_date).execute()
        
        print(f"✅ Cleaned up data older than {days} days")
        return True
        
    except Exception as e:
        print(f"Error cleaning up data: {str(e)}")
        return False
