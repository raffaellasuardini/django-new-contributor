import os
import feedparser
from feedgen.feed import FeedGenerator
from decouple import config

FEED_FILENAME = config('FEED_FILENAME', default='feed.xml')
FEED_URL = config('FEED_URL') + FEED_FILENAME
FEED_PATH = FEED_FILENAME
FEED_TITLE_SUFIX = config('FEED_TITLE_SUFIX', default='')
MAX_ENTRIES = 50


def generate_feed(new_authors):
    fg = FeedGenerator()
    fg.title(f"New Django Contributor {FEED_TITLE_SUFIX}")
    fg.link(href="https://github.com/django/django", rel="alternate")
    fg.link(href=FEED_URL, rel="self", type="application/rss+xml")
    fg.description("New contributor who had their first PR merged into Django")
    fg.language("en")
    fg.id(FEED_URL)

    existing_guids = set()
    old_entities = []

    # check previous feed till MAX_ENTRIES
    if os.path.exists(FEED_PATH):
        parsed_feed = feedparser.parse(FEED_PATH)
        old_entities = parsed_feed.entries[:MAX_ENTRIES]
        existing_guids = set([entry.id for entry in old_entities])

    truly_new_authors = [author for author in new_authors if author.get_url() not in existing_guids]

    # load previous feed till MAX_ENTRIES
    for entry in reversed(old_entities[:MAX_ENTRIES - len(truly_new_authors)]):
        fe = fg.add_entry()
        fe.id(entry.id)
        fe.title(entry.title)
        fe.link(href=entry.link)
        fe.description(entry.description)
        fe.pubDate(entry.published)

    # add new contributor
    for author in truly_new_authors:
        guid = author.get_url()

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
