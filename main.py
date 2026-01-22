from src.github import get_new_contributors
from src.feed import generate_feed


def main():
    new_authors = get_new_contributors()
    if not new_authors:
        print("No new contributors found.")
    else:
        print("I'm creating a feed rss")
        generate_feed(new_authors)
        print("New contributors:")
        for author in new_authors:
            print(author.login)


if __name__ == "__main__":
    main()
