import os
import feedparser
from feedgen.feed import FeedGenerator
from decouple import config

FEED_FILENAME = config('FEED_FILENAME', default='feed.xml')
FEED_URL = config('FEED_URL') + FEED_FILENAME
FEED_PATH = FEED_FILENAME
FEED_TITLE_SUFIX = config('FEED_TITLE_SUFIX', default='')


def generate_feed(new_authors):
    fg = FeedGenerator()
    fg.title(f"New Django Contributor {FEED_TITLE_SUFIX}")
    fg.link(href="https://github.com/django/django", rel="alternate")
    fg.link(href=FEED_URL, rel="self", type="application/rss+xml")
    fg.description("New contributor who had their first PR merged into Django")
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
        fe.link(href=author.get_url())
        fe.description(
            f"{author.get_name_or_login()} just had their first PR merged into Django.\n\n"
            f"GitHub profile: {guid}"
        )
        fe.pubDate(author.date_pr_merged)

    fg.rss_file(FEED_PATH)
