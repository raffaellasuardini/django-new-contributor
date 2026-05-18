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
class PR:
    title: str
    number: int

    def get_url(self) -> str:
        return f"https://github.com/django/django/pull/{str(self.number)}"


@dataclass
class Author:
    login: str
    date_pr_merged: datetime.date
    pr: PR
    name: str = None

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
        f"is:merged "
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

    new_contributors = []
    already_contributors = set()

    for pr in prs:
        current_login = pr.user.login
        if current_login in already_contributors:
            continue
        already_contributors.add(current_login)

        if is_new_contributor(current_login):
            new_contributors.append(
                Author(
                    login=current_login,
                    name=pr.user.name,
                    date_pr_merged=pr.pull_request.merged_at,
                    pr=PR(title=pr.title, number=pr.number),
                )
            )

    return sorted(new_contributors, key=lambda a: a.login)
