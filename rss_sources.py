"""
=============================================================================
RSS SOURCES CONFIGURATION
All major Indian news sources (English + Hindi)
=============================================================================
"""

# ============== MAJOR ENGLISH NEWS SOURCES ==============
ENGLISH_SOURCES = {
    'the_hindu': {
        'name': 'The Hindu',
        'feeds': {
            'national': 'https://www.thehindu.com/news/national/feeder/default.rss',
            'cities': 'https://www.thehindu.com/news/cities/feeder/default.rss',
            'india': 'https://www.thehindu.com/news/national/feeder/default.rss'
        }
    },
    """
    'indian_express': {
        'name': 'Indian Express',
        'feeds': {
            'india': 'https://indianexpress.com/section/india/feed/',
            'cities': 'https://indianexpress.com/section/cities/feed/'
        }
    },
    """
    'the_wire': {
        'name': 'The Wire',
        'feeds': {
            'politics': 'https://thewire.in/politics/feed',
            'rights': 'https://thewire.in/rights/feed',
            'environment': 'https://thewire.in/environment/feed',
            'women': 'https://thewire.in/women/feed'
        }
    },
    'scroll': {
        'name': 'Scroll.in',
        'feeds': {
            'latest': 'https://scroll.in/feeds/latest.rss',
            'india': 'https://scroll.in/feeds/india.rss'
        }
    },
    'ndtv': {
        'name': 'NDTV',
        'feeds': {
            'india': 'https://feeds.feedburner.com/ndtv/India',
            'cities': 'https://feeds.feedburner.com/ndtvcities'
        }
    },
    'hindustan_times': {
        'name': 'Hindustan Times',
        'feeds': {
            'india': 'https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml',
            'cities': 'https://www.hindustantimes.com/feeds/rss/cities/rssfeed.xml'
        }
    },
    'the_print': {
        'name': 'The Print',
        'feeds': {
            'india': 'https://theprint.in/category/india/feed/',
            'opinion': 'https://theprint.in/category/opinion/feed/'
        }
    },
    'news18': {
        'name': 'News18',
        'feeds': {
            'india': 'https://www.news18.com/rss/india.xml'
        }
    },
    'firstpost': {
        'name': 'Firstpost',
        'feeds': {
            'india': 'https://www.firstpost.com/rss/india.xml'
        }
    },
    'deccan_herald': {
        'name': 'Deccan Herald',
        'feeds': {
            'national': 'https://www.deccanherald.com/rss/national.rss'
        }
    },
    'telegraph_india': {
        'name': 'Telegraph India',
        'feeds': {
            'nation': 'https://www.telegraphindia.com/rss/nation'
        }
    },
    'livemint': {
        'name': 'Livemint',
        'feeds': {
            'politics': 'https://www.livemint.com/rss/politics',
            'news': 'https://www.livemint.com/rss/news'
        }
    },
    'outlook': {
        'name': 'Outlook India',
        'feeds': {
            'national': 'https://www.outlookindia.com/rss/national'
        }
    }
    """
}

# ============== HINDI NEWS SOURCES ==============
HINDI_SOURCES = {
    'bbc_hindi': {
        'name': 'BBC Hindi',
        'feeds': {
            'india': 'https://feeds.bbci.co.uk/hindi/india/rss.xml',
            'international': 'https://feeds.bbci.co.uk/hindi/international/rss.xml'
        }
    },
    """
    'navbharat_times': {
        'name': 'नवभारत टाइम्स',
        'feeds': {
            'india': 'https://navbharattimes.indiatimes.com/rssfeedstopstories.cms'
        }
    },
    'dainik_jagran': {
        'name': 'दैनिक जागरण',
        'feeds': {
            'national': 'https://www.jagran.com/rss/news-national-hindi.xml'
        }
    },
    'amar_ujala': {
        'name': 'अमर उजाला',
        'feeds': {
            'india': 'https://www.amarujala.com/rss/india-news.xml'
        }
    },
    'patrika': {
        'name': 'पत्रिका',
        'feeds': {
            'india': 'https://www.patrika.com/rss/india-news.xml'
        }
    },
    'nai_dunia': {
        'name': 'नई दुनिया',
        'feeds': {
            'national': 'https://www.naidunia.com/rss/national-news'
        }
    }
    """
}

# ============== CATEGORY-SPECIFIC SPECIALIZED SOURCES ==============
SPECIALIZED_SOURCES = {
    # जलवायु/पर्यावरण
    'climate_environment': {
        'down_to_earth': {
            'name': 'Down To Earth',
            'feeds': {
                'climate': 'https://www.downtoearth.org.in/rss/climate-change',
                'environment': 'https://www.downtoearth.org.in/rss/environment',
                'pollution': 'https://www.downtoearth.org.in/rss/air'
            }
        },
        """
        'mongabay_india': {
            'name': 'Mongabay India',
            'feeds': {
                'all': 'https://india.mongabay.com/feed/'
            }
        },
        'india_climate_dialogue': {
            'name': 'India Climate Dialogue',
            'feeds': {
                'all': 'https://indiaclimatedialogue.net/feed/'
            }
        },
        'climate_home_news': {
            'name': 'Climate Home News (India)',
            'feeds': {
                'india': 'https://www.climatechangenews.com/tag/india/feed/'
            }
        }
        """
    },
    
    # महिला सशक्तिकरण
    'women_rights': {
        'feminism_india': {
            'name': 'Feminism in India',
            'feeds': {
                'all': 'https://feminisminindia.com/feed/'
            }
        },
        'shethepeople': {
            'name': 'SheThePeople',
            'feeds': {
                'news': 'https://www.shethepeople.tv/rss'
            }
        }
    },
    """
    # शिक्षा व युवा
    'education_youth': {
        'the_better_india_education': {
            'name': 'The Better India - Education',
            'feeds': {
                'education': 'https://www.thebetterindia.com/category/education/feed/'
            }
        },
        'yourstory_education': {
            'name': 'YourStory Education',
            'feeds': {
                'education': 'https://yourstory.com/education/feed'
            }
        }
    },
    
    # Mental Health
    'mental_health': {
        'white_swan': {
            'name': 'White Swan Foundation',
            'feeds': {
                'all': 'https://www.whiteswanfoundation.org/rss.xml'
            }
        }
    },
    
    # सामाजिक मुद्दे
    'social_issues': {
        'sabrang_india': {
            'name': 'Sabrang India',
            'feeds': {
                'all': 'https://sabrangindia.in/feed/'
            }
        },
        'countercurrents': {
            'name': 'Countercurrents',
            'feeds': {
                'all': 'https://countercurrents.org/feed/'
            }
        }
    }
    """
}

# ============== RSS FEED TO CATEGORY MAPPING ==============
CATEGORY_RSS_MAPPING = {
    'consciousness': [
        # Mainstream sources (philosophical/spiritual content)
        ('the_hindu', 'india'),
        ('scroll', 'latest'),
        ('outlook', 'national')
    ],
    
    'climate': [
        # Specialized environment sources
        ('down_to_earth', 'climate'),
        ('down_to_earth', 'environment'),
        ('down_to_earth', 'pollution'),
        ('mongabay_india', 'all'),
        ('india_climate_dialogue', 'all'),
        # Mainstream sources
        ('the_hindu', 'national'),
        ('the_wire', 'environment'),
        ('indian_express', 'india'),
        ('bbc_hindi', 'india')
    ],
    
    'animal': [
        # Mainstream sources for animal rights coverage
        ('the_hindu', 'national'),
        ('indian_express', 'india'),
        ('scroll', 'india'),
        ('the_wire', 'rights'),
        ('down_to_earth', 'environment')
    ],
    
    'women': [
        # Specialized women's rights sources
        ('feminism_india', 'all'),
        ('shethepeople', 'news'),
        # Mainstream sources
        ('the_wire', 'women'),
        ('the_wire', 'rights'),
        ('scroll', 'india'),
        ('indian_express', 'india'),
        ('bbc_hindi', 'india')
    ],
    
    'education': [
        # Specialized education sources
        ('the_better_india_education', 'education'),
        ('yourstory_education', 'education'),
        # Mainstream sources
        ('the_hindu', 'national'),
        ('indian_express', 'india'),
        ('scroll', 'india'),
        ('dainik_jagran', 'national')
    ],
    
    'religious': [
        # Mainstream sources (communal issues coverage)
        ('scroll', 'india'),
        ('the_wire', 'politics'),
        ('the_wire', 'rights'),
        ('sabrang_india', 'all'),
        ('indian_express', 'india'),
        ('the_hindu', 'national'),
        ('bbc_hindi', 'india')
    ],
    
    'capitalism': [
        # Economic/business sources
        ('livemint', 'politics'),
        ('livemint', 'news'),
        ('the_wire', 'politics'),
        ('scroll', 'india'),
        ('indian_express', 'india'),
        ('countercurrents', 'all')
    ],
    
    'media': [
        # Media criticism sources
        ('scroll', 'latest'),
        ('the_wire', 'politics'),
        ('the_print', 'opinion'),
        ('newslaundry', 'all') if 'newslaundry' in ENGLISH_SOURCES else None
    ],
    
    'caste': [
        # Social justice sources
        ('scroll', 'india'),
        ('the_wire', 'rights'),
        ('sabrang_india', 'all'),
        ('countercurrents', 'all'),
        ('indian_express', 'india'),
        ('the_hindu', 'national')
    ],
    
    'mental': [
        # Mental health specialized
        ('white_swan', 'all'),
        # Mainstream sources
        ('scroll', 'india'),
        ('the_hindu', 'national'),
        ('indian_express', 'cities'),
        ('hindustan_times', 'cities')
    ],
    
    'relationships': [
        # Mainstream sources (family/society coverage)
        ('scroll', 'india'),
        ('the_wire', 'rights'),
        ('feminism_india', 'all'),
        ('indian_express', 'india'),
        ('bbc_hindi', 'india')
    ],
    
    'career': [
        # Business/employment sources
        ('livemint', 'news'),
        ('the_print', 'india'),
        ('yourstory_education', 'education'),
        ('indian_express', 'india'),
        ('hindustan_times', 'india')
    ]
}

# ============== HELPER FUNCTION TO GET ALL RSS URLS ==============
def get_all_rss_urls():
    """Get all RSS feed URLs from all sources"""
    all_urls = []
    
    # English sources
    for source_key, source_data in ENGLISH_SOURCES.items():
        for feed_key, feed_url in source_data['feeds'].items():
            all_urls.append({
                'source': source_data['name'],
                'source_key': source_key,
                'feed_key': feed_key,
                'url': feed_url,
                'language': 'english'
            })
    
    # Hindi sources
    for source_key, source_data in HINDI_SOURCES.items():
        for feed_key, feed_url in source_data['feeds'].items():
            all_urls.append({
                'source': source_data['name'],
                'source_key': source_key,
                'feed_key': feed_key,
                'url': feed_url,
                'language': 'hindi'
            })
    
    # Specialized sources
    for category, sources in SPECIALIZED_SOURCES.items():
        for source_key, source_data in sources.items():
            for feed_key, feed_url in source_data['feeds'].items():
                all_urls.append({
                    'source': source_data['name'],
                    'source_key': source_key,
                    'feed_key': feed_key,
                    'url': feed_url,
                    'language': 'english',
                    'specialized': category
                })
    
    return all_urls

def get_category_feeds(category_key):
    """Get relevant RSS feeds for a specific category"""
    mapping = CATEGORY_RSS_MAPPING.get(category_key, [])
    feeds = []
    
    for source_key, feed_key in mapping:
        if source_key is None:
            continue
            
        # Check English sources
        if source_key in ENGLISH_SOURCES:
            source = ENGLISH_SOURCES[source_key]
            if feed_key in source['feeds']:
                feeds.append({
                    'source': source['name'],
                    'url': source['feeds'][feed_key],
                    'language': 'english'
                })
        
        # Check Hindi sources
        elif source_key in HINDI_SOURCES:
            source = HINDI_SOURCES[source_key]
            if feed_key in source['feeds']:
                feeds.append({
                    'source': source['name'],
                    'url': source['feeds'][feed_key],
                    'language': 'hindi'
                })
        
        # Check specialized sources
        else:
            for cat_sources in SPECIALIZED_SOURCES.values():
                if source_key in cat_sources:
                    source = cat_sources[source_key]
                    if feed_key in source['feeds']:
                        feeds.append({
                            'source': source['name'],
                            'url': source['feeds'][feed_key],
                            'language': 'english'
                        })
    
    return feeds
