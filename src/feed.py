import os
import feedparser
from feedgen.feed import FeedGenerator

FEED_URL = "https://raffaellasuardini.github.io/django-new-contributor/feed.xml"
FEED_PATH = "feed.xml"


def generate_feed(new_authors):
    fg = FeedGenerator()
    fg.title("New Django Contributors")
    fg.link(href="https://github.com/django/django", rel="alternate")
    fg.link(href=FEED_URL, rel="self", type="application/rss+xml")
    fg.description("New contributors who had their first PR merged into Django")
    fg.language("en")
    fg.id(FEED_URL)

    existing_guids = set()

    # load previous feed
    if os.path.exists(FEED_PATH):
        old_feed = feedparser.parse(FEED_PATH)
        for entry in old_feed.entries:
            existing_guids.add(entry.id)

            fe = fg.add_entry()
            fe.id(entry.id)
            fe.title(entry.title)
            fe.link(href=entry.link)
            fe.description(entry.description)
            fe.pubDate(entry.published)

    # add new contributor
    for author in new_authors:
        guid = author.get_url()

        if guid in existing_guids:
            continue

        fe = fg.add_entry()
        fe.id(guid)
        fe.title(f"🎉 Welcome {author.get_name_or_login()}")
        fe.description(
            f"{author.get_name_or_login()} just had their first PR merged into Django.\n\n"
            f"GitHub profile: {guid}"
        )
        fe.pubDate(author.date_pr_merged)

    fg.rss_file(FEED_PATH)
