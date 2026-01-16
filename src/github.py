import subprocess
import json
import datetime
from dataclasses import dataclass
from typing import List

REPO = "django/django"
contributors = set()


@dataclass
class Author:
    login: str
    date_pr_merged: str
    name: str = None

    def __hash__(self):
        return hash(self.login)

    def __eq__(self, other):
        return isinstance(other, Author) and self.login == other.login

    def get_url(self) -> str:
        return f"https://github.com/{self.login}"

    def get_name_or_login(self):
        return self.name or self.login


def _run_gh(command: str) -> list[dict]:
    process = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
    )
    if process.returncode != 0:
        raise RuntimeError(process.stderr)
    return json.loads(process.stdout)


def get_merged_prs(start_date: datetime.date, end_date: datetime.date) -> list[dict]:
    command = (
        f'gh pr list --repo {REPO} '
        f'-S "is:pr merged:{start_date}..{end_date}" '
        f'-L 50 '
        '--json author,mergedAt,createdAt'
    )
    return _run_gh(command)


def is_new_contributor(author_login: str, end_date: datetime.date = None) -> bool:
    command = (
        f'gh pr list --repo {REPO} '
        f'-S "is:pr is:merged author:{author_login} merged:1970-01-01..{end_date}" '
        f' --json number'
    )
    prs = _run_gh(command)
    return len(prs) <= 1


def get_new_contributors(start_date: datetime.date = None, end_date: datetime.date = None) -> List[Author]:
    today = datetime.date.today()
    last_sunday = today - datetime.timedelta(days=today.weekday() + 1)
    last_monday = last_sunday - datetime.timedelta(days=6)

    if end_date is None:
        end_date = last_sunday
    if start_date is None:
        start_date = last_monday

    prs = get_merged_prs(start_date, end_date)

    authors = {
        Author(
            login=pr.get('author').get('login'),
            name=pr.get('author').get('name'),
            date_pr_merged=pr.get('mergedAt')
        )
        for pr in prs
    }

    new_contributors = [
        author for author in authors if is_new_contributor(author.login, end_date=end_date)
    ]

    return new_contributors
