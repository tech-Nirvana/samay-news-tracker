"""
=============================================================================
MINIMAL — CLEAN — STABLE RSS CONFIG
(2 English + 2 Hindi + 2 Specialized Categories)
=============================================================================
"""

# ============== ENGLISH NEWS SOURCES ==============
ENGLISH_SOURCES = {
    "the_hindu": {
        "name": "The Hindu",
        "feeds": {
            "national": "https://www.thehindu.com/news/national/feeder/default.rss",
            "cities": "https://www.thehindu.com/news/cities/feeder/default.rss",
        },
    },

    "indian_express": {
        "name": "Indian Express",
        "feeds": {
            "india": "https://indianexpress.com/section/india/feed/",
            "cities": "https://indianexpress.com/section/cities/feed/",
        },
    },
}

# ============== HINDI NEWS SOURCES ==============
HINDI_SOURCES = {
    "bbc_hindi": {
        "name": "BBC Hindi",
        "feeds": {
            "india": "https://feeds.bbci.co.uk/hindi/india/rss.xml",
            "international": "https://feeds.bbci.co.uk/hindi/international/rss.xml",
        },
    },

    "navbharat_times": {
        "name": "नवभारत टाइम्स",
        "feeds": {
            "india": "https://navbharattimes.indiatimes.com/rssfeedstopstories.cms",
        },
    },
}

# ============== SPECIALIZED CATEGORIES (Only 2) ==============
SPECIALIZED_SOURCES = {
    "climate_environment": {
        "down_to_earth": {
            "name": "Down To Earth",
            "feeds": {
                "climate": "https://www.downtoearth.org.in/rss/climate-change",
                "environment": "https://www.downtoearth.org.in/rss/environment",
            },
        }
    },

    "women_rights": {
        "feminism_india": {
            "name": "Feminism in India",
            "feeds": {
                "all": "https://feminisminindia.com/feed/",
            },
        }
    },
}

# ============== CATEGORY TO RSS MAPPING (only valid keys) ==============
CATEGORY_RSS_MAPPING = {
    "climate": [
        ("down_to_earth", "climate"),
        ("down_to_earth", "environment"),
        ("the_hindu", "national"),
        ("bbc_hindi", "india"),
    ],

    "women": [
        ("feminism_india", "all"),
        ("indian_express", "india"),
        ("bbc_hindi", "india"),
    ],
}


# ============== UTILITIES (unchanged) ==============
def get_all_rss_urls():
    all_urls = []

    for key, s in ENGLISH_SOURCES.items():
        for feed, url in s["feeds"].items():
            all_urls.append(
                {
                    "source": s["name"],
                    "source_key": key,
                    "feed_key": feed,
                    "url": url,
                    "language": "english",
                }
            )

    for key, s in HINDI_SOURCES.items():
        for feed, url in s["feeds"].items():
            all_urls.append(
                {
                    "source": s["name"],
                    "source_key": key,
                    "feed_key": feed,
                    "url": url,
                    "language": "hindi",
                }
            )

    for category, sources in SPECIALIZED_SOURCES.items():
        for key, s in sources.items():
            for feed, url in s["feeds"].items():
                all_urls.append(
                    {
                        "source": s["name"],
                        "source_key": key,
                        "feed_key": feed,
                        "url": url,
                        "language": "english",
                        "specialized": category,
                    }
                )

    return all_urls


def get_category_feeds(category_key):
    mapping = CATEGORY_RSS_MAPPING.get(category_key, [])
    feeds = []

    for source_key, feed_key in mapping:

        if source_key in ENGLISH_SOURCES and feed_key in ENGLISH_SOURCES[source_key]["feeds"]:
            s = ENGLISH_SOURCES[source_key]
            feeds.append(
                {"source": s["name"], "url": s["feeds"][feed_key], "language": "english"}
            )

        elif source_key in HINDI_SOURCES and feed_key in HINDI_SOURCES[source_key]["feeds"]:
            s = HINDI_SOURCES[source_key]
            feeds.append(
                {"source": s["name"], "url": s["feeds"][feed_key], "language": "hindi"}
            )

        else:
            for cat_sources in SPECIALIZED_SOURCES.values():
                if source_key in cat_sources and feed_key in cat_sources[source_key]["feeds"]:
                    s = cat_sources[source_key]
                    feeds.append(
                        {"source": s["name"], "url": s["feeds"][feed_key], "language": "english"}
                    )

    return feeds
