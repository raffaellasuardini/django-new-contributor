# Django New Contributors RSS Feed

This project generates an RSS feed listing **first-time contributors** whose pull requests have been merged into the official Django repository.

The feed can be used by feed reader (e.g. MEE6) to announce and welcome new contributors.

## How it works

The project:
1. Uses `PyGithub` to fetch merged pull requests from `django/django`.
2. Detects which authors are first-time contributors.
3. Generates a static RSS feed (`feed.xml`).
4. Publishes the feed via GitHub Pages.

A scheduled GitHub Action periodically runs the script and updates the feed.

## Example output

Each RSS item looks like:

> 🎉 Welcome @username  
> @username just had their first PR merged into Django.  
> GitHub profile: https://github.com/username


## Requirements

- Python 3.10+
- PyGithub
- `feedgen` and `feedparser` library

## Installation
1. After creating a GitHub Token, copy `.env.example` and insert your token in the `.env` file
```bash
cp .env.example .env
```
2. Create a virtual env:
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install `uv` and dependencies:
```bash
pip install uv
uv sync
```
4. Run locally to generate `feed.xml`
```bash
python main.py
```
5. Use [GitHub pages](https://docs.github.com/en/pages) to publish the live `feed.xml`

Feed URL : `https://<your-username>.github.io/<repo-name>/feed.xml`