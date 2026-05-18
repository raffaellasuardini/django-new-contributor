import datetime
from dataclasses import dataclass
from typing import List
from github import Github, Auth
from decouple import config

REPO = "django/django"
GITHUB_TOKEN = config("GITHUB_TOKEN")
auth = Auth.Token(GITHUB_TOKEN)
g = Github(auth=auth)

@dataclass
class Author:
    login: str
    date_pr_merged: datetime.date
    name: str = None

    def __hash__(self):
        return hash(self.login)

    def __eq__(self, other):
        return isinstance(other, Author) and self.login == other.login

    def get_url(self) -> str:
        return f"https://github.com/{self.login}"

    def get_name_or_login(self):
        return self.name or self.login


def get_merged_prs(current_date: datetime.date):
    query = (
        f"repo:{REPO} "
        f"type:pr "
        f"merged:{current_date.strftime('%Y-%m-%d')} "
    )
    prs = g.search_issues(query)
    return prs


def is_new_contributor(author_login: str) -> bool:
    query = (
        f"repo:{REPO} "
        f"state:closed "
        f"is:pr "
        f"author:{author_login} "
    )
    prs = g.search_issues(query)

    return prs.totalCount <= 1


def get_new_contributors(
        current_date: datetime.date = None
) -> List[Author]:
    today = datetime.date.today()

    if current_date is None:
        current_date = today

    prs = get_merged_prs(current_date)

    if prs.totalCount == 0:
        return []

    authors = {
        Author(
            login=pr.user.login,
            name=pr.user.name,
            date_pr_merged=pr.pull_request.merged_at,
        )
        for pr in prs
    }

    new_contributors = [
        author
        for author in authors
        if is_new_contributor(author.login)
    ]

    return sorted(new_contributors, key=lambda a: a.login)
