"""
=============================================================================
NIRVANA READ - Simplified Learning System (localStorage only)
No Supabase dependency - works completely free
=============================================================================
"""

# Supabase disabled for now - using client-side localStorage only
supabase_client = None

def init_supabase():
    """Supabase initialization (disabled)"""
    print("⚠️ Supabase disabled - using client-side learning only")
    return False

def track_interaction(user_id, news_url, action, category, reading_time=0):
    """Track interaction (no-op without Supabase)"""
    return True

def get_user_preferences(user_id, days=30):
    """Get user preferences (returns empty without Supabase)"""
    return {}

def update_news_feedback(news_url, action):
    """Update news feedback (no-op without Supabase)"""
    return True

def get_news_quality_score(news_url):
    """Get news quality score (returns None without Supabase)"""
    return None

def update_category_stats(category, engagement_time):
    """Update category stats (no-op without Supabase)"""
    return True

def get_trending_categories(limit=5):
    """Get trending categories (returns empty without Supabase)"""
    return []

def calculate_personalized_score(base_score, news_url, category, user_id=None):
    """Calculate personalized score (returns base score without Supabase)"""
    return base_score

def setup_database_tables():
    """Setup database (disabled)"""
    print("⚠️ Supabase disabled")
    return False

def cleanup_old_data(days=90):
    """Cleanup old data (disabled)"""
    return False
