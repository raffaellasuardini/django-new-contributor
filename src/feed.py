from feedgen.feed import FeedGenerator
from datetime import timezone


def generate_feed(new_authors, output_path="feed.xml"):
    FEED_URL = "https://raffaellasuardini.github.io/django-new-contributor/feed.xml"

    fg = FeedGenerator()
    fg.title("New Django Contributors")
    fg.link(href="https://github.com/django/django", rel="alternate")
    fg.link(href=FEED_URL, rel="self", type="application/rss+xml")
    fg.description("New contributors who had their first PR merged into Django")
    fg.language("en")
    fg.id(FEED_URL)

    for author in new_authors:
        fe = fg.add_entry()
        fe.id(author.get_url())
        fe.title(f"🎉 Welcome @{author.login}")
        fe.link(href=author.get_url())
        fe.description(
            f"@{author.login} just had their first PR merged into Django.\n\n"
            f"GitHub profile: {author.get_url()}"
        )

    fg.rss_file(output_path)
